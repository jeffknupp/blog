title: Creating and Optimizing a Letterpress Cheating Program in Python
date: 2013-01-04 16:17
categories: python optimization idiomatic

I first discovered the iOS game [Letterpress](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&ved=0CDQQFjAA&url=https%3A%2F%2Fitunes.apple.com%2Fus%2Fapp%2Fletterpress-word-game%2Fid526619424%3Fmt%3D8&ei=GkfnUIeQIong0gHdxIC4Cg&usg=AFQjCNHyT3bdcIUDWZdtFQdbeGEFV62jcA&sig2=ChzpCnxYsMKS-GPcdkN7WQ&bvm=bv.1355534169,d.dmQ) while reading Marco Arment's *The Magazine* (*Letterdepressed*, Josh Centers, Issue 5). 
I installed it immediately after finishing the article and was instantly hooked.
It's a compelling mix of strategy and vocabulary demonstration. Easier to learn
and quicker to play than Scrabble, while still providing a means for Liberal
Arts majors to demonstrate superiority over their gainfully employed peers, if
only for a few minutes. 

A few days ago, I needed a distraction from finishing my
[upcoming book](http://www.jeffknupp.com/blog/2012/10/18/writing-a-python-book-in-python/). 
Writing a Python based Letterpress "assistant" *cough* seemed like a fun diversion. 
I started with code originally written for Scrabble, but it was *painfully*
slow. In this post, I'll show how I optimized and refactored the original code
to the point that it's actually useful for Letterpress.

<!--more-->

I didn't want to start from scratch, so I Googled for a Scrabble solver
(figuring it was a close approximation) and basically took the first result I
saw. It turned out to be an [answer on StackOverflow](http://stackoverflow.com/questions/5485654/how-can-this-python-scrabble-word-finder-be-made-faster)
to a question about optimizing a Scrabble solver. The approach was similar to
what I had in mind (use Linux's words file to build up data structure suitable
for searching for words, etc.).

The code is in two parts. The first script (which only needs to be run
once) takes words using the `words` file found on most Linux machines at 
`/usr/share/dict/words` (on Arch I had to install the `words` package). First
we'll take a look at the original code:

    #!py
    f = open('/usr/share/dict/words')
    d = {}
    lets = set('abcdefghijklmnopqrstuvwxyz\n')
    for word in f:
    if len(set(word) - lets) == 0 and len(word) > 2 and len(word) < 9:
        word = word.strip()
        key = ''.join(sorted(word))
        if key in d:
            d[key].append(word)
        else:
            d[key] = [word]
    f.close()
    anadict = [' '.join([key]+value) for key, value in d.iteritems()]
    anadict.sort()
    f = open('anadict.txt','w')
    f.write('\n'.join(anadict))
    f.close()

Straightforward enough. It creates a trie-like dictionary of words were the key
is a sorted series of letters and the value is a list of all the words that can
be made using exactly those letters. Here's the version I ended up with:

    #!py
    import collections

    with open('/usr/share/dict/words') as file_handle:
        words = collections.defaultdict(list)
        letters = set('abcdefghijklmnopqrstuvwxyz\n')
        for word in file_handle:
            if len(set(word) - letters) == 0 and len(word) > 2 and len(word) < 20:
                word = word.strip()
                key = ''.join(sorted(word))
                words[key].append(word)

    anagram_dictionary = sorted([' '.join([key] + value) for key, value in words.items()])
    with open('anadict.txt', 'w') as file_handle:
        file_handle.write('\n'.join(anagram_dictionary))

The differences? The new version uses context managers for handling file access.
It also uses `collections.defaultdict` to avoid the need for the if statement in
the inner loop. The last change uses the built in function `sorted` directly on
the list comprehension. 

You might be asking yourself "Why change it at all? None of the 
functionality changed?". Three reasons. First, I'm making the code available on
GitHub and using it as a teaching aid, so I want it to be written in idiomatic
Python. Second, it's easier to read and comprehend than the first version, so
it better suits my goals. Lastly, it's a habit that I've forced myself into over
the years. No matter how short or trivial the code, write it in a 
straightforward, idiomatic way. The goal is for it to become automatic, so 
you never want to kick your own ass for writing a module that leaked file 
descriptors like they were going out of style because you were too lazy 
to use a context manager.

Rant over. Back to the code.

The second block of code is the real meaty part: it uses the word list produced
by the script above to find all possible words that can be made from whatever
you give it. The original version is below (I've removed a few Scrabble specific 
portions and a bit related to calculating run time). 

    #!py
    from bisect import bisect_left
    from itertools import combinations
    from time import time

    def loadvars():
    f = open('anadict.txt','r')
    anadict = f.read().split('\n')
    f.close()
    return anadict

    def findwords(rack, anadict):
        rack = ''.join(sorted(rack))
        foundwords = []
        for i in xrange(2,len(rack)+1):
            for comb in combinations(rack,i):
            ana = ''.join(comb)
            j = bisect_left(anadict, ana)
            if j == len(anadict):
                continue
            words = anadict[j].split()
            if words[0] == ana:
                foundwords.extend(words[1:])
        return foundwords

    if __name__ == "__main__":
        import sys
        rack = sys.argv[1].strip()
        anadict = loadvars()
        foundwords = set(findwords(rack, anadict))
        print(len(foundwords))

(I added the last line as a crude correctness test: we should still find
the same number of words after any changes we make.) 

Now that we've gotten our stolen Internet code all set up, let's see how she
runs:

    #!bash
    time python2.7 presser_old.py asdwti
    43
    python2.7 presser_old.py asdwti  0.03s user 0.01s system 96% cpu 0.038 total    

Not bad! For a six letter string, it found all 43 possible words that can be
made from our dictionary. But wait. A Letterpress board has 25 letters, all of
which can be used at any time. We'll need to test it on a 25 letter string to
see if it's suitable for our purposes.

    #!bash
    time python2.7 presser_old.py asdwtribnowplfglewhqagnbe
    **Jeff goes to get a cup of coffee...**
    **Jeff drinks the cup of coffee...**
    **Jeff stares impatiently at screen...**
    8594
    python2.7 presser_old.py asdwtribnowplfglewhqagnbe  52.48s user 0.01s system 99% cpu 52.578 total

OK, so it takes a bit longer for a Letterpress board. Can we make it faster than
a minute? 


**No. End of blog post.**


Alright, fine, we'll try. Let's see if we can understand what the code is doing. `loadvars`
just loads the dictionary file we created as one big list. Each element in the
list is a series of strings: a sequence of letters in sorted order, followed by
all of the words you can make with those letters. So far, so good.

`findwords` takes the string we entered on the command line and does some weird
loop over it. Well, not too weird. The two `for` loops effectively loop over successively
longer sub-sequences of our sorted string (the `rack`). It basically says,
"Let's find all the two letter words we can make. Now all the three letter
words. Now the four...". It does so by using the `itertools.combinations`
function to get all possible combinations of each subset of our `rack`.

In the inner loop, it uses `bisect.bisect_left` to determine if the current
subset of letters exists in the anagram dictionary. Since the anagram dictionary is a sorted
list, `bisect_left` gives us the position in the anagram dictionary
that we would insert our current sub-sequence. Everything before it is "less" than it (in alphabetical order).
Everything after is greater than *or equal to* it. If our current sub-sequence
has a match in the anagram dictionary, it has to be at the position
`bisect_left` returns. Clever.

Now that we understand the algorithm, how do we make it faster? First, we
profile to see where time is being taken. Let's use a somewhat shorter string so
I can finish this post before March.

    #!bash
    ~/c/presser >>> python2.7 -m cProfile presser_old.py asdwtribnowplf
    1115
            66453 function calls in 0.043 seconds

    Ordered by: standard name

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.000    0.000 bisect.py:1(<module>)
         1    0.000    0.000    0.043    0.043 presser_old.py:1(<module>)
         1    0.017    0.017    0.036    0.036 presser_old.py:13(findwords)
         1    0.000    0.000    0.007    0.007 presser_old.py:4(loadvars)
     16369    0.010    0.000    0.010    0.000 {_bisect.bisect_left}
     16372    0.001    0.000    0.001    0.000 {len}
         1    0.000    0.000    0.000    0.000 {method 'close' of 'file' objects}
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
       962    0.000    0.000    0.000    0.000 {method 'extend' of 'list' objects}
     16370    0.003    0.000    0.003    0.000 {method 'join' of 'str' objects}
         1    0.001    0.001    0.001    0.001 {method 'read' of 'file' objects}
     16370    0.010    0.000    0.010    0.000 {method 'split' of 'str' objects}
         1    0.000    0.000    0.000    0.000 {method 'strip' of 'str' objects}
         1    0.000    0.000    0.000    0.000 {open}
         1    0.000    0.000    0.000    0.000 {sorted}


We see the two most costly functions are `split` and `bisect_left`. This is
pretty intuitive. `split` has to create a bunch of new string objects, meaning
memory allocation, meaning slow. `bisect_left`, if we think back to CS101, is at
best O(log n) since it's doing a search on a sorted list (the implementation of
`bisect_left` is a simple binary search). So what do we do to make this faster?

Stop calling `split` and `bisect_left`! That's only a half-joke. If we could do
the same work without those two calls, the battle would be won. Let's take them
one at a time.

Why do we need `split`? Because our anagram dictionary is a list of space
separated strings, and we need to extract the key (first string) and values (all
the rest of the strings). Similarly, we need `bisect_left` because we're
operating on a sorted list. O(log n) is about the best we're gonna do.

So we need to change the data structure used to store our anagram dictionary. It
needs to allow us to access our "key" string and "value" strings quickly. It
also needs constant time look up.

Now is when you guess what data structure we use. Here's a hint: I've been
referring to the list of anagrams as the "anagram dictionary"...

A dictionary! How novel! Using a dictionary obviates the need for both of the
costly function calls. Here's the code after our changes (and a bit of cleanup):

    #!py
    from itertools import combinations
    import collections

    def load_anagrams():
        anagrams = collections.defaultdict(list)
        with open('anadict.txt', 'r') as file_handle:
            for line in file_handle:
                words = line.split()
                anagrams[words[0]] = words[1:]
        return anagrams


    def find_words(board, anagrams):
        board = ''.join(sorted(board))
        target_words = []
        for word_length in range(2, len(board) + 1):
            for combination in combinations(board, word_length):
                anagram = ''.join(combination)
                if anagram in anagrams:
                    target_words += anagrams[anagram]
        return target_words

    if __name__ == "__main__":
        import sys
        if len(sys.argv) == 2:
            rack = sys.argv[1].strip()
        else:
            exit()
        anagrams = load_anagrams()
        target_words = set(find_words(rack, anagrams))
        print(len(target_words)) 


Let's see if it made a difference...

    #!bash
    ~/c/presser >>> time python2.7 presser_new.py asdwtribnowplfglewhqagnbe
    8594
    python2.7 presser_new.py asdwtribnowplfglewhqagnbe  15.22s user 0.04s system 99% cpu 15.282 total


Down from 52 seconds to 15. Not bad. But I think we can do better... Let's
profile again.


    #!bash
    ~/c/presser >>> python2.7 -m cProfile presser_new.py asdwtribnowplf
    1115
         87762 function calls in 0.078 seconds

        Ordered by: standard name

        ncalls  tottime  percall  cumtime  percall filename:lineno(function)
             1    0.000    0.000    0.000    0.000 bisect.py:1(<module>)
             1    0.000    0.000    0.001    0.001 collections.py:1(<module>)
             1    0.000    0.000    0.000    0.000 collections.py:25(OrderedDict)
             1    0.000    0.000    0.000    0.000 collections.py:356(Counter)
             1    0.000    0.000    0.000    0.000 heapq.py:31(<module>)
             1    0.000    0.000    0.000    0.000 keyword.py:11(<module>)
             1    0.001    0.001    0.078    0.078 presser_new.py:1(<module>)
             1    0.006    0.006    0.008    0.008 presser_new.py:17(find_words)
             1    0.042    0.042    0.069    0.069 presser_new.py:4(load_anagrams)
             3    0.000    0.000    0.000    0.000 {len}
             1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
         16370    0.003    0.000    0.003    0.000 {method 'join' of 'str' objects}
         71375    0.027    0.000    0.027    0.000 {method 'split' of 'str' objects}
             1    0.000    0.000    0.000    0.000 {method 'strip' of 'str' objects}
             1    0.000    0.000    0.000    0.000 {open}
             1    0.000    0.000    0.000    0.000 {range}
             1    0.000    0.000    0.000    0.000 {sorted}


`join`, `split`'s sneaky cousin dominates the execution time. Note that `split` is there
due to its use in `load_anagrams`, not the `find_words` function. I'm fine with
that since it's a flat cost (and note that the string I used for profiling was
only 14 characters long, so `split` will use comparatively less time on the full
25 character board). How do we make this faster still?

