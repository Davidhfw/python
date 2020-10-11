def generator(k):
    i = 1
    while True:
        yield i ** k
        i += 1

gen_1 = generator(1)
gen_3 = generator(3)
print(gen_1)
print(gen_3)

def get_sum(n):
    sum1, sum3 = 0, 0
    for i in range(n):
        next1 = next(gen_1)
        next3 = next(gen_3)
        print('next_1 = {}, next_3 = {}'.format(next1, next3))
        sum1 += next1
        sum3 += next3
    print(sum1 * sum1, sum3)
get_sum(8)

def index_generator(l, target):
    for i, num in enumerate(l):
        if num == target:
            yield i


print(list(index_generator([1, 6, 2, 4, 5, 2, 8, 6, 3, 2], 2)))