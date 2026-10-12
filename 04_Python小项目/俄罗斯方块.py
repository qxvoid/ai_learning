"""
俄罗斯方块（tkinter 版）
========================
运行：python 俄罗斯方块.py
操作：左右移动，下键加速，上键旋转，空格直接落底，P 暂停。

练习点：二维列表表示棋盘和方块、矩阵旋转、碰撞检测、消行、计分。
"""

import tkinter as tk
import random

CELL = 28
COLS, ROWS = 10, 20
WIDTH, HEIGHT = CELL * COLS, CELL * ROWS

# 7 种方块形状（用 0/1 矩阵表示）
SHAPES = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
}
COLORS = {"I": "cyan", "O": "yellow", "T": "magenta", "S": "green",
          "Z": "red", "J": "blue", "L": "orange"}


class Tetris:
    def __init__(self, root):
        self.root = root
        root.title("俄罗斯方块 - tkinter")
        self.score_var = tk.StringVar()
        tk.Label(root, textvariable=self.score_var, font=("微软雅黑", 12)).pack()
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#222")
        self.canvas.pack()

        root.bind("<Left>", lambda e: self.move(-1, 0))
        root.bind("<Right>", lambda e: self.move(1, 0))
        root.bind("<Down>", lambda e: self.move(0, 1))
        root.bind("<Up>", lambda e: self.rotate())
        root.bind("<space>", lambda e: self.hard_drop())
        root.bind("p", lambda e: self.toggle_pause())
        root.bind("P", lambda e: self.toggle_pause())

        self.reset()

    def reset(self):
        # 棋盘：0 表示空，否则存颜色名
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.lines = 0
        self.paused = False
        self.game_over = False
        self.new_piece()
        self.draw()
        self.loop()

    def new_piece(self):
        name = random.choice(list(SHAPES))
        self.piece = [row[:] for row in SHAPES[name]]
        self.color = COLORS[name]
        self.px = COLS // 2 - len(self.piece[0]) // 2   # 出现位置（列）
        self.py = 0                                      # 行
        if self.collides(self.piece, self.px, self.py):
            self.game_over = True

    # 碰撞检测：方块矩阵放到 (x,y) 是否与墙/已有块重叠
    def collides(self, piece, x, y):
        for r, row in enumerate(piece):
            for c, val in enumerate(row):
                if not val:
                    continue
                bx, by = x + c, y + r
                if bx < 0 or bx >= COLS or by >= ROWS:
                    return True
                if by >= 0 and self.board[by][bx]:
                    return True
        return False

    def move(self, dx, dy):
        if self.paused or self.game_over:
            return
        if not self.collides(self.piece, self.px + dx, self.py + dy):
            self.px += dx
            self.py += dy
        elif dy:                       # 向下走不动 -> 落定
            self.lock()
        self.draw()

    def rotate(self):
        if self.paused or self.game_over:
            return
        # 顺时针旋转 = 转置后逐行反转
        rotated = [list(row) for row in zip(*self.piece)]
        for row in rotated:
            row.reverse()
        # 简单踢墙：转不下就左右各试一格
        for kick in (0, -1, 1, -2, 2):
            if not self.collides(rotated, self.px + kick, self.py):
                self.piece = rotated
                self.px += kick
                break
        self.draw()

    def hard_drop(self):
        while not self.collides(self.piece, self.px, self.py + 1):
            self.py += 1
        self.lock()
        self.draw()

    def toggle_pause(self):
        if not self.game_over:
            self.paused = not self.paused

    # 落定：把方块写进棋盘，消行，再出新块
    def lock(self):
        for r, row in enumerate(self.piece):
            for c, val in enumerate(row):
                if val and self.py + r >= 0:
                    self.board[self.py + r][self.px + c] = self.color
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        kept = [row for row in self.board if any(cell is None for cell in row)]
        cleared = ROWS - len(kept)
        for _ in range(cleared):
            kept.insert(0, [None] * COLS)
        self.board = kept
        self.lines += cleared
        self.score += [0, 100, 300, 500, 800][cleared]

    def loop(self):
        if not self.paused and not self.game_over:
            self.move(0, 1)
        speed = max(80, 500 - self.lines * 15)
        self.root.after(speed, self.loop)

    def draw(self):
        self.canvas.delete("all")
        # 已落定方块
        for r in range(ROWS):
            for c in range(COLS):
                color = self.board[r][c]
                if color:
                    self.box(c, r, color)
        # 当前下落方块
        for r, row in enumerate(self.piece):
            for c, val in enumerate(row):
                if val:
                    self.box(self.px + c, self.py + r, self.color)
        self.score_var.set(f"得分：{self.score}  消行：{self.lines}")
        if self.game_over:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2,
                                    text="游戏结束\n关闭后重开", fill="white",
                                    font=("微软雅黑", 18))
        elif self.paused:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="暂停",
                                    fill="white", font=("微软雅黑", 18))

    def box(self, c, r, color):
        self.canvas.create_rectangle(c * CELL, r * CELL,
                                     (c + 1) * CELL, (r + 1) * CELL,
                                     fill=color, outline="#333")


if __name__ == "__main__":
    root = tk.Tk()
    Tetris(root)
    root.mainloop()
