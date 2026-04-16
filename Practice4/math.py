# The min() and max() functions can be used to find the lowest or highest value in an iterable:

x = min(5, 10, 25)
y = max(5, 10, 25)

print(x)
print(y)


# The abs() function returns the absolute (positive) value of the specified number:

x = abs(-7.25)

print(x)


# The pow(x, y) function returns the value of x to the power of y (xy).


x = pow(4, 3)

print(x)


# import math


import math

x = math.sqrt(64)

print(x)


# The math.ceil() method rounds a number upwards to its nearest integer, and the math.floor() method rounds a number downwards to its nearest integer, and returns the result:

import math

x = math.ceil(1.4)
y = math.floor(1.4)

print(x) # returns 2
print(y) # returns 1

# The math.pi constant, returns the value of PI (3.14...):

import math

x = math.pi

print(x)


import math

# --- min() and max() ---

# Example 1

print(min(1, 10, 100))
print(max(1, 10, 100))

# Example 2

print(min(-50, 0, 50))
print(max(-50, 0, 50))

# Example 3

nums = (12, 45, 2, 89)
print(min(nums))
print(max(nums))

# Example 4

print(min(1.5, 1.2, 1.9))
print(max(1.5, 1.2, 1.9))
# Example 5

fps_drops = (144, 120, 60, 165)
print(min(fps_drops))
print(max(fps_drops))

# --- abs() ---

# Example 1

print(abs(-10))

# Example 2

print(abs(-3.14))
# Example 3

print(abs(5 - 10))

# Example 4

temp_diff = -15
print(abs(temp_diff))

# Example 5

print(abs(-4070))

# --- pow(x, y) ---

# Example 1

print(pow(2, 3))

# Example 2

print(pow(5, 2))

# Example 3

print(pow(10, 4))

# Example 4

print(pow(1.5, 2))

# Example 5

print(pow(-2, 3))

# --- math.sqrt() ---

# Example 1

print(math.sqrt(100))

# Example 2

print(math.sqrt(25))

# Example 3

print(math.sqrt(16))

# Example 4

print(math.sqrt(2.25))

# Example 5

print(math.sqrt(2))

# --- math.ceil() and math.floor() ---

# Example 1

print(math.ceil(4.1))
print(math.floor(4.9))

# Example 2

print(math.ceil(10.01))
print(math.floor(10.99))

# Example 3

print(math.ceil(-1.5))
print(math.floor(-1.5))

# Example 4

print(math.ceil(0.1))
print(math.floor(0.9))

# Example 5

val = 7.5
print(math.ceil(val))
print(math.floor(val))

# --- math.pi ---
# Example 1

print(math.pi)

# Example 2

r = 5
print(2 * math.pi * r)

# Example 3

print(math.pi * pow(r, 2))

# Example 4

print(math.pi / 2)

# Example 5

print(round(math.pi, 2))