Stop calling `join`!

We only need it because `combinations` returns a `tuple` and the keys for
`anagrams` are strings. Let's change that. Here is the new version of the two
relevant functions: 


    #!py
    def load_anagrams():
    anagrams = collections.defaultdict(list)
    with open('anadict.txt', 'r') as file_handle:
        for line in file_handle:
            words = line.split()
            anagrams[tuple(words[0])] = words[1:]
    return anagrams


    def find_words(board, anagrams, max_length=25):
        board = ''.join(sorted(board))
        target_words = []
        for word_length in range(2, len(board) + 1):
            for combination in combinations(board, word_length):
                if combination in anagrams:
                    target_words += anagrams[combination]
        return target_words


Lean and mean. Let's see what the judges say...


    #!bash
    ~/c/presser >>> python2.7 -m cProfile presser_new.py asdwtribnowplf
    time python2.7 presser_new.py asdwtribnowplfglewhqagnbe
    8594
    python2.7 presser_new.py asdwtribnowplfglewhqagnbe  7.13s user 0.02s system 99% cpu 7.166 total


Down from 52 seconds to 15 to 7. I think the search portion of my Letterpress
solver is usable now. You can find the code for *presser*, the name of this
little gem, [on GitHub](https://github.com/jeffknupp/presser). Note that while
the word finding portion is done, the optimal move evaluation is still a work in
progress.

If you found this post useful, you may be interested in my upcoming ebook
[Writing Idiomatic Python](http://www.jeffknupp.com/blog/2012/10/18/writing-a-python-book-in-python/). 
It's nearly complete, and preorder copies should be available by January 15th.
Sign up for the email list to get an email when it's released.
