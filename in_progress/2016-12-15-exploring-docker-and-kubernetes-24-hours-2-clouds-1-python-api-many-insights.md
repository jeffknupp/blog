title: Exploring Docker and Kubernetes: 24 Hours, 2 Clouds, 1 Python API, Many Insights
date: 2016-12-15 17:33
categories: python kubernetes docker aws gce

**tl;dr After a week dedicated to deploying and managing a system using kubernetes, I'm convinced that the ecosystem in general and kubernetes in particular is not mature enough to run large-scale production systems. To do so would require an investment of manpower and time with "negative ROI" for at least 2-4 years.**

I've been a software developer for almost 15 years. While I'm best known for my [Python
book](https://jeffknupp.com/writing-idiomatic-python-ebook), articles, and projects, I
wrote high-frequency trading servers in C++ on Linux for the first 8 years of my career. I'm very familiar with both 
Linux systems administration as well as deployment of distributed systems. Back then, if you told me I'd eventually
need to write a complex, distributed system that could be deployed "on-prem" (using a client's own hardware without being given direct access to *any* of it) I probably would have started crying.  

<!--more-->

Then Docker and Kubernetes set out to turn everything on its head.

Docker solved the longstanding problem of deploying applications to hetergeneous systems. Today, Docker is entrenched as the de-facto way to bundle and distribute applications. It provides abstraction of the underlying hardware, OS, and system configuration from developers. As long as a machine can run the Docker daemon, it can run your Docker-ized application.

[Kubernetes](http://k8s.io) is trying to solve the same meta-problem: how do we abstract away the notion of machines as individual
resources? If we're to scale out rather than up as an industry, the administration of hundreds or thousands of machines can't be
a requirement. In the kubernetes vision, you don't care about (or even know, most likely) individual machines. You don't
give them cute names. You don't have them in your `.ssh/config`. You don't worry if they catch fire. 

To see why this is useful, an analogy is helpful. The high-availability systems folks often talk about the "pets vs cattle" mindset (and, until version 1.5, kubernetes even had a type of resource called a `PetSet`). If you have individual machines that *can't* go down or else all hell breaks loose, it's a "pet". It must be cared for and watched.

If you have a "herd" of machines where you can (and routinely *do*) solve individual machine health problems by "taking it out back and shooting it", you've got "cattle". After all, another machine can just take its place and one less cow doesn't cause the herd to go crazy. Your goal is to keep your systems running in the face of network issues and hardware failures. Back when you had 8 machines, that was doable by administering them individually. With dozens or hundreds of physical machines, you probably want your application powered by a herd of cattle rather than Socks the Redis Cat, Peanuts the Postgres elephant, and your twin `nginx` wolverines.

But how realistic is this vision, and how far has the technology to support it come? For a project I'm working on, we're looking to (eventually) move away from [terraform](https://www.terraform.io/) and [ansible](https://www.ansible.com) for machine provisioning and deployment as the application is meant to be deployed on-prem at customer sites. We'll also need *something* to do orchestration, service discovery, secret management, etc. So, having played around with [kubernetes](http://k8s.io) before and watched its progress closely, I decided it was time to take a deeper dive and get a real feel for its maturity and usefulness.

I dedicated a single week (_all_ of a single week) to see what it would take to get the application fully
[Docker-ized](https://www.docker.com) and deployed to a cluster managed by [kubernetes](http://kubernetes.io/). Not only
that, I would deploy on two totally different cloud providers: AWS, which we use for 98% of our infrastructure, and
Google Cloud Platform (specifically Google Container Engine), with which I had no prior experience. If sucessful, I
could be confident that the application is cloud-provider agnostic. It would also show as many of the warts of kubernetes as possible
in a week of use.

Luckily, the application's technology stack is *very* common:

* Python (Flask) API Service
* React-based front end
* Postgres for traditional storage needs
* Elasticsearch for advanced search capabilities
* Redis for various caching needs

So getting all of this up and running should be no problem, right? Well, yes and no. I won't spoil the details.

# Docker Is Growing Up

I've used Docker before a number of times, but it's been a while since I used it in a serious capacity. It's gained a
lot of functionality over the past year and Docker has _seriously_ grown its ecosystem (e.g. Docker Machine,
Docker Swarm, Docker Datacenter, Docker Cloud...). At its heart, though, it's still the Linux container system we've all
grown to love.

The first decision was how to "properly" Docker-ize the first-party components in the system, namely the Flask API
service and React front end. In our current deployments, these live on a single machine with the standard setup:

* [nginx](http://nginx.org)
* [uwsgi](http://uwsgi-docs.readthedocs.io/en/latest/)
* [supervisord](http://supervisord.org)

A request for the root page arrives, the 10-line HTML page requests the required javascript files to bootstrap itself,
and from then on, the front end is driving. The Flask API is run by `uwsgi` under the watchful eye of `supervisord`.
When the front end makes an API request, `nginx` communicates with `uwsgi` over a Unix domain socket using the `uwsgi`
binary protocol. If one of the Python process spawned by `uwsgi` (or `uwsgi` itself) goes down, `supervisord` restarts
it.

This is about as vanilla a deployment one could have for a web-based Python application. And I figured (correctly) that
this would work in my favor. We weren't doing anything crazy in terms of the setup of the machine. Creating a Docker
container should be a piece of cake.

I realized, though, that our deployment was really two orthogonal components with a very clear boundary/interface.
`nginx` and the static assets the drove the frontend were one portion. `uwsgi` and the Flask app were completely
separate. The two components "met" in exactly one place: a socket connection.

## Dockerizing A Python Web App In 10 Minutes

I decided, then, that I would separate this part of the application into _two_ containers. The first I tackled was the Flask app. The only thing that threw me for a bit of a loop was realizing how much of our current provisioning steps I could get rid of. Since the container would be managed externally, `supervisord` was unneccessary. Since only one Python application would be on the machine, no virtualenv would be required. 

I could have gone through the exercise of installing all of the system-packaged versions of the contents of `requirements.txt` but I'm not in the "creating pain for myself" business, so I just `pip install`-ed them on the machine. To be honest, I felt simultanesouly liberated and dirty for not using a virtualenv. It was disrobing at a nude beach if you're not a nudist.

Here's the file in all its glory. I'm sure there are Docker nerds who will point out all the things I could have done to
make this 22 line file shorter, but it's not worth my time.

<script src="https://gist.github.com/jeffknupp/ad7202703e49244aca0ef84fa17fdad8.js"></script>

## Dockerizing nginx And A JavaScript Front End in Way Less Than 10 Minutes

If the Python app was easy, the `nginx` part was like playing basketball against toddlers. I'm not even going to bother
to _try_ to defend the shortcuts taken in this 6 line file, since time was of the essence.

<script src="https://gist.github.com/jeffknupp/09b485e09025b9198c098a228b3f1f1a.js"></script>

## Enter `kubernetes`

I had two images built and could run the contianers as a single unit using `docker-compose` and a simple YAML file.
Everything worked fine... as long as they could connect to our existing Postgre, Redis, and Elasticsearch machines.
It was now time to switch gears. I wasn't looking to build any sort of bespoke Docker images for any of those
components, so I'd just use some "off the shelf" images avaiable from one of the half-dozen or so public container registries.

To determine the best practices for deploying both my system and the third-party components, I turned to the 
kubernetes documentation. It is, in short, a mess. Here are some gripes:

* Different portions were clearly written at different times. There's no way to tell what information is out-of-date.
* Concepts that are now deprecated are used in the tutorials.
* The same concepts are half-described in multiple places. It takes a lot of clicking around to develop a complete picture of any one concept. Understanding how *everything* works together takes marathon-runner persistence.
* New tools are being developed at a breakneck pace, often building on and/or replacing older tools that did similar things. The AWS cluster-creation tool ecosystem is particularly hillarious.
* Support for *obvious* usage patterns (like, say, a database that needs to have persisent storage and can't just be killed at will) is all over the map. The fact that kubernetes was designed for long-running, stateless processes is still painfully obvious.
* Many *very* important caveats are mentioned in passing and alternative approaches are rarely given (see the documentation for the admittedly alpha version of [`kubeadm`](http://kubernetes.io/docs/getting-started-guides/kubeadm/) for some examples)

## Pressing Onward

To be fair, the documentation for most projects is pretty bad. I decided the best way to determine how to deploy *my*
application on kubernetes would be to see how the *other* components were deployed. This proved... confusing.


