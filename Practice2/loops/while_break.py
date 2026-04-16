#while_break

i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1


# Example 1
i = 2
while i < 10:
    print(i)
    if i == 6:
        break
    i += 2  # Выведет 2, 4, 6

# Example 2
num = 10
while num > 0:
    print(num)
    if num == 7:
        break
    num -= 1  # Выведет 10, 9, 8, 7

# Example 3
count = 0
while count < 20:
    print(count)
    if count == 12:
        break
    count += 4  # Выведет 0, 4, 8, 12

# Example 4
x = 5
while x <= 20:
    print(x)
    if x == 15:
        break
    x += 5  # Выведет 5, 10, 15

# Example 5
y = 100
while y >= 50:
    print(y)
    if y == 70:
        break
    y -= 10  # Выведет 100, 90, 80, 70


