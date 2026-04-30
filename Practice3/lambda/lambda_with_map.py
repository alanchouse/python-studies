#1
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

#2
numbers = [1, 2, 3, 4, 5]
powered = list(map(lambda x: x ** 2, numbers))
print(powered)

#3
numbers = [1, 2, 3, 4, 5]
a = list(map(lambda x: x - 1, numbers))
print(a)

#4
numbers = [1, 2, 3, 4, 5]
b = list(map(lambda x: x // 2, numbers))
print(b)

#5
numbers = [1, 2, 3, 4, 5]
c = list(map(lambda x: x ** 0.5, numbers))
print(c)