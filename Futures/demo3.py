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
