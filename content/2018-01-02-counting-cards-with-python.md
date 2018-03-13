title: Counting Cards With Python
date: 2018-01-02 11:26
categories: python cli blackjack

Having grown up about 20 minutes from Atlantic City, I'm no stranger to casinos. When I was younger (but over 21! *cough*) I learned to count cards, a tool used by Blackjack players to help them gain a statistical edge over the casino and thus, in a perfect world, win money over the long term. It appealed to me mainly for the allure of beating the casino at its own game (literally). While every other game in the casino has a negative expected value over the long term, the card counter really can beat the house (I'll outline card counting in more detail below).

Something just happened in New Jersey that rekindled my interest in counting: a casino offering Blackjack *with live dealers* online.
<!--more-->
New Jersey recently legalized online gambling for New Jersey residents. This typically included slots, Poker, and "table games" like Blackjack and Roulette and all the casinos were quick to offer online versions of the live experience. The Blackjack games were always fully computerized, though, and never simulated using actual decks that would need to be shuffled periodically. They were more like slot machines in the sense that the odds were fixed and there was no way to affect them.

**Live dealers**, though, changes everything. I was skeptical at first of how it would work, but I can honestly say they've done a pretty great job of offering exactly what they promise: A live game of Blackjack with real dealers, cards, and tables where one simply inputs their moves via the computer. It's as if you could go down to Atlantic City, put a laptop down at one of the seats of a Blackjack table, then drive home and use FaceTime to see the game and instruct whether to Hit, Stand, Split, or Double Down. And you're free to chat with the dealer and other players as well.

The key point to the description above is that all of the action is taking place at the casino (which you can see and hear), *but the casino can no longer see or hear you*. Many of the realities that make counting difficult in practice vanish when the casino has no idea what you're doing other than making bets or playing the game. I can play in my underwear listening to bagpipes. I can waste time on Twitter while the hand is being dealt (cell phones are a big no-no at Blackjack tables). In fact, *I can run a computer program that counts cards and tells me what to do* all while playing "online".

That was compelling enough for me to write a simple counting program in Python, put it to use in a live game, and see what happened. The results have been good so far, but with a few caveats. Before we get into the code and results, lets discuss what "counting cards" really means.

## Even YOU Can Count Cards!

Counting cards sounds easy. The basic premise (which I may or may not include mathematical proofs to, depending on how long this goes) is that when there are a high concentration of Aces, Tens, Jacks, Queens, and Kings the player is more likely to be dealt a blackjack (which pays 3:2, or 150% of the bet) and those same cards make it more likely for the dealer to bust. Remember, the dealer can't stand whenever he or she wants; the dealer *must* hit until they reach 17, so lots of high-value cards means a higher chance of busting. Conversely, when there is a high concentration of Twos, Threes, Fours, Fives, and Sixes, there is both a reduced chance of a blackjack for the player and an increased likelihood that the dealer *won't* bust. The remaining cards are about equally as helpful to the player and the dealer and are simply ignored.

The most popular counting scheme, High-Low, just requires the player to add one when a low (2-6) card is dealt and subtract one when a high-value card is dealt (AJQK10). If I am dealt a 10 and a 6 and the dealer shows a King, the count is -1: -1 for the 10, +1 for the 6, and -1 for the King. Simply repeat this for all the cards as they're dealt and, congratulations, you're counting cards. Of course, just knowing the concentration of certain cards doesn't help if we don't act on the information, so the key remaining piece is to *increase the size of your bet* when the count is high and reduce it when the count is low. That's really about it.

## No, You Probably Can't

Of course, if it were easy everyone would do it. There are a number of practical problems with counting cards. The first is it takes a significant amount of concentration (it takes a long while before this becomes natural). That includes being able to carry on conversations and ignore distractions while at the same time not appearing to be concentrating at all.

It also requires playing *perfect* Blackjack. Counting is absolutely useless unless one is already playing statistically perfect Blackjack. This is actually easier than it sounds, as there are dozens of sites online that have what are called "basic strategy" charts that describe what action to take in every possible situation. In fact, you can print this out and sit with it in front of you, directly referencing it while you play. The casino doesn't care. Even when the player is playing "perfectly" the casino still enjoys a statistical edge.

