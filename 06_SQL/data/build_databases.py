# -*- coding: utf-8 -*-
"""
构建 SQL 学习用的 SQLite 数据库（可重复运行，结果稳定）。
运行：  C:\\Users\\Public\\miniconda3\\envs\\ai_learn\\python.exe build_databases.py

产出两个数据库到本目录：
  1) shop.db        —— 一个连锁零售公司的“规范化”业务库（多表 + 主外键），
                       用于系统学习 SELECT / 聚合 / JOIN / 子查询 / 窗口函数。
  2) superstore.db  —— 把你已经用 Pandas 分析过的 Superstore 超市数据导入 SQLite，
                       作为“同一批数据、Pandas vs SQL 对照”的桥梁。

为什么自己造数据而不是只下载现成库？
  - 可复现：固定随机种子，任何人跑出来都一样（你也能看清数据是怎么来的）；
  - 贴合教学：特意设计了“自关联员工表”“一对多订单”等结构，专门覆盖窗口函数、自连接等考点；
  - 零网络：不依赖下载即可学习。
学完本库后，README 里给了 Chinook / Northwind / Sakila 三个真实世界经典库的地址作为进阶。
"""
import os
import sqlite3
import random
from datetime import date, timedelta

import pandas as pd

# 固定随机种子，保证可复现（你自己写代码也建议养成设种子的习惯）
SEED = 20260913
random.seed(SEED)

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# 一、构建 shop.db
# ----------------------------------------------------------------------------
REGIONS = ["华东", "华北", "华南", "西南", "华中"]
CITIES = {
    "华东": ["上海", "杭州", "南京", "苏州", "宁波"],
    "华北": ["北京", "天津", "济南", "青岛", "石家庄"],
    "华南": ["广州", "深圳", "厦门", "佛山", "东莞"],
    "西南": ["昆明", "成都", "重庆", "贵阳", "南宁"],
    "华中": ["武汉", "长沙", "郑州", "合肥", "南昌"],
}
SEGMENTS = ["个人客户", "企业客户", "家庭办公"]
GENDERS = ["男", "女"]
SURNAMES = list("王李张刘陈杨黄赵吴周徐孙马朱胡郭何高林罗郑梁谢宋唐许")
GIVEN = ["伟", "芳", "娜", "敏", "静", "磊", "军", "洋", "勇", "艳", "杰", "娟",
         "涛", "明", "超", "秀英", "霞", "平", "刚", "桂英", "雨辰", "子轩", "梓涵",
         "一诺", "思远", "若曦", "浩然", "欣怡", "宇航", "佳琪"]

# 商品目录：大类 -> (子类别, 基础价位)
CATALOG = {
    "家具": [("椅子", 300), ("桌子", 800), ("书架", 450), ("沙发", 2000), ("床", 1500)],
    "办公用品": [("文具", 20), ("装订机", 120), ("纸张", 45), ("收纳", 60), ("标签", 25)],
    "科技产品": [("手机", 3000), ("电脑", 5500), ("耳机", 400), ("显示器", 1200), ("平板", 2200)],
}

DEPTS = ["销售部", "市场部", "运营部", "技术部"]
TITLES = {
    "销售部": ["销售代表", "销售经理", "区域总监"],
    "市场部": ["市场专员", "市场经理", "市场总监"],
    "运营部": ["运营专员", "运营经理", "运营总监"],
    "技术部": ["工程师", "高级工程师", "技术总监"],
}
SHIP_MODES = ["标准配送", "二级配送", "一级配送", "当天达"]


def rand_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))


