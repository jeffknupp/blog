title: My Development Environment For Python
date: 2013-12-04 19:20
categories: python vim powerline pdb ipython

It seems a number of people are interested in what my development setup looks
like. I'm constantly emailed questions asking what IDE I use, what OS, what
packages, etc. To stem the tide, I'll outline my dev setup here.

<!--more-->

## Editor: Vim

It should come as no surprise that I use a pure text editor (rather than an IDE)
for writing code. Outside of Java, it seems like most professional developers
use either vim or emacs. The reason, I assume, is that they're always available
(especially in vi's case). No matter what company I work for, regardless of the
platform they're on, I know I'll always be able to use Vim.

In addition, a decade with Vim makes me a *very* fast editor of code. I don't
care how quick you are with your favorite IDE and a mouse; I'm faster. Every
time I try to move to an IDE, I switch back after a few days if it doesn't have
vi key bindings. So many Vim commands have become muscle memory that it doesn't
feel like I'm *using* an editor to write code. Vim feels like an extension of
myself, and I shape the code at will.

Here's a picture of what my Vim window looks like (on OS X):


<img src="http://www.jeffknupp.com/images/vim.jpg">

That being said, there are a couple of rather nice Vim packages that I use.

In no particular order, here are the packages I use:

* [vundle](http://www.github.com/gmarik/vundle)
    Essential as a package manager (I can finally list all my Vim dependencies in my .vimrc file). Vim packages are installable directly from GitHub, which is a nice touch. 
* [fugitive](http://www.github.com/tpope/vim-fugitive)
    Best git interface for Vim
* [vim-repeat](http://www.github.com/tpope/vim-repeat)
    Use `.` to repeat much more than simple inserts or deletes
* [ctrlp.vim](http://www.github.com/kien/ctrlp.vim)
    A buffer/file/mru/tag explorer with fuzzy text matching
* [vim-markdown](http://www.github.com/plasticboy/vim-markdown')
    Markdown syntax highlighting for Vim
* [gundo.vim](http://www.github.com/sjl/gundo.vim)
    Visualize and traverse your undo tree. A must
* [YouCompleteMe](http://www.github.com/Valloric/YouCompleteMe)
* [syntastic](http://www.github.com/scrooloose/syntastic)
    These two together make the absolute best autocomplete package around
* [vim-colors-solarized](http://www.github.com/altercation/vim-colors-solarized)
    Solarized color scheme for Vim
* [powerline](https://github.com/Lokaltog/powerline)
    Powerline integration for Vim

## OS: Arch Linux

My OS of choice is Linux. Specifically, [Arch Linux](http://www.archlinux.org). Having used Linux on the desktop for the past ten years, Arch is exactly what I'm looking for in a distro: don't force choices on me, stay at the bleeding edge, and get out of my way. While some bemoan insurmountable issues they encountered during simple upgrades, I can count on one hand the number of problems I've run into that took more than 15 minutes to solve. Arch also acts as a good way to *really* learn Linux.

### But Also OS X

Since I run Linux on most of my personal PCs, I never had the need for a Mac.
When I joined AppNexus, I was given a Mac Book Pro Retina. I was lost until I
found Terminal (and later iTerm2). OS X, especially in comparison to Windows, is
great. I do, however, hate the Command key and the reliance on Homebrew/Macports
for all my favorite software.

## Shell: zsh

I was a bash user by default, as that's what I most commonly found installed by
default at the various companies I worked for. Once I discovered zsh, however,
there was no going back. First with "oh-my-zsh" and now with "prezto", I have an
amazing shell setup. The tab-completion alone is worth the price of admission
(here's what I see when I type `sh <Tab>`:

<img src="http://www.jeffknupp.com/images/shell.jpg">

zsh just does everything *right*. I also use [powerline](https://github.com/Lokaltog/powerline) in both the shell and vim. It's suitably awesome (looks great, nice git integration, etc) without slowing things down.

If you're interested in my configuration files (.vimrc, .zshrc, etc), they're publicly available on
GitHub under my [config_files](http://www.github.com/jeffknupp/config_files)
repo.

## Font: Adobe's Source Code Pro

When this font came out, everyone went nuts for it. Well, I'm still nuts for it.
In my opinion, Source Code Pro is the single best programming font, hands-down.
It's almost *too* pretty.

## Python Version: Mercurial Latest

One of the first things I do when I get a new machine is `hg clone` the cPython
repo and build both a 2.7.x and 3.x version of the interpreter. I like to stay
at the bleeding edge (frequently pulling down changes) and not rely on whatever
happens to be installed on the system (I'm looking at you CentOS 5). One of my
former employers had very strict rules about what software could be installed on
servers (including dev servers), so I got very good at `wget`-ing the source,
`./configure`-ing it and `make install`-ing it (and dealing with all the
problems that popped up as a result). Therefore, I'm quite happy to build the
interpreter from scratch and have done so a dozen times.

## Python Tools: A Bunch

Here are the Python packages and tools I can't live without:

###### Requests

No surpise here...

###### iPython

The best interpreter experience around

###### virtualenvwrapper

Makes working with virtualenvs a breeze

###### BeautifulSoup

HTML/XML manipulation library

###### Flask

The most user-friendly web framework in the Python ecosystem

###### pip

Duh...

###### SQLAlchemy

Is there even a competitor for database ORMs? I honestly don't know the answer
to that.

###### tox, mock, py.test, coverage, pylint, pep8

Makes testing actually enjoyable

###### Pandas / numpy

Awesome library for data analysis 

###### selfspy

Really cool "Quantified Self" daemon

###### pdb

For someone coming from C/C++, ipdb is a godsend. Simply the best Python
debugger

###### Cython

Sometimes you just gotta write C

###### pypy

It's fun to write your own language in RPython and get a JIT-enabled interpreter
for it for free

###### HTTPie

A better `curl` than `curl`

## Wrap-Up

In the end, I have a pretty boring setup: zsh and vim on Linux. The key thing to
realize is just how powerful each of those tools are on their own. Combined,
they make for an excellent development experience.
