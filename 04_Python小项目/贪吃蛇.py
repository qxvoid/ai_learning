"""
贪吃蛇（tkinter 版）
====================
Python 自带的 tkinter 就能写图形界面，无需安装任何库。

运行方法：
    在 VSCode 中打开本文件，点右上角运行，或在终端执行：
    python 贪吃蛇.py

操作：方向键控制移动，空格暂停，回车重新开始。

练习点：列表、字典、随机数、键盘事件、定时器（after）、Canvas 绘图。
"""

import tkinter as tk
import random

# ---------- 基本参数 ----------
CELL = 20               # 每格像素大小
COLS = 25               # 横向格数
ROWS = 20               # 纵向格数
WIDTH = CELL * COLS
HEIGHT = CELL * ROWS
SPEED = 110             # 移动间隔（毫秒），越小越快


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("贪吃蛇 - tkinter")

        # 顶部计分
        self.score_var = tk.StringVar()
        tk.Label(root, textvariable=self.score_var, font=("微软雅黑", 12)).pack()

        # 画布
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#111")
        self.canvas.pack()

        # 键盘事件：方向键 / 空格 / 回车
        root.bind("<Up>", lambda e: self.change_dir((0, -1)))
        root.bind("<Down>", lambda e: self.change_dir((0, 1)))
        root.bind("<Left>", lambda e: self.change_dir((-1, 0)))
        root.bind("<Right>", lambda e: self.change_dir((1, 0)))
        root.bind("<space>", lambda e: self.toggle_pause())
        root.bind("<Return>", lambda e: self.reset())

        self.reset()

    # ---------- 初始化/重开 ----------
    def reset(self):
        # 蛇身：列表里每个元素是 (列, 行) 坐标，头在最后
        center = (COLS // 2, ROWS // 2)
        self.snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
        self.direction = (1, 0)       # 向右
        self.next_dir = (1, 0)
        self.score = 0
        self.paused = False
        self.game_over = False
        self.spawn_food()
        self.draw()
        self.loop()

    # ---------- 食物 ----------
    def spawn_food(self):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in self.snake:      # 别刷在蛇身上
                self.food = pos
                return

    # ---------- 方向 ----------
    def change_dir(self, d):
        # 禁止直接掉头（向右时不能立刻向左）
        if (d[0] + self.direction[0], d[1] + self.direction[1]) != (0, 0):
            self.next_dir = d

    def toggle_pause(self):
        if not self.game_over:
            self.paused = not self.paused

    # ---------- 主循环：每隔 SPEED 毫秒走一步 ----------
    def loop(self):
        if not self.paused and not self.game_over:
            self.move()
            self.draw()
        self.root.after(SPEED, self.loop)   # after：定时器，到点再调用自己

    # ---------- 移动逻辑 ----------
    def move(self):
        self.direction = self.next_dir
        head = self.snake[-1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # 撞墙
        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            self.game_over = True
            return
        # 撞自己
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.append(new_head)         # 头前进
        if new_head == self.food:           # 吃到食物：加分，不移尾巴（变长）
            self.score += 10
            self.spawn_food()
        else:
            self.snake.pop(0)               # 没吃到：去掉尾巴，长度不变

    # ---------- 绘制 ----------
    def draw(self):
        self.canvas.delete("all")
        # 食物（红色圆）
        fx, fy = self.food
        self.canvas.create_oval(fx * CELL, fy * CELL,
                                (fx + 1) * CELL, (fy + 1) * CELL,
                                fill="red", outline="")
        # 蛇（绿色方块）
        for i, (x, y) in enumerate(self.snake):
            color = "#7CFC00" if i == len(self.snake) - 1 else "#2E8B57"
            self.canvas.create_rectangle(x * CELL, y * CELL,
                                         (x + 1) * CELL, (y + 1) * CELL,
                                         fill=color, outline="")
        self.score_var.set(f"得分：{self.score}")

        if self.game_over:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2,
                                    text=f"游戏结束  得分{self.score}\n按回车重开",
                                    fill="white", font=("微软雅黑", 18))
        elif self.paused:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2,
                                    text="暂停（空格继续）", fill="white",
                                    font=("微软雅黑", 18))


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
