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
    SELECT Vehicle.Model, Vehicle.Year FROM Vehicle, ServiceHistory WHERE Vehicle.VIN = ServiceHistory.VIN AND Price > 75.00;

This query seeks to determine the Model and Year for all cars where the repair costs were
greater than $75.00.
