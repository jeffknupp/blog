title: 'You're Solving The Wrong Problem'
date: 2014-05-19 22:17
categories: python programming

I have a tutoring client who emailed me that he was interested in learning about SQLAlchemy, especially
its use with existing databases. Now, [having a little experience in that area,](http://www.github.com/jeffknupp/sandman)
I was happy to oblige. He told me he would be displaying data to
a client using Flask with a Microsoft SQL Server database for storage.

When he came to me, he said he not only needed to learn about SQLAlchemy, but
traversing complicated relationships, table versioning, and "shadow tables". I
asked him what, exactly, he needed to do.

He explained that the problem required him to create snapshots of each database table each time a
change was made, and also snapshot of each table's related tables. This would
cascade until eventually it encompassed the entire database. He drew up a
complicated diagram of what the DBA assigned to the project had proposed as the
schema.

By the end of the session, we were having a very different conversation.
"You're solving the wrong problem," I said. "You don't need a relational
database. Heck, you don't need a database at all. Or a web server. I have an
easy solution."

"We've already got a developer and a DBA assigned to it. What resources will we
need?" he asked.

"Oh, just some time," I replied.

"How much?"

**"About thirty minutes."**

<!--more-->

He was shocked. But, much to his credit, he agreed that he (and the DBA) had
been overcomplicating a very straightforward problem. It turns out, the project
was essentially a weekly progress report entered in a single HTML form. The client didn't want to waste
time filling in all the values because the form was quite long, so each week had to have the data from the previous week
pre-populated.

All they needed to save were the values entered in a single form.

There are a number of straightforward ways to do this. I'll leave exact
implementations as an excercise for the reader, but if you hit "NoSQL database,"
you've gone too far.

## Recognizing Patterns

One of the last and most difficult skills to aquire as a software developer is the
ability to "sense" the simplest way to solve a problem. If my client had continued
down the road he and the DBA had started on, not only would the system have been more complex,
but **his job as a programmer would be much more difficult.** Our simplified solution will end 
up saving the client's employer tens of thousands of dollars at a minimum.

What it required was experience and the ability to recognize patterns. 
