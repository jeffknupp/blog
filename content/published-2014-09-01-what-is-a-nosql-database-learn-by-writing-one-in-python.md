# What is a NoSQL Database? Learn By Writing One In Python

*NoSQL* is a term that has become ubiquitous in recent years. But what does
"NoSQL" actually mean? How and why is it useful? In this article, we'll answer
these questions by creating a toy NoSQL database in pure Python (or, as I like
to call it, "slightly structured pseudo-code").
<!--more-->
## OldSQL

To most, SQL is synonymous with "database". **SQL**, an acronym for *Structured Query Language*,
is not a database technology itself, however. Rather, it describes the language
by which one retrieves data from a **RDBMS**, or *Relational Database Management
System*. MySQL, PostgreSQL, MS SQL Server, and Oracle are all examples of
RDBMSs.

The word "Relational" in the acronym RDBMS is the most informative.  Data
is organized into *tables*, each with a set series of *columns* with an
associated *type*. The description of all tables, their columns, and the
columns' types are referred to as the database's *schema*. The schema completely
describes the structure of the database, with a description of each table.
For example, a `Car` table may have the following columns:

* Make: a string
* Model: a string
* Year: a four-digit number; alternatively, a date
* Color: a string
* VIN (Vehicle Identification Number): a string

A single entry in a table is called a *row*, or *record*. To distinguish one
record from another, a *primary key* is usually defined. The *primary key* for a
table is one of its columns (or a combination thereof) that uniquely identifies
each row. In the `Car` table, VIN is a natural choice to be the table's primary key as it
is guaranteed to be unique between cars. Two rows may share the exact same
values for Make, Model, Year, and Color but refer to different cars, meaning
they would have different VINs. If two rows have the same VIN, we don't even
have to check the other columns, they must refer to the same car.

### Querying

SQL lets us *query* this database to gain useful information. To *query* simply means
to ask questions of the RDBMS in a structured language and interpret the rows it returns as the answer.
Imagine the database represents all vehicles registered in the US. To get 
*all* records, we could write the following *SQL query* against the database: 

    #!sql
    SELECT Make, Model FROM Car;

A translation of the SQL into plain English might be:

* "SELECT": "Show me"
* "Make, Model": "the value of Make and Model" 
* "FROM Car": "for each row in the Car table"

Or, *"Show me the value of Make and Model for each row in the Car table"*.
We'd get back a list of results, each with Make and Model. If
we cared only about the color of cars from 1994, we could say:

    #!sql
    SELECT Color FROM Car WHERE Year = 1994;

In this case, we'd get back a list like

    Black
    Red
    Red
    White
    Blue
    Black
    White
    Yellow

Lastly, using the table's *primary key*, we could look up a specific car by
looking up a VIN:

    #!sql
    SELECT * FROM Car where VIN = '2134AFGER245267';

That would give us the specific properties of that car.

Primary keys are defined to be *unique*. That is, a specific car with a specific
VIN must only appear in the table at most once. Why is that important? Let's
look at an example:

### Relations

Imagine we are running an auto repair business. Among other things, we need to keep track 
of a vehicle's service history: the record of all repairs and tune ups we've
performed on that car. We might create a `ServiceHistory` table with the
following columns:

* VIN
* Make
* Model
* Year
* Color
* Service Performed
* Mechanic
* Price
* Date

Thus, each time a car comes in to get serviced, we add a new row to the table
with all of the car's information along with what we did to it, who the mechanic
was, how much it cost, and when the service was performed.

But wait. All of the columns related to the car itself are always the same for
the same car. That is, if I bring in my Black 2014 Lexus RX 350 10 times for service,
I'll need to record the Make, Model, Year, and Color each time, even though they
won't change. Rather than repeat all of that information, it makes more sense to
store it once and look it up when necessary.

How would we do this? We'd create a second table: `Vehicle`, with the following
columns:

* VIN
* Make
* Model
* Year
* Color

For the `ServiceHistory` table, we now want to trim down to the following
columns:

* VIN
* Service Performed
* Mechanic
* Price
* Date

Why does VIN appear in both tables? Because we need a way to specify that *this*
vehicle in the `ServiceHistory` table refers to *that* vehicle in the `Vehicle`
table. This way, we only have to store information about a particular car once.
Each time it comes in for repair, we create a new row in the `ServiceHistory`
table *but not* the `Vehicle` table; it's the same car, after all.

