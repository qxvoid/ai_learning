# AI 学习地图（总目录）

> 这是整个 AI 自学路线的**总入口**。目标：从已有的 Python 数据处理基础，系统补齐 **SQL（求职硬门槛）→ Git/GitHub（工程基本功 + 读懂开源源码）→ 网络爬虫（兴趣 + 真实实战）**，并为后续机器学习、深度学习、后端服务铺好路。
>
> 所有新内容都**优先取材于 GitHub 高星开源项目与官方文档**，消化后用中文重写，每篇文末标注来源 URL，并区分「长期稳定的核心知识」与「会变的工具版本」。

---

## 一、目录总览（按编号即推荐主线顺序）

```
AI学习/
├── 01_NumPy/                 【已完成】数值计算基础（00~07，含广播升维专题、生命游戏项目）
├── 02_Pandas/                【已完成】数据处理（01~07，含 2.x 新特性与练习卷）
├── 03_可视化/                 【预留】Matplotlib 进阶 / Seaborn / 交互可视化（待补）
├── 04_Python小项目/           【已完成】贪吃蛇/扫雷/俄罗斯方块/文字冒险/Wordle
├── 05_实战项目/               【1 完成 · 1 进行中】MovieLens EDA（已批改）、Superstore EDA
├── 06_SQL/                   【本次新增 · 最高优先级】7 课教学 + 零售经营分析项目
├── 07_Git与GitHub/           【本次新增 · 尽早掌握】Git/GitHub 文档 + 开源源码阅读路线
├── 08_爬虫/                  【本次新增 · 兴趣可并行】6 课教学 + 3 个实战项目
└── 09_算法可视化与AI游戏/      【已完成】寻路可视化器、AI 自动寻路贪吃蛇
```

> 编号说明：`09_算法可视化与AI游戏` 是早前的作品，本次整理时由 06 顺延为 09，以解决与 SQL 的编号冲突；内容未改动。

---

## 二、当前进度与下一步

| 模块 | 状态 | 说明 |
|---|---|---|
| NumPy / Pandas / Python 小项目 | ✅ 已完成 | 基础已打牢 |
| 实战项目 1 · MovieLens | ✅ 已完成并批改 | 第一个完整 EDA |
| 实战项目 2 · Superstore | 🟡 进行中 | **建议先把它独立做完**，再开新模块 |
| **06_SQL** | 🆕 全新，待学 | **本阶段主线，优先级最高** |
| **07_Git与GitHub** | 🆕 全新，待学 | 前几天先掌握，便于上传已有项目 |
| **08_爬虫** | 🆕 全新，待学 | 兴趣导向，可与 SQL 并行 |
| 03_可视化 | ⬜ 预留 | 学完 SQL/爬虫后用 Seaborn 补齐 |

---

## 三、三大新模块怎么学（先后顺序与配合）

### 推荐四周节奏（可按课业弹性调整）

**第 0 步（1~2 天）：收尾 + 装好“工程基本功”**
1. 把 `05_实战项目/02_Superstore` 独立做完。
2. 读 `07_Git与GitHub/文档/01_Git是什么与本地工作流.md`，边读边敲。
3. 读 `07_Git与GitHub/文档/02_GitHub远程仓库与上传项目.md`，**把 MovieLens、Superstore 两个项目真正上传到你的 GitHub**（这是最好的作品集起点）。

**第 1~3 周（主线）：系统学 SQL**
- 按 `06_SQL/` 的 `00 → 06` 顺序逐课推进，每课先读概念、再跑代码、做文末练习。
- **第 5 课「窗口函数」是面试最高频，花最多时间**。
- 全部学完后，**独立完成** `06_SQL/项目/SQL零售经营分析项目_任务书.ipynb`，卡住再看同目录参考答案。

**并行（兴趣）：爬虫**
- 爬虫与 SQL **不冲突，天然互补**：爬虫负责「取数据」，SQL 负责「查数据」。
- 学完爬虫第 03 课 + SQL 基础后，就能跑通完整数据链路：
  ```
  requests/Scrapy 采集 → 清洗去重 → 存入 SQLite → 用 SQL 做分析
  ```
- 时间紧就把爬虫放在周末/课余，SQL 始终是主线。

**长期（贯穿之后）：读懂开源源码**
- 从 `07_Git与GitHub/源码阅读/00_源码阅读方法论.md` 学方法，用一个下午读完第一个项目 `pallets/click`。
- 之后**配合正在学的内容**推进：学爬虫读 `requests`/`scrapy`，学后端读 `Flask`/`FastAPI`，学机器学习读 `scikit-learn`，最终长线读 `PyTorch`。

### 一图看懂模块关系

```
                    ┌──────────────────────────────┐
                    │  07_Git与GitHub（地基/协作）   │
                    │  版本控制 · 上传项目 · 读源码  │
                    └──────────────┬───────────────┘
                                   │ 贯穿全程
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
┌────────────────┐        ┌────────────────┐        ┌────────────────────┐
│ 08_爬虫（取数） │  入库  │  SQLite 数据库  │  查询  │ 06_SQL（查数/分析） │
│ requests/Scrapy │──────▶│  (本地 .db)     │──────▶│ 窗口函数/经营分析   │
└────────────────┘        └────────────────┘        └────────────────────┘
                                                          │
                                                          ▼
                                            后续：可视化 → ML → DL → AI 服务
```

