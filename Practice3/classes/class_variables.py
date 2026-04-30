#1
class Person:
  species = "Human" # This is a class variable
  def __init__(self, name):
    self.name = name # This is an instance variable


#2
p1 = Person("Emil")
p2 = Person("Tobias")

# Accessing via an instance
print(p1.species) # Output: Human
print(p2.species) # Output: Human

# Accessing via the class name
print(Person.species) # Output: Human


#3
class Person:
  lastname = "" # Class variable
  def __init__(self, name):
    self.name = name

p1 = Person("Linus")
p2 = Person("Emil")

# Modify the class variable using the class name
Person.lastname = "Refsnes"

print(p1.lastname) # Output: Refsnes
print(p2.lastname) # Output: Refsnes


#4
class Employee:
    # Class variable to track number of employees
    num_employees = 0

    def __init__(self, name):
        self.name = name # Instance variable
        Employee.num_employees += 1 # Increment class variable

emp1 = Employee("Alice")
emp2 = Employee("Bob")

print(f"Total employees: {Employee.num_employees}") # Output: Total employees: 2

#5
class Dog:
    # Class variable
    legs = 4

d1 = Dog()
d2 = Dog()

print(f"Dog 1 has {d1.legs} legs.") # Output: Dog 1 has 4 legs.
print(f"Dog 2 has {d2.legs} legs.") # Output: Dog 2 has 4 legs.