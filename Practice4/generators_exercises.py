# 1 
def gen_squares(N):
    for i in range(N):
        yield i ** 2

for x in gen_squares(5):
    print(x)


# 2 
def even_gen(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)

n = int(input())
print(", ".join(even_gen(n)))


# 3
def div_3_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

for num in div_3_4(50):
    print(num)


# 4
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

for val in squares(3, 6):
    print(val)


# 5
def countdown(n):
    for i in range(n, -1, -1):
        yield i

for i in countdown(5):
    print(i)