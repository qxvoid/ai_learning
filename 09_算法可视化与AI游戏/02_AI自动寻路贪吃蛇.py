"""
AI 自动寻路贪吃蛇
====================
运行：python 02_AI自动寻路贪吃蛇.py

蛇不再由玩家操作：每一步用BFS重新计算"蛇头到食物、且不撞自己身体"的最短路径，
自动往路径的下一格走。这是把"寻路算法"和"贪吃蛇规则"拼在一起的项目，
比01的纯可视化器多一层"每帧都要重新规划"的逻辑。

来源依据：GitHub上 Ta-Pc/AI-Snake-Game（明确写"用Pygame做可视化演示搜索算法"）、
dhillyon/snake-ai（Dijkstra版）、hayderkharrufa/snake_pathfinding_ai（BFS版，配教程），
都是同一个思路的独立实现，说明这不是冷门点子。

设计说明：
- 每吃到一次食物或蛇头位置变化后，就用BFS重新搜一次"蛇头->食物"的路径
  （把蛇身当作墙），取路径的第二个点（第一个点是蛇头自己）作为下一步方向
- 如果BFS找不到路径（比如食物被身体围死），退化成"随便找一个不会立刻撞死的方向"，
  这样蛇至少能继续存活等下一次机会，而不是直接卡死
"""

import random
from collections import deque

import pygame

CELL = 20
COLS, ROWS = 30, 24
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + 40
FPS = 12  # 蛇的移动速度，越大越快

COLOR_BG = (20, 20, 25)
COLOR_SNAKE = (80, 200, 120)
COLOR_HEAD = (40, 160, 90)
COLOR_FOOD = (220, 70, 70)
COLOR_TEXT = (230, 230, 230)

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def load_chinese_font(size):
    for path in (r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"):
        try:
            return pygame.font.Font(path, size)
        except (FileNotFoundError, OSError):
            continue
    return pygame.font.Font(None, size)


def bfs_path(start, goal, blocked):
    """在(blocked=蛇身)之外找从start到goal的最短路径，找不到返回None"""
    if start == goal:
        return [start]
    frontier = deque([start])
    came_from = {start: None}
    while frontier:
        current = frontier.popleft()
        if current == goal:
            break
        for dx, dy in DIRS:
            nxt = (current[0] + dx, current[1] + dy)
            if not (0 <= nxt[0] < COLS and 0 <= nxt[1] < ROWS):
                continue
            if nxt in blocked or nxt in came_from:
                continue
            came_from[nxt] = current
            frontier.append(nxt)
    if goal not in came_from:
        return None
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path


def pick_fallback_direction(head, body_set):
    """BFS找不到路径时的兜底：随便挑一个不会立刻撞墙/撞身体的方向，能拖一步是一步"""
    random.shuffle(DIRS)
    for dx, dy in DIRS:
        nxt = (head[0] + dx, head[1] + dy)
        if 0 <= nxt[0] < COLS and 0 <= nxt[1] < ROWS and nxt not in body_set:
            return nxt
    return None  # 真的无路可走了


def spawn_food(body_set):
    while True:
        pos = (random.randrange(COLS), random.randrange(ROWS))
        if pos not in body_set:
            return pos


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI 自动寻路贪吃蛇")
    font = load_chinese_font(16)
    clock = pygame.time.Clock()

    snake = deque([(COLS // 2, ROWS // 2)])
    food = spawn_food(set(snake))
    score = 0
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                snake = deque([(COLS // 2, ROWS // 2)])
                food = spawn_food(set(snake))
                score = 0
                game_over = False

        if not game_over:
            body_set = set(snake)
            body_set_without_head = body_set - {snake[0]}
            path = bfs_path(snake[0], food, body_set_without_head)

            if path and len(path) >= 2:
                next_cell = path[1]
            else:
                next_cell = pick_fallback_direction(snake[0], body_set_without_head)

            if next_cell is None:
                game_over = True
            else:
                snake.appendleft(next_cell)
                if next_cell == food:
                    score += 1
                    food = spawn_food(set(snake))
                else:
                    snake.pop()  # 没吃到食物，尾部缩一格（正常前进）

                # 撞墙/撞自己检测（fallback方向已经排除了这种情况，这里是双重保险）
                hx, hy = next_cell
                if not (0 <= hx < COLS and 0 <= hy < ROWS):
                    game_over = True

        screen.fill(COLOR_BG)
        for i, (x, y) in enumerate(snake):
            color = COLOR_HEAD if i == 0 else COLOR_SNAKE
            pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL - 1, CELL - 1))
        fx, fy = food
        pygame.draw.rect(screen, COLOR_FOOD, (fx * CELL, fy * CELL, CELL - 1, CELL - 1))

        bar = pygame.Rect(0, ROWS * CELL, WIDTH, 40)
        pygame.draw.rect(screen, (35, 35, 40), bar)
        status = f"得分:{score}  蛇长:{len(snake)}"
        if game_over:
            status += "  游戏结束！按 R 重开"
        text = font.render(status, True, COLOR_TEXT)
        screen.blit(text, (8, ROWS * CELL + 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