We can also issue queries that span the implicit relationship between `Vehicle` and `ServiceHistory`:

    #!sql
    SELECT Vehicle.Model, Vehicle.Year FROM Vehicle, ServiceHistory WHERE Vehicle.VIN = ServiceHistory.VIN AND ServiceHistory.Price > 75.00;

This query seeks to determine the Model and Year for all cars where the repair costs were
greater than $75.00. Notice that we specify that the way to match rows from the
Vehicle table to rows in the ServiceHistory table is to match up the VIN values.
What it gives us back is a set of rows with the columns of both tables. We
refine this by saying we only want the "Model" and "Year" columns of the "Vehicle" table.

If our database has no *indexes* (or, more correctly, indices), the query above would need to
perform a *table scan* to locate rows that match our query. Table scans are an inspection of
each row in the table in sequence and are notoriously slow. Indeed,
they represent the slowest possible method of query execution.

Table scans can be avoided through the use of an index on a column or set of columns.
Think of indices as data structures that allow us to find a particular value 
(or range of values) in the indexed column very quickly by pre-sorting the
values. That is, if we had an index on the Price column, instead of looking 
through all rows one-at-a-time to determine if the price was greater 
than `75.00`, we could simply use the information contained in the index 
to "jump" to the first row with a price greater than `75.00` and return every
subsequent row (which would have a price at least as high as `75.00`, since the
index is ordered).

When dealing with non-trivial amounts of data, indices become an indispensable
tool for improving query speed. Like all things, however, they come at a cost:
the index's data structure consumes memory that could otherwise be used to
store more data in the database. It's a trade off that one must examine in each
individual case, but it's *very* common to index frequently queried columns.

### The Clear Box

Advanced features like indices are possible due to the database's ability to
inspect a table's *schema* (the description of what type of data each column
holds) and make rational decisions based on the data. That is, to a database, a
table is the opposite of a "black box" (a clear box?).

Keep this fact in mind when we talk about NoSQL databases. It becomes an
important part of the discussion regarding the ability to *query* different
types of database engines.

### Schemas

A table's *schema*, we've learned, is a description of the names of the columns
and the type of data they contain. It also contains information like which
columns can be blank, which must be unique, and all other constraints on column values.
A table may only have one schema at any given time 
and *all rows in the table must conform to the schema*.

This is an important restriction. Imagine you have a database table with
millions of rows of customer information. Your sales team would like to begin
capturing an additional piece of data (say, the user's age) to increase the precision
of their email marketing algorithm. This requires you to *alter* the table by adding
a column. You'll also need to decide if each row in the table needs a value for
this column. Often times, it makes sense to make a column required, but doing so would require
information we simply don't have access to (like the age of every user already
in the database). Therefore, trade offs are often made in this regard.

In addition, making schema changes to very large database tables is rarely a
simple matter. Having a rollback plan in case something goes wrong is important,
but it's not always possible to undo a schema change once it's been made. Schema
maintenance is probably one of the most difficult parts of the job of a DBA.

## Key/Value Stores

Far before the term "NoSQL" existed, *Key/Value Data Stores* like `memcached`
provided storage for data without the overhead of a table schema. Indeed, in K/V
stores, there are no "tables" at all. There are simply *keys* and *values*.
If a key/value store sounds familiar, that's because it's built upon the same
principles as Python's `dict` and `set` classes: using hash tables to provide
quick key-based access to data. The most primitive Python-based NoSQL database
would simply be a big dictionary.

To understand how they work, let's write one ourselves! We'll start with a very
simple design:

* A Python `dict` as the primary data store
* Only support strings as keys
* Support for storing integers, strings, and lists
* A simple TCP/IP server that uses ASCII strings for messaging
* Slightly advanced commands like `INCREMENT`, `DELETE`, `APPEND`, and `STATS`

The benefit of building the data store with an ASCII-based TCP/IP interface is
that we can use the simple `telnet` program to interact with our server; no
special client is needed (though writing one would be a good exercise and can be
done in about 15 lines).

We need a "wire format" for the messages we send to the server and for the
responses it sends back. Here's a loose specification:

### Commands Supported

* PUT
    * Arguments: Key, Value
    * Purpose: Insert a new entry into the data store
* GET
    * Arguments: Key
    * Purpose: Retrieve a stored value from the data store
