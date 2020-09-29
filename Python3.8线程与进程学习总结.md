# Python3.8线程与进程学习总结

## 1 `multiprocessing`--基于进程的并行

### 概述

multiprocessing是一个支持使用与threading模块类似的API来产生进程包。multiprocessing包同时提供了本地和远程并发操作，通过使用子进程而非线程有效地绕过了全局解释锁。因此，multiprocessing模块允许程序员充分利用给定机器上的多个处理器。它在Unix和Windows上均可运行。

multiprocessing还提供了Pool对象，它提供了一种快捷的方法，赋予函数并行化处理一系列输入值的能力，可以将输入数据分配给不同进程处理（数据并行）。

```python
from multiprocessing import Pool


def f(x):
    return x*x


if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 3, 3]))
```

### Process类

在multiprocessing中，通过创建一个Process对象然后调用它的start()方法来生成进程。调用join()等待进程执行完成，代码示例如下：

```python
from multiprocessing import Process


def f(name):
    print('hello', name)


if __name__ == '__main__':
    p = Process(target=f, args=('bob', ))
    p.start()
    p.join()
```

要显示所涉及的各个进程ID，这是一个扩展示例

```python
from multiprocessing import Process
import os


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(name):
    info('function f')
    print('hello', name)


if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob', ))
    p.start()
    p.join()
```

结果如下：

```shell
main line
module name: __main__
parent process: 8952
process id: 8360
function f
module name: __mp_main__
parent process: 8360
process id: 9944
hello bob
```

### 上下文和启动方法

根据不同的平台，multiprocessing支持三种启动进程的方法：

- spawn

  > 父进程启动一个新的Python解释器进程。子进程只会继承那些运行进程对象的run()方法所需的资源。特别是父进程中非必须的文件描述符和句柄不会被继承。相当于使用fork或者forkserver，使用这个方法启动进程相当慢。可在Unix和Windows上使用。Windows上的默认设置

- fork

  > 父进程使用os.fork()来产生Python解释器分叉。子进程在开始时实际上与父进程想同，父进程的所有资源都由子进程继承，只存在Unix。

- forkserver

  > 程序启动并选择forkserver启动方法时，将启动服务器进程。从那时起，每当需要一个新进程时，父进程就会连接到服务器并请求它分叉一个新进程。分叉服务器进程时单线程的，因此使用os.fork()是安全的。没有不必要的资源被继承。

要选择一个启动方法，需要在主模块`if __name__ == __main__`子句中调用`set_start_method()`。例如：

```python
import multiprocessing as mp


def foo(q):
    q.put('hello')


if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q, ))
    p.start()
    print(q.get())
    p.join()
```

在程序中set_start_method()不应该被多次调用。或者，你可以使用get_context()来获取上下文对象。上下文对象与multiprocessing模块具有相同的API，并允许在同一程序中使用多种启动方法。

```python
import multiprocessing as mp


def foo(q):
    q.put('hello')


if __name__ == '__main__':
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    P = ctx.Process(target=foo, args=(q, ))
    P.start()
    print(q.get())
    P.join()
```

请注意，关联到不同上下文的对象和进程之间可能不兼容。特别是，使用fork上下文创建的锁不能传递给使用spawn或forkserver启动方法启动的进程。想要使用特定启动方法的库应该使用get_context()以避免干扰库用户的选择。

### 在进程之间交换对象

multiprocessing支持进程之间的两种通信通道：

#### 队列

Queue类是一个近似于queue.Queue的克隆， 如：

```python
from multiprocessing import Process, Queue


def f(q):
    q.put([42, None, "hello"])


if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q, ))
    p.start()
    print(q.get())
    p.join()
```

队列是线程和进程安全的。

#### 管道

Pipe()函数返回一个由管道连接的连接对象，默认情况下是双工。例如：

```python
from multiprocessing import Process, Pipe


def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn, ))
    p.start()
    print(parent_conn.recv())
    p.join()
```

