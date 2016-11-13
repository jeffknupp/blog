title: How Python Makes Working With Data More Difficult in the Long Run
date: 2016-11-13 14:46
categories: python data

Before we begin, let's be clear on terminology. When I refer to "working with data" in the context of software
development I could mean one of two things:

1. *Interactively* working with data, with perhaps Jupyter (née IPython) or the live interpreter
1. *Writing, testing, reading, reviewing* and *maintaining* programs that primarily manipulate data

**In short: Python is awesome for interactive data analysis but terrible for writing long-lived programs dealing with
complicated data structures.**

The second definition is perhaps overly broad, but I'll clarify in a minute. Before that, let me be the first to say
that Python is an **incredible** language for interactively working with, or *exploring*, data. The ecosystem of third-party packages and
tools that have sprung up around data manipulation, visualization, and data science in general has been nothing short of
remarkable. 

*If working with interactive data is your nail, Python should be your hammer.*

But what about that second interpretation? Actually, it can be thought of as a logical extension of the first. Imagine you're
writing a program to query a database for a search term, do some sentiment analysis, and return the results in JSON.
Working interactively with the database results, the results returned by your sentiment analysis library, and the JSON
you produce is the natural first step. You're still in "exploration mode". Not really writing the program yet, just
seeing what the data looks like and how you'll need to manipulate it.

