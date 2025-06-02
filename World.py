__author__ = 'philippe'

import matplotlib
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.animation as animation

# This is all to do with matplotlib
plot_x = []
plot_y1 = []
plot_y2 = []
plt.plot([], [])
# plt.ion()
# plt.legend()
fig, ax = plt.subplots()
# plt.show()
# legendmarker = 0

import random
import tkinter
from tkinter import *
root = Tk()

# this is not the most efficient way to do this plot but this at least works
class mclass:
    def __init__(self,  window):
        self.window = window
        self.plot
        self.animate
        #self.box1 = Entry(window)
        #self.box2 = Entry(window)
        #self.button1 = Button (window, text="Click Here to Plot", command = self.plot)
        #self.box1.grid()
        #self.button1.grid()
        # the end of the next line needs to say "plot" to plot and "animate" to animate; will later automate this
        #self.button2 = Button (window, text="Click Here to Animate", command = self.animate)
        #self.box2.grid()
        #self.button2.grid()

    def plot(self):
        x = np.array (plot_x)
        v = np.array (plot_y1)
        p = np.array (plot_y2)
        fig = Figure(figsize=(5,5))
        a = fig.add_subplot(131)
        b = fig.add_subplot(132)
        a.clear()
        a.scatter(x,p,color='red')
        b.clear()
        b.plot(x,p,color='blue')
        a.invert_yaxis()

        a.set_title ("Amazing If This Works", fontsize=16)
        a.set_ylabel("Score on Success/Fail", fontsize=14)
        a.set_xlabel("Attempt", fontsize=14)

        qvalues = FigureCanvasTkAgg(fig, master=self.window)
        qvalues.get_tk_widget().grid()
        qvalues.draw()

        #toolbar = NavigationToolbar2Tk(qvalues, root)
        #toolbar.update()
        #qvalues.get_tk_widget().grid()

    def animate(self):
        xList = np.array(plot_x)
        yList = np.array(plot_y2)

        fig = Figure(figsize = (5,5), dpi = 100)
        c = fig.add_subplot(111)
        c.clear()
        c.plot(xList, yList)

        c.set_title ("Amazing If This Works", fontsize=16)
        c.set_ylabel("Score on Success/Fail", fontsize=14)
        c.set_xlabel("Attempt", fontsize=14)

        qvalues = FigureCanvasTkAgg(fig, master=self.window)
        qvalues.get_tk_widget().grid()
        qvalues.draw()


triangle_size = 0.2
cell_score_min = -0.5
cell_score_max = 0.5
(x, y) = (10, 10)
Width = 500/x
actions = ["up", "down", "left", "right"]

offset = 400
# this is a "child" widget to root = Tk() and grid should just sort out multiple plots
board = Canvas(root, width=x*Width+offset, height=y*Width)
qvalues = Canvas(root, width = x*Width, height = y*Width)

success_count = 0
fail_count = 0
attempts = 0
count = 0
total = 0
mean = 0

score = 1
restart = False
walk_reward = -1/(x*y)  # the Fail/Success test is fallacious because sometimes on a big grid the search depletes the score below 0

walls = [(x-1,y-1)]
new_wall = (1,1)
for i in range(x+y):
    new_wall = (random.randint(0,x-1), random.randint(0,y-1))
    while new_wall not in walls:
        walls.append(new_wall)
#print(walls)

# the final figures in each of "specials" are the rewards for failure and success passed back through World.Score to Bellman
fail = (x-1,y-1,"red",-1)
succeed = (x-1,y-1,"green",1) # choose fail and succeed to lie inside walls to force next loop to execute
while (fail[0],fail[1]) in walls or (succeed[0],succeed[1]) in walls:
    fail = (random.randint(0,x-1), random.randint(0,y-1), "red", -1)
    succeed = (random.randint(0,x-1), random.randint(0,y-1), "green", 1)
# now neither are inside walls we can assign to specials
specials = [fail,succeed]
cell_scores = {}

# now we choose the starting-position avoiding cells already occupied or special and store the result
player = walls[2] # set up player to be in walls to force next loop to execute
while player in specials or player in walls:
    player = (random.randint(0,x-1),random.randint(0, y-1)) # This randomises the starting position
#print("Player start-point is",player)
player_store = player

def create_triangle(i, j, action):
    global triangle_size
    # triangle_size+=0.0001
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)

def render_scoreboard():
    board.create_rectangle(offset+Width*x/2-120,Width*y/2-120,offset+Width*x/2+120,Width*y/2+120, fill="yellow", width=1)

def render_successboard():
    board.create_rectangle(offset+Width*x/2-120,Width*y/2+140,offset+Width*x/2-10,Width*y/2+200, fill="light green", width=3)

def render_failureboard():
    board.create_rectangle(offset+Width*x/2+10,Width*y/2+140,offset+Width*x/2+120,Width*y/2+200, fill="red", width=3)

def render_Qscoreboard():
    qvalues.create_rectangle(Width*x/2-120,Width*y/2-120,Width*x/2+120,Width*y/2+120, fill="green", width=1)

render_scoreboard() # Note that you have to initialise this as at the bottom of the code
render_successboard()
render_failureboard()
render_Qscoreboard()

def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()


