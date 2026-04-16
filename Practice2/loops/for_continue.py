#for_countinue

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)


# Example 1
fruits = ["mango", "orange", "pineapple"]
for x in fruits:
    if x == "orange":
        continue
    print(x)  # Выведет mango, pineapple

# Example 2
numbers = [10, 15, 20, 25, 30]
for num in numbers:
    if num % 10 == 0:
        continue
    print(num)  # Выведет 15, 25 (пропускает кратные 10)

# Example 3
letters = ["a", "b", "c", "d"]
for letter in letters:
    if letter in ["b", "d"]:
        continue
    print(letter)  # Выведет a, c

# Example 4
colors = ["red", "green", "blue", "yellow"]
for color in colors:
    if color.startswith("b"):
        continue
    print(color)  # Выведет red, green, yellow

# Example 5
animals = ["cat", "dog", "rabbit", "hamster"]
for animal in animals:
    if "a" in animal:
        continue
    print(animal)  # Выведет dog



