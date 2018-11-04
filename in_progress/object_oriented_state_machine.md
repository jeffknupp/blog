One issue that plauges both novice and even intermediate developers is the question of "when to use classes". Often, the default approach for these developers will skew towards "make a class for everything, and everything should be in a class." I don't think I'm alone amongst Python veterans when I say that classes tend to be overused by most novice-to-intermediate Python programmers, but that's not to say they're not useful. They're an incredibly powerful tool for abstraction, encapsulation, and interface definition purposes. But how does that help you decide whether or not you should write something using a class or not?

I have a simple litmus test to determine if using a class is *innappropriate* (i.e. it's not a positive signal you *should* use a class but passing the test at least means there isn't an obvious reason not to). Classes should be used to:

1. Keep some sort of state
1. Control how that state can be manipluated or accessed

## What is "State"?

When I refer to "state", I mean a bit more than just "data". I'm using *state* in the same way it is used when describing FSM ([Finite State Machine](https://en.wikipedia.org/wiki/Finite-state_machine), or "Finite State Automaton"). An FSM can be used to model many things, including those in the real-world. The wikipedia entry [has a good example](https://en.wikipedia.org/wiki/Finite-state_machine#Example:_coin-operated_turnstile), showing how one might model a coin-operated turnstile (the kind you might find in a subway station). The idea is that, if we want to define how a turnstile is supposed to work, we can do so in terms of the various *states* the turnstile can be in as well as the events that can cause a *transition* from this state to another. They are typically represented visually as directed graphs, where each node represents an individual state and the edges represent the possible transitions to other states.

Let's think about a turnstile's possible states. There are really only two. Most of the time the "arm" is locked. Only when a coin is inserted does the arm unlock. After the arm in unlocked *and then pushed*, it returns to the locked state, waiting for the next person to insert a coin and pass through.