# the colour-coding of the exit triangles works better with starting-values of temp[action] around 0.5
def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    walls_marker = 0
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)

# It seems strange that the reward return for hitting walls or off board isn't larger, so now -1
# And the reason this is awkward is that this function doesn't return anything anywhere to say what the outcome was
def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart, success_count, fail_count, attempts, count, mean, total
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    # first we check that the new location is inside the board and not in one of the walls
    # this is quite clumsy because it doesn't distinguish the two cases of outside and in walls
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        attempts += 1
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
        render_scoreboard()     # just delete everything; the Tkinter delete doesn't seem to work for me
        render_Qscoreboard()
        setup_show_Q("Scores",score)
        setup_show_Q("Tries",count)
    else:
        walls_marker = -10       # same negative reward for being in a wall
    # now we check for a terminator condition if the location is inside the special squares
    # this is where we can add rewards that boost score for going outside board or into walls

    start= mclass(qvalues)

    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            attempts += 1
            count += 1
            total += score
            plot_x.append(attempts)
            #mean = total/count
            plot_y1.append(mean)
            plot_y2.append(score)
            # print(plot_x, plot_y1, plot_y2)
            score -= walk_reward
            score += w
            if c == "green":
                print ("Success! score: ", score)
                success_count += 1
                setup_show_Q("Successes", success_count)
            elif c == "red":
                print ("Fail!    score: ", score)
                fail_count += 1
                setup_show_Q("Failures", fail_count)
            restart = True
    for (i, j) in walls:        # this is adding a negative reward for hitting a wall or going outside board
        if (new_x == i and new_y == j) or new_x < 0 or new_x >= x or new_y < 0 or new_y >= y:
            score -= walk_reward
            score += walls_marker
            return              # this seems to be the only place where a return is done
    # print ("score: ", score)


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart
    player = player_store   # return the player to the starting-position
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

# I don't see the point of the call to this function
# Why no just test for restart == True?
def has_restarted():
    return restart

def setup_show_Q(action,p):
    if action == "up":
        show_Q(offset+Width*x/2,Width*y/2-80,round(p,3),"Up")
    elif action == "down":
        show_Q(offset+Width*x/2,Width*y/2+80,round(p,3),"Down")
    elif action == "left":
        show_Q(offset+Width*x/2-80,Width*y/2,round(p,3),"Left")
    elif action == "right":
        show_Q(offset+Width*x/2+80,Width*y/2,round(p,3),"Right")
    elif action == "Reward":
        show_Q(offset+Width*x/2,Width*y/2-40,round(p,3),"Reward")
    elif action == "Alpha":
        show_Q(offset+Width*x/2,Width*y/2+40,round(p,3),"Alpha")
    elif action == "Scores":
        show_Q(offset+Width*x/2, Width*y/2,round(p,3),"Score")
    elif action == "Tries":
        show_Q(offset+Width*x/2+80, Width*y/2+40,round(p,3),"Tries")
        show_Q(offset+Width*x/2-80, Width*y/2+40,round(p,3),"Attempts")
    elif action == "Successes":
        render_successboard()
        show_Q(offset+Width*x/2-65,Width*y/2+180,round(p,3),"Successes")
    elif action == "Failures":
        render_failureboard()
        show_Q(offset+Width*x/2+65,Width*y/2+180,round(p,3),"Failures")
    else:
        return

def show_Q(xcoord, ycoord, Q_value, heading):
    # render_scoreboard()
    board.create_text(xcoord, ycoord-20,text = heading)
    board.create_text(xcoord, ycoord,text = str(Q_value))
    qvalues.create_text(xcoord-offset, ycoord,text = str(Q_value))
    return

# These four lines are calling the Tkinter root bind; is this the threading element?
# Could it be that all the matplotlib routines need to be called from World no Learner?
root.bind("<Up>", call_up)
root.bind("<Down>", call_down)
root.bind("<Right>", call_right)
root.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)
qvalues.grid(row=0, column=1)

# What follows is for the matplotlib display
# this is supposed to be running in mainloop() but it isn't in Tk.main_loop()
# show_the_data():

'''
if not has_restarted():
    global legendmarker
    restart_game()
    legendmarker += 1
    plot_x.append(attempts)
    plot_y1.append(mean)
    plot_y2.append(count)
    plt.plot(plot_x, plot_y1,'b', label = 'mean')
    plt.plot(plot_x, plot_y2,'r', label = 'moves')
    fig = pylab.gcf() # These two lines are supposed to change the window title
    fig.canvas.set_window_title('Mean Time to Fail or Success Behaviour')
    plt.suptitle('Mean Time to Termination Iteration', fontsize=10)
    plt.ylabel('Cumulative Mean Attempts to Success/Fail and Moves',fontsize=8)
    plt.xlabel('Attempts in Run',fontsize=8)
    if legendmarker == 1:
        plt.legend(loc=2)  # Maddeningly doesn't work properly
        for i in range(x):      # was xmax and ymax
            for j in range(y):
                print(i, j, Q[i,j])
                ax.text(i, j, str(c), va='center',ha='center')
                ax.matshow(Q)
plt.show()
'''

def start_game():
    # ani = animation.FuncAnimation(fig, animate, interval = 1000)
    root.mainloop()

