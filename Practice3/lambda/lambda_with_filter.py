#1
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

#2
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)

#3
numbers = [-3, -2, -1, 0, 1, 2, 3]
odd_numbers = list(filter(lambda x: x >= 0, numbers))
print(pos_numbers)

#4
numbers = [-3, -2, -1, 0, 1, 2, 3]
odd_numbers = list(filter(lambda x: x < 0, numbers))
print(neg_numbers)

#5
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
_numbers = list(filter(lambda x: x % 3 == 0, numbers))
print(_numbers)