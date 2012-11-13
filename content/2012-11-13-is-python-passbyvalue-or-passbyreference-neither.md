title: "Is Python pass-by-value or pass-by-reference? Neither."
date: 2012-11-13 14:23
categories: python interpreter object reference
---
One aspect of Python programming that trips up those coming from languages like C or Java is how arguments are passed to functions in Python. At a more fundamental level, the confusion arises from a misunderstanding about Python's use of objects and its treatment of assignment. When asked whether Python function calling model is "pass-by-value" or "pass-by-reference", the correct answer is: **neither**. Indeed, to try to shoe-horn those terms into a conversation about Python's model is misguided. "pass-by-object," or "pass-by-object-reference" is a reasonably correct way of describing it. But what does "pass-by-object" even mean?
<--more-->

In Python, (almost) everything is an object. Objects are referred to by *names* and exist in a *namespace*. To clarify, think about what happens when the following C++ code is executed:

~~~~.{cpp}
string some_guy = "Fred";
// ...
some_guy = "George";
~~~~

In the above, ```some_guy``` refers to some location in memory, and the value 'Fred' is inserted in that location. Later, the value in the location reffered to by ```some_guy``` is changed to 'George'. The previous value no longer exists. This likely matches your intuitive understanding (even if you don't program in C++).

Let's take a similar block of Python code and see what's different:

~~~~.{python}
some_guy = 'Fred'
# ...
some_guy = 'George'
~~~~

In the first line, we create a *name*, 'some_guy', that references the *object* 'Fred' (a string object). That is to say we alter the local *namespace* by inserting a name 'some_guy' that refers to a newly created object whose contents is 'Fred'. When we later say ```some_guy = 'George'```, the object containing 'Fred' is unaffected. We've just changed what ```some_guy``` refers to. **We haven't, however, changed either the 'Fred' or 'George' objects.

With only a single assignment, this may seem overly pedantic, but it becomes more important when references are shared and function calls are involved. Let's say we have the following bit of Python code:

~~~~.{python}
some_guy = 'Fred'

first_names = []
first_names.append(some_guy)

another_list_of_names = first_names
another_list_of_names.append('George')
some_guy = 'Bill'

print (some_guy, first_names, another_list_of_names)
~~~~

So what get's printed in the final line? Well, to start, the name ```some_guy``` is added to the local namespace and refers to a new string object: 'Fred'. The name ```first_names``` refers to an empty list object. In line 4, a method is called on the list object referred to by ```first_names```, appending the object referred to by ```some_guy```. At this point, there are still only two objects that exist: the string object and the list object. ```some_guy``` and ```first_names[0]``` *both refer to the same object*.

Let's continue breaking this down. In line 6, a new name is entered into the namespace: ```another_list_of_names```. Asignment between names does not create a new object. Rather, both names simply point to the same object. As a result, the string object and list object are still the only objects that have been created by the interpreter. In line 7, a member function is called on the object refered to by ```another_list_of_names``` and it is *mutated* to contain a reference to a new object: 'George'. 

This brings us to an important point: there are actually two kinds of objects in Python. A *mutable* object exhibits time-varying behavior. A change to a mutable object is visible to all that refer to it. Python's lists are mutable objects. An *immutable* object does not exhibit time-varying behavior. The value of immutable objects can not be modified. They *can* be used to compute the values of **new** objects, which is how a function like string.join works, for example. When you think about it, this dichotomy is necessary because, again, everything is an object in Python. If integers were not immutable I could change the meaning of the number '2' throughout my program.

It would be incorrect to say that "mutable objects can change and immutable ones can't", however. Consider the following:

~~~~.{python}
first_names = ['Fred', 'George', 'Bill']
last_names = ['Smith', 'Jones', 'Williams']
name_tuple = (first_names, last_names)

first_names.append('Igor')
~~~~

Tuples in Python are immutable. We can't change the tuple object referred to by ```name_tuple```. But immutable containers may contain references to mutable objects, which we know from before is what a list is. Therefore, even though ```name_tuple``` is immutable, it "changes" when 'Igor' is appended to ```first_names``` on the last line. It's a subtlety that can sometimes (though very infrequently) prove useful.

By now, you should almost be able to intuit how function calls work in Python. If I call ```foo(bar)```, I'm merely passing a reference to the objected referred to by the name ```bar``` to the function ```foo```. If ```bar``` refers to a mutable object and ```foo``` changes its value, then these changes will be visible outside of the scope of the function.

~~~~.{python}

def foo(bar):
    bar.append(42)
    print(bar)
    # >> [42]

answer_list = []
foo(answer_list)
print(answer_list)
# >> [42]
~~~~

On the other hand, if ```bar``` refers to an immutable object, the most that ```foo``` can do is create a name ```bar``` in its local namespace and have it refer to some other object.

~~~~.{python}
def foo(bar):
    bar = 'new value'
    print (bar)
    # >> 'new value'

answer_list = 'old value'
foo(answer_list)
print(answer_list)
# >> 'old value'
~~~~

Hopefully by now it is clear why Python is neither "pass-by-reference" nor "pass-by-value". In Python a variable is not an alias for a location in memory. Rather, it is simply an entry in the local namespace that refers to some object. While the notion of "everything is an object" is undoubtedly a cause of confusion for those new to the language, it allows for powerful and flexible language constructs, which I'll discuss in my next post. 
