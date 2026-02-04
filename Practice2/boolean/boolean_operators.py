#Boolean operators 

#And
x = 5

print(x > 0 and x < 10)

# Example 1
x = 52
print(x > 50 and x < 100)   # True

# Example 2
x = 67
print(x < 50 and x > 20)    # False

# Example 3
x = 10000
print(x > 5000 and x < 20000)  # True

# Example 4
x = -10000
print(x < 0 and x > -20000)    # True

# Example 5
x = 885
print(x > 800 and x < 900)     # True


#OR
x = 5

print(x < 5 or x > 10)

# Example 1
x = 52
print(x < 50 or x > 100)        # False

# Example 2
x = 67
print(x < 50 or x > 60)         # True

# Example 3
x = 10000
print(x < 5000 or x > 8000)     # True

# Example 4
x = -10000
print(x < -5000 or x > 0)       # True

# Example 5
x = 885
print(x < 800 or x > 900)       # False


#NOT
x = 5

print(not(x > 3 and x < 10))


# Example 1
x = 52
print(not(x < 50 or x > 60))    # False

# Example 2
x = 67
print(not(x < 50 or x > 60))    # False

# Example 3
x = 10000
print(not(x > 5000 and x < 20000)) # False

# Example 4
x = -10000
print(not(x < 0 and x > -20000))   # False

# Example 5
x = 885
print(not(x > 800 and x < 900))    # False





