title: Setting Up Octopress/Jekyll with Apache
date: 2012-02-02 02:06
categories: apache octopress jekyll git linode illestrhyme

So now that I got my "Hello World" post out of the way, I think it would be instructive to describe the setup process for this blog. Octopress is exactly what I've been looking for: a well styled, static page based blogging engine that doesn't get in my way. The fact that Jekyll (on which Octopress is based) is so closely integrated with git is a definite plus. So how did the install go? First some background.

<!--more-->
I'm the founder of [IllestRhyme.com](http://www.illestrhyme.com), a site where users post rap verses they wrote and other users comment/vote on them. There's a ton of other features, but that's the gist of it. Anyway, I run IllestRhyme on a [Linode](http://www.linode.com/?r=ae1808f234f8e219de24842336fada09ef81d52f) server running Ubuntu. I use Apache for dynamic content and Lighttpd for static content. Since I already have a Linux machine on the Interwebs, I followed the [instructions](http://octopress.org/docs/setup/) on my Linode machine... which is to say I basically copy and pasted the instructions:

    :::bash
    rvm install 1.9.2 && rvm use 1.9.2
    git clone git://github.com/imathis/octopress.git octopress
    cd octopress    # If you use RVM, You'll be asked if you trust the .rvmrc file (say yes).
    gem install bundler`
    bundle install`

Everything went smoothly. Next I needed to make Apache serve both www.jeffknupp.com and www.illestrhyme.com. I created a new file in /etc/apache2/sites-available/ named 'jeffknupp.com' and added the normal VirtualHost settings. After running `sudo a2ensite jeffknupp.com` and reloading apache (`sudo service apache2 reload`), Apache helpfully warned me that I didn't have NameVirtualHost set and nothing was going to be listening on port 80. After quickly adding `NameVirtualHost 50.116.49.236:80` to my apache2.conf file, I reloaded again. I pointed my browser to www.jeffknupp.com and... saw a directory listing of my Octopress install. One quick edit to my jeffknupp.com site configuration and I was good to go. I successfully saw my Hello World post.

So how long did this all take? Maybe 20 minutes, and most of that was installing Ruby. I'm quite happy with the result: I now have a blogging engine "for hackers" that suits my needs perfectly.
