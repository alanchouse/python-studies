#1
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

#2
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

#3
siblings = [("Amina", 24), ("Batyrkhan", 18), ("Issakhan", 28)]
sorted_siblings = sorted(siblings, key=lambda x: x[-1])
print(sorted_siblings)

#4
fruits = ["apple", "banana", "mango", "cherry"]
sorted_fruits = sorted(fruits, key=lambda x: x)
print(sorted_fruits)

#5
vegetables = ["potato", "cucumber", "pumpkin", "carrot"]
sorted_vegetables = sorted(vegetables, key=lambda x: len(x))
print(sorted_vegetables)