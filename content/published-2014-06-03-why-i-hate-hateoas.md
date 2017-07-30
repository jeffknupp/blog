# Why I Hate HATEOAS

Most of the population of people who have read
[Roy Fielding's dissertation](http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) tell us that, 
while we may understand HTTP verbs, we don't know anything about *hypermedia*.
Our REST APIs, they say, are not *really* RESTful, and certainly do not 
exhibit **H**ypertext **A**s **T**he **E**ngine **O**f **A**pplication **S**tate, or *HATEOAS*. 
The fact that we have APIs you need to read documentation to 
understand is a clear signal, they tell us, that the client is using 
out-of-band information to navigate the server. *Hypermedia*, they say, 
is the answer. We simply embed enough information in our responses that 
the client can intelligently choose what action to take next 
using only the contents of the HTTP response.

## Why This Is Tremendously Stupid
<!--more-->
When designing a hypermedia API, you're really designing for a client that
**does not, and will never, exist**. Imagine you're asked by your manager to create a 
"REST API" for your business. Knowing the latest trends in API design, you come 
up with a hypermedia-driven design that uses *HAL* or some such nonsense. When
your manager asks you if the API is ready, you answer in the affirmative. 

When he asks if the documentation is ready as well, you gleefully tell him 
that such extraneous information is not necessary, and that your API 
responses include enough information for *smart* clients to use the
API without any explicit documentation, minus a brief spec that
describes what your `rel` values mean and so-forth.

**Your manager then asks you again: "Is the documentation also ready?"**

At this point, you hurry to write the "standard" REST documentation with
explicit endpoints, the verbs they accept, and how to use them.

What you've *really* provided by writing the "standard" documentation is exactly
the thing that makes hypermedia APIs ridiculous: *lack of semantic understanding*.
There is no magical "smart client" that somehow knows that `rel=comments` means
that the link leads to comments about the current resource *and* can figure out
it should `POST` there to create a new comment. It has no idea what the hell a
"comment" is. 

Unless you tell it explicitly. But using out-of-band information to give
*meaning* to your content is not acceptable. Instead, you must wait for the
"smart client" that will never exist. Why am I sure of that?
Because if it did, then it would effectively be a single client that
could make use of *every single (properly built) REST API in existence* without
requiring documentation. What would that even mean?

Here's a question:

**Why are we collectively trying to build servers for which there can never be acceptable clients.**

People are trying to wrangle their APIs into hypermedia formats or (worse)
inventing new ones, all because someone decided that
*everything must be self-documenting, despite the fact that the consumers of that implicit documentation (machines) have no hope of understanding it.*

*Why* are we killing ourselves to build HATEOAS systems? Are today's ["don't call me REST"](http://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven) REST APIs so broken that we *must write code with our heads in the sand, pretending that if we solve the server side issues, the client side will eventually catch up*? Well, news flash. It won't catch up. Ever.

# Keep Doing What You've Been Doing

Rather than striving for hypermedia systems, design ones that people can
actually *use* without having to read 12 different specs and no documentation.
Today's automated REST API documentation tools are fantastic, use them. Keep
building "REST" APIs and calling them that, because *there is no sensible alternative*.

Of course, if you want to design a system using principles which, by definition,
your system can never be said to use, go right ahead. In the meantime, I'll be
getting stuff done.