def build_shop(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    # 1) 客户表
    cur.execute("""
    CREATE TABLE customers (
        customer_id  INTEGER PRIMARY KEY,          -- 客户编号
        name         TEXT NOT NULL,                -- 姓名
        gender       TEXT,                          -- 性别
        age          INTEGER,                       -- 年龄
        segment      TEXT NOT NULL,                 -- 客户类型
        region       TEXT NOT NULL,                 -- 地区
        city         TEXT NOT NULL,                 -- 城市
        signup_date  TEXT NOT NULL                  -- 注册日期(ISO8601文本)
    );""")

    # 2) 商品表
    cur.execute("""
    CREATE TABLE products (
        product_id   INTEGER PRIMARY KEY,          -- 商品编号
        product_name TEXT NOT NULL,                -- 商品名称
        category     TEXT NOT NULL,                 -- 大类
        subcategory  TEXT NOT NULL,                 -- 子类别
        unit_price   REAL NOT NULL,                 -- 标准单价
        unit_cost    REAL NOT NULL                  -- 单位成本
    );""")

    # 3) 员工表（manager_id 指向本表 -> 自关联，专门用于 SELF JOIN / 递归）
    cur.execute("""
    CREATE TABLE employees (
        employee_id  INTEGER PRIMARY KEY,          -- 员工编号
        name         TEXT NOT NULL,                -- 姓名
        department   TEXT NOT NULL,                 -- 部门
        title        TEXT NOT NULL,                 -- 职位
        region       TEXT NOT NULL,                 -- 负责地区
        hire_date    TEXT NOT NULL,                 -- 入职日期
        salary       REAL NOT NULL,                 -- 月薪
        manager_id   INTEGER REFERENCES employees(employee_id)  -- 直属上级
    );""")

    # 4) 订单主表（一张订单一行）
    cur.execute("""
    CREATE TABLE orders (
        order_id     INTEGER PRIMARY KEY,          -- 订单编号
        customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
        order_date   TEXT NOT NULL,                 -- 下单日期
        ship_date    TEXT NOT NULL,                 -- 发货日期
        ship_mode    TEXT NOT NULL,                 -- 配送方式
        region       TEXT NOT NULL,                 -- 地区
        city         TEXT NOT NULL                   -- 城市
    );""")

    # 5) 订单明细表（一张订单含多个商品 -> 多行）
    cur.execute("""
    CREATE TABLE order_items (
        item_id      INTEGER PRIMARY KEY,          -- 明细编号
        order_id     INTEGER NOT NULL REFERENCES orders(order_id),
        product_id   INTEGER NOT NULL REFERENCES products(product_id),
        quantity     INTEGER NOT NULL,             -- 数量
        discount     REAL NOT NULL DEFAULT 0,      -- 折扣率 0~0.8
        sales        REAL NOT NULL,                 -- 销售额(折后)
        profit       REAL NOT NULL                  -- 利润
    );""")

    # ---- 灌数据：客户 ----
    customers = []
    for cid in range(1, 301):
        region = random.choice(REGIONS)
        city = random.choice(CITIES[region])
        name = random.choice(SURNAMES) + random.choice(GIVEN)
        customers.append((cid, name, random.choice(GENDERS), random.randint(18, 65),
                          random.choices(SEGMENTS, weights=[6, 3, 2])[0],
                          region, city, rand_date(date(2021, 1, 1), date(2024, 12, 31)).isoformat()))
    cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)", customers)

    # ---- 灌数据：商品 ----
    products = []
    pid = 0
    for category, subs in CATALOG.items():
        for sub, base in subs:
            for k in range(4):  # 每个子类别4款
                pid += 1
                price = round(base * random.uniform(0.7, 1.6), 2)
                cost = round(price * random.uniform(0.45, 0.8), 2)
                products.append((pid, f"{sub}-{k + 1:02d}号", category, sub, price, cost))
    cur.executemany("INSERT INTO products VALUES (?,?,?,?,?,?)", products)

    # ---- 灌数据：员工（先建各部门总监，再建经理，再建专员，形成层级）----
    employees = []
    eid = 0
    # 总经理（无上级）
    eid += 1
    employees.append((eid, "张总", "管理层", "总经理", "全国",
                      date(2018, 3, 1).isoformat(), 60000, None))
    gm = eid
    for dept in DEPTS:
        eid += 1
        director = eid
        employees.append((eid, f"{dept[:2]}总监", dept, TITLES[dept][2], "全国",
                          rand_date(date(2018, 1, 1), date(2020, 1, 1)).isoformat(),
                          random.randint(35000, 45000), gm))
        # 每个地区一个经理
        managers = []
        for region in REGIONS:
            eid += 1
            employees.append((eid, f"{region}{dept[:2]}经理", dept, TITLES[dept][1], region,
                              rand_date(date(2019, 1, 1), date(2022, 1, 1)).isoformat(),
                              random.randint(18000, 26000), director))
            managers.append((eid, region))
        # 每个经理带 1~2 个专员/工程师
        for mgr, region in managers:
            for _ in range(random.randint(1, 2)):
                eid += 1
                title = TITLES[dept][0]
                employees.append((eid, random.choice(SURNAMES) + random.choice(GIVEN),
                                  dept, title, region,
                                  rand_date(date(2021, 1, 1), date(2025, 6, 30)).isoformat(),
                                  random.randint(7000, 15000), mgr))
    cur.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?,?,?)", employees)

    # ---- 灌数据：订单 + 明细 ----
    item_id = 0
    order_rows = []
    item_rows = []
    for oid in range(1, 2601):
        cust = random.choice(customers)
        cust_id, _, _, _, _, region, city, _ = cust
        odate = rand_date(date(2022, 1, 1), date(2025, 12, 28))
        sdate = odate + timedelta(days=random.randint(1, 6))
        ship_mode = random.choices(SHIP_MODES, weights=[6, 3, 2, 1])[0]
        order_rows.append((oid, cust_id, odate.isoformat(), sdate.isoformat(),
                           ship_mode, region, city))
        for _ in range(random.randint(1, 4)):
            item_id += 1
            prod = random.choice(products)
            p, _, _, _, price, cost = prod[0], prod[1], prod[2], prod[3], prod[4], prod[5]
            qty = random.randint(1, 6)
            discount = random.choices([0, 0.1, 0.2, 0.4, 0.6], weights=[6, 4, 3, 2, 1])[0]
            sales = round(qty * price * (1 - discount), 2)
            profit = round(sales - qty * cost, 2)
            item_rows.append((item_id, oid, p, qty, discount, sales, profit))
    cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", order_rows)
    cur.executemany("INSERT INTO order_items VALUES (?,?,?,?,?,?,?)", item_rows)

    # 建几个常用索引（教学里会讲为什么）
    cur.execute("CREATE INDEX idx_items_order ON order_items(order_id);")
    cur.execute("CREATE INDEX idx_items_product ON order_items(product_id);")
    cur.execute("CREATE INDEX idx_orders_customer ON orders(customer_id);")
    cur.execute("CREATE INDEX idx_orders_date ON orders(order_date);")

    conn.commit()
    for t in ["customers", "products", "employees", "orders", "order_items"]:
        n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  shop.db.{t:12s} {n} 行")
    conn.close()


