<h1 align="center">Python2.7多线程执行shell命令实践</h1>

在Python语言中，通常会面对两种任务，一种是计算密集型的任务；一种是IO密集型任务。通常正对这两种任务的处理，都有对应的编程模式。对于计算密集型任务，需要使用Python多进程来处理，因为这种任务要发挥多核CPU的处理能力；对于I/O密集型任务，可以使用Python多线程或协程来处理，大量的时间都是消耗在IO请求与响应处理上，CPU处理器基本用不到。

在OpenStack的nova和cinder组件中，通常要通过执行`nova delete vm_uuid`或`cinder delete vol_uuid`这种shell命令的方式来执行删除云主机和云硬盘的操作，而这种删除如果串行执行的话，基本上每个删除操作之间都要间隔3秒左右的时候，如果云主机或者云硬盘数量少（小于100台），删除耗时倒还是可以勉强接受；而如果云主机的数量有上万台，那么基本上需要9到10个小时才能删除完10000台云主机，这个时间成本是无法忍受的。此外，这种任务的特点是IO密集型，正好可以利用python语言的多线程来处理这种任务。由于openstack的nova和cinder组件自带的python解释器是python2.7的版本，因此我们采用基于python2.7版本的多线程来处理这种任务。

此外，通常在性能测试中，我们需要一次创建上万台虚拟机，不可能通过启动10000多个线程来去处理删除。因为pod的内存资源支撑不了这么多的线程同时创建。不过我们可以将这些云主机的uuid存储到队列这种数据结构中，只需要创建少量的线程，比如20个线程，让这20个线程轮番从队列中取数据，执行删除操作。接下来我们就通过实际的代码来熟悉下python2.7多线程方式执行shell命令的实践

```python
# coding=utf-8
import sys
import threading
import subprocess
import re
import time 
from Queue import Queue

#获取云主机uuid列表
def get_nova_vm_list():
    vm_list = subprocess.check_output("nova list --all | awk -F '|' '{print $2}'", shell=True)
    vm_list = vm_list.strip().split("\n")[2:]
    post_process_vm_list = []
    pattern = re,compile(r"^\s+|\s+$")
    for vm in vm_list:
        if vm != '':
            n_vm = pattern.sub("", vm)
            post_process_vm_list.append(n_vm)
    return post_process_vm_list

#构造自己的线程类
class NovaThread(threading.Thread):
    def __init__(self, thread_name, q):
        threading.Thread.__init__(self)
        self.name = thread_name
        self.q = q
    #线程执行函数 
    def run(self):
        print "%s Starting" % self.name
        delete_vm(self.name, self.q)
        print "%s Ended" % self.name
        
#线程执行  
def delete_vm(thread_name, q):
    while not q.empty():
        vm = q.get()
        try:
            output = subprocess.check_output("nova delete %s " % vm, shell=True)
        except subprocess.CalledProcessError:
            pass
        except KeyboardInterrupt:
            sys.exit(0)
        else:
            print "thread_name and it's output is %s and %s respectively" % (thread_name, output)
    else:
        exit(0)
        

def main():
    thread_name_list = []
    work_queue = Queue()
    threads= []
    vm_list = get_nova_vm_list()
    for i in range(20):
        thread_name_list.append("Thread-%d" % (i + 1))
    for vm in vm_list:
        work_queue.put(vm)
    
    start_t = time.time()
    for t_name in thread_name_list:
        thread = NovaThread(t_name, work_queue)
        thread.start()
        threads.append(thread)
        
    for t in threads:
        t.join()
        
    end_t = time.time()
    print "Delete nova vm task finished, it costs %s seconds" % (end_t - start_t)
    
    
if __name__ == '__main__':
    main()
        
            
```

