import threading
import time

def run(n):
    print('task',n)
    time.sleep(1)
    print('2s')
    time.sleep(1)
    print('1s')
    time.sleep(1)
    print('0s')
    time.sleep(1)
if __name__=='__main__':
    t1=threading.Thread(target=run,args=('t1',))#target是放入线程的函数，args是函数总需要传递的参数，以元祖的形式传入
    t2=threading.Thread(target=run,args=('t2',))
    t1.start()
    t2.start()


二‘线程类
class Mythread(threading.Thread):
    def __init__(self,n):
        super.().__init__()#用来重构run函数，相当于更改函数本身的运行模式为多线程
        self.n=n
        print('task',n)
    def run(n):
        print('task',n)
        time.sleep(1)
        print('2s')
        time.sleep(1)
        print('1s')
        time.sleep(1)
        print('0s')
        time.sleep(1)
if __name__=='__main__':
    t1=Mythread('t1')
    t2=Mythread('t2')
    t1.start()
    t2.start()


三’设置守护线程#所谓’线程守护’，就是主线程不管该线程的执行情况，只要是其他子线程结束且主线程执行完毕，主线程都会关闭。也就是说:主线程不等待该守护线程的执行完再去关闭。
#使用setDaemon(True)把所有的子线程都变成了主线程的守护线程，
# def run(n):
#     print('task',n)
#     time.sleep(1)
#     print('3s')
#     time.sleep(1)
#     print('2s')
#     time.sleep(1)
#     print('1s')
#
# if __name__ == '__main__':
#     t=threading.Thread(target=run,args=('t1',))
#     t.setDaemon(True)#主线程不管子线程执行情况直接执行完毕就结束
#     
#     t.start()
#     print('end')
'''
    通过执行结果可以看出，设置守护线程之后，当主线程结束时，子线程也将立即结束，不再执行
        
#主线程等待子线程结束
为了让守护线程执行结束之后，主线程再结束，我们可以使用join方法，让主线程等待子线程执行

# def run(n):
#     print('task',n)
#     time.sleep(2)
#     print('5s')
#     time.sleep(2)
#     print('3s')
#     time.sleep(2)
#     print('1s')
# if __name__ == '__main__':
#     t=threading.Thread(target=run,args=('t1',))
#     t.setDaemon(True)    #把子线程设置为守护线程，必须在start()之前设置
#     t.start()
#     t.join()     #设置主线程等待子线程结束
#     print('end')

四‘多线程共享全局变量
线程时进程的执行单元，进程时系统分配资源的最小执行单位，所以在同一个进程中的多线程是共享资源的      
由于线程之间是进行随机调度，并且每个线程可能只执行n条执行之后，当多个线程同时修改同一条数据时可能会出现脏数据，
    所以出现了线程锁，即同一时刻允许一个线程执行操作。线程锁用于锁定资源，可以定义多个锁，像下面的代码，当需要独占
    某一个资源时，任何一个锁都可以锁定这个资源，就好比你用不同的锁都可以把这个相同的门锁住一样。
        由于线程之间是进行随机调度的，如果有多个线程同时操作一个对象，如果没有很好地保护该对象，会造成程序结果的不可预期，
    我们因此也称为“线程不安全”。
        为了防止上面情况的发生，就出现了互斥锁（Lock）

        