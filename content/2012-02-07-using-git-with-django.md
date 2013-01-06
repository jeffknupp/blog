title: Using Git with Django
date: 2012-02-07 07:57
categories: git django python 

When I started [IllestRhyme](http://www.illestrhyme.com), I had never used git . Git gives me distributed version
control and the ease (and speed!) of the git workflow for a slight learning
curve. Below is how I set up my Django project to use git, from start to
finish.

To begin, I had my Django project already created and a bit of code in
there, so I needed to "add" it to a new git repo. All that's needed for
this is to `cd` into the top level directory and run `git init .` This
sets up a git repo in the directory, __but doesn't commit the files.__
Before committing, we'll want to setup our `.gitignore` file to tell
git what files not to track in version control. Since I'm working with Python files using
vim, my `.gitignore` file has the following contents:

    :::bash
    *.pyc
    *.swp
    local_settings.py

The `local_settings.py` file is part of my development workflow, as
explained in [this post](http://www.jeffknupp.com/blog/2012/02/05/django-production-deployment-using-git/). After we create
the `.gitignore` file, we add _everything_ to the repository, using `git
add .` This stages all of our files for commit to git. At this point, we
can run `git commit` to actually commit our files for the first time.

At this point, we have our Django project in a (local) git repository. I
use Bitbucket as a "backup" git repo in case I lose my web server. As
you might have guessed, I do all my work on the web server directly
using ssh, gvim, and X tunneling. This is not necessarily recommended
for large projects, but it works well for a single developer. Whenever I
make a change and commit it, I use `git push` to push the commit to
Bitbucket, so that Bitbucket always has the latest copy of the repo.

Once we've committed to git, the first thing to do is clone our
repository to create a development environment in a new area on our
machine reserved for development. If you're cloning on the
same machine, you'll use `git clone <path/to/original/git/repo>`. Github
or Bitbucket users will use `git clone <remote repository>`, where
"<remote repository>" is what the service shows is the URL for your repo. Regardless,
clone your repo to create a dev environment that exactly mirrors your
prod environment.

In our new development area, we'll first want to create a
branch, using `git branch <branchname>`. Git creates a branch of the
current branch (which for us will have been 'master'). __It does not,
however, switch you to that branch.__ To switch to working on your new
branch, use `git checkout <branchname>`. To see what branches are
available, just type `git branch`. The branch you are currently on will
be marked with a '\*'. 

Once you've done some work on your branch that you're happy with, it's
time to commit. If you added files during this phase, run `git add
<filenames>` to stage them to be committed. Alternately, you can use
`git add .` to add _all_ untracked files to be committed. From here,
just commit using `git commit <changedfiles>` or `git commit -a` for all
changed files that git is tracking.

Now it's time to merge your changes back into your master branch. Switch
back to the master branch with `git checkout master` and merge the
changes with `git merge <branchname>`. If there are no conflicts, _git
will autocommit the merge changes_ and nothing more needs to be done. If
conflicts do arise, manually fix them and `git commit` them. Git will
prepopulate the commit message with something like 'Merge from
<branchname>', which you can replace or, better yet, enhance.

Now that we've got our changes committed to the master branch in our
development area, it's time to push them to production. If you're using
a service like Github or Bitbucket, first push the changes there with a
`git push`. Next, `cd` into your production area and pull down the
changes using `git pull` (or `git pull <development repo area>` for a
repo on the local machine). This should update the master branch in your
production area with all of the changes committed from development.
That's it! You've successfully used git to manage changes in a Django
project!

I'm certainly no git guru and there are likely aspects of this workflow
that can be enhanced or simplified. If you see something that doesn't
make sense or can be streamlined, please let me know in the comments.
I'm always looking to improve my git-Fu!
