#Iterators

#Return an iterator from a tuple, and print each value:
 
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))


# Example 1

games = ("Counter-Strike 2", "Valorant", "Apex Legends")
game_it = iter(games)
print(next(game_it))
print(next(game_it))
print(next(game_it))


# Example 2

ram_sizes = (8, 16, 32)
ram_it = iter(ram_sizes)
print(next(ram_it))
print(next(ram_it))
print(next(ram_it))


# Example 3

components = ("Ryzen 7 7800X3D", "RTX 4070", "B650 Motherboard")
pc_it = iter(components)
print(next(pc_it))
print(next(pc_it))
print(next(pc_it))


# Example 4

cities = ("Almaty", "Astana", "London")
city_it = iter(cities)
print(next(city_it))
print(next(city_it))
print(next(city_it))


# Example 5

friends = ("Kurban", "Dmitry", "Alex")
friend_it = iter(friends)
print(next(friend_it))
print(next(friend_it))
print(next(friend_it))


#Iterate the values of a tuple:

mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x)


# Example 1

games = ("Counter-Strike 2", "Valorant", "Apex Legends")
for x in games:
  print(x)


# Example 2

ram_sizes = (8, 16, 32, 64)
for x in ram_sizes:
  print(x)


# Example 3

components = ("Ryzen 7 7800X3D", "RTX 4070", "B650 Motherboard", "32GB RAM")
for x in components:
  print(x)


# Example 4

cities = ("Almaty", "Astana", "London", "New York")
for x in cities:
  print(x)


# Example 5

friends = ("Kurban", "Dmitry", "Alex", "Max")
for x in friends:
  print(x)







