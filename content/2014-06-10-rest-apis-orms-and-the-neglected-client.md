title: REST APIs, ORMs, And The Neglected Client
date: 2014-06-10 18:34
categories: python rest hateoas

Much of my work recently has been focused on API creation (REST APIs in particular) and,
in my spare time, trying to push the boundaries of ORM usage (through [sandman](http://www.github.com/jeffknupp/sandman)). 
While I once believed these to be entirely separate pursuits, now I'm not so
sure. Thinking about all the REST API hype, and [hypermedia's neglected client](http://jeffknupp.com/blog/2014/06/03/why-i-hate-hateoas/),
perhaps the two are more closely intertwined than I thought.
<!--more-->
## What Is The Endgame?

With all of this work on the API side, what is the end game for the client?
Hypermedia's perfect hypothetical client is, essentially, a hand-rolled client
library. For example, if I need to use the GitHub API to create a comment on a
pull request, the perfect hypermedia API essentially lets me say
`pull_request.create_comment('This stinks!')`; it (the client) already has enough knowledge
about `pull requests` and `comments` to know how to create one on the other
(remember, through all of the information transmitted through previous requests,
or through the client's ability to explore the API).

But wouldn't that then bring us all the way back to a full-on client library (albeit
this one dynamically created)? The current focus on REST APIs is, at least partially, however, a revolt 
against the heavy client libraries of the 90s. The holy-grail of hypermedia is to *always* be able
to dynamically create such a client API dynamically, regardless of how the
server changes.

Now we're back at the beginning again, however. We would have (machine) hand-rolled client APIs,
but how different would they be from the finely crafted, non-REST, client
libraries against which we were rebelling? Do these new libraries not amount to an attempt
to solve the client library issue in a generic fashion, "once and for all"? 
Why do we think that a single, generic, approach to client library construction for all systems is a *good* thing?

## Reversing the ORM

If creating "smart" client libraries that know how to manage the life-cycle of a resource
is the end game, then I submit that this issue has been solved: **ORMs**.
ORMs are responsible for tracking the actions taken on a resource and generating
the proper series of interactions with the back-end system (i.e. the database)
automatically. What prevents us from turning the lens of the ORM the other way,
and declaring resources for which the ORM library is responsible for making the
proper set of REST API calls? With all the effort to marry storage and REST
APIs, can it be so difficult to rewire a library meant to handle one to use the
other?

If nothing else, it's an interesting notion: take the best-case end result
clients created for use with hypermedia APIs and see what they look like. If
they're familiar, perhaps there's a quicker way to reach their nirvana then
jamming server responses with what is effectively a client library?

I'll be exploring this a bit more (in Python code) in the coming weeks, along
with all the *other* stuff I've committed to "exploring". Real progress has been
made, however, on the Kickstarter campaign as the [first video is now live!](https://www.youtube.com/watch?v=g0gNWGg2JxM&feature=youtu.be&a).
More progress is being made on the book, and I hope to have more information to
be able to release on that in the next few weeks. Lastly, I'll be giving a talk
titled, ["Automated Building of REST APIs in Python" at the Wharton Web Conference](https://www.sas.upenn.edu/wwc/).
It's not too late to buy tickets!
