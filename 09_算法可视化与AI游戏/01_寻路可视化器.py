"""
寻路算法可视化器
====================
运行：python 01_寻路可视化器.py

操作：
- 左键点格子：先点起点(绿)，再点终点(红)，之后点的都是墙(黑)
- 右键点墙：清除这个墙
- 按 1/2/3/4 切换算法：1=BFS  2=贪心(greedy best-first)  3=A*  4=DFS
- 按 空格 开始搜索动画
- 按 C 清空重来

来源依据：这类"网格+鼠标画墙+算法逐帧点亮"的寻路可视化器是被反复实现的经典项目
（GitHub上 davepetrov/Pathfinding-Algo、sujal-goswami/Pathfinding-Visualizer 等独立仓库
都是同一个思路），属于用Pygame练"把算法变成能看见的东西"的标准入口项目。

设计说明：
- 算法函数是生成器（yield），每次yield交出"当前正在处理的节点"，
  主循环每帧从生成器里取一步、画一帧——这样算法逻辑和动画播放解耦，
  你之后想换算法只需要写一个新的生成器函数，不用碰渲染代码。
- BFS/贪心/A* 共享同一个"取出队列里最该处理的节点"框架，区别只在
  队列的排序方式（FIFO / 按到终点直线距离 / 按已走距离+估计距离）。
"""

import heapq
from collections import deque

import pygame

# ---------- 基础设置 ----------
CELL = 20
COLS, ROWS = 40, 30
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + 40   # 底部留40像素显示状态栏

COLOR_BG = (255, 255, 255)
COLOR_GRID = (200, 200, 200)
COLOR_WALL = (30, 30, 30)
COLOR_START = (40, 180, 90)
COLOR_END = (220, 60, 60)
COLOR_VISITED = (180, 210, 255)      # 已经访问过的格子：淡蓝
COLOR_FRONTIER = (255, 235, 150)     # 待访问队列里的格子：淡黄
COLOR_PATH = (255, 200, 40)          # 最终路径：金色
COLOR_TEXT = (0, 0, 0)

ALGO_NAMES = {1: "BFS", 2: "贪心 Greedy", 3: "A*", 4: "DFS"}


def neighbors(pos, walls):
    x, y = pos
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in walls:
            yield (nx, ny)


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bfs(start, end, walls):
    """广度优先：队列是普通FIFO，逐层扩散，保证找到的是最短路径（无权图）"""
    frontier = deque([start])
    came_from = {start: None}
    while frontier:
        current = frontier.popleft()
        yield current, set(frontier), came_from
        if current == end:
            return came_from
        for nxt in neighbors(current, walls):
            if nxt not in came_from:
                came_from[nxt] = current
                frontier.append(nxt)
    return came_from


def dfs(start, end, walls):
    """深度优先：用栈代替队列，一条路走到底再回头——不保证最短路径"""
    frontier = [start]
    came_from = {start: None}
    while frontier:
        current = frontier.pop()
        yield current, set(frontier), came_from
        if current == end:
            return came_from
        for nxt in neighbors(current, walls):
            if nxt not in came_from:
                came_from[nxt] = current
                frontier.append(nxt)
    return came_from


def greedy_best_first(start, end, walls):
    """贪心最佳优先：每次挑"离终点直线距离最近"的节点，跑得快但不保证最短"""
    counter = 0
    frontier = [(manhattan(start, end), counter, start)]
    came_from = {start: None}
    visited = {start}
    while frontier:
        _, _, current = heapq.heappop(frontier)
        yield current, {f[2] for f in frontier}, came_from
        if current == end:
            return came_from
        for nxt in neighbors(current, walls):
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = current
                counter += 1
                heapq.heappush(frontier, (manhattan(nxt, end), counter, nxt))
    return came_from


