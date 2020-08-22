# Python并发编程之Futures

## 1 并发与并行

- **并发**：并发并不是指同一时刻有多个操作同时操作，而是，在某个特定的时刻，它只允许有一个操作发生，只不过线程／任务之间会互相切换，直到完成。具体如图1所示：

![image-20200822120113421](/home/rapheal-wu/.config/Typora/typora-user-images/image-20200822120113421.png)

<p align="center">图1 Python线程/协程并发模型</p>

图1中出现了thread和task两种切换顺序的不同方式，分别对应Python中两种并发方式－threading和asyncio。

对于threading，操作系统知道每个线程的所有信息，因此他会在适当的时候做线程切换。这样的好处是，代码容易书写，程序员不需要做任何线程切换的处理；但是切换线程的操作，也可能出现在一个线程不安全的场景（如x+=1）中，这样容易出现race condition的情况。

对于asyncio，主程序想要进行任务切换时，必须得到此任务可以被切换的通知，这样一来，就可以避免线程切换中出现的race condition的情况。

- **并行**，指的是同一时刻，有多个操作同时发生。Python中的multi-processing就是这个意思。比如你的电脑是8核的，你可以在运行程序时，开启8个进程，同时执行，以加快运行速度。原理图如图2所示：

![image-20200822121457622](/home/rapheal-wu/.config/Typora/typora-user-images/image-20200822121457622.png)

<p align="center">图2 Python并行原理图</p>

对比来看，

- 并发通常应用与I/O操作频繁的场景，比如你要从网站上下载多个文件，I/O操作的时间可能会比让CPU运行处理的时间长的多。
- 并行更多应用于CPU heavy的场景，比如MapReduce中的并行计算，为了加快运行速度，一般会用多台机器、多个处理器来完成。

## 2 单线程与多线程性能比较

接下来，通过具体实例，从代码角度理解并发编程中的Futures，并进一步来比较其与单线程的性能区别。

假设有一个任务，是下载一些网站的内容并打印。如果使用单线程的方式，它的代码实现如下所示：

```python
import requests
import time


def download_one(url):
    resp = requests.get(url)
    print(f'Read {resp.content} from {url}')


def download_all(sites):
    for site in sites:
        download_one(site)


def main():
    sites = [
        'https://baike.baidu.com/item/Python',
        'https://baike.baidu.com/item/Java',
        'https://baike.baidu.com/item/Java',
        'https://baike.baidu.com/item/c%23',
        'https://baike.baidu.com/item/php',
        'https://baike.baidu.com/item/go',
        'https://baike.baidu.com/item/perl',
        'https://baike.baidu.com/item/shell',
        'https://baike.baidu.com/item/lua',
        'https://baike.baidu.com/item/android',
        'https://baike.baidu.com/item/bash',
        'https://baike.baidu.com/item/c语言',
        'https://baike.baidu.com/item/C%2B%2B',
        'https://baike.baidu.com/item/node.js',
        'https://baike.baidu.com/item/javascript'
    ]
    start_time = time.perf_counter()
    download_all(sites)
    end_time = time.perf_counter()
    cost_time = end_time - start_time
    print(f'Download {len(sites)} sites in {cost_time} seconds')


if __name__ == '__main__':
    main()

    
result:
    Download 15 sites in 5.101922350999303 seconds
```

这种方式是最直接也最简单的：

- 显示遍历存储网站的列表；
- 对当前网站进行下载操作；
- 等到当前操作完成之后，再对下一个网站进行同样的操作，一直到结束

当前操作耗时约5秒。明显效率低下，接下来我们用多线程版本实现，代码如下：

