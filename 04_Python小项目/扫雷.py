"""
扫雷（tkinter 版）
==================
运行：python 扫雷.py
左键翻开，右键插旗/取消；翻开数字0会自动展开周围；踩雷失败，全部安全格翻开则胜利。

练习点：二维列表、随机布雷、BFS/递归展开、鼠标左右键事件、状态管理。
"""

import tkinter as tk
import random
from collections import deque

SIZE = 24
COLS, ROWS, MINES = 9, 9, 10


class Minesweeper:
    def __init__(self, root):
        self.root = root
        root.title("扫雷 - tkinter")
        self.status = tk.StringVar(value="左键翻开，右键插旗")
        tk.Label(root, textvariable=self.status, font=("微软雅黑", 11)).pack()
        self.canvas = tk.Canvas(root, width=SIZE * COLS, height=SIZE * ROWS,
                                bg="#bbb", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)
        self.reset()

    def reset(self):
        self.mines = [[False] * COLS for _ in range(ROWS)]
        self.revealed = [[False] * COLS for _ in range(ROWS)]
        self.flagged = [[False] * COLS for _ in range(ROWS)]
        self.counts = [[0] * COLS for _ in range(ROWS)]
        self.first = True
        self.over = False
        self.draw()

    def place_mines(self, safe_r, safe_c):
        # 第一次点击后布雷，保证该格及周围无雷
        forbidden = {(safe_r + dr, safe_c + dc)
                     for dr in (-1, 0, 1) for dc in (-1, 0, 1)}
        cells = [(r, c) for r in range(ROWS) for c in range(COLS)
                 if (r, c) not in forbidden]
        for r, c in random.sample(cells, MINES):
            self.mines[r][c] = True
        for r in range(ROWS):
            for c in range(COLS):
                self.counts[r][c] = self.around(r, c)

    def around(self, r, c):
        return sum(self.mines[r + dr][c + dc]
                   for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                   if 0 <= r + dr < ROWS and 0 <= c + dc < COLS
                   and (dr or dc))

    def cell(self, event):
        return event.x // SIZE, event.y // SIZE

    def left_click(self, event):
        if self.over:
            return
        c, r = self.cell(event)
        if not (0 <= r < ROWS and 0 <= c < COLS) or self.flagged[r][c]:
            return
        if self.first:
            self.place_mines(r, c)
            self.first = False
        if self.mines[r][c]:
            return self.lose()
        self.reveal(r, c)
        self.win_check()
        self.draw()

    def right_click(self, event):
        if self.over:
            return
        c, r = self.cell(event)
        if not self.revealed[r][c]:
            self.flagged[r][c] = not self.flagged[r][c]
            self.draw()

    # 翻开：0 用 BFS 向周围扩散
    def reveal(self, r, c):
        q = deque([(r, c)])
        while q:
            x, y = q.popleft()
            if self.revealed[x][y] or self.flagged[x][y]:
                continue
            self.revealed[x][y] = True
            if self.counts[x][y] == 0 and not self.mines[x][y]:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = x + dr, y + dc
                        if 0 <= nr < ROWS and 0 <= nc < COLS \
                                and not self.revealed[nr][nc]:
                            q.append((nr, nc))

    def win_check(self):
        safe = ROWS * COLS - MINES
        opened = sum(self.revealed[r][c] for r in range(ROWS) for c in range(COLS))
        if opened == safe:
            self.over = True
            self.status.set("你赢了！关闭后重开")

    def lose(self):
        self.over = True
        self.status.set("踩到雷了！关闭后重开")
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        nums = ["", "blue", "green", "red", "purple",
                "maroon", "turquoise", "black", "gray"]
        for r in range(ROWS):
            for c in range(COLS):
                x, y = c * SIZE, r * SIZE
                if self.revealed[r][c]:
                    self.canvas.create_rectangle(x, y, x + SIZE, y + SIZE,
                                                 fill="#ddd", outline="#999")
                    if self.mines[r][c]:
                        self.canvas.create_oval(x + 4, y + 4, x + SIZE - 4,
                                                y + SIZE - 4, fill="black")
                    elif self.counts[r][c]:
                        self.canvas.create_text(x + SIZE / 2, y + SIZE / 2,
                                                text=self.counts[r][c],
                                                fill=nums[self.counts[r][c]],
                                                font=("Arial", 12, "bold"))
                else:
                    self.canvas.create_rectangle(x, y, x + SIZE, y + SIZE,
                                                 fill="#bbb", outline="#888")
                    if self.flagged[r][c]:
                        self.canvas.create_text(x + SIZE / 2, y + SIZE / 2,
                                                text="⚑", fill="red",
                                                font=("Arial", 13, "bold"))


if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()
