from tkinter import *
import random
import time


class Ball(object):
    def __init__(self, canvas, paddle, color, score):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[0] < 0:
            self.x = 3
        if pos[2] > self.canvas_width:
            self.x = -3
        if pos[1] < 0:
            self.y = 3
        if pos[3] > self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos):
            self.y = -3
            self.x += paddle.x

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[0] <= paddle_pos[2] and pos[2] >= paddle_pos[0]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.score.scores += 1
                return True
        return False

class Paddle(object):
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 350)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<Button-1>', self.start_game)
        self.is_start = False

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id) 
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        pos = self.canvas.coords(self.id) 
        if pos[0]-4 >= 0:
            self.x = -4
    def turn_right(self, evt):
        pos = self.canvas.coords(self.id) 
        if pos[2]+4 <= self.canvas_width:
            self.x = 4

    def start_game(self, evt):
        self.is_start = True

class Gameover(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = self.canvas.create_text(240, 350, text="You Died!", font=('Courier', 25), state='hidden')

class Score(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.scores = 0
        self.id = self.canvas.create_text(470, 10, text=self.scores, font=('Helvetica', 15), state='normal')
    def draw(self):
        canvas.itemconfig(self.id, text=self.scores)




tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()


score = Score(canvas)
paddle = Paddle(canvas, 'green')
ball = Ball(canvas, paddle, 'blue',score)
game_over = Gameover(canvas)

while 1:
    if ball.hit_bottom == False and paddle.is_start:
        ball.draw()
        paddle.draw()
        score.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
    if ball.hit_bottom:
        time.sleep(0.5)
        canvas.itemconfig(game_over.id, state='normal')


