title: Linkrdr Rises From the Ashes
date: 2012-12-10 17:14
categories: python linkrdr django

In the beginning of 2012, I developed a site called Linkrdr. It was designed to be "the next generation RSS reader." Instead of simply listing each item in your RSS feeds in chronological order, it would: scan their content, extract links it found, then intelligently rank all of the links from all new entries and display them accordingly. 

The idea was, if I subscribe to TNW and TechCrunch and they both have a writeup of the same story, I'd rather see the link they're talking about than two entries from secondary sources. As you interacted with it, Linkrdr learned your preferences and factored them in to its rankings. The result: a personalized list of interesting links, with some traditional RSS reader functionality to boot.

The system worked, but faced some scaling challenges. Users could import their feeds from other sources, and some had hundreds of feeds they followed. This meant the content retrieval and analysis process had a ton of work to do, even for a relatively small number of users.

But the main issue was I was solving a problem that didn't exist for very many people. Those that understood it and had a large number of feeds found it really helpful. Most, however, didn't get it and weren't particularly unhappy with the way they consumed RSS feeds. It solved a problem they didn't have.

So Linkrdr wilted due to lack of development. I could see the writing on the wall and, rather than pour even more effort into something not many people wanted, I shut it down. It wasn't a total loss, though. I learned a great deal about developing data and computation intensive web applications. More importantly, I learned how *not* to build a useful web application.

Linkrdr was born from my frustration with finding good technical content to read. Each day, I read twenty or more articles, blog posts, white papers, etc. I can't help it, I genuinely love software development and technology. My current workflow is to find content using Zite, then save each interesting looking article to Pocket (aka ReadItLater) to read offline. I spend a tremendous amount of time in those two applications.

But the setup is not ideal. For one, I need to use two different applications for one task, neither of which is optimized for what I do. Here are the pros and cons of each application as they apply directly to me:

**Zite** 

* Pros
    1. Decent content discovery
* Cons
    1. No offline reading
    1. Impossible to tell why a specific story is presented to you
    1. No history of viewed pages (impossible to find article you read a month ago)
    1. Something as simple as changing phone orientation causes page redownload (really annoying)

**Pocket**

* Pros
    1. Local storage to save articles
    1. Readability-style view
* Cons
    1. Content must be manually pushed from elsewhere
    1. Often chokes on code examples in articles (rendering them basically useless) 
    1. Gets the wrong portion of a page (i.e. a navbar, a comments section) often enough to be annoying

So I decided that Linkrdr would solve my specific problem, and no more. At a minimum, I'll need a server process to collect content and a mobile app to view it. Here's the workflow I came up with:

**Server Process** 

* Each hour, check for new content and save the URLs
* Download the HTML for each new link and run it through a Readability-style processor
* Present a single client facing view of all articles ever downloaded by the user (history)
* Respond to requests from mobile clients for
    * New content
    * Stripped HTML of an article
    * Updates of read/archived articles by user

**Mobile App** 

* Choose from a small, predefined number of technical topics to get content for
* Two basics tasks: Get updated content list and Read saved articles
    * Get updated content list
        * Present URL of each new article in a checklist
        * Download stripped HTML for each article checked
        * Save for offline viewing
    * Read saved articles
        * Present list of articles
        * Clicking article shows article view (stripped HTML) and marks as read

That's it. The entire application. It's exactly what my ideal application would do, but no more. And it's implemented in the simplest way possible: 

* Links are gathered by querying the Twitter search API with simple, hardcoded queries.
* Categories are restricted to a dozen or so software focused keywords
* The mobile app will be for Android (because I own a Galaxy S3) and use PhoneGap as the development platform (because I don't feel like writing Java and most of the functionality is incredibly straightforward).
* The web facing portion will be written in Django because I miss doing Django development. It's also often the source of  blog posts others find helpful. I definitely would have used Flask otherwise.
* The server side process of stripping HTML is hand tuned for technical articles, so code examples are both included and presented in a readable way.

Because of these self-imposed design constraints, the implementation is simple. The server side is already done and took about two days. The mobile portion is progressing nicely. I'm not setting a concrete date for it to be ready, but "soon" is a good approximation.

So, if you have the exact same issue as me with finding and consuming technology focused content offline, check back here to see when Linkrdr goes live. If not, well, it's not your problem I'm solving. It's mine.