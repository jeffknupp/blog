## Continuous Integration with TravisCI

*Continuous Integration* refers to the process of continuously integrating all
changes for a project (rather than periodic bulk updates). For our purposes, it
means that *each time we push a commit to GitHub, our tests our run to tell us if the commit broke something.*
As you can imagine, this is an incredibly valuable practice. There's no more
"forgetting to run the tests" before committing/pushing. If you push a commit
that breaks the tests, you'll get an email telling you so.

[TravisCI](http://www.travis-ci.org) is a service that makes continuous
integration for GitHub projects embarassingly easy. Head over there and create
an account if you don't yet have one. Once you're done, we'll need to create
one simple file before we're swimming in CI goodness.

#### Configuration via `.travis.yml`

Individual projects on TravisCI are configured via a file, `.travis.yml`, 
in the project's root directory. Briefly, we need to tell Travis:

1. What language our project is written in
1. What version of that language it uses
1. What commands are used to install it
1. What commands are used to run the project's tests

Doing so is quite straightforward. Here are the contents of the `.travis.yml`
file from [sandman](http://www.github.com/jeffknupp/sandman):

    #!yml
    language: python
    python:
        - "2.7"
    install: 
        - "pip install -r requirements.txt --use-mirrors"
        - "pip install coverage"
        - "pip install coveralls"
    script: 
        - "coverage run --source=sandman setup.py test"
    after_success:
        coveralls

After listing the lanugage and version, we tell Travis how to install our
package. Under `install:`, make sure you have the line:

    #!yml
    - "pip install -r requirements.txt --use-mirrors"

This `pip install`s our projects requirments (and uses PyPI mirrors if
necessary). The other two lines in `install` are specific to [sandman](http://www.github.com/jeffknupp/sandman).
It's using an additional service ([coveralls.io](http://coveralls.io)) to continuously monitor 
test case coverage, but that's not neccessary for all projects.

`script:` lists the command needed to run the project's tests. Again, [sandman](http://www.github.com/jeffknupp/sandman)
is doing some extra stuff. All your project needs is `python setup.py test`.
And the `after_success` portion can be dropped all together.

Once you've committed this file and activated your project's repo in TravisCI,
push to GitHub. In a few moments, you should see a build kick off on TravisCI
based on your most recent commit. If all is successful, you build will be
"green" and the status page will show that the build passed. You'll be able to
see the history of all of your project's builds at any time. This is especially
useful for multi-developer projects, where the history page can be used to see 
how often a particular developer breaks the build...

You should also receive an email letting you know the build was successful.
Though you can probably configure it otherwise, you'll get emails only when the
build is broken or fixed, but not if a commit has the same outcome as the build
that preceeded it. This is incredibly useful, as your not inundated by useless
"the build passed!" emails but are still alerted when something changes.
