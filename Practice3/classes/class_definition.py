#1
class MyClass:
  x = 5

#2
p1 = MyClass()
print(p1.x)

#3
del p1 #Delete the p1 object:
 
#4 Create three objects from the MyClass class:

p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)


#5 
class Person:
  pass

#class definitions cannot be empty, but if you for some reason have a class definition with no content, put in the pass statement to avoid getting an error.