title: Why I Still Hate HATEOAS
date: 2016-05-09 20:37
categories: rest hateoas api

A while ago, I wrote a short post titled [Why I Hate HATEOAS](https://jeffknupp.com/blog/2014/06/03/why-i-hate-hateoas/). It was a bit polarizing, with supporters and detractors taking to social media in roughly equal numbers. Well, almost two years have passed, and HATEOAS is just as popular and stupid as ever. To show you why it's nonsense, I'll list the arguments HATEOAS apollogists use in its defense and point out exactly where logic leaves the room.

## Argument 1: The Server Can Restructure Its URLs And Things Will Still Work

This is one of the most common arguments I hear, and certainly the dumbest. The line of thinking goes: since the server is sending the client enough information to reach any resource in the system (without requiring out-of-band knowledge like the URL, or even URL patterns, for resources). The server, then, is no longer tied to a specific URL structure. It can be changed at will and clients will simply follow the new links returned in HTTP responses to find the old resources.

I can't even... WHAT?! **Who thinks changing the URL structure of an API at one's leisure is a good or useful thing?**
There are so many things wrong with this that I can't even begin to imagine how people say it with a straight face.

Suppose GitHub, who generally takes their REST API pretty seriously, decided that they were going full HATEOAS. It would
be an announcement that few people actually cared about. After all, *it doesn't affect existing clients at all (yet)*.
Now imagine, many units of time later, GitHub decides that, since they've been full HATEOAS for some time now, clients
should be caught up and they are thus free to change their URL structure. Repositories are no longer located at `https://api.github.com/repos/{owner}/{repo}`, but at `https://api.github.com/crazy-town/why-would-we-do-this/resource/{repo}`. That's a totally valid thing to do in HATEOAS world. After all, clients _are_ hitting `https://api.github.com`, parsing all the entities, resolving their semantic meaning, and following the URL pattern in case it changed, right?

**Then the Internet breaks.**

Changing the URL structure of a public API is a bad idea for so many obvious reasons. Heck, [even the W3C is with me on this one](https://www.w3.org/Provider/Style/URI.html). They have a whole page devoted to why this is a stupid idea! And they're right!

So, yeah, the ability to restructure your API's URLs is not exactly a benefit. It does, however, lead to a significant
problem (which I'll discuss later).
