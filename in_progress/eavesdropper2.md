## Extending Eavesdropper

The [original eavesdropper](http://foo.com) server was quite simple: it queried
Twitter for recent tweets on a subject, saved the results to a database, and
created a straightforward visualization of the results. In this article, I add
three search engines to the list of sources, greatly increasing the utility of
the tool. I'll describe how I used [scrapy](http://www.scrapy.org) and Amazon's
S3 to programatically query Google, Google Blog Search, and Bing for occurrences of a
certain term (my name).
<!--more-->

### My Name Is On Twitter, But Where Else?

Twitter was the obvious choice for the single source powering the first cut of the
system. After Twitter, though, the choice was a bit less obvious. My first
inclination was actually to build a web crawler which would start at any
known mention of my name and use that page as the root from which to crawl.

The obvious drawbacks are network utilization (we need to fetch a lot of pages),
speed, and thoroughness. Instead, I decided, I would let search engines due what
they do best and query *them* for pages in which my name appears. After all, if
Google isn't aware of a certain page with my name on it, it's unlikely to help
my appearence in search results. 

#### Everything Has APIs These Days

Everything aside from search engines, that is. The reason is obvious: if they had a free 
REST API, you could effectively clone that search engine and add your own
advertising. While advertising drives their revenue, search is their secret
sauce.

Except Google *did* have a Web Search API (and Bing currently has one). It is
rate limited (to prevent the situation mentioned above) and deprecated, but it
still exists and works. Given this fact, "scraping" Google search reults for my search
term became much more straightforward.

I decided to use [scrapy]](http://www.scrapy.org) as the engine for my
application. Though likely overkill at the moment, using scrapy will allow me to
eventually add a crawler as an additional source of mentions. Scrapy has two
main functions: web crawling and web scraping. It also includes mechanisms to
persist the results in a variety of formats and locations. 

For this project (again because I'd never used it and wanted an excuse 
to do so), I chose to save the results of the "scraping" to S3. This choice is
practical because we want to store the results in a central location. That
allows us to separate the crawling portion of the project from the web
interface. Interfacing with *any* Amazon web service can/should be done with
[boto](http://FIXME). It's a handy tool if you're ever writing Python code that
needs to interact with an Amazon web service.

###
