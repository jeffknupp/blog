title: Docker is the Most Disruptive Technology For Software Development in the Last Decade
date: 2014-06-24 05:09
categories: docker python golang

There have been a number of technology innovations in the field of
software development over the last five or ten years. Cloud computing, Hadoop,
and NoSQL are just a few technologies that have seen reaonably quick growth and
adoption. But in terms of long-term effect on the software industry, these
technologies are miles behind a relative newcomer.

**That technology is *[docker](http://www.docker.com).**

## What's Docker?

Docker is an application build and deployment management system. It is based on
the idea of homogenous application *containers*. The shipping industry has long realized the
benefit of such containers.

Before an industry standard container existed, loading and unloading 
cargo ships was extremely time consuming. All of this was due to the nature of 
the shipping containers: they were all of different sizes and shapes, so 
they couldn't be stacked neatly or removed in an orderly fashion. Once a 
standard size and shape were agreed upon, it revolutionized the industry.

New infrastructure could be built that dealt only with containers of a single size. Loading and unloading became orderly and
automated. *And shipping things got a lot faster*.

## OK, But What Is Docker *Really*?

Docker consists of containers, based on preexisting technologies like lxc and
union file systems. Certainly, launching Linux containers from the command line
is nothing revolutionary. However, the containers themselves are only half the
story.

The other half is *images*. Images are indexed snapshots of the entire 
filesystem a container is meant to run. Every time a change to the filesystem
is made, a new version of the image is automatically created and assigned a hash ID.

In one stroke, a *number* of longstanging problems in managing software systems are
solved by Docker:

* Repeatability of deployments: every previous production deployment should be
    re-buildable)
* Management of applications with conflicting dependencies: two applications
    that rely on different versions of the same package
* Isolation of orthogonal applications: two unrelated applications that happen
    to run on the same machine should not be able to negatively affect one
    another
* Distributed management of virtual envrionments: a GitHub like repository
    to manage organization and deployment of application versions
* Low overhead: Unlike traditional virtual machine solutions that require a
    hypervisor, any solution should be based on much lighter-weight Linux
    contianers

I kid you not. Docker solves all of these issues. Let's see how.

### Flask: Dockerized

Imagine you 
