#for_break

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break


# Example 1
fruits = ["mango", "orange", "pineapple"]
for x in fruits:
    print(x)
    if x == "orange":
        break  # Выведет mango, orange


# Example 2
numbers = [10, 20, 30, 40, 50]
for num in numbers:
    print(num)
    if num == 30:
        break  # Выведет 10, 20, 30

# Example 3
letters = ["a", "b", "c", "d"]
for letter in letters:
    print(letter)
    if letter == "c":
        break  # Выведет a, b, c

# Example 4
colors = ["red", "green", "blue"]
for color in colors:
    print(color)
    if color == "green":
        break  # Выведет red, green

# Example 5
animals = ["cat", "dog", "rabbit", "hamster"]
for animal in animals:
    print(animal)
    if animal == "rabbit":
        break  # Выведет cat, dog, rabbit


