#1
def my_function1(fname):
    print(fname + " Refsnes")

my_function1("Emil")
my_function1("Tobias")
my_function1("Linus")


#2
def my_function2(name): # name is a parameter
    print("Hello", name)

my_function2("Emil") # "Emil" is an argument




#3
def my_function3(fname, lname):
    print(fname + " " + lname)

my_function3("Emil", "Refsnes")


#4
def my_function4(name = "friend"):
    print("Hello", name)

my_function4("Emil")
my_function4("Tobias")
my_function4()
my_function4("Linus")



#5

def my_function(animal, name):
    print("I have a", animal)
    print("My", animal + "'s name is", name)

my_function(name = "Buddy", animal = "dog")