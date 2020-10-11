"""
== VS is
== 值比较
is 是否是同一个对象，　是否指向同一个内存地址
浅拷贝：是指重新分配一块内存，创建一个新的对象，里面的元素是原对象中子对象的引用。因此，如果原对象中的元素不可变，那倒也无所谓，但是如果元素有变，浅拷贝通常会带来副作用
深拷贝：是指重新分配一块内存，创建一个新的对象，并且将原对象中的元素，以递归的方式，通过创建新的子对象拷贝到新对象中。因此，新对象和原对象没有任何关联。
"""
import copy
a = 10
b = 10
print(a == b)
print(id(a))
print(id(b))
print(a is b)
a1 = 257
b1 = 257
print(a1 == b1)
print(id(a1))
print(id(b1))
print(a1 is b1)
a2 = -8
b2 = -8
print(a2 == b2)
print(id(a2))
print(id(b2))
print(a2 is b2)
l1 = [1, 2, 3]
l2 = list(l1)
print(l2)
print(l1 == l2)
print(l1 is l2)

s1 = {1, 2, 3}
s2 = set(s1)

print(s2)

print(s1 == s2)
print(s1 is s2)

l3 = [1, 2, 4]
l4 = l3[:]
print(l3 == l4)
print(l3 is l4)
l1 = [1, 3, 4]
l2 = copy.copy(l1)
print(l2)

t1 = (1, 2, 3)
t2 = tuple(t1)
print(t1 == t2)
print(t1 is t2)

l1 = [[1, 2], (30, 40)]
l2 = list(l1)
l1.append(100)
l1[0].append(3)
print(l1)
print(l2)
l1[1] += (50, 60)
print(l1)
print(l2)
l1 = [[1, 2], (30, 40)]
l2 = copy.deepcopy(l1)
l1.append(100)
l1[0].append(3)
print(l1)
print(l2)
x = [1]
x.append(x)
print(x)
y = copy.deepcopy(x)
print(y)
print(x == y)