* PUTLIST
    * Arguments: Key, Value
    * Purpose: Insert a new list entry into the data store
* GETLIST
    * Arguments: Key
    * Purpose: Retrieve a stored list from the data store
* APPEND
    * Arguments: Key, Value
    * Purpose: Add an element to an existing list in the data store
* INCREMENT
    * Arguments: Key
    * Purpose: Increment the value of an integer value in the data store
* DELETE
    * Arguments: Key
    * Purpose: Delete an entry from the data store
* STATS
    * Arguments: N/A
    * Purpose: Request statistics on how many successful/unsuccessful executions
               of each command were executed

Now let's define the message structure itself.

### Message Structure

#### Request Messages

A *Request Message* consists of a command, a key, a value, and a value type. The
last three are optional depending on the message. A `;` is used as a delimiter.
There must always be three `;` characters in the message, even if some optional
fields are not included.

> COMMAND;[KEY];[VALUE];[VALUE TYPE]

* **COMMAND** is a command from the list above
* **KEY** is a string to be used as a data store key (optional)
* **VALUE** is a integer, list, or string to be stored in the data store (optional)
    * Lists are represented as a comma-separated series of strings, e.g. "red,green,blue"
* **VALUE TYPE** describes what type **VALUE** should be interpreted as
    * Possible values: INT, STRING, LIST

##### Examples

* > "PUT;foo;1;INT"
* > "GET;foo;;"
* > "PUTLIST;bar;a,b,c;LIST"
* > "APPEND;bar;d;STRING
* > "GETLIST;bar;;"
* > "STATS;;;"
* > "INCREMENT;foo;;"
* > "DELETE;foo;;"
 
#### Response Messages

A *Response Message* consists of two parts, separated by a `;`. The first part is always `True|False`
based on whether the command was successful. The second part is the command message.
On errors, this will describe the error. On successful commands that don't
expect a value to be returned (like `PUT`), this will be a success message. For
commands that expect a value to be returned (like `GET`), this will be the value
itself.

##### Examples

* > "True;Key [foo] set to [1]"
* > "True;1"
* > "True;Key [bar] set to [['a', 'b', 'c']]"
* > "True;Key [bar] had value [d] appended"
* > "True;['a', 'b', 'c', 'd']
* > "True;{'PUTLIST': {'success': 1, 'error': 0}, 'STATS': {'success': 0, 'error': 0}, 'INCREMENT': {'success': 0, 'error': 0}, 'GET': {'success': 0, 'error': 0}, 'PUT': {'success': 0, 'error': 0}, 'GETLIST': {'success': 1, 'error': 0}, 'APPEND': {'success': 1, 'error': 0}, 'DELETE': {'success': 0, 'error': 0}}"

## Show Me The Code!

I'll present the code in digestible chunks. The entire server clocks in at just
under 180 lines of code, so it's a quick read.

#### Set Up

Below is a lot of the boilerplate setup code required for our server:

    #!py
    """NoSQL database written in Python."""

    # Standard library imports
    import socket

    HOST = 'localhost'
    PORT = 50505
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    STATS = {
        'PUT': {'success': 0, 'error': 0},
        'GET': {'success': 0, 'error': 0},
        'GETLIST': {'success': 0, 'error': 0},
        'PUTLIST': {'success': 0, 'error': 0},
        'INCREMENT': {'success': 0, 'error': 0},
        'APPEND': {'success': 0, 'error': 0},
        'DELETE': {'success': 0, 'error': 0},
        'STATS': {'success': 0, 'error': 0},
        }

Not much to see here, just an import and some initialization of data.

#### Set Up (Cont'd)

