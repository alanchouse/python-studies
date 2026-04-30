#1
def my_function(x, y):
    return x + y

result = my_function(5, 3)
print(result)


#2
def my_function2():
    return ["apple", "banana", "cherry"]

fruits = my_function2()
print(fruits[0])
print(fruits[1])
print(fruits[2])



#3
def my_function3():
    return (10, 20)

x, y = my_function3()
print("x:", x)
print("y:", y)



#4
def f(n):
    return n**2

n = int(input())
print(f(n))



#5
def f0(n):
    return n**2 + 3

num = int(input())
print(f0(num))