title: How linkrdr went semi-viral
date: 2012-02-21 04:34
categories: linkrdr seo viral blog


I was a bit under the weather this past weekend, but it turns out I
wasn't the only thing to go viral. Below is a brief story of how [linkrdr](http://www.linkrdr.com) enjoyed it's first encounter with virality.

Background
----------

Before Saturday, linkrdr had about 10 users, who had figured out a way
to sign up without me really providing one. Sometime Thursday evening, I
believe, I slapped a 'Beta' sticker on the front page, cleaned some
stuff up, and declared linkrdr open for business. Come the weekend, I
was under the weather and not feeling like working on anything, so I
didn't check any of my sites until Monday at 4pm. I cruised over to my
[Clicky](http://getclicky.com/66528953) dashboard and took a look at the
stats for this blog. Then something caught my eye...

{% img http://66.228.46.113/static/img/linkrdr_growth.png linkrdr visits per day%}

<!--more-->

"Uh oh"
---------------

The graph for linkrdr, which is usually totally flat, had suddenly
shot up almost vertically. I quickly checked the number of users via the
django console and felt a pit in my stomach: __720 users had signed up
in the past 24 hours__. I caught my breath, then checked how many total
links linkrdr was managing. I read the number three times. I couldn't
believe it: __109,214 links__ across about 3,700 feeds. I fired up my
browser to see if the site had melted down. To my surprise, it was
pretty responsive. After clicking around more and convincing myself the
server wasn't on fire, I did a little [Clicky](http://getclicky.com/66528953) style investigating.

It became clear rather quickly that most of my links were coming from
two sources: [startupsea.com](http://www.startupsea.com), a new
startup-roundup type site I hadn't heard of, and
[scripting.com](http://www.scripting.com). When I saw the second site,
my heart skipped a beat. I'm very familiar with scripting.com, the blog
of [Dave Winer](http://en.wikipedia.org/wiki/Dave_Winer). I checked out
scripting.com and sitting there on his list of links was a link to
linkrdr. He had also tweeted about it to his __75,000__ followers.
Between the two sites, linkrdr had gone mini-viral.

Aftermath
--------------

I quickly decided that I needed to bullet-proof the site (how I did so
will be the topic of my next post). I was proud
that the site could handle the drastic uptick in flow, but I wasn't
going to leave anything to chance. Over the past 18 hours, I've been
adding features that users have been clamoring for (OPML import has been
added, for one), fixing bugs, and generally cleaning things up. It's still too early to
tell if this was just a one-off blip, as the US public had Monday off of
work. Tuesday morning will be an interesting one. Let's hope linkrdr
gets more viral-love!

Questions or comments on _How linkrdr Went Semi-Viral_? Let me know in the comments below. Also, [follow me on Twitter](http://www.twitter.com/jeffknupp) to see all of my blog posts and updates.
