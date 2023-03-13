#!/usr/bin/python3

import random
import time
from tkinter import Tk, Canvas


class Paddle:
    def __init__(self, _canvas: Canvas, color: str):
        self.canvas = _canvas
        self.id = self.canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.speed = 3
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all("<KeyPress-Left>", self.turn_left)
        self.canvas.bind_all("<KeyPress-Right>", self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] < 0:
            self.x = self.speed
        elif pos[2] > self.canvas_width:
            self.x = -self.speed
        elif (
            pos[0] - self.speed + 1 <= 0 or pos[2] +
                self.speed - 1 >= self.canvas_width
        ):  # paddle is exactly on edge of screen
            self.x = 0

    def turn_left(self, _evt):
        self.x = -self.speed

    def turn_right(self, _evt):
        self.x = self.speed


class Ball:
    def __init__(self, _canvas: Canvas, paddle: Paddle, color: str):
        self.canvas = _canvas
        self.paddle = paddle
        self.score = 0
        self.id = _canvas.create_oval(10, 10, 25, 25, fill=color)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                return True
            return False

    def collision_check(self):
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos):
            self.score += 1
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        self.collision_check()


class Score:
    def __init__(self, _canvas: Canvas, ball: Ball):
        self.canvas = _canvas
        self.ball = ball
        self.id = _canvas.create_text(
            10, 10, text=str(self.ball.score), font=("comic sans ms", 15)
        )

    def draw(self):
        self.canvas.itemconfig(self.id, text=str(self.ball.score))
        if self.ball.hit_bottom:
            self.canvas.move(self.id, 250, 200)
            self.canvas.itemconfig(
                self.id, text="Game Over!", font=("comic sans ms", 40)
            )


tk = Tk()
tk.title("Levi's ball game")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()
paddle = Paddle(canvas, "blue")
ball = Ball(canvas, paddle, "red")
score = Score(canvas, ball)

while 1:
    if not ball.hit_bottom:
        ball.draw()
        paddle.draw()
        score.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
