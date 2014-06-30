title: Docker Blurs the Line Between SaaS and Self-Hosted Apps
date: 2014-06-30 10:10
categories: docker

The more I use Docker, the more I notice it being used. One interesting example
was when I recently decided to add a [Discourse](http://www.discourse.org) site
to [jeffknupp.com](http://www.jeffknupp.com) (it's not ready yet, but will be
soon). When I finally found instructions for installing a self-hosted version of
Discourse (rather than their SaaS hosted version that requires a monthly
payment), I was shocked.
<!--more-->

Looking at the [installation instructions for Discourse](https://github.com/discourse/discourse/blob/master/docs/INSTALL.md), I was
immediately struck by the fact that, not only did they support Docker
installations, but Docker was the *only* method of installation they supported. Why? This
question, from their FAQ, is quite telling:

> Why do you only officially support Docker?
>
> Hosting Rails applications is complicated. Even if you already have Postgres, Redis and Ruby installed on your server, you still need to worry about running and monitoring your Sidekiq and Rails processes. Additionally, our Docker install comes bundled with a web-based GUI that makes upgrading to new versions of Discourse as easy as clicking a button.

## A Taste Of Things To Come

Indeed, Docker makes it so easy to install and manage applications that
self-hosting Docker-based applications is a very real option for those
who would otherwise use the hosted version of applications like Discourse or WordPress. 
While installing something like WordPress is beyond the skills of most non-technical bloggers,
installing it via Docker (if that were an option) certainly is not. 

Discourse's installation documentation is fantastically detailed yet remarkably short. 
It walks you through every single command you need to type after connecting to a freshly
provisioned VPS, down to commands as simple as `cd /var/docker`. In all,
*Discourse can be fully installed on a new VPS machine in only 8 command line commands (including things like `mkdir`, `cd`, and `apt-get install git`).*
That, to me, is mind-blowing. It is also a taste of things to come.

## A Short Example

To demonstrate to myself how easy it is to set up a rather specialized environment,
I decided to "Dockerize" my development environment. By downloading and running the
Docker image I created, you can `ssh` into an exact replica of my development
environment, down to my `vim` plugins and `zsh` shell. The directory structure
is also organized according to how I work: a `code` directory with a
`github_code` sub-directory containing clones of all my GitHub repos.

Want to install it? It's simple. I created [a GitHub repo called
"docker"](https://raw.githubusercontent.com/jeffknupp/docker) to contain all my
Dockerfiles not attached to specific projects. Run the following command to
download the Dockerfile for my dev environment:

    #!bash
    $ wget https://raw.githubusercontent.com/jeffknupp/docker/master/dev_environment/Dockerfile

Next, you need to *build* the image by running the following command:

    #!bash
    $ sudo docker build -t jeffknupp/dev:devel .

After that completes, start the `ssh` server in the virtual environment by
running:

    #!bash
    $ sudo docker run -P -d --name dev jeffknupp/dev:devel

Then check what port `ssh` was mapped to by running:

    #!bash
    $ sudo docker ps
    CONTAINER ID        IMAGE                 COMMAND             CREATED             STATUS              PORTS                   NAMES
    74aed65dc132        jeffknupp/dev:devel   /usr/sbin/sshd -D   2 days ago          Up 2 seconds        0.0.0.0:49153->22/tcp   dev

And now you can `ssh` into the machine by running:

    #!bash
    $ ssh jknupp@0.0.0.0 -p 49153

(The password is `temp123`.)

### What Just Happened?

In four commands, you were able to create a virtual environment that exactly
mirrors my development setup. After `ssh`-ing into the machine, take a look at
the `code/github_code` directory. You should see all of my public GitHub repos
checked out. Run `vim` and type the command `:PluginInstall` after it starts.
Let it install the plugins and then restart. You're looking at an exact copy of my `vim`
setup.

Creating the Dockerfile for this was relatively simple, and if you open it up
you'll see it's pretty short (about 60 lines). I'm amazed at what those 60 lines
were able to accomplish, though, and it only cements my assertion that [Docker is the most disruptive technology for software developers in the past decade](http://jeffknupp.com/blog/2014/06/24/docker-is-the-most-disruptive-technology-for-software-development-in-the-last-decade/). And, as we've seen, that's not just for organizations using Docker to simplify their application management and reduce their hardware footprint. I think we're going to start seeing *individuals* coming up with innovative ways to use Docker to do things that simply weren't possible without it.

What's more, since Docker includes a GitHub-like image management site called
[Docker Hub](https://registry.hub.docker.com/), you could have pulled
`jeffknupp/dev:devel` straight from Docker Hub and ran it straight away. That's
because I `push`ed to Docker Hub after confirming the Dockerfile built as
expected. Now my development environment is easily available for you to tinker
with.

## SaaS versus Self-Hosted

For many SaaS applications, there exists a free, self-hosted version that few
use due to the inherent requirement of understanding how to administer a
Linux machine. I assert, however, that Docker makes it simple enough for *anyone* to run a
full suite of completely separate applications. Imagine renting a VPS and running my dev
environment from above, a web application, a blogging platform and a log monitoring
application, all Dockerized. In the old days, that would scare off 99% of the population. With
Docker, I think 100% of the population could get all of that working on a single
machine without issue.

So what does this mean for SaaS businesses? First, there is an incentive to
Dockerize their applications: it gives them complete control over the
dependencies and initial configuration, drastically reducing the number of
support tickets related to clients setting up the application on private hardware. A
Dockerized version allows for push-button installation *on the client's hardware.*

Second, it paves the way for SaaS companies to reduce their hardware expenses. Many 
of their clients already have a substantial hardware footprint and would be happy
to host the application locally if it were an option (and one that didn't require
any maintenance). Especially at larger companies, the "extra cost" of running
the application is barely measurable. For SaaS companies, the collective savings could mean
the difference between operating in the red or the black.

SaaS companies spend a tremendous amount on hardware for application servers.
Docker could be a game changer here. By simply offering a Dockerized version
and letting clients run the application themselves, they kill two birds with one stone.
They reduce their hardware costs while ensuring the application is installed in
exactly the way they want with exactly the dependencies it requires.

## It Only Gets Better

Remember, Docker is still in its infancy. Version 1.0 was only released a short
time ago. The adoption rate, however, is staggering. Google Compute Engine,
Amazon Web Services, Rackspace, and IBM Softlayer. And I'm betting that list grows
very quickly in the near future.

The case for Docker for the organization is clear. More interesting is how
Docker will be used by *individuals* and small companies. Two examples of
small-scale Docker were shown in this article (Discourse and my development
environment). But these are just the beginning. I honestly can't wait to see the
cool stuff people use it for. And soon, you'll be able to discuss this on my
new, self-hosted, Discourse site.