```python
import concurrent.futures
import requests
import threading
import time


def download_one(url):
    resp = requests.get(url)
    print(f'Read {resp.content} from {url}')


def download_all(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_one, sites)


def main():
    sites = [
        'https://baike.baidu.com/item/Python',
        'https://baike.baidu.com/item/Java',
        'https://baike.baidu.com/item/Java',
        'https://baike.baidu.com/item/c%23',
        'https://baike.baidu.com/item/php',
        'https://baike.baidu.com/item/go',
        'https://baike.baidu.com/item/perl',
        'https://baike.baidu.com/item/shell',
        'https://baike.baidu.com/item/lua',
        'https://baike.baidu.com/item/android',
        'https://baike.baidu.com/item/bash',
        'https://baike.baidu.com/item/c语言',
        'https://baike.baidu.com/item/C%2B%2B',
        'https://baike.baidu.com/item/node.js',
        'https://baike.baidu.com/item/javascript'
    ]
    start_time = time.perf_counter()
    download_all(sites)
    end_time = time.perf_counter()
    cost_time = end_time - start_time
    print(f'Download {len(sites)} sites in {cost_time} seconds')


if __name__ == '__main__':
    main()
result:
Download 15 sites in 1.1036411129989574 seconds
```

非常明显，总共耗时1.1秒，效率一下子提升了5倍。接下来，看一下多线程版本与单线程版本之间的主要区别：

```python
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_one, sites)
```

这里我们创建了一个线程池，总共有5个线程可以分配使用。`executor.map()`与前面所讲的Python内置的`map()`函数类似，表示对sites中的每一个元素，并发地调用函数`download_one()`。

顺便提下，`requests.get()`方法是线程安全的，因此在多线程环境中不会也可以安全使用。注意，线程数并不是越多越好，保持合理的线程数量。

## 3 到底什么是Futures?

Python中的Futures模块，位于`concurrent.futures`和`asyncio`中，都表示带有延迟操作。Futures会将处于等待状态的操作包裹起来放到队列中，这些操作的状态随时可以查询，当然，他们的结果或是异常，也能够在操作完成后获取。

通常来说，作为用户，我们不用考虑如何去创建Futures，这些Futures底层都会帮我们处理好。我们只需要去调度这些Futures的执行。比如，

- Executor类，当执行`executor.submit(func)`时，它便会安排里面的func()函数执行，并返回创建好的future实例，以便你之后查询调用。
- 方法done()，表示想对应的操作是否完成，True表示完成，False表示没有完成。done()是非阻塞，会立即返回结果。相对应的`add_done_callback(fn)`，则表示Futures完成后，相对应的参数函数fn，会被通知并执行调用。
- Futures中还有一个很重要的函数result()，它表示future完成后，返回其对应的结果或异常。而as_completed(fs)，则是针对给定的future迭代器fs，在其完成后，返回完成后的迭代器。

```python
import concurrent.futures
import requests
import threading
import time


def download_one(url):
    resp = requests.get(url)
    print(f'Read {resp.content} from {url}')


def download_all(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        to_do = []
        for site in sites:
            future = executor.submit(download_one, site)
            to_do.append(future)
        for future in concurrent.futures.as_completed(to_do):
            future.result()


def main():
    sites = [
        'https://baike.baidu.com/item/Python',
        'https://baike.baidu.com/item/Java',
        'https://baike.baidu.com/item/Java',
        'https://baike.baidu.com/item/c%23',
        'https://baike.baidu.com/item/php',
        'https://baike.baidu.com/item/go',
        'https://baike.baidu.com/item/perl',
        'https://baike.baidu.com/item/shell',
        'https://baike.baidu.com/item/lua',
        'https://baike.baidu.com/item/android',
        'https://baike.baidu.com/item/bash',
        'https://baike.baidu.com/item/c语言',
        'https://baike.baidu.com/item/C%2B%2B',
        'https://baike.baidu.com/item/node.js',
        'https://baike.baidu.com/item/javascript'
    ]
    start_time = time.perf_counter()
    download_all(sites)
    end_time = time.perf_counter()
    cost_time = end_time - start_time
    print(f'Download {len(sites)} sites in {cost_time} seconds')


if __name__ == '__main__':
    main()

```

这里首先调用`executor.submit()`，将下载每一个网站的内容都放进future队列to_do，等待执行，然后是as_completed()函数，在future完成后，便输出结果。

## 4　为什么多线程每次只能有一个线程执行？

事实上，Python的解释器并不是线程安全的，为了解决由此带来的race condition等问题，Python便引入了全局解释锁，也就是同一时刻，只允许一个线程执行。当然，在执行I/O操作时，如果一个线程被block了，全局解释锁便会被释放，从而让另一个线程能够继续执行。

