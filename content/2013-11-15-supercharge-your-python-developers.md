title: Supercharge Your Python Developers
date: 2013-11-15 08:53
categories: python ci pylint pep8

After a recent reorganization at work, I became the technical lead on a project
to rewrite an existing PHP application that consisted of tens of thousands of lines of
code. My team of five decided that Python and Flask would be a good
implementation choice as it would allow us to see results quickly. The group
ranged from complete Python novices to Python journeymen. 

**They quickly became rockstars.**

How did this happen? How was it possible that, in less than a month from the
project's inception, these python beginners were writing beautiful, idiomatic
code? That code reviews were simple, straightforward, and usually took almost
no time? The answer may surprise you.

## Enabling Your Developers

Continuous integration with deep integration with Python testing and
static analysis tools, along with simple scripts to aid developers has been the
key to the amazing productivity of the team. It may sound silly, and I certainly
didn't expect this outcome, but I can't deny what I see: novice programmers
writing expert code.

Why did I put so much emphasis on the build process and developer tools? Before
I answer that question, a bit of background on the old system is in order.

### The Legacy System

The legacy system was so difficult to develop against that even small changes took three
times as long as they should have. Testing was a nightmare.
Simply trying to run the unit tests was an exercise in futility; most required a
connection to a sandbox MySQL instance that was shared among 20 developers and
was never in the delicate state required for testing. Other tests were out of
date and no longer matched the database schema, failing immediately.

There was no build process or continuous integration for the old project.
Even if the tests worked perfectly, no one would run them. We would only
be finding bugs after the buggy code had already been committed. And we had no
sense of how comprehensive the tests were; code coverage reporting was
non-existent.

The codebase was also horribly confusing. There was layer upon layer of
abstraction and indirection, followed by giant functions spanning hundreds of
lines with no documentation. The lack of coding conventions meant that each new
file I opened in vim was written in a completely different style than the
previous.

### "Whatever they did, do the opposite"

I told myself that the guiding principle in the design and development of the
new system would be "the new system is as straightforward, quick, and easy to
develop against as the old system is frustrating." I know a lot of best
practices when it comes to starting a large Python project (many of which are
detailed in my post [Open Sourcing a Python Program the Right Way](http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/)). And so I set out to do exactly the 
opposite of everything the previous project did.

### The Setup

Now for the meat of the article: the specific steps I took that inadvertently turned
novices into rockstars. I'll list a number of areas I focused on and what I did
in that space.

##### Design For Simplicity

First and foremost, I spent a good deal of time thinking the design of the
system. My goal was to write the "scaffolding" code and then let my
team's other developers add functionality. As such, I strived for a design that would
make adding new functionality as straight-forward and error-free as possible. 

My implementation of the scaffolding (or "skeleton") contained more than a
simple class structure and set of interactions. It included a number of 
convenience functions and mechanisms to automate tasks that would be repeated often. 

For example, service endpoints are written as classes. Ones that are POSTed to
take their arguments as JSON data. Checking for the existence of required fields
and sending returning an error if not present, therefore, would be a common
task. For that reason, I included a mechanism that allowed the developer to simply list 
the required and optional JSON fields in the class implementation and they would automagically 
be extracted and added as attributes to the class. That meant that one could write:

    #!py
    class MyEndpoint(BaseEndpoint):
        """Endpoint class implementing the '/foo' service endpoint."""

        __required_fields__ = ['date', 'time', 'event']
        __optional_fields__ = ['location']

        @extract_fields
        def post(self, request):
            if self.location:
                do_something(self.date, self.time, self.event, self.location)
            else:
                do_something_else(self.date, self.time, self.event)

