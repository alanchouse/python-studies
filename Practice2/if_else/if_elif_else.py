#if_elif_else

a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")



# Example 1
a = 200
b = 33
if b > a:
    print("b is greater than a")
elif a == b:
    print("a and b are equal")
else:
    print("a is greater than b")  # True

# Example 2
x = 52
y = 67
if x > y:
    print("x is greater than y")
elif x == y:
    print("x and y are equal")
else:
    print("x is less than y")  # True

# Example 3
p = -10
q = -20
if p < q:
    print("p is smaller than q")
elif p == q:
    print("p and q are equal")
else:
    print("p is greater than q")  # True

# Example 4
num1 = 100
num2 = 100
if num1 > num2:
    print("num1 is bigger")
elif num1 == num2:
    print("num1 and num2 are equal")  # True
else:
    print("num1 is smaller")

# Example 5
score = 85
if score >= 90:
    print("Excellent")
elif score >= 70:
    print("Good")  # True
else:
    print("Needs Improvement")


