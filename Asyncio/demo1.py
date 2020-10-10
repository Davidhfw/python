import asyncio
import aiohttp
import time

import logging
async def download_one(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(f'Read {resp.content_length} from {url}')

async def download_all(sites):
    tasks = [asyncio.create_task(download_one(site)) for site in sites]
    await asyncio.gather(*tasks)

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
    asyncio.run(download_all(sites))
    end_time = time.perf_counter()
    cost_time = end_time - start_time
    print(f'Download {len(sites)} sites in {cost_time} seconds')


if __name__ == '__main__':
    main()
    print("dafdafdafaf")