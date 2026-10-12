# 项目 1 · 静态列表站采集 → 清洗 → SQLite 入库 → SQL 分析

> 业务背景：你要给一个“图书价格观察”小工具攒一份数据集。目标站是 Scrapy 官方提供的练习站
> `https://books.toscrape.com/`（公开允许练习，无登录、无个人信息）。你要写一个命令行爬虫，
> 把全站书籍的标题、价格、星级、库存抓下来，干净地存进 SQLite，再用 SQL 做几个有意思的分析。
>
> **合规提醒**：这是专门的练习站；即便如此，也要加请求间隔（建议 ≥1 秒），别高并发狂刷。
>
> **前置知识**：先学完 01~05（请求基础）、06~10（HTML 解析与 CSV/SQLite 存储），以及 13（合规红线）。
> 本项目是把前面学的零件串成一条完整流水线。

---

## 数据字典（每张表/每条记录应包含的字段）

`books` 表：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| title | TEXT UNIQUE | 书名（去重键） |
| price | REAL | 人民币价格（去掉货币符号后的数字） |
| star | INTEGER | 星级 1~5 |
| upc | TEXT | 详情页里的商品 UPC（从详情页抓） |
| detail_url | TEXT | 详情页完整 URL |
| crawled_at | TEXT | 抓取时间（ISO 字符串） |

---

## 分模块任务

### 模块 A · 列表页翻页采集
- [ ] 从第 1 页 `https://books.toscrape.com/catalogue/page-1.html` 开始。
- [ ] 解析每页所有书籍卡片，提取 title、价格文本、星级 class。
- [ ] 找到“下一页”链接，用 `urljoin` 补全，循环直到没有下一页。
- [ ] 全程加 `time.sleep(1)` 级别的礼貌延迟；用 `requests.Session()`。

```python
# TODO: 写一个函数 parse_list_page(html) -> list[dict]
# TODO: 写主循环：从 page-1 开始，跟随 next 链接翻完所有页
```

### 模块 B · 详情页补全（可选加分）
- [ ] 从列表页拿到每本书的 `detail_url`，访问详情页抓 `upc`。
- [ ] 注意详情页 URL 是相对路径，要补全。
- [ ] 详情页请求也要限速。

```python
# TODO: 写 fetch_upc(detail_url) -> str
```

### 模块 C · 清洗与去重
- [ ] 价格 `"¥51.77"` → float。
- [ ] 星级 class `"Three"` → 整数 3。
- [ ] 按 `title` 去重。

```python
# TODO: 写 clean_record(raw) -> dict
```

### 模块 D · SQLite 落盘
- [ ] 建 `books` 表，`title` 设 UNIQUE。
- [ ] 用**参数化** `INSERT OR IGNORE` 写入（不要 f-string 拼 SQL）。
- [ ] 让脚本可以重复运行：第二次跑不应产生重复行。

```python
# TODO: 写 init_db() 和 save_records(records)
```

### 模块 E · SQL 分析
用 SQL 回答下面问题（在脚本里打印结果，或单独写一个分析脚本）：
- [ ] 一共抓了多少本书？
- [ ] 价格最高的 10 本书是哪些？
- [ ] 平均价格、价格中位数（可用 AVG + 排序近似）。
- [ ] 按星级分组，每个星级各有多少本？
- [ ] 价格低于 30 元的书里，星级 ≥ 4 的有几本？

```python
# TODO: 写若干 SELECT 语句完成上述分析
```

---

## 交付规范

1. 一个 `project1_crawler.py`（或 notebook），可重复运行。
2. 产出 `books.db`（SQLite 文件）。
3. 一段简短说明：你抓了多少页、多少本书、总耗时、平均每本书请求间隔。
4. 把 SQL 分析结果贴出来。

## 检查点（自查）

- [ ] 第二次运行脚本，数据库行数不增加（增量/去重生效）。
- [ ] 价格列是 REAL，能直接 `ORDER BY price`。
- [ ] 全程有请求延迟，没有被 `429`。
- [ ] 没有抓任何个人信息、没有绕登录。

---

## 提示（卡住时再看）

- 列表页选择器：书籍卡片在 `article.product_pod` 里；标题 `h3 a`；价格 `p.price_color`；星级 `p.star-rating` 的第二个 class。
- 下一页在 `li.next a::attr(href)`。
- 详情页 UPC 在 `table.table tr:first-of-type td`。
- 完整可运行参考见同目录 `项目1_参考答案.md`（**先自己做，卡住再看**）。