rather than: 

    #!py
    class MyEndpoint(BaseEndpoint):
        """Endpoint class implementing the '/foo' service endpoint."""

        def post(self, request):
            data = request.get_json(force=True, silent=True)
            if 'date' not in data:
                return InvalidUsage('date' is a required field
            if 'time' not in data:
                return InvalidUsage('time' is a required field
            if 'event' not in data:
                return InvalidUsage('event' is a required field

            date = data['date']
            time = data['time']
            event = data['event']
            location = None

            if 'location' in data:
                location = data['location']
                do_something(self.date, self.time, self.event, self.location)
            else:
                do_something_else(self.date, self.time, self.event)

This type of convenience is important, as it allows developers to focus on
what's important rather than forcing them to perform mundane bookkeeping tasks.
It also prevents errors, as the developer can no longer accidentally forget to check 
for an optional field or take the wrong action if a field isn't present. 

**In short, reducing boilerplate should be a focus during the design phase.** 
A design that, purposely or not, requires excess boilerplate code to add new 
features is, in my mind, a poor one. It frustrates developers, and frustrated 
developers don't write the quality code they're capable of producing.

##### Create a `virtualenv`

In terms of the actual project set up, first (as you would expect) I created 
a `virtualenv` and `requirements.txt` file, pegging our package requirements to 
specific versions. This allowed new developers to immediately get up and 
running via `mkvirtualenv <project_name> -r requirements.txt`. It also ensured 
that whatever packages an individual developer had on their machine didn't 
interfere with the packages required for the new system.

##### Run unit tests on each commit via Jenkins

AppNexus uses Jenkins for continuous integration. I immediately set up
[py.test](http://www.pytest.org) and wrote some quick unit tests against the
scaffolding code I had written. Most importantly, I included a number of tests
that mocked out the database connection and checked to ensure the queries we
expected to run actually ran. These tests would serve as examples to other developers
required to test database interaction (a somewhat tricky subject). 

I also installed `pytest-cov`, which gives `py.test` code coverage capabilities.
I integrated this with Jenkins by using the `--junitxml` flag, producing test
results in junit-style XML. If the coverage drops below a certain percent, the
build fails, plain and simple.

##### Using `make` to simplify everything

Next I created a `Makefile` to automatically create and activate the
`virtualenv`, run the tests, and also clean the environment by deleting the
`virtualenv`. Now, `make test` installed the required packages and ran the unit 
tests straight from a fresh `git clone`. As a developer, that's a nice
convenience. *Making the process to run your automated tests as simple as 
possible is **very** important. If it's too difficult or takes to 
long, developers won't run them.*

##### `pylint` and `pep8`, CI style

After writing a quick coding conventions document, I installed
[pylint](http://www.pylint.org) and [pep8](https://pypi.python.org/pypi/pep8).
For `pylint`, I generated a `.pylintrc` file (using the awesome `--generate-rcfile` flag. Seriously, why don't more tools have this?) to hold project specific settings.
I setup `pylint` to run with the `--rcfile=.pylintrc` flag and followed a similar process
for `pep8`. Then I promptly added them to the `Makefile` to run during the tests
and produce output that Jenkins could use to create reports. 

I now had a project where unit tests were run on every commit and
test results, test coverage, coding conventions, and "bad code" reports 
were generated.  These reports are saved, and Jenkins produces graphs that track 
these metrics over time. More importantly, they impacted whether or not the
build itself actually succeeded.

I set up Jenkins to *fail the build* if the number of `pylint` and `pep8`
violations passed some threshold. This was an important step, as it made it
clear that writing idiomatic, properly formatted code was something to be taken
seriously. More importantly, *it took the burden of remembering to use the tools
off of the developer*. If a developer "forgets" to run `pylint` or `pep8` before
committing, the build process has their back.

##### Documentation 

Needless to say, documentation was a focus for the new system. I set up
a [Sphinx](sphinx.pocoo.org) build to automatically generate documentation for
the project (using `sphinx-apidoc`) and added it to the Makefile as a new
target. *I also enabled documentation coverage*. The
coding conventions mandated `docstrings` for all modules, classes, and
functions. `Sphinx` (and `pylint`) now enforce this automatically and fail
the build if coverage isn't 100%.

##### Developer-friendly Scripts

Perhaps most important of all, I spent a good deal of time on an
oft-neglected topic: writing scripts to make my developers' lives easier. 
For this project, I created the following:

* A schema file and script that created the database from scratch
* A dump script to fill the database with test data 
    * The script first cleaned up the database to make sure it was in a known,
      easily recreatable state
* A script that chose sensible default configuration values and started the
  server, giving the developer the option to run against a real MySQL database 
  or an SQLite in-memory database. It also took care of sending `stdout` and
  `stderr` to a log file (in addition to the `syslog` logging the system
  performs. 
* A script aware of the pre-populated database data that
  curled a request with JSON data to the server, then
  checked the database to make sure the expected changes were present.
* A script called **should_i_commit_this.sh**. It runs `pylint` and `pep8` with
  the project-specific configuration and determines if the code receives poor
  scores from either. If it does, the script says not to commit
  the code, gives the score assigned by the tool that complained, and prints
  that tool's output.

Especially with the last script, my goal was to make it as easy as possible to 
answer the question, "Did I just write good code?". Starting up the database 
and server, sending a test request, and performing static analysis on the 
code are each one command away. Another way of looking at it would be to say
**I tried to make it as difficult as possible to write (and commit) bad code.**

## The Results

With all of these tools and conveniences in place, my team's developers took the
reigns. Within a week, each team member had written the code for a non-trivial
endpoint. The code they produced was truly impressive. They made excellent use
of the utility code I had written, wrote extensive unit tests, documented
everything, and had code that precisely followed PEP-8. One of the most telling
signs we had succeeded was the fact that, after looking over the code, a member
of another team thought it was all written by a single person. "The style is
identical," they said (after hearing five people worked on it).

The clearest indicator of success, though, has been code reviews. All of my
career, code reviews have been tedious wastes of time. Reviewers always focused
on style rather than substance. Now, code reviews are a source of interest rather 
than frustration. We never have to say, "Please add a space after the colon on 
line 14." Reviews are focused on the logic and soundness of the approach rather 
than nitpicking style issues.

## Looking Back

So there you have it. My secret for making your team of Python developers
produce great code, regardless of skill level: focus on catching as much as
possible in your build process and afford developers convenience through
scripts, Makefiles, and easy-to-create/use development environments.

Got any other suggestions for supercharging a team of Python developers? Let me
know in the comments, on Twitter ([@jeffknupp](http://www.twitter.com/jeffknupp)), or via
email ([jeff@jeffknupp.com](mailto:jeff@jeffknupp.com)).
