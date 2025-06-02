__author__ = 'philippe'
import World
import threading
import time

discount = 0.3
actions = World.actions
states = []
Q = {}

# First just set up a rectangular array 0, ... x-1 by 0, ... y-1
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

# Now initialise the Q-grid with initial values, here all 0.1 and related to max cell_score
# And initialise the World.set_cell_score with state, action and 0.1
for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)

# Depending on the action (left, right, down, up) try it
# Update scores
def do_action(action):
    s = World.player
    r = -World.score        # store the old score as negative
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score        # if score has changed, r much larger; else r back to before
    return s, action, r, s2

# Find the max in a given Q(s) and return it with the associated action
# Note that in the Update Q lines below we here pass Q(s2); "s" is a dummy variable
# So we call this twice, once with Q(s) and once with Q(s2), so the "print" line is wrong second time
def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        World.setup_show_Q(a, q) # Show all the weights in their respective locations
        # print (s, a, q, "\n", Q[s].items())
        # we step through Q[s].items looking for the max; equal values mean we choose the first
        # It is also slightly odd that we are picking an action from the cell we move into
        if val is None or (q > val):
            val = q                                 # what about abs(q)? Doesn't work!
            act = a
    # print(s, "Moved .................. ", act, val) # Is wrong on second visit because s2 is passed
    return act, val

# This is the iterative update of the Q function on which everything depends
# "inc" comes from the Bellman iteration in run() below
def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    World.set_cell_score(s, a, Q[s][a])
    #print(s, "for move", a,"has an updated Q-value of ...", Q[s][a])
    print(f'State: {s} | {Q[s]["up"]:0.3f} | {Q[s]["down"]:0.3f} | {Q[s]["left"]:0.3f} | {Q[s]["right"]:0.3f}')


def run():
    global discount
    time.sleep(1)
    alpha = 1
    t = 1

    # the point is that this loop runs indefinitely since no test is ever failed
    # within the loop the World.restart_game() serves to reset the game
    # but doesn't really restart it, and I don't see what resets the thread
    while True:
        # Pick the right action
        s = World.player
        max_act, max_val = max_Q(s)                 # Here we seem to use max_act but not max_val
        # print("From cell ",s,"we will now move ",max_act)
        # this do_action is internal to Learner
        # and returns the reward but this needs adjusting if outside board or in walls
        (s, a, r, s2) = do_action(max_act)          # because max_val gets overwritten below
        World.setup_show_Q("Reward",r)              # and s2 is returned as the target cell
        World.setup_show_Q("Alpha",alpha)           # r is the reward in the target cell
        # World.setup_show_Q(max_act, max_val)        # display the max_val at the appropriate location
        # Update Q
        # print("We now update ",s,"using the Q-values from ",s2)
        # print("Before ",s,Q[s].items())
        # print("Before ",s2,Q[s2].items())
        max_act, max_val = max_Q(s2)                # Do we ever use max_act after this?
        inc_Q(s, a, alpha, r + discount * max_val)  # the last parameter is "inc" which is Bellman
        # print("After ",s,Q[s].items())
        # print("After ",s2,Q[s2].items())

        # Check if the game has restarted
        t += 1.0
        # pause = input() # wait for enter to be pressed to see what is happening

        # reset alpha if the game has restarted
        if World.has_restarted():
            World.restart_game()
            time.sleep(0.01)
            t = 1.0

        # Update the learning rate; this is not absolutely necessary
        alpha = pow(t, -0.1)
        # print("Now the value of alpha is ...............................", alpha)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.01)

# What is going on here?
# This first line defines a new thread to be the "run" function in Learner.py
t = threading.Thread(target=run)
# Force thread "run" to finish as soon as main_loop() finishes using daemon
# thread "run" will go on forever unless ... what?
# t.daemon = True but commented out because I can't understand what purpose it serves
# the next line starts the thread "run"
t.start()
# The next line starts the main_loop
# Notice that matplotlib and Tkinter MUST run in the main loop (I think)
# or at least in the same thread
World.start_game()


