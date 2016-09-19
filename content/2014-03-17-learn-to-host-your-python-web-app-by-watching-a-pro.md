title: Learn to Host Your Python Web App by Watching a Pro
date: 2014-03-17 15:01
categories: python vps straphost

A tutoring client who was nearing the end of the Django project he's been
working on asked how he should host his service. I explained to him that there
are basically two options: use a service that takes care of everything for you
(like Heroku or Google App Engine) or get a VPS and do everything yourself.
After begrudgingly suggesting he use a service like Heroku, I wondered why there
wasn't some sort of middle ground.

<!--more-->
## The Problem

My client's situation is an extremely common one: "I finished my web app and
want to launch it. I'm not a Linux sysadmin. **Now what?**" If you decide
to pay for a service to take care of all the details for you, you learn nothing in the
process. Worse, when stuff goes sideways (and it always does), you're totally
reliant on said service to fix things. You, yourself, don't have any power to
fix issues outside of your application. If you need to scale, you better hope the service
you chose scales with you.

On the other hand, if you rent a VPS, you're essentially dumped to the command
line of a fresh Linux distro installation. Forget things like security and
monitoring, just *getting your web application working consistently* involves a
ton of work. You need to become a DBA/sysadmin over night. Any issues with the
machine and you're in for a night of Googling about arcane Apache error messages or
PostgreSQL config files.

Why doesn't a third option exist? In home repair, for example, there *is* an
option between "hire someone" and "buy the materials and do it from
scratch": many chains (like Home Depot) offer classes taught by professionals
wherein you'll learn enough to complete your project, while still maintaining total
control over it. Why doesn't something like that exist for web hosting?

## `straphost`: The Solution

When I was first learning to deploy web applications, I would have **thrown money** at 
someone offering to set up my application while at the same time
explaining *what* they were doing and *why*. **I think there's a real need for a service that sets up your web app according to up-to-date best practices while at the same time teaching you how to do so.**
I would also have appreciated someone teaching me how to solve common
maintenance issues, so let's include that as well.

That's why I'm announcing the creation of [straphost](http://www.straphost.com) ("bootstrapped hosting"). Think of it as 
both a VPS provider and a tutoring service. I'll teach you how to set up your Python web application
with the web server/database of your choice as well as provide you the infrastructure on which to do so.
We'll also set up tools like [supervisord](http://www.supervisord.org) and cron/[celery](http://www.celeryproject.org) for your project.
After your application is installed, you'll have full control of your application server. Want to enable 
a service like [Loggly](http://www.loggly.com) or [PagerDuty](http://www.pagerduty.com)?
Feel free to do so yourself, or ask for help and we'll do it together.

## Where We Are

At the moment, I'm still in the process of provisioning the hardware, but that
will be finished in days. I've not come up with a pricing model, but assume it
will be a *very* reasonable flat monthly rate plus an hourly charge for tutoring
sessions in which we administer the application. Note that the tutoring portion
is entirely optional; if you know how to do it yourself and just want a VPS from
some random Internet blogger, that's fine with me. Also, I'll be hiring 24/7
technical support for when you have a problem that needs to be solved **now**.

Which reminds me: there's a lot of sales-y type stuff for me to do (for example: *make a web site*
for this). That said, if I've piqued your interest, **please email me at [jeff@jeffknupp.com](mailto:jeff@jeffknupp.com)** to get notified
when this is available (likely sometime later this week). The initial cohort
of clients will be *extremely* limited. This will let me devote enough time to each
client while at the same time proving to myself that the model works.

## Let's Do This

I've been tutoring long enough to know that this *is* a real issue; you either
pay a service to take care of *everything* or pay a VPS provide to take care of
*nothing*. There needs to be some middle ground. If you have a Python-based web application
you'd like to learn how to launch and maintain, [straphost](http://www.straphost.com) 
may be just what you're looking for. [Email me](mailto:jeff@jeffknupp.com) and
we'll find out together.
