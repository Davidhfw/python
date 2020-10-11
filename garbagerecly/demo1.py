import objgraph

a = [1, 2, 3]
b = [2, 4, 6]
a.append(b)
b.append(a)
objgraph.show_refs([a])
assert 1 == 2, 'This should fail'
