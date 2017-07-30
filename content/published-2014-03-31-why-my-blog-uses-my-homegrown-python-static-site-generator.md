# Why My Blog Uses My Home-grown Python Static Site Generator

Recently, I've seen a number of nice-looking blogging platforms pop up. Each
basically let's you write your content in Markdown, shows you a live preview,
and can keep posts unpublished until you're ready to bestow them upon the world.
They all look nifty, but I'll never use them. 

Why? I've been using [blug](http://www.github.com/jeffknupp/blug), my Python-based static blog generator, to generate 
this site for years. *blug* was designed with a certain workflow in mind (mine)
and has grown since then. I have a private fork of the public `blug` repo where I
have all my settings and special templates. That repo is the one that sees the
most love (and I'm *long* overdue for a sync between the private code and the
public). But more importantly than `blug` being tuned for how I work, `blug` gives
me something other blogging platforms don't: **control**.
<!--more-->
If I were to try and replace `blug`, I'd basically have two options: static site
generators and blogging platforms. The former are attractive because I have more
control over the infrastructure of the blog. The latter are attractive because
they offer a turn-key solution to something I've had to write my own tool for.
Ultimately, neither solution is palatable.

I know of static site generators like [Jekyll](http://jekyllrb.com/),
[Octopress](http://octopress.org/), and [Pelican](http://blog.getpelican.com/).
In fact this blog used to be generated via Octopress until I grew tired of my
blog looking identical to every other tech blog out there. Octopress felt
bloated, had no real community, and development ground to a halt. Jekyll felt
too heavyweight, as it's built to accommodate any kind of site (and I'm just
building a blog). Pelican didn't offer anything compelling and had minimal
theming support.

Online blogging platforms lack two key features: offline editing and analytics
integration. If I am drawn to a platform because it has a nice workflow, but
that workflow only works with an Internet connection, it's a non-starter.
Analytics, I've found, are hugely important to budding blogs, especially if said
blog sells something [like mine does](https://www.jeffknupp.com/writing-idiomatic-python-ebook).
Not being able to change the HTML on a whim after signing up for a service like
Optimizely was too restrictive.

Especially when I decided to focus on embedding microdata in my site (look at
the source, it's there!), it became clear that what I really wanted was *control*.
And `blug` gives me that control. It generates a site containing the features that
are important to me: microdata, archives, little JavaScript, an atom.xml, and
that's about it. My blog "builds" in about a second and updating after a new
post is a one-command affair.

Most importantly, I *am* able to change the HTML whenever I want. Static site
generators allow this, for the most part, but you have to strip a lot away to
get at the core functionality. When you *do* that, you're left with something
like [blug](http://www.github.com/jeffknupp/blug).

`blug` is written in Python and aimed at Python 3. I knew I wanted my generator to
be Python 3-based, if only because so little *else* was at the time. It has a
very straightforward interface: you can create a new post, generate the site, or
serve it locally. That's it. 

When creating a new post, it slugifies the title
with nice looking URLs, adds the Markdown front matter that contain things like
the title, date, and categories, and puts it in the directory it uses as a
source for posts when generation occurs. In my setup, this is just a symlink to
the `content` directory of my `blog` repo. That means after creating a new post,
I open it, write what I want, commit and push to `GitHub`, and that's about it.
"Deployment" involves deleting my existing blog directory, generating the site
fresh, and copying the results back in place. 

It may seem quaint or pedestrian, but that's really it. While I'm glad I created `blug`,
I wouldn't really recommend it to others. Why? Static site generators are so easy to
write you can do so in an evening, so why not roll your own? You'll end up with
a tool that supports *your* workflow and retain full control over how your site
is structured. Also, static blogs can be used as an awesome introduction to
self-hosting.

Generating my blog with `blug` has been a journey, and I've been forced to learn
a lot on the way. I'm glad I did, however, because now I *always* have the site I want.
And whenever "the site I want" changes, `blug` is happy to oblige.