def astar(start, end, walls):
    """A*：綜合"已经走了多远(g)"和"估计还要走多远(h)"，两者都考虑就能保证最短路径"""
    counter = 0
    g_score = {start: 0}
    frontier = [(manhattan(start, end), counter, start)]
    came_from = {start: None}
    while frontier:
        _, _, current = heapq.heappop(frontier)
        yield current, {f[2] for f in frontier}, came_from
        if current == end:
            return came_from
        for nxt in neighbors(current, walls):
            tentative_g = g_score[current] + 1
            if nxt not in g_score or tentative_g < g_score[nxt]:
                g_score[nxt] = tentative_g
                came_from[nxt] = current
                counter += 1
                f_score = tentative_g + manhattan(nxt, end)
                heapq.heappush(frontier, (f_score, counter, nxt))
    return came_from


ALGOS = {1: bfs, 2: greedy_best_first, 3: astar, 4: dfs}


def reconstruct_path(came_from, end):
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path


def draw_grid(screen, font, walls, start, end, visited, frontier, path, algo_id, status):
    screen.fill(COLOR_BG)
    for x in range(COLS):
        for y in range(ROWS):
            rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
            pos = (x, y)
            if pos == start:
                color = COLOR_START
            elif pos == end:
                color = COLOR_END
            elif pos in path:
                color = COLOR_PATH
            elif pos in walls:
                color = COLOR_WALL
            elif pos in visited:
                color = COLOR_VISITED
            elif pos in frontier:
                color = COLOR_FRONTIER
            else:
                color = COLOR_BG
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, COLOR_GRID, rect, 1)

    bar = pygame.Rect(0, ROWS * CELL, WIDTH, 40)
    pygame.draw.rect(screen, (245, 245, 245), bar)
    text = font.render(
        f"算法:{ALGO_NAMES[algo_id]}(按1-4切换)  空格=开始  C=清空  {status}", True, COLOR_TEXT
    )
    screen.blit(text, (8, ROWS * CELL + 10))


def load_chinese_font(size):
    """pygame.font.SysFont 在部分Windows机器上扫描字体注册表会直接崩溃（本机验证过），
    优先尝试系统微软雅黑字体文件，失败则退回pygame内置默认字体（不显示中文但不会崩）。"""
    for path in (r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"):
        try:
            return pygame.font.Font(path, size)
        except (FileNotFoundError, OSError):
            continue
    return pygame.font.Font(None, size)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("寻路算法可视化器")
    font = load_chinese_font(16)
    clock = pygame.time.Clock()

    walls = set()
    start = None
    end = None
    algo_id = 3  # 默认A*
    running_gen = None
    visited, frontier, path = set(), set(), []
    status = "左键设起点/终点/墙，右键清除墙"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if my >= ROWS * CELL:
                    continue
                pos = (mx // CELL, my // CELL)
                if event.button == 1:  # 左键
                    if start is None:
                        start = pos
                    elif end is None and pos != start:
                        end = pos
                    elif pos != start and pos != end:
                        walls.add(pos)
                elif event.button == 3:  # 右键清墙
                    walls.discard(pos)

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    algo_id = int(event.unicode)
                    running_gen = None
                elif event.key == pygame.K_SPACE and start and end:
                    running_gen = ALGOS[algo_id](start, end, walls)
                    visited, frontier, path = set(), set(), []
                    status = "搜索中..."
                elif event.key == pygame.K_c:
                    walls, start, end = set(), None, None
                    running_gen = None
                    visited, frontier, path = set(), set(), []
                    status = "已清空"

        if running_gen is not None:
            try:
                current, frontier_set, came_from = next(running_gen)
                visited.add(current)
                frontier = frontier_set
                if current == end:
                    path = reconstruct_path(came_from, end)
                    running_gen = None
                    status = f"找到路径！长度={len(path)-1}  已访问{len(visited)}个格子"
            except StopIteration:
                running_gen = None
                if not path:
                    status = "没有找到路径（被墙完全挡住了）"

        draw_grid(screen, font, walls, start, end, visited, frontier, path, algo_id, status)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
