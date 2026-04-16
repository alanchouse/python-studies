
#Booleans represent one of two values: True or False.

a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

# Example 1
a = 200
b = 33
if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# Example 2
a = 10
b = 20
if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# Example 3
a = 50
b = 50
if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# Example 4
a = -5
b = 0
if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# Example 5
a = 100
b = -100
if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")








#Evaluate a string and a number:

print(bool("Hello"))
print(bool(15))

# Example 1
print(bool("Hello"))   # True непустая строка
print(bool(15))        # True любое ненулевое число

# Example 2
print(bool(""))        # False пустая строка
print(bool(0))         # False ноль

# Example 3
print(bool("Python"))  # True
print(bool(-1))        # True любое ненулевое число

# Example 4
print(bool(" "))       # True пробел тоже считается непустым
print(bool(0.0))       # False ноль в виде float

# Example 5
print(bool("False"))   # True непустая строка
print(bool(None))      # False






#Evaluate two variables:
x = "Hello"
y = 15

print(bool(x))
print(bool(y))

# Example 1
x = "Hello"
y = 15
print(bool(x))  # True
print(bool(y))  # True

# Example 2
x = ""
y = 0
print(bool(x))  # False
print(bool(y))  # False

# Example 3
x = "Python"
y = -10
print(bool(x))  # True
print(bool(y))  # True

# Example 4
x = " "
y = 0.0
print(bool(x))  # True строка с пробелом
print(bool(y))  # False 0.0 = False

# Example 5
x = None
y = []
print(bool(x))  # False
print(bool(y))  # False пустой список