Once you get a "feel" for the "shape" of the data at each step, you can begin to write your program. You'll likely refer
back to examples of the output you created during exploration when implementing the logic of your program. Particularly
with deeply nested data structures (I'm looking at you, "everyone's abuse of JSON..."), it's often too difficult to keep the "shape" of
the data at each stage in your head.

But Python makes working with data *easy*, so your program is finished in no time. It works, it's well-documented, and
even has 100% test coverage. If you never need to return to this code, huzzah! Your job is done.

## Dynamic Typing Is The Root Of All Evil (j/k...kind of...)

The very property of Python that made your program so easy to write is the same one that will make it difficult to
review, read, and (most importantly) *maintain*. Python's dynamic type system means that, in most cases, you don't have
to enumerate the complete set of fields, types, and value constraints that define the data as it moves through your
system. You can just jam it all in a `dict`! Heterogeneous values FTW!

The task above would be much more laborious and time-consuming in a statically typed language like C or Go. In Go, for
example, to parse and return a JSON response from some web API, you first need to create a `struct` whose fields and
field-types *exactly* match the structure of the response. Here is how one must prepare to work with a JSON response
from [`etcd`](https://github.com/coreos/etcd) (taken from their client library):

```go
type Response struct {
	// Action is the name of the operation that occurred. Possible values
	// include get, set, delete, update, create, compareAndSwap,
	// compareAndDelete and expire.
	Action string `json:"action"`

	// Node represents the state of the relevant etcd Node.
	Node *Node `json:"node"`

	// PrevNode represents the previous state of the Node. PrevNode is non-nil
	// only if the Node existed before the action occurred and the action
	// caused a change to the Node.
	PrevNode *Node `json:"prevNode"`

	// Index holds the cluster-level index at the time the Response was generated.
	// This index is not tied to the Node(s) contained in this Response.
	Index uint64 `json:"-"`
}

type Node struct {
	// Key represents the unique location of this Node (e.g. "/foo/bar").
	Key string `json:"key"`

	// Dir reports whether node describes a directory.
	Dir bool `json:"dir,omitempty"`

	// Value is the current data stored on this Node. If this Node
	// is a directory, Value will be empty.
	Value string `json:"value"`

	// Nodes holds the children of this Node, only if this Node is a directory.
	// This slice of will be arbitrarily deep (children, grandchildren, great-
	// grandchildren, etc.) if a recursive Get or Watch request were made.
	Nodes Nodes `json:"nodes"`

	// CreatedIndex is the etcd index at-which this Node was created.
	CreatedIndex uint64 `json:"createdIndex"`

	// ModifiedIndex is the etcd index at-which this Node was last modified.
	ModifiedIndex uint64 `json:"modifiedIndex"`

	// Expiration is the server side expiration time of the key.
	Expiration *time.Time `json:"expiration,omitempty"`

	// TTL is the time to live of the key in second.
	TTL int64 `json:"ttl,omitempty"`
}
```

The "`json:...`" part after each field describes what that field's name should be when the object is marshaled from a
JSON message. And notice that, because `Response` contains a nested object (`Node`), we must fully define that nested
object as well.

*Note: to be fair, there **are** some shortcuts one might take in Go to reduce the need for a portion of the above, but they're rarely taken (and for good reason).*

In Python, you'd be all like:

```py
    result = make_etcd_call("some", "arguments", "here")
```

If you wanted to see if the `node` in question was a directory, you'd pound this out:

```py
    if result.json()['node']['dir']:
        # make magic happen... 
```

And the Python version is less code and takes less time to write than the Go version.

### "I Don't See The Problem"

The Python version is better, right? Let's consider two definitions of "good code" so we can be clear what we mean by better.

1. Code that is short, concise, and can be written quickly
1. Code that is maintainable

If we're using the first definition, the Python version is "better". If we're using the second, **it's far, far worse.**
The Go version, despite containing a boatload of boilerplate-ish definition code, *makes clear the exact structure of the
data we can expect in `result`*. 

Boss: "What can you tell me about the Python version, just by looking at our code above?"
Me: "Uh, it's JSON and has a 'node' object which probably has a 'dir' field."
Boss: "What type of value is in `dir`? Is it a boolean, a string, a nested object?
Me: "Uh, I dunno. It's truthy, though!"
Boss: "So is everything else in Python. Is `dir` guaranteed to be part of the `node` object in the response?"
Me: "Uh...."

And I've met my "3-Uh" limit for describing what a portion of code does. If you refer to the Go version, you can answer
those questions and sound like a damned genius in comparison. But these are *exactly the sort of questions your peers
should be asking in a code review*. The answers to the questions in the Go version are self-evident. The answers for the
Python version, not so much...

### Making Changes

What happens when we need to make a change to the Python version? Perhaps we want to say "only `make magic happen` if the
directory was just created, not for every response with a directory?" 

It's pretty clear how to do that in the Go
version. Compared to the Python version, the Go version is like the Library at Alexandria of `etcd` `Response`s. For the
Python version, *we have nothing local to refer to in order to figure out the structure of `result` and the change we
need to make.* We'll have to go look up the `etcd` HTTP API documentation. Let's hope that:

* it exists
* it is well maintained
* the tubes aren't clogged

And this is a *very* simple change we're talking about on a *very* simple JSON object. I could tell horror stories about
what happens when you get knee-deep in Elasticsearch JSON responses... (spoiler alert: `response['hits_']['hits_']['hits_']...`).
The fun doesn't stop at just *making* the code change, though. Remember, we're professionals, so all of our code is peer
reviewed and unit-tested. After updating the code *correctly* we can still barely reason about it. All of a sudden, we're
back to that conversation between my boss and I where I say "Uh" a lot and he wonders why he didn't go into carpentry.

## Everybody Panic!

I've painted a rather bleak picture of using Python to manipulate complex (and even not-so-complex) data structures in a maintainable way. In truth, however, it's a shortcoming shared by **most** dynamic languages.
In the second half of this article, I'll describe what various people/companies are doing about it, from simple things like the movement towards "live data in the editor" [all the way to the Dropboxian "type-annotate all the things"](https://www.dropbox.com/s/efatwr0pozsargb/PyCon%20mypy%20talk%202016.pdf?dl=0). In short, there's a lot of interesting work going on in this space and *lot's* of people are involved (notice the second presenter name in that Dropbox deck *<ahem>*).
