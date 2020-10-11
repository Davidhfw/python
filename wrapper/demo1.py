import functools


def func(message):
    print('Got a message: {}'.format(message))

send_message = func
send_message('hello world')


def get_message(message):
    return 'Got a message: ' + message

def root_call(func, message):
    print(func(message))

root_call(get_message, "hello world")


def func1(message):
    def get_message(message):
        print('Got a message: {}'.format(message))
    return get_message(message)

func1('hello world')

def func_closure():
    def get_message(message):
        print('Got a message: {}'.format(message))
    return get_message

send_message = func_closure()
send_message('hello world')

def my_decorator(func):
    def wrapper():
        print('wrapper of decorator')
        func()
    return wrapper

def greet():
    print('hello world')

greet = my_decorator(greet)
greet()

def my_decorator1(func):
    def wrapper():
        print('wrapper of decorator')
        func()
    return wrapper

@my_decorator1
def greet():
    print('hello world')

greet()

def repeat(num):
    def my_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(num):
                print('wrapper of decorator')
                func(*args, **kwargs)
        return wrapper
    return my_decorator


@repeat(4)
def greet4(message):
    print(message)


greet4('hello world')
print(greet4.__name__)


class Count:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print('num of calls is : {}'.format(self.num_calls))
        return self.func(*args, **kwargs)

@Count
def example():
    print('hello world')
example()
example()
