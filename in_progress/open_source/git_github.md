## Source Control With Git, Project Management with GitHub

In ["Starting a Django Project The Right Way,"](http://www.jeffknupp.com/blog/2012/10/24/starting-a-django-14-project-the-right-way/) I suggest either git
or mercurial for version control. For a project meant to be both shared and
contributed to, there's really only one choice: git. In fact, I'll go so far as
to say that not only is the use of git necessary, you'll also need to use
[GitHub](http://www.github.com) to maintain your project if you want people to
actually use and contribute to it. 

It's not meant to be an inflamitory statement (though no doubt many will 
take issue with it). Rather, for better or worse, git
and [GitHub](http://www.github.com) have become the de-facto standard for
Open Source projects. GitHub is the site potential contributors are 
most likely to be registered on and familiar with. That, I believe, is not a
point to be taken likely.

#### Create a `README.md` File

The project description for repos on GitHub is taken from a file in the project's
root directory: `README.md`. This file should contain the following
pieces of information:

* A description of your project
* Links to the project's ReadTheDocs page
* A TravisCI button showing the state of the build
* "Quickstart" documentation (how to quickly install and use your project)
* A list of non-Python dependencies (if any) and how to install them

It may sound silly, but this is an important file. It's quite likely to be the first
thing both prospective users *and* contributors read about your project. Take
some time to write a clear description and make use of GFM (**G**itHub**F**lavored**M**arkdown)
to make it look somewhat attractive. You can actually create/edit this 
file right on GitHub with a live-preview editor if you're not comfortable 
writing documents in raw Markdown.

We haven't yet covered the second and third items in the list yet (ReadTheDocs
and TravisCI). You'll find these discussed below.

#### Using the "Issues" Page

Like most things in life, the more you put into GitHub, the more you get out of
it. Since users will be using it to file bug reports anyway, making use of 
GitHub's "Issues" page to track feature requests and enhancements just makes
sense. 

More importantly, it allows potential contributors to both see a list of
things they might implement and automatically manages the pull request workflow in
a reasonably elegant manner. GitHub issues and their comments can be cross-linked
with commits, other issues in your project, issues in *other* projects, etc.
This makes the "Issues" page a good place to keep all of the information related
to bugfixes, enhancements, and feature requests.

Make sure to keep "Issues" up to date and to at least briefly respond to new
issues in a timely manner. As a contributor, there's nothing more 
demotivating than fixing a bug and watching as it languishes on the 
issues page, waiting to be merged.