返回的两个连接对象Pipe()表示管道的两端，每个连接对象都有send()和recv()方法。请注意，如果两个进程或线程同时读取或写入管道的同一端，则管道中的数据可能会损坏。当然，在不同进程中同时使用管道的不同端的情况下不存在损坏的风险。

### 进程间同步

multiprocessing包含来自threading的所有同步原语等价物，例如，可以使用锁来确保一次只有一个进程打印到标准输出：

```python
from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()


if __name__ == '__main__':
    lock = Lock()
    for num in range(10):
        Process(target=f, args=(lock, num)).start()
```

不使用锁的情况下，来自多线程的输出很容易产生混淆。

### 进程间共享状态

在并发编程时，最好尽量避免使用共享状态。使用多进程时尤其如此。但是，如果你真的需要使用一些共享数据，那么multiprocessing提供了两种方法。

#### 共享内存

可以使用Value或Array将数据存储在共享内存映射中，例如以下代码：

```python
from multiprocessing import Process, Value, Array


def f(n, a):
    n.value = 3.1415926
    for i in range(len(a)):
        a[i] = -a[i]


if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
```

创建num和arr时使用的是'd'和‘i’参数是array模块使用的类型typecode：‘d’表示双精度浮点数，‘i’表示有符号整数，这些共享对象将是进程和线程安全的。为了更灵活得使用共享内存，可以使用multiprocessing.sharedctypes模块，该模块支持创建共享内存分配的任意ctypes对象。

#### 服务进程

由Manager()返回的管理对象控制一个服务进程，该进程保存Python对象并允许其他进程使用代理操作他们。Manager()返回的管理支持类型包括：list，dict，Namespace、Lock、RLock、Semaphore、BoundedSemphore、Condition、Event、Barrier、Queue、Value和Array。例如

```python
from multiprocessing import Process, Manager


def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()


if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))

        p = Process(target=f, args=(d, l))
        p.start()
        p.join()

        print(d)
        print(l)
```

使用服务进程的管理器比使用共享内存对象更灵活，因为他们可以支持任意对象类型，此外，单个管理器可以通过网络有不同计算机上的进程共享，但是，他们比使用共享内存慢。

### 使用工作进程

Pool类宝石一个工作进程池，它具有允许以几种不同方式将任务分配到工作进程的方法。例如：

```python
from multiprocessing import Pool, TimeoutError
import time
import os


def f(x):
    return x*x


if __name__ == '__main__':
    # 开启4个工作进程
    with Pool(processes=4) as pool:
        print(pool.map(f, range(10)))

    # print same numbers in arbitrary order
        for i in pool.imap_unordered(f, range(10)):
            print(i)

        # evaluate "f(20)" asynchronously
        res = pool.apply_async(f, (20, ))
        print(res.get(timeout=1))
        # evaluate "os.getpid()" asynchronously
        res1 = pool.apply_async(os.getpid, ())
        print(res1.get(timeout=1))
        # launching multiple evalutions asynchronously *may* use more processes
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        print([res.get(timeout=1) for res in multiple_results])

        # make a single worker sleep for 10 secs
        res = pool.apply_async(time.sleep, (10, ))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print('We lacked patience and got a multiprocessing.TimeError')
        print("For the moment, the pool remains available for more work")
    print("Now the pool is closed and no longer available")
```

## 2 concurrent.futures---启动并行任务

concurrent.futures模块提供异步执行可调用对象高层接口。

异步执行可以由ThreadPoolExecutor使用线程或由ProcessPoolExecutor使用单独的进程来实现。两者都是实现抽象类Executor定义的接口。

### Executor对象

class concurrent.futures.**Executor**
抽象类提供异步执行调用方法。要通过它的子类调用，而不是直接调用。

#### submit(fn, *args, **kwargs)

调度可调用对象fn，以fn(*args, \*\*kwargs)方式执行并返回Future对象代表可调用对象的执行。

```python
with ThreadPoolExecutor(max_workers=1) as executor:
	future = executor.submit(pow, 323, 1235)
	print(future.result())
```

