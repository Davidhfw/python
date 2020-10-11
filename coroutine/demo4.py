import asyncio


async def worker1():
    await asyncio.sleep(1)
    return 1


async def worker2():
    await asyncio.sleep(2)
    return 2 / 0


async def worker3():
    await asyncio.sleep(3)
    return 3


async def main():
    task1 = asyncio.create_task(worker1())
    task2 = asyncio.create_task(worker2())
    task3 = asyncio.create_task(worker3())

    await asyncio.sleep(2)
    task3.cancel()
    res = await asyncio.gather(task1, task2, task3, return_exceptions=True)
    print(res)

asyncio.run(main())