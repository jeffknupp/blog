title: What is a NoSQL Database? A Pure Python Implementation
date: 2014-07-02 10:27
categories: python nosql database

*NoSQL* is a term that has become ubiquitous in rencent years. But what does
"NoSQL" actually mean? How and why is it useful? In this article, we'll answer
these questions by creating a toy NoSQL database in pure Python (or, as I like
to call it, "slightly structured psuedo-code").

## OldSQL

To most, SQL is synonymous with "database". **SQL**, an acronym for *Structured Query Language*,
is not a database technology itself, however. Rather, it describes the language
by which one retrieves data from a **RDBMS**, or *Relational Database Management
System*. MySQL, PostgreSQL, MS SQL Server, and Oracle are all examples of
RDBMSs.

The word "Relational" in the acronym RDBMS is the important one. These databases
require that data be stored as a set of relations described in a *schema*. Data
is oranized into *tables*, each with a set series of *columns* with an
associated *type*. For example, a `Car` table may have the following columns:

* Make: a string
* Model: a string
* Year: a four-digit number; alternatively, a date
* Color: a string
* VIN (Vehicle Identification Number): a string

A single entry in a table is called a *row*, or *record*. To distinguish one
record from another, a *primary key* is usually defined. The *primary key* for a
table is one of its columns (or a combination thereof) that uniquely identifies
each row. In the `Car` table, VIN is a natural choice for primary key as it
differentiaties between one car and another. Two rows may share the exact same
values for Make, Model, Year, and Color but be different cars, meaning
they would have different VINs. If two rows have the same VIN, we don't even
have to check the other columns, they must refer to the same car.

### Querying

SQL lets us *query* this database to gain useful information. Imagine the database
represents all vehicles registered in the US. To get *all* records, we could
write the following *SQL query* against the database: 

    #!sql
    SELECT * FROM Car;

What this says, in essence, is "select all columns from every row in `Car`".
We'd get back a list of results, each with Make, Model, Year, Color, and VIN. If
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
store it once and look it up if necessary.

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
greater than $75.00.

### Indexes

If our database has no *indexes* (indices), the query above would need to
perform a *table scan*, or an inspection of each row in the table in sequence,
to locate rows that match our query. Table scans are notoriously slow. Indeed,
they represent the slowest possible method of query execution.

Table scans can be avoided through the use of an index on a column or column.
Think of indices as data structures that allow us to find a particular value 
(or range of values) in the indexed column very quickly by pre-sorting the
values. That is, if we had an index on the Price column, instead of looking 
through all rows one-at-a-time to determine if the price was greater 
than `75.00`, we could simply use the information contained in the index 
to "jump" to the first row with a price greater than `75.00` and return every
subsequent row (which would have a price at least as high as `75.00`, since the
index is ordered).

When dealing with non-trivial amounts of data, indices become an indespensable
tool for improving query speed. Like all things, however, they come at a cost:
building the index's data structure takes memory that would otherwise be used to
store more database data. It's a tradeoff that one must examine in each
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
columns can be blank and which must be unique. A table may only have one schema at any given
time and *all rows in the table must conform to the schema*.

This is an important restriction. Imagine you have a database table with
millions of rows of customer information. Your sales team would like to begin
capturing an additional piece of data (say, the user's age) so their email marketing
algorithm can be more precise. This requires you to *alter* the table by adding
a column. You'll also need to decide if this column is required. Often times, it
makes sense to make a column required, but doing so would require having
information we simply don't have access to (like the age of every user already
in the database). Therefore, tradeoffs are often made in this regard.

In addition, making schema changes to very large database tables is rarely a
simple matter. Having a rollback plan in case something goes wrong is important,
but it's not always possible to undo a schema change once it's been made. Schema
maintenance is probably one of the most difficult parts of the job of a DBA.

## Key/Value Stores

Far before the term "NoSQL" existed, *Key/Value Data Stores* like `memcached`
provided storage for data without the overhead of a table schema. Indeed, in K/V
stores, there are no "tables" at all. There are simply *keys* and *values*.