Probably most difficult is controlling one's emotions and, yes, boredom. Getting over the shock of losing big hands you "should have" won, stomaching the natural swings in your bankroll, and sitting for hours straight doing the same thing over and over again (perfectly) are all truly difficult. Letting any of them affect your play likely means you'll erase the slight edge that counting provides. It is a grind, and sometimes it feels like doing arithmetic during a hurricane, with the rest of the casino goings on swirling behind you.

## To The Code!

But remember, we're now playing in an environment where the distractions of the casino fall away and they can't tell what we're doing while we play. Counting is made much simpler. I wrote the following program in about 10 minutes. The idea is simple: allow the user to input the cards as they're being dealt (you can enter more than one card at a time, so I can enter `06K` for the Ten-Six vs. King described earlier and hit enter rather than having to enter each card one-at-a-time.

    #!py
    CARD_VALUES = {
            '2': 1,
            '3': 1,
            '4': 1,
            '5': 1,
            '6': 1,
            '7': 0,
            '8': 0,
            '9': 0,
            '0': -1, # use '0' for 10 to keep everything a single character
            'J': -1,
            'Q': -1,
            'K': -1,
            'A': -1,
            '*': -1, # use '*' as an alias for 'A' to make using the number pad easier
            }

    DECKS = 8

    def main():
        count = 0
        cards = 0
        user_input = True
        decks_played = 0
        while user_input:
            user_input = raw_input('>> ')
            cards += len(user_input)
            for card in user_input:
                count += CARD_VALUES[card.upper()]
            decks_played = cards / 52.0
            true_count = count / (DECKS - decks_played)
            print('Count: {}'.format(count))
            print('True Count: {}'.format(true_count))
        print('Decks played: {}'.format(decks_played))

    if __name__ == '__main__':
        main()

That's it. A few points to go over. You may have noticed the `DECKS` value and the `decks_played` and `true_count` variables. We need these to determine the "true count". The count alone is helpful, but a count of `9` has a much different meaning after a single hand versus one of the last hands in the shoe. The fewer cards there are remaining, the more impactful the count is. The "true count" is simply the current count divided by the number of decks remaining. While at a casino one would have to eyeball the size of the burn pile and estimate the number of decks remaining, we can calculate it precisely since every card is counted. When the true count climbs above 1.0, the odds move in favor of the player. This is when we increase the size of our bet.

## The Setup

The last message, `'Decks played: ...'`, was added to help me determine how they were inserting the cut card. I could tell immediately they were using an 8-deck shoe (meaning 8 decks of cards were being used to deal) but how many were actually getting *played* before the cut card is a hugely important number. After all, if they play with 8 decks but only get through 2 before shuffling, it doesn't give a lot of time for the count to become favorable.

Unlike at the casino, the cut card seems to be placed *right around the middle of the shoe* rather than about two decks from the end, which is typical in live casino play. I consistently saw almost exactly four decks played before shuffling, which isn't great. It means that the count has to be reasonably high for the true count to rise above one. In practice, though, the true count exceeds one often enough to still be worth the time.

One interesting advantage in online play is that it's very typical for players to sit out a few hands. In the casino, doing so regularly would immediately raise suspicion. Not so online. This means when the count is negative and working against us, we can actually sit out a hand or two until it reverts back (if it ever does).

Since only four of eight decks are being dealt from, it's especially important to capitalize as much as possible on a favorable count. For that reason, I played two hands at a time (the most they'll let a single user play) with small bets until the count became favorable. Similar to increasing your bet when the count is good, playing more than one hand is a way to extract value from a high count.

## The Results

After about 4 hours of play at modest stakes I tripled my money. This is likely an aberration. Remember, even a highly favorable count only confers a percentage point or two of expected return rate to the player. That said, there were some fun times. Blackjacks with big bets down. Splitting 8s four times and doubling on each of them when a bunch of 3s showed up (knowing that there was a high concentration of 10-value cards remaining). Doing some quick calculations and realizing that one of the side bets (which are almost always a terrible idea, just like insurance and even-money) offered a positive expected return based on the concentration of cards, then watching it immediately pay off.

## In Closing

I hope you enjoyed the article. I'll be the first to admit it was light on code, but I thought it made an interesting case study about how card counting works and how Python can be put to use in some off-the-beaten-path ways. It will be interesting to see how successful the live-dealer games become. If they prove popular, it could spark a new generation of card-counting Blackjack players, possibly using more advanced statistical techniques on-the-fly to determine the best play.

Also, it's fun to win money.
