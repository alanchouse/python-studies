#1
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()

#2
x = Student("Mike", "Olsen")
x.printname()

#3
class Student(Person):
  def __init__(self, fname, lname):
    #add properties etc.

#4
class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)

#5
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)