import asyncio


async def worker1():
    print('worker1 start')
    await asyncio.sleep(1)
    print('worker1 done')


async def worker2():
    print('worker2 start')
    await asyncio.sleep(2)
    print('worker2 done')


async def main():
    task1 = asyncio.create_task(worker1())
    task2 = asyncio.create_task(worker2())
    print('before wait')
    await task1
    print('awaited worker1')
    await task2
    print('awaited worker2')

asyncio.run(main())