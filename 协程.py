import asyncio
import time
async def hello():
    print('hello1')
    #await是告诉程序别往下面继续走了，要等待这个动作完成之后再走，你先执行其他任务
    await asyncio.sleep(3)#使用time.sleep（）不是一个等待对象，它返回None改成asyncio.sleep(3)
    print('hello2')

loop=asyncio.get_event_loop()
task=[hello(),hello()]#用两个任务
loop.run_until_complete(asyncio.wait(task))
loop.close()
