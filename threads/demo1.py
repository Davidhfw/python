import threading
import time


def worker():
    print("worker1 is working")
    time.sleep(2)


if __name__ == '__main__':
    t = threading.Thread(target=worker, name="test thread")
    t.start()
    time.sleep(2)
    t.join()
