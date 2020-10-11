import asyncio
import random


async def consumer(queue, id):
    while True:
        val = await queue.get()
        print('{} get a val: {}'.format(id, val))
        await asyncio.sleep(1)


async def producer(queue, id):
    for i in range(5):
        val = random.randint(1, 10)
        await queue.put(val)
        print('{} put a val: {}'.format(id, val))
        await asyncio.sleep(1)


async def main():
    queue = asyncio.Queue()
    c1 = asyncio.create_task(consumer(queue, "c1"))
    c2 = asyncio.create_task(consumer(queue, "c2"))

    p1 = asyncio.create_task(producer(queue, 'p1'))
    p2 = asyncio.create_task(producer(queue, 'p2'))

    await asyncio.sleep(10)
    c1.cancel()
    c2.cancel()

    await asyncio.gather(c1, c2, p1, p2, return_exceptions=True)

asyncio.run(main())