I'll now skip a bit of code so that I can show the rest of the setup code. Note
that it refers to functions that don't exist yet. That's fine, since I'm jumping
around. In the full version (presented at the end), everything is in the proper
order. Here's the rest of the setup code:

    #!py
    COMMAND_HANDLERS = {
        'PUT': handle_put,
        'GET': handle_get,
        'GETLIST': handle_getlist,
        'PUTLIST': handle_putlist,
        'INCREMENT': handle_increment,
        'APPEND': handle_append,
        'DELETE': handle_delete,
        'STATS': handle_stats,
        }
    DATA = {}

    def main():
        """Main entry point for script."""
        SOCKET.bind((HOST, PORT))
        SOCKET.listen(1)
        while 1:
            connection, address = SOCKET.accept()
            print 'New connection from [{}]'.format(address)
            data = connection.recv(4096).decode()
            command, key, value = parse_message(data)
            if command == 'STATS':
                response = handle_stats()
            elif command in (
                'GET',
                'GETLIST',
                'INCREMENT',
                'DELETE'
                    ):
                response = COMMAND_HANDLERS[command](key)
            elif command in (
                'PUT',
                'PUTLIST',
                'APPEND',
                    ):
                response = COMMAND_HANDLERS[command](key, value)
            else:
                response = (False, 'Unknown command type [{}]'.format(command))
            update_stats(command, response[0])
            connection.sendall('{};{}'.format(response[0], response[1]))
            connection.close()

    if __name__ == '__main__':
        main()

We've created what's commonly referred to as a *look-up table* called `COMMAND_HANDLERS`. It works by
associating the name of the command with the function used to handle commands of
that type. So, for example, if we get a `GET` command, saying
`COMMAND_HANDLERS[command](key)` is the same as saying `handle_get(key)`.
Remember, functions can be treated as values and can be stored in a `dict` like
any other value.

In the code above, I decided to handle each group of commands requiring the same
number of arguments separately. I could have simply forced all `handle_`
functions to accept a `key` and `value`, I just decided this was made the
handler functions more clear, easier to test, and was less error prone.

Note that the socket code is minimal. Though our entire server is based on
TCP/IP communication, there's really not much interaction with low-level
networking code.

The last thing to note is so innocuous you might have missed it: the `DATA`
dictionary. This is where we'll actually store the key-value pairs that make up
our database.

#### Command Parser

Let's take a look at the *command parser*, responsible for making sense of
incoming messages:

    #!py
    def parse_message(data):
        """Return a tuple containing the command, the key, and (optionally) the
        value cast to the appropriate type."""
        command, key, value, value_type = data.strip().split(';')
        if value_type:
            if value_type == 'LIST':
                value = value.split(',')
            elif value_type == 'INT':
                value = int(value)
            else:
                value = str(value)
        else:
            value = None
        return command, key, value

Here we can see type conversion occurring. If the value is meant to be a list,
we know we can create the proper value by calling `str.split(',')` on the
string. For an `int`, we simply make use of the fact that `int()` can take
strings. Ditto for strings and `str()`.


#### Command Handlers

