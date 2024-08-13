from itertools import product
def fun(*abc, c=0, d):
    print(abc, c)

# fun(2, 3)
def fun2(*dimensions):
    print(*dimensions)
    for index in range(*dimensions):
        print(index)

fun2(2, 3)

for i in product([1,], (2, 3),[4, 5]):
    print(i)

fun3 = lambda x: x + 3

print(fun3(4))