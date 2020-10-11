import multiprocessing
import time


def cpu_bound(number):
    return sum(i * i for i in range(number))


def find_sums(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)


def main():
    numbers = [100000000 + x for x in range(20)]
    s_t = time.time()
    find_sums(numbers)
    dur = time.time() - s_t
    print(f'duration {dur} seconds')


main()