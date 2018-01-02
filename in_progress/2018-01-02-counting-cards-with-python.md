title: Counting Cards With Python
date: 2018-01-02 11:26
categories: python cli blackjack

Having grown up about 20 minutes from Atlantic City, I'm no stranger to casinos. When I was younger (but over 21! *cough*) I learned to count cards, a tool used by Blackjack players to help them gain a statistical edge over the casino and thus, in a perfect world, win money over the long term. It appealed to me mainly for the allure of beating the casino at its own game (literally). While every other game in the casino has a negative expected value over the long term, the card counter really can beat the house (I'll outline card counting in more detail below).

Something just happened in New Jersey that rekindled my interest in counting: a casino offering Blackjack *with live dealers* online.
<!--more-->
New Jersey recently legalized online gambling for New Jersey residents. This typically included slots, Poker, and "table games" like Blackjack and Roulette and all the casinos were quick to offer online versions of the live experience. The Blackjack games were always fully computerized, though, and never simulated using actual decks that would need to be shuffled periodically. They were more like slot machines in the sense that the odds were fixed and there was no way to affect them.

**Live dealers**, though, change everything. I was skeptical at first of how it would work, but I can honestly say they've done a pretty great job of offerring exactly what they promise: A live game of Blackjack with real dealers, cards, and tables where one simply inputs their moves via the computer. It's as if you could go down to Atlantic City, put a laptop down at one of the seats of a Blackjack table, then drive home and use FaceTime to see the game and instruct whether to Hit, Stand, Split, or Double Down. And you're free to chat with the dealer and other players as well.

The key point to the description above is that all of the action is taking place at the casino (which you can see and hear), *but the casino can no longer see or hear you*. Many of the realities that make counting difficult in practice vanish when the casino has no idea what you're doing other than making bets or playing the game. I can play in my underwear listening to bagpipes. I can waste time on Twitter while the hand is being dealt (cell phones are a big no-no at Blackjack tables). In fact, *I can run a computer program that counts cards and tells me what to do* all while playing "online".

That was compelling enough for me to write a simple counting program in Python, put it to use in a live game, and see what happened. The results have been good so far, but with a few caveats. Before we get into the code and results, lets discuss what "counting cards" really means.

## Even YOU Can Count Cards!

Counting cards sounds easy. The basic premise (which I may or may not include mathematical proofs to, depending on how long this goes) is that when there are a high concentration of Aces, Tens, Jacks, Queens, and Kings the player is more likely to be dealth a blackjack (which pays 3:2, or 150% of the bet) and those same cards make it more likely for the dealer to bust. Remember, the dealer can't stand whenever he or she wants; the dealer *must* hit until they reach 17, so lots of high-value cards means a higher chance of busting. Conversely, when there is a high concentration of Twos, Threes, Fours, Fives, and Sixes, there is both a reduced chance of a blackjack for the player and an increased likelihood that the dealer *won't* bust. The remaining cards are about equally as helpful to the player and the dealer and are simply ignored.

The most popular counting scheme, High-Low, just requires the player to add one when a low (2-6) card is dealt and subtract one when a high-value card is dealt (AJQK10). If I am dealt a 10 and a 6 and the dealer shows a King, the count is -1: -1 for the 10, +1 for the 6, and -1 for the King. Simply repeat this for all the cards as they're dealt and, congratulations, you're counting cards. Of course, just knowing the concentration of certain cards doesn't help if we don't act on the information, so the key remaining piece is to *increase the size of your bet* when the count is high and reduce it when the count is low. That's really about it.

## No, You Probably Can't

Of course, if it were easy everyone would do it. There are a number of practical problems with counting cards. The first is it takes a significant amount of concentration (it takes a long while before this becomes natural). That includes being able to carry on conversations and ignore distractions while at the same time not appearing to be concentrating at all.

It also requires playing *perfect* Blackjack. Counting is absolutely useless unless one is already playing statistically perfect Blackjack. This is actually easier than it sounds, as there are dozens of sites online that have what are called "basic strategy" charts that describe what action to take in every possible situation. In fact, you can print this out and sit with it in front of you, directly referencing it while you play. The casino doesn't care. Even when the player is playing "perfectly" the casino still enjoys a stastical edge.

Probably most difficult is controlling one's emotions and, yes, boredom. Getting over the shock of losing big hands you "should have" won, stomaching the natural swings in your bankroll, and sitting for hours straight doing the same thing over and over again (perfectly) are all truly difficult. Letting any of them affect your play likely means you'll erase the slight edge that counting provides. It is a grind, and sometimes it feels like doing arithmetic during a hurricaine, with the rest of the casino goings on swirling behind you.
