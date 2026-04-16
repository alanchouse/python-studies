from functools import reduce

nums = [1, 2, 3, 4, 5, 6]

# map: squaring each number
squared = list(map(lambda x: x**2, nums))

# filter: keeping only even numbers
evens = list(filter(lambda x: x % 2 == 0, nums))

# reduce: calculating the sum of all elements
total_sum = reduce(lambda x, y: x + y, nums)

print(f"Original list: {nums}")
print(f"Squared list: {squared}")
print(f"Even numbers: {evens}")
print(f"Total sum: {total_sum}")