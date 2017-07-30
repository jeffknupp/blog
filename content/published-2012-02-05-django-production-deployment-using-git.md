# Django Production Deployment and Development Using Git


When I started [IllestRhyme](http://www.illestrhyme.com), I had never before managed a web application. Much was similar to enterprise development. Much wasn't. One of the things I had no idea about was how to manage production deployment of a web app. I settled on some common Django trickery and Git, and it has worked like a charm.

<!--more-->
I knew going in that I would use Git for source control. I wanted a distributed version control system to give me an opportunity to work anywhere git was installed. I didn't suspect I would use git for deployment, also. 

When the site began, I didn't even have a "deployment" strategy. There were so few visitors to the site that I could work on it live. Within two weeks, it was clear I couldn't be showing users HTML 500 errors as frequently as I had been. I needed to start acting like I was working on a "real" project.

(Re)Enter Git. <!-- more -->I would have a few mis-starts before I settled on a safe, productive way to work. Initially, I created a new directory on my machine for development. I cloned my git repository and created a dev branch. The dev branch had the same settings.py file as the master branch, and I was editing this manually as I switched between the dev and master branches. I knew this was a dangerous practice, and this proved true when I hosed the production database because of a bad settings file. Good thing I had DB backups... 

There had to be a better way. I decided that, since the Django settings.py file was just Python, I would create a `localsettings.py` file that the settings.py file would import. For development, this would point to the development database and settings. For production, the production settings. This file is imported by the settings.py file and is not tracked by git (there's an entry for it in the .gitignore file).

Now I was free to work on my dev branch without worrying about messing up production. When I was happy with a change, it was merged with the master branch and pushed to bitbucket. Then the production area pulled down the changes and Apache was restarted. Perfect.

Something that took a bit to get used to using git was branching. In enterprise development with CVS or SVN, branches are more substantial "things" then personal development with git. A branch in git can both be created and deleted quickly. I frequently have five or six active branches of development for [IllestRhyme](http://www.illestrhyme.com): some for large sweeping changes that require database migrations, some just adding a few new pages/views to the site, some as small as correcting typos or adding a link or two. 

Where git really shines is in switching between active branches. I can be working on a branch with 70 new files, say `git checkout <somesmallbranch>`, and everything is exactly as it should be, with the added files removed and the changes merged back to my small change branch. This allows me to work almost in real-time. If I'm deep in a change but get alerted to an error via email, I can quickly switch to my main dev branch, make a change, test it, commit it and pull it down in mere minutes.

Git has opened up a new world for me in terms of productivity. It's been so useful on IllestRhyme that I've begun to use it at my day job as an "out-of-band" VCS. I checkout with our enterprise VCS, do a quick `git add .` to my personal git repository, and branch/commit/merge to my heart's content. When I'm happy with my changes, I commit to my enterprise VCS, which has been instructed to ignore my .git directory. 
