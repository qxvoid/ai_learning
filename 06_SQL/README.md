# 06_SQL · 系统学习指南

> 面向大一、C++ 竞赛出身、已会 Python/Pandas、SQL 不系统的学习者。
> 目标：**从“会一点点”到“能独立做业务分析 + 过面试 SQL 关”**。所有教学都围绕本地 `data/shop.db` 真实库展开，讲底层原理、与 Pandas 类比、讲易错点，不堆语法。

---

## 一、路线图（推荐学习顺序）

| 顺序 | Notebook | 你会学会什么 |
|---|---|---|
| 00 | `00_环境与关系模型.ipynb` | 数据库是什么、主键外键、范式直觉、NULL 三值逻辑、两种跑 SQL 的方式 |
| 01 | `01_SELECT基础与过滤.ipynb` | SELECT / 别名 / DISTINCT / WHERE 全套 / ORDER BY / LIMIT / CASE |
| 02 | `02_聚合与分组_GROUP_BY_HAVING.ipynb` | 三种 COUNT、SUM/AVG、GROUP BY、HAVING、SQL 执行顺序 |
| 03 | `03_多表连接_JOIN.ipynb` | INNER/LEFT/RIGHT/FULL/CROSS、自连接、行数膨胀陷阱 |
| 04 | `04_子查询与集合操作.ipynb` | 标量/列/相关子查询、EXISTS、派生表、UNION/EXCEPT |
| 05 | `05_窗口函数_重点专题.ipynb` | **面试最高频**：ROW_NUMBER/RANK、LAG/LEAD、累计与移动平均 |
| 06 | `06_进阶_CTE_视图_索引_事务.ipynb` | CTE/递归、视图、B-Tree 索引、事务 ACID、SQL 注入 |
| 实战 | `项目/SQL零售经营分析项目_任务书.ipynb` | 独立完成完整经营分析 |
| 对照 | `项目/SQL零售经营分析项目_参考答案.ipynb` | 卡住再看 |

**学法**：每课先读 Markdown 概念 → 跑通代码 → 做文末练习。第 5 课（窗口函数）花最多时间。全部做完后，独立完成项目任务书，再对答案。

---

## 二、环境验证

本模块**零额外安装**，用你已有的 `ai_learn` 环境即可。打开 PowerShell 验证：

```powershell
& "C:\Users\Public\miniconda3\envs\ai_learn\python.exe" -c "import sqlite3,pandas; print('sqlite', sqlite3.sqlite_version, 'pandas', pandas.__version__)"
```

应看到类似 `sqlite 3.53.4 pandas 2.3.3`。SQLite 3.25+ 才完整支持窗口函数，你的 3.53.4 完全够用。

数据已就绪，无需重建：

```
data/shop.db         规范化业务库（customers/products/employees/orders/order_items）
data/superstore.db   你之前 EDA 过的 Superstore 单表数据（9994 行）
data/build_databases.py  建库脚本（种子 20260913，想重建可跑）
```

---

## 三、两种跑 SQL 的方式

### 方式 A：Python（本课程 notebook 用法）

每个教学 notebook 开头都有这段“启动样板”，连 `shop.db` 并包装 `q(sql)` 函数，把查询结果直接返回成 Pandas DataFrame：

```python
import sqlite3, pandas as pd
conn = sqlite3.connect(r"C:\Users\千禧\Doubao\chats\2026-09-23\new-chat\AI学习\06_SQL\data\shop.db")
def q(sql): return pd.read_sql_query(sql, conn)

q("SELECT * FROM products LIMIT 5")
```

> 为什么用 Pandas 显示？因为你已经熟 DataFrame，不用再学一套表格打印 API。底层仍是 `sqlite3` 游标。

### 方式 B：VSCode SQLite 扩展（边写边看）

你已装 `alexcvzz.vscode-sqlite`：

1. 左侧文件栏**右键 `data/shop.db`** → `Open Database`；
2. `SQLITE EXPLORER` 里点表名直接看数据；
3. `Ctrl+Shift+P` → `SQLite: New Query` 开 `.sql` 文件，光标放进 SQL，右键 `Run Query`；
4. 关闭：命令面板搜 `SQLite: Close All Databases`。

建议：学语法用扩展（所见即所得），做项目/沉淀用 notebook（可复现、可传 GitHub）。

---

## 四、MySQL / PostgreSQL 的定位，以及“什么时候迁”

| 数据库 | 定位 | 你现在要不要学 |
|---|---|---|
| **SQLite** | 嵌入式单文件库，零配置 | **本模块全程用它**，先把语言学透 |
| **MySQL** | 互联网后端最流行 | 找后端实习时再补，方言差异小 |
| **PostgreSQL** | 功能最强的开源库 | 数据/算法岗首选，窗口函数文档最好 |

**核心理念**：SQL 这门语言（SELECT/JOIN/窗口函数）是**长期稳定核心**，十年后写法不变；具体哪个数据库是**会变的工具**。先用 SQLite 把语言学透，等岗位明确了再按需求切。语法 90% 通用，剩下 10%（分页、日期函数、自增主键）查文档即可。

**什么时候真的需要换成 MySQL/PG**：
- 要做真实后端、多用户并发写（SQLite 写锁太粗）；
- 公司岗位明确要求；
- 需要 JSON、GIS、复杂类型等高级特性。

在那之前，**不要花时间装 MySQL 服务**——把时间花在写对 SQL 上收益高得多。

---

## 五、配套外部资源（浏览器里练手）

- SQLBolt（交互式入门）：https://sqlbolt.com/
- SQLZoo：https://sqlzoo.net/
- Select Star SQL（叙事极佳）：https://selectstarsql.com/
- Mode SQL 教程：https://mode.com/sql-tutorial/
- LeetCode 数据库：https://leetcode.com/problemset/database/
- DataLemur（面试真题）：https://datalemur.com/
- 窗口函数官方文档：https://www.sqlite.org/windowfunctions.html

---

## 六、目录结构

```
06_SQL/
├── README.md                     ← 本文件
├── 00_环境与关系模型.ipynb
├── 01_SELECT基础与过滤.ipynb
├── 02_聚合与分组_GROUP_BY_HAVING.ipynb
├── 03_多表连接_JOIN.ipynb
├── 04_子查询与集合操作.ipynb
├── 05_窗口函数_重点专题.ipynb
├── 06_进阶_CTE_视图_索引_事务.ipynb
├── data/
│   ├── shop.db  superstore.db  build_databases.py
└── 项目/
    ├── SQL零售经营分析项目_任务书.ipynb      ← 纯任务，留空
    └── SQL零售经营分析项目_参考答案.ipynb    ← 先独立做，卡住再看
```
