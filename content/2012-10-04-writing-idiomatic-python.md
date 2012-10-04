title: "Writing Idiomatic Python"
date: 2012-10-04 14:00
categories:
---
As someone who evangelizes Python at work, I see a lot of code written by
professional programmers new to Python. I've written a good amount of Python
code in my time, but I've certainly *read* far more. The single quickest way to
increase maintainability and decrease 'simple' bugs is to strive to write
*idiomatic* Python. Whereas some dynamic languages embrace the idea there being
no 'right' way to solve a problem, the Python community generally appreciates
the liberal use of 'Pythonic' solutions to problems. 'Pythonic' refers to the
principles laid out in 'The Zen of Python' (try typing 'import this' in an
interpreter...). One of those principles is 

    'There should be one-- and preferably only one --obvious way to do it'
                                                    -from 'The Zen of Python' by Tim Peters

In that vein, I've begun compiling a list of Python idioms that programmers
coming from other languages may find helpful. I know there are a ton of things
not on here; it's merely a skeleton list that I'll add to over time. If you have
a specific idiom you think should be added, let me know in the comments and I'll
add it with attribution to the name you use in your comment. 

This list will temporarily live here as a blog post, but I have an interesting
idea for its final home. More on that next week.

#Idioms

##Formatting
Identifier Type|Format|Example|
----|------|-------|----|
Class|Camel case|class StringManipulator:||
Variable|Words joined by underscore| words_joined_by_underscore = True
Function|Words joined by underscore| def are_words_joined_by_underscore(words):
'Internal' class members/functions| Prefixed by single underscore| def _update_statistics(self):

Unless wildly unreasonable, abbreviations should not be used (acronyms are fine if in common use, like 'HTTP') 

##Working With Data

####Avoid using a temporary variable when swapping two variables
There is no reason to swap using a temporary variable in Python. We can use
tuples to make our intention more clear.

######Harmful

    temp = foo
    foo = bar
    bar = temp

######Idiomatic
    
    (foo, bar) = (bar, foo)

####Use tuples to unpack data
In Python, it is possible to 'unpack' data for multiple assigment. Those familiar with LISP may know this as 'desctructuring bind'.

######Harmful

   list_from_comma_seperated_value_file = ['dog', 'Fido', 10] 
   animal = list_from_comma_seperated_value_file[0]
   name = list_from_comma_seperated_value_file[1]
   age = list_from_comma_seperated_value_file[2]

######Idiomatic
    
   list_from_comma_seperated_value_file = ['dog', 'Fido', 10] 
   (animal, name, age) = list_from_comma_seperated_value_file

##Control Structures

###If Statement

####Avoid placing conditional branch on the same line as the colon
Using indentation to indicate scope (like you already do everywhere
else in Python) makes it easy to determine what will be executed as part of a
conditional statement.

######Harmful

    if name: print (name)
    print address

######Idiomatic
    
    if name:
        print (name)
    print address

####Avoid having multiple statements on a single line
Though the language definition allows one to use a semi-colon to delineate
statments, doing so without reason makes one's code harder to read. Typically
violated with the previous rule.

######Harmful

    if this_is_bad_code: rewrite_code(); make_it_more_readable();

######Idiomatic

    if this_is_bad_code: 
        rewrite_code()
        make_it_more_readable()

####Avoid repeating variable name in compound if Statement
When one wants to check against a number of values, repeatedly listing the
variable whose value is being checked is unneccesarily verbose. Using a temporary
collection makes the intention clear.

######Harmful

    if name == 'Tom' or name == 'Dick' or name == 'Harry':
        is_generic_name = True

######Idiomatic

    if name in ('Tom', 'Dick', 'Harry'):
        is_generic_name = True

####Use list comprehensions to create lists that are subsets of existing data
List comprehensions, when used judisciously, increase clarity in code that
builds a list from existing data. Especially when data is both checked for some
condition *and* transformed in some way, list comprehensions make it clear
what's happening. There are also (usually) performance benefits to using list
comprehensions (or alternately, set comprehensions) due to optimizations in the
cPython interpreter.

######Harmful

    some_other_list = range(1, 100)
    my_weird_list_of_numbers = list()
    for element in some_other_list:
        if is_prime(element):
            my_list_of_primes.append(element+5)


######Idiomatic

    some_other_list = range(1, 100)
    my_weird_list_of_numbers = [element + 5 for element in some_other_list if is_prime(element)]

###Loops

####Use the 'in' keyword to iterate over an Iterable
Programmers coming languages lacking a for_each style construct are used to
iterating over a container by accessing elements via index. Python's **in**
keyword handles this gracefully.

######Harmful

    my_list = ['Larry', 'Moe', 'Curly']
    index = 0
    while index < len(my_list):
        print (my_list[index])
        index+=1

######Idiomatic

    my_list = ['Larry', 'Moe', 'Curly']
    for element in my_list:
        print element

####Use the **enumerate** function in loops instead of creating an 'index' variable
Programmers coming from other languages are used to explicitly declaring a
variable to track the index of a container in a loop. For example, in C++:

    #!cpp
    for (int i=0; i < container.size(); ++i)
    {
        // Do stuff
    }

In Python, the **enumerate** built-in function handles this role.

######Harmful

    index = 0
    for element in my_container:
        print (index, element)
        index+=1

######Idiomatic

    for index, element in enumerate(my_container):
        print (index, element)

