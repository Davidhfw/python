"""
参数传递：　值传递和引用传递
值传递：拷贝参数的值，然后传给函数里的新变量。这样，原变量和新变量之间互相独立，互不影响
引用传递：通常是把参数的引用传给新的变量，这样，原变量和新变量就会指向同一块内存地址。如果改变了任何一个变量的值，那么另一个变量也会相应地随之改变。
Python的参数传递是赋值传递，或者叫对象的引用传递。Python里面所有的数据类型都是对象，所以参数传递时，知识让新变量与原变量指向相同的对象而已，并不存在之传递或者引用传递
"""
a = 1
b = a
a = a + 1
print(a)
print(b)
l1 = [1, 2, 4]
l2 = l1
l1.append(4)
print(l1)
print(l2)

def my_fun1(b):
    b = 2
    return b
a = 1
print(my_fun1(a))
def my_func3(l2):
    l2.append(4)

l1 = [1, 2, 3]
my_func3(l1)
print(l1)
def my_fun4(l2):
    l2 = l2 + [4]
l1 = [1, 2, 3]
my_fun4(l1)
print(l1)
def my_fun5(l2):
    l2 = l2 + [4]
    return l2
l1 = [1, 2, 3]
print(my_fun5(l1))

l1 = [1, 2, 3]
l2 = [1, 2, 3]
l3 = l2
print(id(l1))
print(id(l2))
print(id(l3))

def func(d):
    d['a'] = 10
    d['b'] = 20
d = {'a': 1, 'b': 2}
print(func(d))
print(d)


