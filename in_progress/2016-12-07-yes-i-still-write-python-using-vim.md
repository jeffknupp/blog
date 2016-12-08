title: Yes, I Still Write Python Using VIM
date: 2016-12-07 19:42
categories: python vim

I admit it: I am of the old guard. I cut my teeth on C++ systems (originally running on Solaris) in Finance. To date, there has never been a usable IDE for C++ (prove me wrong :) ). Moreover, one couldn't rely on SublimeText or its ilk to be installed on 8-year behind Linux distro dejur, so I had to learn *some* way to edit files. I chose vIM. Learning it was hard. Almost comically so. But after 15+ years of sustained use, *I've never looked back.*

Of course, **Python** has a *any number* of workable IDEs ([PyCharm](https://www.jetbrains.com/pycharm/) being the best, IMHO), so I needn't stay in the dark ages when writing Python. Surely the whiz-bang features of modern IDEs more than make up for sheer editing speed and manuverability, right?

** Erm, no...**

VIM (and it's spiritual sucessor-cum-rewrite [neovim](https://neovim.io/)) are not only *adequate* for day-to-day Python work, *they are superior.* I know you don't believe me.

*You will.*

<!--more-->

## Many Will Try To Sell You VIM As An IDE...

Do not listen to them. VIM has/can be extended to include several IDE-like features (code completion, inline documentation, etc) but excels when it's running with exactly what is *really useful* and no more. It is, at its heart, a minimalist editor. That's why every Linux distro people actually use has VIM installed by default. Emacs is almost always nowhere to be seen... (<sarcasm>because it's a 400mb binary</sarcasm>).

So let's not go the "throw every possible plugin at VIM and feature compare to other IDEs" route. Instead, let's focus on what one needs to actually write code using a program that will not use more RAM than Chrome + Photoshop.

## THIS IS MY .VIMRC! THERE ARE MANY LIKE IT BUT THIS ONE IS MINE...

Your `.vimrc` file (typically located in `$HOME/.vimrc`) is intensely personal. It contains all the settings and tweaks you've accumulated for VIM usage over the years. Some have a well structured `.vimrc` file. Others have a giant ball of garbage. [My `.vimrc` file](https://github.com/jeffknupp/dotfiles/blob/master/.vimrc) falls somewhere closer to the former, with a bit of the latter tacked on the end. The important thing to realize is that VIM is *really, really customizable.* Almost every key binding can be rewritten. You can create easy shortcuts for doing insanely complicated things (not complicated, but one of my favorite personal shortcuts is the following, which forces the current file to be written using `sudo` even if we didn't open the file using `sudo vim <filename>`): 

```
" sudo write this
cmap W! w !sudo tee % >/dev/null
```

You can see from that sample that the `.vimrc` format support comments. You can also see it's almost totally inscrutable to beginners. VIM has a learning curve. It doesn't apologize for that (or, at least, I don't...) But what you pay for up front in awkward, frustrated editing you make back tenfold in pure VIM nirvana. Give it six months or so to really sink in. No, that's not a typo...

Anyway, your `.vimrc` file can be blank aside from some boilerplate necessary to set up your plugins.

## Did You Say "Plugin"?

Yep, "plugin". Plugins (and, more accurately, a *plugin manager*) are the key to keeping VIM both sane and extensible. Before we get there, though, let's talk about VIM's configuration file: `.vimrc`.



While things are changing a bit for neovim, the best plugin manager for VIM is [Vundle.vim](https://github.com/VundleVim/Vundle.vim). For the SAT crowd out there - Vundle:VIM::pip:Python. 