#### map(func, *iterable, timeout=None, chunksize=1)

类似于map(func, *iterable)函数，除了以下两点：

- iterables是立即执行而不是异步执行；
- func是异步执行的，对func的多个调用可以并发执行。

如果从原始调用Executor.map()经过timeout秒后，\_\_next___()以被调用且返回的结果还不可用，那么已返回的迭代器将触发concurrent.futures.TimeoutError。timeout可以是整数或浮点数。如果timeout没有指定或为None，则没有超时限制。

如果func调用引发一个异常，当从迭代器中取回它的值时这个异常被引发。

使用ProcessPoolExecutor时，这个方法会将iterables分割任务块并作为独立的任务并提交到执行池中。这些块的大概数量可以由chunksize指定正整数设置。对很长的迭代器来说，使用大的chunksize值比默认值1能显著地提高性能。chunksize对ThreadPoolExecutor没有效果。

#### shutdown(wait=True)

当待执行的future对象完成执行后像执行者发送信号，它就会释放正在使用的任何资源。在关闭后调用Executor.submit()会触发RuntimeError。

如果wait为True则此方法只有在所有待执行的future对象完成执行且释放已分配的资源才会返回。如果wait为False，方法立即返回。所有待执行的future对象完成执行后释放已分配资源。

如果使用with语句，会避免显示调用这个方法。如：

```python
import shutil
with ThreadPoolExecutor(max_workers=4) as e:
    e.submit(shutil.copy, 'src1.txt', 'dest1.txt')
    e.submit(shutil.copy, 'src2.txt', 'dest2.txt')
    e.submit(shutil.copy, 'src3.txt', 'dest3.txt')
    e.submit(shutil.copy, 'src4.txt', 'dest4.txt')
```

### ThreadPoolExecutor

ThreadPoolExecutor是Executor的子类，他使用线程池来异步执行调用。

*class concurrent.futures.ThreadPoolExecutor(max_workers=None, thread_name_prefix='', initializer=None, initargs=())*

Executor子类使用最多max_workders个线程的线程池异步执行调用。initializer是在每个工作者线程开始出调用一个可选可调用对象。initargs是传递给初始化器的元祖参数。

ThreadPoolExecutor例子

```python
import concurrent.futures
import urllib.request

URLS = [
    'http://www.uestc.edu.cn/',
    'http://www.baidu.com',
    'http://www.jd.com',
    'http://www.alibaba.com',
    'http://www.ustc.edu.cn/'
]


def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
```

### ProcessPoolExecutor

ProcessPoolExecutor类是Executor的子类，它使用进程池来异步地执行调用。ProcessPoolExecutor会使用multiprocessing模块，这允许它绕过全局解释器锁，但也意味着只可以处理和返回可封存的对象。

`__main__`模块必须可以被工作者子进程导入。这意味着ProcessPoolExecutor不可以工作在交互解释器中。

从可调用对象中调用Executor或Future的方法提交给ProcessPoolExecutor会导致死锁。

*class concurrent.futures.ProcessPoolExecutor(max_workers=None, mp_context=None, initializer=Noen, initargs=())*

```python
import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112232535095293,
    115280095190773,
    115797848077099,
    1099726899285419
]


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))


if __name__ == '__main__':
    main()
```

### Future对象

Future类可将调用对象封装为异步执行。Future实例由Executor.submit()创建。

*class concurrent.futures.Future*

- cancel()：尝试取消调用。
- cancelled()：如果调用成功取消返回True
- running()：如果调用正在执行而且不能被取消那么返回True
- done()：如果调用已被取消或正常结束那么返回True
- result(timeout=None)：返回调用返回的值
- add_done_callback(fn)：附加可调用fn到future对象

下面这些Future方法用于单元测试和Executor()实现。

- set_running_or_notify_cancel()
- set_result(result)
- set_exception(execption)

参考资料：http://docs.python.org/zh-cn/3/library