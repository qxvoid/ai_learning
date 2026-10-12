# 08 · Python 网络爬虫（零基础慢速版）

> 这份教程专门写给**会写 Python / C++ 控制台程序、但完全不懂网页**的你。
> 昨天的版本一次塞太多概念，现在全部**拆小、放慢**：一共 14 课（00~13），每课只讲一个新概念，跟着敲就能零卡顿上手。

---

## ⚠️ 动手前先读：合规红线（最高优先级）

爬虫是“替你去别人电脑上取东西”，所以**先有规矩，再学技术**。三条铁律：

1. **技术上能做 ≠ 合规上该做。** 会绕过反爬，不等于你被允许抓取。
2. **个人信息是红线。** 不抓姓名 / 手机号 / 身份证 / 人脸等（《个人信息保护法》）；不绕登录、不绕验证码、不盗用他人登录态（可能触及《网络安全法》）。
3. **对目标站保持克制。** 限速、限并发、见好就收；出现 `429` 或验证码就是“停手信号”，不是“再想想办法”。

练习**只用官方练习站和本地夹具**：`https://books.toscrape.com/`、`https://quotes.toscrape.com/`（Scrapy 官方专为练手搭建），以及本目录 `data\` 里的离线 HTML。不要拿电商 / 社交 / 教务处做并发练习。

---

## 学习路径（按编号顺序，一课一个概念）

### 第一阶段：看懂网页与第一次请求
| 课 | 文件 | 学什么 |
|---|---|---|
| 00 | `00_Web零基础前置.ipynb` | 互联网、客户端—服务器、从输入网址到看到页面的全过程、HTML、为什么 HTML 是一棵树、F12 工具 |
| 01 | `01_第一个GET请求.ipynb` | **pip install 和 import 的区别**、`requests.get`、状态码、响应文本 |

### 第二阶段：把请求写“像浏览器”
| 课 | 文件 | 学什么 |
|---|---|---|
| 02 | `02_查询参数与URL.ipynb` | 网址的结构、用查询参数向服务器传筛选条件 |
| 03 | `03_请求头与浏览器伪装.ipynb` | 请求头、User-Agent、为什么默认 Python 会被一些站点拒绝（结合你的豆瓣尝试） |
| 04 | `04_Cookie与Session.ipynb` | Cookie 是什么、Session 如何让服务器“认出”你 |
| 05 | `05_超时重试与编码.ipynb` | 超时、简单重试、中文乱码与编码 |

### 第三阶段：从 HTML 里把数据抠出来
| 课 | 文件 | 学什么 |
|---|---|---|
| 06 | `06_HTML结构与树.ipynb` | 把网页看成一棵多叉树（你的图论老本行） |
| 07 | `07_BeautifulSoup查找.ipynb` | 用 BeautifulSoup 的 find / find_all 找节点 |
| 08 | `08_CSS选择器.ipynb` | 用 CSS 选择器 `.class`、`#id` 精准定位 |
| 09 | `09_XPath.ipynb` | 另一种强大的定位语言 XPath |
| 10 | `10_数据存储_CSV与SQLite.ipynb` | 把数据存成 CSV / SQLite，参数化写入、去重 |

### 第四阶段：进阶
| 课 | 文件 | 学什么 |
|---|---|---|
| 11 | `11_动态渲染_Selenium_Playwright.ipynb` | 数据是 JavaScript 后加载的怎么办，用浏览器自动化拿到它 |
| 12 | `12_Scrapy框架.ipynb` | 成熟爬虫框架的六大组件与工程化写法 |
| 13 | `13_反爬与合规红线.ipynb` | robots.txt、反爬技术边界、法律与职业操守 |

> 学法：**逐格运行、亲手改、做每课最后的小练习**。一次学一课，别跳。解析课断网也能跑（用本地夹具）。

---

## 体系化实战项目（学完第三阶段再做）

在 `项目\` 目录，**任务书只给题目、留空，参考答案单独放（卡住再看）**：

1. **项目 1**：静态列表站采集 → 清洗 → 存入 SQLite → 用 SQL 分析（任务书 + 参考答案）。
2. **项目 2**：动态页面采集（任务书）。
3. **项目 3**：Scrapy 全站 / 分页采集（任务书）。

你自己的 `爬豆瓣小尝试\douban.py` 已保留，它是很好的起点：第 3 课会带你看懂为什么它可能拿不到 200、怎么改进。

---

## 环境验证（已全部装好）

统一使用 conda 环境 **ai_learn**，解释器：`C:\Users\Public\miniconda3\envs\ai_learn\python.exe`。

```powershell
$py = "C:\Users\Public\miniconda3\envs\ai_learn\python.exe"
& $py -c "import requests,bs4,lxml,scrapy,selenium,playwright; print('爬虫环境 OK')"
```

已实测：requests 2.34.2 / beautifulsoup4 4.15.0 / lxml 6.1.3 / scrapy 2.19.0 / selenium 4.50.0 / playwright + Chromium。

> 记住：**包装一次（pip install），但每个 notebook 开头都要 import**。详见第 1 课 1.0 节。

执行单本 notebook：
```powershell
& $py -m jupyter nbconvert --to notebook --execute --inplace "00_Web零基础前置.ipynb"
```

---

## 与 SQL 模块的联动

爬虫和 SQL 是一条完整数据链，建议两个模块一起学：

```
requests/Scrapy 采集 → 清洗去重 → 存入 SQLite（第10课）→ 用 SQL 做分析（06_SQL 模块）
```

---

## 目录结构

```
08_爬虫/
├── README.md                    ← 本文件
├── 00_Web零基础前置.ipynb
├── 01_第一个GET请求.ipynb
├── 02_查询参数与URL.ipynb
├── 03_请求头与浏览器伪装.ipynb
├── 04_Cookie与Session.ipynb
├── 05_超时重试与编码.ipynb
├── 06_HTML结构与树.ipynb
├── 07_BeautifulSoup查找.ipynb
├── 08_CSS选择器.ipynb
├── 09_XPath.ipynb
├── 10_数据存储_CSV与SQLite.ipynb
├── 11_动态渲染_Selenium_Playwright.ipynb
├── 12_Scrapy框架.ipynb
├── 13_反爬与合规红线.ipynb
├── data/                        ← 本地 HTML 夹具（离线解析用）
├── output/                      ← 运行后生成的 CSV / SQLite / JSONL
├── 项目/                        ← 3 个体系化项目（任务书 + 参考答案）
└── 爬豆瓣小尝试/douban.py         ← 你自己的第一次尝试（已保留）
```

---

## 来源与延伸

- Scrapy 官方仓库（约 64.7k★）：https://github.com/scrapy/scrapy ；文档：https://docs.scrapy.org
- requests 文档：https://requests.readthedocs.io
- BeautifulSoup 文档：https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- lxml 文档：https://lxml.de/
- Selenium 文档：https://www.selenium.dev/documentation/ ；Playwright Python：https://playwright.dev/python/
- MDN Web 入门（最权威的零基础前端资料）：https://developer.mozilla.org/zh-CN/docs/Learn
- Robots 协议 RFC 9309：https://www.rfc-editor.org/rfc/rfc9309
