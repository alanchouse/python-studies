# Import the datetime module and display the current date:

import datetime

x = datetime.datetime.now()
print(x)


# Return the year and name of weekday:

import datetime

x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))


# Create a date object:

import datetime

x = datetime.datetime(2020, 5, 17)

print(x)


# Display the name of the month:

import datetime

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))


# Example 1:
 
now = datetime.datetime.now()
print(now.year)


# Example 2: 

now = datetime.datetime.now()
print(now.month)


# Example 3:
 
now = datetime.datetime.now()
print(now.day)


# Example 4:

now = datetime.datetime.now()
print(now.strftime("%A"))


# Example 5:
 
my_birthday = datetime.datetime(2000, 5, 15)
print(my_birthday)
