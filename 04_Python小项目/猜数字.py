"""
猜数字（控制台版）
==================
运行：python 猜数字.py
程序想一个 1~100 的数字，你来猜，会提示大了/小了。

练习点：input、while、随机数、比较、用 try/except 处理非法输入。
"""

import random


def main():
    target = random.randint(1, 100)
    tries = 0
    print("我想了一个 1 到 100 之间的整数，猜猜看？（输入 q 退出）")

    while True:
        raw = input("请输入：").strip()

        if raw.lower() == "q":
            print(f"答案是 {target}，下次再战！")
            return

        # 输入校验：不是数字时不要让程序崩溃
        try:
            guess = int(raw)
        except ValueError:
            print("请输入一个整数，或输入 q 退出。")
            continue

        tries += 1
        if guess < target:
            print("小了，往大猜。")
        elif guess > target:
            print("大了，往小猜。")
        else:
            print(f"猜对了！答案就是 {target}，你用了 {tries} 次。")
            # 再来一局
            again = input("再来一局吗？(y/n)：").strip().lower()
            if again == "y":
                return main()
            return


if __name__ == "__main__":
    main()
