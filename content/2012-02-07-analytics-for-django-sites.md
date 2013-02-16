title: Analytics for Django Sites
date: 2012-02-07 22:44
categories: seo analytics clicky google illestrhyme

This is the first in a series of posts I plan to do over the next month about Analytics and Django. In this post I'll walk through how I began to use a number of analytics tools to
drive decisions about my site, [IllestRhyme](http://www.illestrhyme.com).

One of the first things I did when writing
[IllestRhyme](http://www.illestrhyme.com) was to sign up for Google
Analytics. I had never run a web site before, but I was aware of
Google's analytics offering. I admit, for the first few weeks after the
site went live I would start at the Google Analytics page and __hope__ to
see users in the Live View. I wasn't really using the data for anything.
I was using Google Analytics as a virtual scoreboard.

It wasn't until I signed up for [Clicky](http://getclicky.com/66528953)
that I started to take analytics seriously. In fact, more specifically,
it was when I combined Clicky and
[django-analytical](https://github.com/jcassee/django-analytical) that I
really took my first deep-dive into using analytics data for decision
making. Since django-analytical already integrates with a number of
analytics services, including Clicky, setup was a breeze. Sure, I could
have inserted the raw code into my Django templates, but
django-analytical gave me a single point at which to configure all my
analytics services. 

More importantly, and I can not stress this enough,
__django-analytical's Clicky integration let me see my users in Clicky via
their contrib.auth usernames__. This was __huge__. Now, instead of
staring at IP addresses, I could follow users on their visit to the site (using
[Clicky's](http://getclicky.com/66528953) awesome Spy feature) in
real-time by user name. Believe me, nothing will teach you more about you
users than recognizing usernames and their associated behavior patterns.
I could tell which users were hitting the site to check quickly for
updates, which users hung around for a while, and which users _used the
site like it was crack_. It was this last group that I was initially
interested in.

<!--more-->
I discovered I had about four or five _hardcore_ users, that were on the
site for hours a day. Now, part of that is just personality, but in
addition, _something on the site clicked for them_. Since I want all my
users on the site for hours a day, I decided to determine what they were
doing in a more rigorous fashion. Naturally, I started coding...

I ended up writing a middleware that tracked a configurable set of users as
they browsed the site and stored this information in the database. I
then processed this information and organized it into "activities". If a
user was going through all the new rhymes submitted and voting on them,
this was 'updating'. If the user was submitting a bunch of new rhymes,
this was 'bulk submitting', etc. After analyzing this information for my
power users and a random sampling of other users, I noticed they were doing one thing more than any other,
which I didn't even have a category for: they were following each other.

This was strange to me, as I didn't think of IllestRhyme as a community.
To me it was more like a tool to get better at rapping. To some of my users, at least, it
was a destination; a way to interact with like-minded people. I quickly
realized the value of this and set to work adding tools that would
encourage this interaction.

Using
[django-postman](https://bitbucket.org/psam/django-postman/wiki/Home) I
gave them the ability to send Private Messages. I encouraged commenting
by increasing the amount of Rep (virtual points representing a user's
'reputation' on the site, sort of like StackOverflow) adding comments
was worth. Voting on other users' verses also received a boost. 

That's just one example of the ways I use the analytics data I collect
from [Clicky](http://getclicky.com/66528953), Google Analytics, HubSpot,
and the rest to make decisions about my site. In my next Analytics post,
I'll take a look at A/B testing in Django. Stay tuned!

Questions or comments on _Analytics for Django Sites_? Let me know in the comments below. Also, [follow me on Twitter](http://www.twitter.com/jeffknupp) to see all of my blog posts and updates.