Below is the code for the command handlers. They are all quite straight-forward
and (hopefully) look as you would expect. Notice there's a good deal of error
checking, but it's certainly not exhaustive. As you're reading, try to find
error cases the code misses and post them [in the discussion.](http://discourse.jeffknupp.com)

    #!py
    def update_stats(command, success):
        """Update the STATS dict with info about if executing
        *command* was a *success*."""
        if success:
            STATS[command]['success'] += 1
        else:
            STATS[command]['error'] += 1


    def handle_put(key, value):
        """Return a tuple containing True and the message
        to send back to the client."""
        DATA[key] = value
        return (True, 'Key [{}] set to [{}]'.format(key, value))


    def handle_get(key):
        """Return a tuple containing True if the key exists and the message
        to send back to the client."""
        if key not in DATA:
            return(False, 'ERROR: Key [{}] not found'.format(key))
        else:
            return(True, DATA[key])


    def handle_putlist(key, value):
        """Return a tuple containing True if the command succeeded and the message
        to send back to the client."""
        return handle_put(key, value)


    def handle_getlist(key):
        """Return a tuple containing True if the key contained a list and
        the message to send back to the client."""
        return_value = exists, value = handle_get(key)
        if not exists:
            return return_value
        elif not isinstance(value, list):
            return (
                False,
                'ERROR: Key [{}] contains non-list value ([{}])'.format(key, value)
                )
        else:
            return return_value


    def handle_increment(key):
        """Return a tuple containing True if the key's value could be incremented
        and the message to send back to the client."""
        return_value = exists, value = handle_get(key)
        if not exists:
            return return_value
        elif not isinstance(value, int):
            return (
                False,
                'ERROR: Key [{}] contains non-int value ([{}])'.format(key, value)
                )
        else:
            DATA[key] = value + 1
            return (True, 'Key [{}] incremented'.format(key))


    def handle_append(key, value):
        """Return a tuple containing True if the key's value could be appended to
        and the message to send back to the client."""
        return_value = exists, list_value = handle_get(key)
        if not exists:
            return return_value
        elif not isinstance(list_value, list):
            return (
                False,
                'ERROR: Key [{}] contains non-list value ([{}])'.format(key, value)
                )
        else:
            DATA[key].append(value)
            return (True, 'Key [{}] had value [{}] appended'.format(key, value))


    def handle_delete(key):
        """Return a tuple containing True if the key could be deleted and
        the message to send back to the client."""
        if key not in DATA:
            return (
                False,
                'ERROR: Key [{}] not found and could not be deleted'.format(key)
                )
        else:
            del DATA[key]


    def handle_stats():
        """Return a tuple containing True and the contents of the STATS dict."""
        return (True, str(STATS))

Two things to take note of: the use of *multiple assignment* and code re-use. A
number of functions are simply wrappers around existing functions with a bit
more logic, like `handle_get` and `handle_getlist` for example. Since we are
occasionally just sending back the results of an existing function and other
times inspecting what that function returned, *multiple assignment* is used.

Look at `handle_append`. If we try to call `handle_get` and the key doesn't
exist, we can simply return exactly what `handle_get` returned. Thus, we'd like
to be able to refer to the tuple returned by `handle_get` as a single return
value. That lets us simply say `return return_value` if the key does not exist.

If it *does* exist, we need to inspect the value that was returned. Thus, 
we'd also like to refer to the return value of `handle_get` as separate
variables. To handle both the case above and the case where we need to handle
the results separately, we use multiple assignment. This gives us the best of
both worlds without requiring multiple lines where our purpose is unclear.
`return_value = exists, list_value = handle_get(key)` makes it explicit that we're
going to be referring to the value returned by `handle_get` in at least two
different ways.

## How Is This a Database?

The program above is certainly not an RDBMS, but it definitely qualifies as a
NoSQL database. The reason it was so easy to create is because we don't have any
real interaction with *the data*. We do minimal type checking, but otherwise
just store whatever the user sends. If we needed to store more structured data,
we'd likely need to create a schema for the database and refer to it while 
storing and retrieving data.

So if NoSQL databases are easier to write, easier to maintain, and easier to
reason about, why don't we all just run mongoDB instances and be done with it?
There is, of course, a trade off for all this data flexibility that NoSQL
databases afford us: searchability.

### Querying Data

Imagine we used our NoSQL database above to store the car data from earlier. We
might store them using the VIN as the key and a list of values as each column
value, i.e. `2134AFGER245267 = ['Lexus', 'RX350', 2013, Black]`. Of course,
we've lost the *meaning* of each index in the list. We just have to remember
somewhere that index one stores the Make of the car and index two stores the
Year.

Worse, what happens when we want to run some of the queries from earlier? To
find the colors of all cars from Year 1994 becomes a nightmare. We have to go
through *every value* in `DATA`, somehow determine if the value is storing car
data or something else entirely, look at index two, then take the value of index
three if index two is equal to 1994. That's much worse than a table scan, since
it not only scans every row in the data store but needs to apply a somewhat
sophisticated set of rules to answer the query.

The authors of NoSQL databases are aware of these issues, of course, and (since
querying is generally a useful feature) have come up with a number of ways to
make queries possible. One way is to structure the data using, say, JSON and
allow for references to other rows to represent relationships. Also, most
NoSQL databases have some concept of namespaces, where data of a single type can
be stored in it's own "section" of the database, allowing a query engine to make
use of the fact that it knows the "shape" of the data being queried.

Of course, far more sophisticated approaches exist (and are implemented) to
increase queryability, but there will always exist a trade off between storing
schema-less data and queryability. Our database, for example, only supports
querying by key. Things would get a lot more complex if we needed to support a
richer set of queries.

## Summary

Hopefully, by now it's clear what "NoSQL" means. We learned a bit of SQL and 
how RDBMSs work. We saw how data is retrieved from an RDBMS (using SQL *queries*). 
We built a toy NoSQL database to examine the trade offs between queryability 
and simplicity. We also discussed a few ways database authors deal with this. 

The topic of databases, even of simple key-value stores, is incredibly deep.
We've merely scratched the surface here. Hopefully however, you learned a bit
about what NoSQL means, how it works, and when it's a good idea to use. You can
continue the conversation at [Chat For Smart People](http://discourse.jeffknupp.com),
the discussion board for this site.
