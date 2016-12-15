title: Exploring Docker and Kubernetes: 24 Hours, 2 Clouds, 1 Python API, Many Insights
date: 2016-12-15 17:33
categories: python kubernetes docker aws gce

For a project I'm working on, we're looking to (eventually) move away from [terraform](https://www.terraform.io/) and [ansible](https://www.ansible.com) for machine provisioning and deployment towards something more flexible. The application is relatively straightforward from a technology stack standpoint:

* Python (Flask) API Service
* React-based front end
* Postgres for traditional storage needs
* Elasticsearch for advanced search capabilities
* Redis for various caching needs

I decided to spend a single day (_all_ of a single day) seeing what it would take to get the application fully
[Docker-ized](https://www.docker.com) and deployed to a cluster managed by [kubernetes](http://kubernetes.io/). Not only
that, I would deploy on two totally different cloud providers: AWS, which we use for 90% of our infrastructure, and
Google Cloud Platform (specifically Google Container Engine), with which I have no prior experience.

**tl;dr I learned a metric ton about the current state of orchestration and deployment tools for distributed systems.**

And of course, I'll let you in on the fun.

<!--more-->

# Docker Is Growing Up

I've used Docker before a number of times, but it's been a while since I used it in a serious capacity. It's gained a
lot of functionality over the past year and Docker has _seriously_ grown the tooling ecosystem (e.g. Docker Machine,
Docker Swarm, Docker Datacenter, Docker Cloud...). Still, at its heart, it's still the Linux container system we've all
grown to love.

The first decision was how to "properly" Docker-ize the first-party components in the system, namely the Flask API
service and React front end. In our current deployments, these live on a single machine with the standard setup:

* [nginx](http://nginx.org)
* [uwsgi](http://uwsgi-docs.readthedocs.io/en/latest/)
* [supervisord](http://supervisord.org)

A request for the root page arrives, the 10-line HTML page requests the required javascript files to bootstrap itself,
and from then on, the front end is driving. The Flask API is run by `uwsgi` under the watchful eye of `supervisor`.
When the front end makes an API request, `nginx` communicates with `uwsgi` over a Unix domain socket using the `uwsgi`
binary protocol.

This is about as vanilla a deployment one could have for a web-based Python application. And I figured (correctly) that
this would work in my favor. We weren't doing anything crazy in terms of the setup of the machine. Creating a Docker
container should be a piece of cake.

I realized, though, that our deployment was really two orthogonal components with a very clear boundary/interface.
`nginx` and the static assets the drove the frontend were one portion. `uwsgi` and the Flask app were completely
separate. The two components "met" in exactly one place: a socket connection.

## Dockerizing A Python Web App In 10 Minutes

I decided, then, that I would separate this part of the application into _two_ containers. The first I tackled was the
Flask app. The only thing that threw me for a bit of a loop was realizing how much of our current setup I could get rid
of. Since the container would be managed externally, `supervisord` was unneccessary. Since only one Python application
would be on the machine, no virtualenv would be required. I could have gone through the exercise of installing all of
the system-packaged versions of the contents of `requirements.txt` but I'm not in the "creating pain for myself"
business, so I just `pip install`-ed them on the machine. To be honest, I felt simultanesouly liberated and dirty for
not using a virtualenv. It was like being naked at a nude beach.

Here's the file in all its glory. I'm sure there are Docker nerds who will point out all the things I could have done to
make this 22 line file shorter, but it's not worth my time.

<script src="https://gist.github.com/jeffknupp/ad7202703e49244aca0ef84fa17fdad8.js"></script>

## Dockerizing nginx And A JavaScript Front End in Way Less Than 10 Minutes

If the Python app was easy, the `nginx` part was like playing basketball against toddlers. I'm not even going to bother
to _try_ to explain all the intricacies of the following 6 lines...

<script src="https://gist.github.com/jeffknupp/09b485e09025b9198c098a228b3f1f1a.js"></script>

## So... Now What?

I had two images built and could run the contianers, but making two containers communicate with one another has burned
me in the past (as in 
