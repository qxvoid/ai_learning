"""
文字冒险（match-case 升级版）
====================
运行：python 文字冒险_match版.py

这是对 文字冒险.py 的语法升级，游戏内容不变（地图、钥匙、通关逻辑一样），
换的是"怎么解析玩家输入"这一件事：旧版用一串 if/elif 字符串判断，
这版用 Python 3.10+ 的 match-case（结构化模式匹配）。

这不是我瞎选的练习素材：Real Python 官方教程《Structural Pattern Matching in Python》
和 PEP 636 官方教程，两者都拿"写一个文字冒险游戏"作为讲解 match-case 的示例场景，
说明这个语法天生适合处理"动词+名词"这种带参数的命令（"go north" / "take key"）。

对比旧版能看到的核心区别：
- 旧版：cmd in exits 判断方向，然后单独一段代码处理"quit/look"——命令种类一多，if/elif 会越叠越长
- 这版：把输入按空格拆成词元列表，match 直接对列表结构做模式匹配，
  一条 case 就能同时"匹配形状 + 拆解参数"，比如 case ["take", item] 一步到位拿到 item 是什么
"""

from dataclasses import dataclass, field


@dataclass
class Room:
    exits: dict[str, str] = field(default_factory=dict)   # 方向 -> 房间名
    items: set[str] = field(default_factory=set)          # 房间里的物品


# 房间表：字典描述地图连接关系（和旧版一样是"图的邻接表"思想）
ROOMS = {
    "大厅": Room(exits={"east": "厨房", "south": "书房"}),
    "厨房": Room(exits={"west": "大厅", "south": "花园"}, items={"钥匙"}),
    "书房": Room(exits={"north": "大厅", "east": "花园"}, items={"地图"}),
    "花园": Room(exits={"north": "厨房", "west": "书房", "east": "大门"}),
    "大门": Room(),   # 终点，需要钥匙
}

DIRECTIONS = {"north", "south", "east", "west", "n", "s", "e", "w"}
DIR_ALIAS = {"n": "north", "s": "south", "e": "east", "w": "west"}


def describe(room_name: str) -> None:
    room = ROOMS[room_name]
    print(f"\n你在【{room_name}】")
    if room.items:
        print("这里有：", "、".join(sorted(room.items)))
    print("可走方向：", ", ".join(sorted(room.exits)) or "无（终点）")


def main() -> None:
    current = "大厅"
    inventory: set[str] = set()
    print("=== 文字冒险：找到钥匙，从大门逃出去 ===")
    print("命令：go <方向> / take <物品> / drop <物品> / inventory / look / quit")

    describe(current)
    while True:
        tokens = input("> ").strip().lower().split()

        match tokens:
            case []:
                continue

            case ["quit" | "q" | "退出"]:
                print("游戏结束。")
                return

            case ["look" | "查看" | "l"]:
                describe(current)

            case ["inventory" | "i" | "背包"]:
                print("背包：", "、".join(sorted(inventory)) or "空")

            case ["take" | "get", item] | ["拿", item]:
                room = ROOMS[current]
                if item in room.items:
                    room.items.remove(item)
                    inventory.add(item)
                    print(f"你捡到了：{item}")
                else:
                    print(f"这里没有「{item}」。")

            case ["drop", item]:
                if item in inventory:
                    inventory.remove(item)
                    ROOMS[current].items.add(item)
                    print(f"你放下了：{item}")
                else:
                    print(f"你身上没有「{item}」。")

            # 直接输入方向词，或 "go 方向"，两种都接受
            case [d] if d in DIRECTIONS:
                direction = DIR_ALIAS.get(d, d)
                current = try_move(current, direction, inventory)

            case ["go" | "walk", d] if d in DIRECTIONS:
                direction = DIR_ALIAS.get(d, d)
                current = try_move(current, direction, inventory)

            case _:
                print("没听懂这个命令。试试 go north / take 钥匙 / look / quit")


def try_move(current: str, direction: str, inventory: set[str]) -> str:
    exits = ROOMS[current].exits
    if direction not in exits:
        print("那边没有路，可走：", ", ".join(sorted(exits)))
        return current

    target = exits[direction]
    if target == "大门" and "钥匙" not in inventory:
        print("大门锁着，你需要一把钥匙。")
        return current

    if target == "大门":
        print("你用钥匙打开大门，成功逃脱！通关！")

    describe(target)
    return target


if __name__ == "__main__":
    main()
