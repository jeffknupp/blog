title: Take My Python Development Environment For A Testdrive
date: 2014-06-27 08:35
categories: python environment

In [pmy last article](http://www.jeffknupp.com/2014/06/24/docker-is-the-most-disruptive-technology-for-software-development-in-the-last-decade/), I extolled the virtues
of [Docker](http://www.docker.com). While there are many serious use cases for
Docker, there are also uses that are just for fun. Today, I'll show you how you
can use Docker to create *the exact environment I use for development*. That
includes my highly customized zsh configuration, my extensive vim configs, my
disk layout for project work, and the tools I use every day for development.
<!--more-->
## Bring In The Clones

Before we get to the instructions for cloning my development environment, let's
talk a bit about how we're able to do all this in Docker. Remember from the last
article that Docker has two main concepts: images and containers. An *image* is a
versioned snapshot of the entire filesystem used by the application, including
all its dependencies and configuration. A *container* runs an image. Think of a
container as an extremely lightweight *VM* (Virtual Machine, like you would create
with Virtual Box).

So, clearly, we need a way to create images with out application-specific code
and packages. We do so in one of two ways: by interactively installing
applications in a running container or through a `Dockerfile`. While you *could*
start up a fresh container using the command ` sudo docker run -i -t ubuntu /bin/bash`
and install all your packages via the command line, you wouldn't have a record
of all the changes you had made that would allow others to use your image with
any confidence.

## The `Dockerfile`s

Instead, we'll create a `Dockerfile`. The contents are a simple list of `COMMAND <arguments>`
lines, each specifying an action to take to configure the image. The most
straightforward command supported by `Dockerfiles` is `RUN`, which runs whatever
arguments follow it. To begin the `Dockerfile`, though, we'll need to use an
existing image as a *base*. We'll choose `ubuntu:14.04`, the latest ubuntu
release and an "official" base image.

The first two lines of my Dockerfile will specify the image I'm using as a base
and the fact that I'm the maintainer:

    #!Dockerfile
    FROM ubuntu:14.10
    MAINTAINER Jeff Knupp <jeff@jeffknupp.com>

This sets the base image and maintainer information. Next, knowing that we have
a fresh Ubuntu installation in front of us, we'll update the package repos to
get the latest information about package versions. We'll do so using the `RUN`
command and simply type the command line command we would normally run:

    #!Dockerfile
    RUN apt-get update

### Installing Essential Software

There are a number of tools I use regularly for development, but three in
particular I can't live without: `vim`, `git`, and `zsh`. I have highly customized
configurations for both of them with a number of plugins attached. Let's install
these programs in the `Dockerfile`:

    #!Dockerfile
    RUN apt-get install -yq vim zsh git

We pass the `-y` flag to `apt-get install` to automatically answer "Yes" for all
questions asked by `apt-get`. The `-q` flag suppresses some extraneous output.

Now that we have `git`, we can use it to pull two of my GitHub repos necessary
to set up my environment: [config_files](http://www.github.com/jeffknupp/config_files) and [a forked version of prezto](http://www.github.com/jeffknupp/prezto)
