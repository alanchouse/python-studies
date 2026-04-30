#1
def my_function(*kids):
    print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")


#2
def my_function2(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function2("Emil", "Tobias", "Linus")

#3
def my_function3(greeting, *names):
  for name in names:
    print(greeting, name)

my_function3("Hello", "Emil", "Tobias", "Linus")


#4
def my_function4(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total

print(my_function4(1, 2, 3))
print(my_function4(10, 20, 30, 40))
print(my_function4(5))



#5
def my_function5(*numbers):
  if len(numbers) == 0:
    return None
  max_num = numbers[0]
  for num in numbers:
    if num > max_num:
      max_num = num
  return max_num

print(my_function5(3, 7, 2, 9, 1))





#1 
def my_function_1(**kid):
  print("His last name is " + kid["lname"])

my_function_1(fname = "Tobias", lname = "Refsnes")




#2
def my_function_2(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function_2(name = "Tobias", age = 30, city = "Bergen")


#3
def my_function_3(username, **details):
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print(" ", key + ":", value)

my_function_3("emil123", age = 25, city = "Oslo", hobby = "coding")




#4
def my_function_4(title, *args, **kwargs):
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)

my_function_4("User Info", "Emil", "Tobias", age = 25, city = "Oslo")



#5
def my_function_5(fname, lname):
  print("Hello", fname, lname)

person = {"fname": "Emil", "lname": "Refsnes"}
my_function_5(**person) # Same as: my_function_5(fname="Emil", lname="Refsnes")