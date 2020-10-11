from functools import reduce

square = lambda x:x**2
print(square(3))

result = [(lambda x: x*x)(x) for x in range(10)]
print(result)

l = [(1, 20), (3, 0), (9, 10), (2, -1)]
l.sort(key=lambda x: x[0])
print(l)

squared = map(lambda x: x**2, [1, 2, 3, 4, 5])
print(list(squared))
l1 = [1, 2, 3, 4, 5]
new_list = filter(lambda x: x % 2 == 0, l1)
print(list(new_list))
l2 = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, l2)
print(product)
d = {'mike': 10, 'lucy': 2, 'ben': 30}
print(dict(sorted(d.items(), key=lambda x: x[1], reverse=True)))