# ----------------------------------------------------------------------------
# 二、构建 superstore.db（把已有 CSV 导入 SQLite）
# ----------------------------------------------------------------------------
def build_superstore(path: str, csv_path: str) -> None:
    if not os.path.exists(csv_path):
        print(f"  跳过 superstore.db：找不到 {csv_path}")
        return
    if os.path.exists(path):
        os.remove(path)
    df = pd.read_csv(csv_path, encoding="utf-8")
    # 列名改成对 SQL 友好的英文蛇形命名（原中文任务书里有逐列含义对照）
    rename = {
        "Row ID": "row_id", "Order ID": "order_id", "Order Date": "order_date",
        "Ship Date": "ship_date", "Ship Mode": "ship_mode", "Customer ID": "customer_id",
        "Customer Name": "customer_name", "Segment": "segment", "Country": "country",
        "City": "city", "State": "state", "Postal Code": "postal_code", "Region": "region",
        "Product ID": "product_id", "Product Name": "product_name", "Category": "category",
        "Sub-Category": "subcategory", "Sales": "sales", "Quantity": "quantity",
        "Discount": "discount", "Profit": "profit",
    }
    df = df.rename(columns=rename)
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m-%d")
    df["ship_date"] = pd.to_datetime(df["ship_date"]).dt.strftime("%Y-%m-%d")
    conn = sqlite3.connect(path)
    df.to_sql("orders", conn, index=False, if_exists="replace")
    conn.execute("CREATE INDEX idx_ss_order ON orders(order_id);")
    conn.execute("CREATE INDEX idx_ss_date ON orders(order_date);")
    conn.commit()
    print(f"  superstore.db.orders {len(df)} 行，{df['order_id'].nunique()} 张订单")
    conn.close()


if __name__ == "__main__":
    print("构建数据库 ->", HERE)
    build_shop(os.path.join(HERE, "shop.db"))
    ss_csv = os.path.join(HERE, "..", "..", "05_实战项目", "superstore", "Superstore.csv")
    build_superstore(os.path.join(HERE, "superstore.db"), os.path.abspath(ss_csv))
    print("完成。")
