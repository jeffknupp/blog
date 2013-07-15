title: Simple Spam Filtering in Python
date: 2013-07-15 09:48
categories: python tutorial

Recently, one of my tutoring clients asked to do a project in machine learning. 
Machine learning is a topic I would normally stay away from with a client; even 
if we arrive at a completed, working program, understanding *why* it's
working in the first place requires background knowledge. Luckily, we were able
to choose a project of appropriate size, difficulty, and prerequisite knowledge:
a naive Bayesian spam filter.

## Here Comes the Math

Before we begin the project, we need a bit of background in statistics
(if you already have a basic grasp on Bayesian inference, feel free to skip this
section). Our goal is for the spam filter to classify an email as either "ham" or "spam".
How do we get a stupid Python script to detect spam email? 

It takes two steps.

#### The Learn Phase

The first step is called the "learn phase". In it, we feed the program email for 
which we already know the classification (i.e. "Here's a spam email I got
before. Here's one that's not spam ("ham"). Here's another spam." etc.). The
program will take note of various properties of the email (which we'll discuss
in a bit). It record this data for every email we feed to it, building up a sort
of database of spam/ham email properties.

In the second phase, the program will use this refer back to this data
to determine the *most likely* classification of an unknown email. That is, it
uses what it has "learned" on a new, previously unseen email message.


To begin, we'll record a very simple set of properties: the frequency of words that appear in
the body of the email. At a high level, we'll be using two dictionary-like
structures: one with the word frequencies for known-spam email an identical one
for known-ham email. We'll also keep track of how many messages of each type
we've seen (you'll see why in a minute). 

## Classification

The classification of an unknown email is then relatively
straightforward to determine: 

* Keep a "spam score" and a "ham score", both starting at `0`
* For each word in the email, if it appears in the spam dictionary, add the
overall number of times that word has been seen to the spam score
* Do the same for the ham dictionary and score
* Calculate "relative scores"
* Choose the largest score as the most likely classification

We calculate "relative" scores to even the playingfield between our two data sets. 
For example, we may have seen the word "vacation" 8 times in ham
email and only 3 times in spam email. This suggests that an email with the word
"vaction" is likely to be ham. However, if we saw 200 ham emails and only
10 spam emails during the learn phase, those numbers take on quite a different meaning.
It becomes *much* more likely that an email containing "vacation" is spam, 
since 30% of the spam we saw had this word while only 4% of the ham email did. 

To account for this, we'll give each word a relative score
equal to the frequency in each class of email divided by the number of messages
seen in the learn phase for that class. In our example, those values would be `.3`
for spam and `.04` for ham.

## Finally, Some Code

Before we start writing any code, let's break down each task we know the program
will need to perform:

* During "learning"
    * Parse an email
    * Record salient properties of the parsed message
    * Add those properties to a persistent data store
* During "classification"
    * Parse an email
    * Load classification data from the data store
    * Compare the unkown email's properties to those of already-classified email
    * Decide the most likely classification

That seems like a reasonably comprehensive list. If our program can perform the
last step, it's essentially a spam filter.

Let's begin with the functionality required during the learn phase. Though the
program could be written as a series of !!!CHECK ME!!! unbound functions,
creating a class responsible for managing our interaction with email messages
"feels" right (especially considering the different ways we could extend this
later). Let's start with a generic skeleton for the script. 

Helpfully, I have a simple shell script to generate this skeleton for a new 
Python file. I recommend this practice to avoid writing scripts the correct way
because writing the boiler-plate code "takes too long".

    #!py
    """Simple naive-bayes spam filter"""

    import sys

    def main():
        """Main entry point when called as script"""
        pass

    if __name__ == '__main__':
        sys.exit(main())

Of course, we'll likely need to alter this skeleton code, but it's a good start.
Next let's write an outline for the class. The way I typically write *any* large
portion of a program is to write the definition *and docstrings* of functions
and classes I need. Writing the docstring before you implement the function is a
gut-check to make sure you fully understand what a function will do. If you
can't write the docstring, it's an early sign that you may need to rethink the
structure of your program. Of course, we're not handcuffed to the choices we
make now, but I find it to be a helpful way to organize my thoughts.

Here is the class definition skeleton:
