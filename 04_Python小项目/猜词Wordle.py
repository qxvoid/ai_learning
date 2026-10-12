"""
猜词 Wordle 克隆（终端彩色版，用 rich 库）
====================
运行：python 猜词Wordle.py
（首次用需要 pip install rich，已经在 ai_learn 环境装好）

练习点：rich 库的 Panel/Text 样式着色，字符串比较逻辑，输入校验。
来源依据：Real Python 官方课程《Create a Python Wordle Clone With Rich》，
freeCodeCamp 同款教程也用同一套思路——这是 rich 库最经典的教学案例之一。

为什么选它做"找回Python手感"的项目：
- rich 是目前 Python 终端UI的事实标准（pip、pytest、VSCode终端里的进度条都用它）
- 代码量比贪吃蛇/俄罗斯方块小得多（约120行），一两个晚上能做完看到成果
- 核心逻辑（比较猜测词和答案，给出对/错位/不存在三种反馈）和框架无关，
  这才是"练手感"要练的东西——rich只是负责把结果画得好看

规则：6次机会猜一个5字母英文单词。绿=位置对，黄=字母对但位置错，灰=字母不在答案里。
"""

import random

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# 词库故意选短，练手用，可以自己扩充这个list
WORDS = ["APPLE", "GRAPE", "MANGO", "LEMON", "MELON", "PEACH", "BERRY", "PLUMS"]

MAX_TRIES = 6
WORD_LEN = 5


def evaluate(guess: str, answer: str) -> list[str]:
    """比较guess和answer，返回每个字母的判定结果：hit/present/miss"""
    result = ["miss"] * WORD_LEN
    answer_chars = list(answer)

    # 第一轮：先标记位置完全对的（绿色），把这些字母从"可用池"里划掉
    for i, ch in enumerate(guess):
        if ch == answer[i]:
            result[i] = "hit"
            answer_chars[i] = None  # 占用掉，避免被第二轮重复计数

    # 第二轮：字母存在但位置不对的（黄色）——必须在第一轮之后做，
    # 否则像 answer="APPLE", guess="PPPPP" 这种重复字母的情况会判错
    for i, ch in enumerate(guess):
        if result[i] == "hit":
            continue
        if ch in answer_chars:
            result[i] = "present"
            answer_chars[answer_chars.index(ch)] = None

    return result


def render_row(guess: str, result: list[str]) -> Text:
    style_map = {"hit": "bold white on green", "present": "bold white on yellow", "miss": "bold white on grey37"}
    row = Text()
    for ch, r in zip(guess, result):
        row.append(f" {ch} ", style=style_map[r])
        row.append(" ")
    return row


def main() -> None:
    answer = random.choice(WORDS)
    history: list[tuple[str, list[str]]] = []

    console.print(Panel.fit("[bold cyan]猜词 Wordle[/bold cyan]\n6次机会，猜一个5字母单词", border_style="cyan"))

    while len(history) < MAX_TRIES:
        console.print(f"\n第 {len(history)+1}/{MAX_TRIES} 次，还剩 {MAX_TRIES-len(history)} 次机会")
        for guess, result in history:
            console.print(render_row(guess, result))

        raw = console.input("输入5个字母的单词 > ").strip().upper()

        if len(raw) != WORD_LEN or not raw.isalpha():
            console.print("[red]请输入恰好5个英文字母[/red]")
            continue

        result = evaluate(raw, answer)
        history.append((raw, result))

        if raw == answer:
            console.print(render_row(raw, result))
            console.print(f"\n[bold green]猜中了！答案就是 {answer}，用了 {len(history)} 次[/bold green]")
            return

    console.print(f"\n[bold red]机会用完了，正确答案是 {answer}[/bold red]")


if __name__ == "__main__":
    main()