---

## 四、统一环境（已全部配置并实测，2026-10-09）

**Conda 环境 `ai_learn`**，解释器：`C:\Users\Public\miniconda3\envs\ai_learn\python.exe`（Python 3.10.21）

| 类别 | 包 / 工具 | 版本 | 用途 |
|---|---|---|---|
| 数据处理 | numpy / pandas / matplotlib | 2.2.5 / 2.3.3 / 3.10.9 | 已有 |
| 数据库 | sqlite3（Python 内置） | SQLite 3.53.4 | SQL 教学，零配置，支持窗口函数 |
| 爬虫基础 | requests / beautifulsoup4 / lxml | 2.34.2 / 4.15.0 / 6.1.3 | HTTP、HTML 解析 |
| 爬虫进阶 | scrapy / selenium / playwright | 2.19.0 / 4.50.0 / 已装+Chromium | 框架、动态渲染 |
| VSCode 扩展 | Python 全家桶、Jupyter、Code Runner、**SQLite(alexcvzz)** | — | 已装 |
| 版本控制 | Git for Windows | 2.53.0 | 已装 |

**Git 账号状态（本机实测）**：提交身份已配置为 `qxvoid` / `2854640226@qq.com`，默认分支 `main`；尚无 SSH 密钥，新手先走 **HTTPS + Personal Access Token**（详见 07 模块第 02 篇）。该 QQ 邮箱会随提交公开，文档里给了改用 GitHub 隐私邮箱的方法。

### 环境验证命令（PowerShell）

```powershell
$py = "C:\Users\Public\miniconda3\envs\ai_learn\python.exe"
& $py -c "import sqlite3,requests,bs4,lxml,scrapy,selenium,playwright, numpy,pandas; print('env OK, sqlite', sqlite3.sqlite_version)"
git --version
```

> 更详细的 Notebook/内核使用与排错，见上一级目录的 `环境与Notebook流程速查.md`。

---

## 五、学习方法约定（这套资料怎么用）

1. **教学 notebook**：结构为「概念地图 → 原理/执行机制 → 与 C++/Pandas 类比 → 可运行代码 → 易错点 → 小结 → 来源与延伸」。请逐格运行，不要只看。
2. **练习与项目**：任务书**只给题目、留空（`# TODO`），不含答案**；参考答案单独成文，**先独立完成，卡住再看**。
3. **重原理、轻记忆**：SQL 语法、HTTP 原理、Git 的三区模型是长期稳定核心；具体框架版本会变，遇到差异查官方文档即可。
4. **以开源社区为师**：善用 GitHub 搜索、官方文档、Issue；每学一个框架就去看它的仓库 README、docs 和源码结构。
5. **成就感驱动**：每个项目都做到“能跑、能看懂、能上传 GitHub、能讲给别人听”，沉淀为作品集。

---

## 六、核心外部资源（全部为高星/官方，详见各模块）

- SQL：[SQLBolt](https://sqlbolt.com/) · [SQLZoo](https://sqlzoo.net/) · [Mode SQL 教程](https://mode.com/sql-tutorial/) · [LeetCode 数据库](https://leetcode.com/problemset/database/) · [DataLemur](https://datalemur.com/) · [SQLite 窗口函数文档](https://www.sqlite.org/windowfunctions.html)
- 真实数据库进阶：[Chinook](https://github.com/lerocha/chinook-database) · [Northwind-SQLite](https://github.com/jpwhite3/northwind-SQLite3) · [Sakila](https://dev.mysql.com/doc/sakila/en/)
- Git：[Pro Git 中文书](https://git-scm.com/book/zh/v2) · [GitHub 中文文档](https://docs.github.com/zh) · [firstcontributions](https://github.com/firstcontributions/first-contributions) · [gitignore 模板](https://github.com/github/gitignore)
- 爬虫：[Scrapy(约64.7k★)](https://github.com/scrapy/scrapy) · [learn_python3_spider(约22.2k★)](https://github.com/wistbean/learn_python3_spider) · [PythonSpiderNotes](https://github.com/lining0806/PythonSpiderNotes) · [Playwright Python](https://playwright.dev/python/docs/intro) · [Robots 协议 RFC 9309](https://www.rfc-editor.org/rfc/rfc9309)
- 源码阅读路线（星数已实测）：见 `07_Git与GitHub/源码阅读/01_高星项目阅读路线.md`

---

## 七、后续路线预告（学完本阶段之后）

1. **可视化补齐**：Seaborn 统计绘图、交互式 Plotly，填满 `03_可视化/`。
2. **机器学习**：`scikit-learn`（先读其源码的统一 Estimator API），回归/分类/聚类/评估。
3. **深度学习**：PyTorch，神经网络 → CV/NLP，读 `nn.Module` 与 autograd 源码。
4. **后端与 AI 服务**：Flask / FastAPI，把模型包成 API；Docker 部署。
5. **工程素养**：持续读源码、给开源项目提 PR、维护自己的 GitHub 作品集。

> 学技术的顺序可以灵活，但**“基础打牢 + 动手做项目 + 用 GitHub 沉淀 + 读优秀源码”**这四件事贯穿始终。
