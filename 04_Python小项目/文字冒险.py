""""
文字冒险（控制台版）
====================
运行：python 文字冒险.py
在几个房间里移动、捡钥匙、最终开门通关。输入方向（north/south/east/west）或命令。

练习点：**字典**描述房间连接关系、集合存物品、while 主循环、字符串处理、函数拆分。
这其实就是一个最简单的"游戏地图数据结构"，和你学的图论邻接表是一个思想。
"""

# 房间表：房间名 -> {方向: 通向哪个房间}
# 这就是用字典实现的邻接表
ROOMS = {
    "大厅": {"east": "厨房", "south": "书房"},
    "厨房": {"west": "大厅", "south": "花园"},
    "书房": {"north": "大厅", "east": "花园"},
    "花园": {"north": "厨房", "west": "书房", "east": "大门"},
    "大门": {},   # 终点，需要钥匙
}

# 每个房间里的物品
ITEMS = {
    "厨房": "钥匙",
    "书房": "地图",
}


def main():
    current = "大厅"
    inventory = set()          # 背包用集合
    print("=== 文字冒险：找到钥匙，从大门逃出去 ===")

    while True:
        print(f"\n你在【{current}】，背包：{sorted(inventory) or '空'}")

        # 捡本房间物品
        if current in ITEMS:
            item = ITEMS.pop(current)
            inventory.add(item)
            print(f"你捡到了：{item}")

        exits = ROOMS[current]
        print("可走方向：", ", ".join(sorted(exits)) or "无（终点）")
        cmd = input("> ").strip().lower()

        if cmd in ("quit", "q", "退出"):
            print("游戏结束。")
            return
        if cmd in ("look", "查看"):
            continue
        if cmd in exits:
            current = exits[cmd]
            if current == "大门":
                if "钥匙" in inventory:
                    print("你用钥匙打开大门，成功逃脱！通关！")
                else:
                    print("大门锁着，你需要一把钥匙。")
                    current = "花园"
        else:
            print("那边没有路，可走：", ", ".join(sorted(exits)))


if __name__ == "__main__":
    main()
