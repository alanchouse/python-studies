#while_countine

i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)


# Example 1
i = 1
while i < 8:
    i += 2
    if i == 5:
        continue
    print(i)  # Выведет 3, 7

# Example 2
num = 1
while num <= 10:
    if num % 2 == 0:
        num += 1
        continue
    print(num)  # Выведет 1, 3, 5, 7, 9
    num += 1

# Example 3
count = 0
while count < 10:
    count += 2
    if count == 6:
        continue
    print(count)  # Выведет 2, 4, 8, 10

# Example 4
x = 5
while x < 15:
    x += 1
    if x == 10:
        continue
    print(x)  # Выведет 6, 7, 8, 9, 11, 12, 13, 14, 15

# Example 5
y = 10
while y > 0:
    y -= 1
    if y == 5:
        continue
    print(y)  # Выведет 9, 8, 7, 6, 4, 3, 2, 1, 0







