# 项目 3 · 用 Scrapy 做全站分页采集

> 业务背景：项目 1 你用 requests + BeautifulSoup 手搓了一遍。这次升级到 Scrapy，
> 体会“框架帮你管并发、管队列、管流水线”的感觉。目标仍是练习站
> `https://books.toscrape.com/`。
>
> 重点不是跑通，而是**把 12 课讲的架构真正用一遍**：Spider、Item、Pipeline、settings。
>
> **前置知识**：先学完 12（Scrapy 框架六组件）。本项目把它从“看懂”变成“亲手建一个工程”。

---

## 任务目标

用 `scrapy startproject` 建一个标准 Scrapy 工程，写一个 Spider 抓全站书名+价格，
用 Pipeline 落盘为 JSON Lines。

---

## 分模块任务

### 模块 A · 创建工程
- [ ] 用 `scrapy startproject bookscraper` 建工程。
- [ ] 浏览自动生成的目录结构，给每个文件写一句注释（items / pipelines / settings / spiders）。

```bash
# TODO: scrapy startproject bookscraper
# TODO: cd bookscraper && scrapy genspider book books.toscrape.com
```

### 模块 B · 定义 Item
- [ ] 在 `items.py` 里定义 `BookItem`，字段：title、price、detail_url。

```python
# TODO: class BookItem(scrapy.Item): ...
```

### 模块 C · 写 Spider
- [ ] `start_urls` 指向第 1 页。
- [ ] `parse()` 里用 `response.css()` 提取每本书，`yield BookItem(...)`。
- [ ] 从“下一页”链接 `yield scrapy.Request(...)`，让框架自动翻页。

```python
# TODO: def parse(self, response):
# TODO:     for 每本书: yield BookItem(...)
# TODO:     next_page = response.css('li.next a::attr(href)').get()
# TODO:     if next_page: yield response.follow(next_page, callback=self.parse)
```

### 模块 D · 写 Pipeline
- [ ] 在 `pipelines.py` 写一个 Pipeline，把每个 Item 写成 JSON Lines。
- [ ] 在 `settings.py` 的 `ITEM_PIPELINES` 里注册它。

```python
# TODO: class JsonlPipeline: open_spider / process_item / close_spider
```

### 模块 E · 调 settings
- [ ] 设 `ROBOTSTXT_OBEY = True`。
- [ ] 设 `DOWNLOAD_DELAY = 1.0`。
- [ ] 把 `CONCURRENT_REQUESTS` 调到一个对练习站友好的值（如 8）。

```python
# TODO: 在 settings.py 配置上述三项
```

### 模块 F · 运行与验证
- [ ] `scrapy crawl book` 跑起来。
- [ ] 检查输出的 JSONL 文件行数（全站约 1000 本书）。

```bash
# TODO: scrapy crawl book
```

---

## 交付规范

1. 整个 Scrapy 工程目录（可打包）。
2. 产出的 `books.jsonl`。
3. 一段对比：和项目 1 的手搓脚本相比，Scrapy 让你少写了哪些代码、多理解了什么。

## 检查点（自查）

- [ ] 是靠 `yield Request` / `response.follow` 自动翻完所有页，不是手写 while 循环。
- [ ] 数据从 Pipeline 落盘，不是在 `parse()` 里直接 open 写文件。
- [ ] settings 里开了 robots 遵守和延迟。
- [ ] JSONL 每行一个合法 JSON 对象，行数接近全站书籍数。

---

## 提示（卡住时再看）

- `response.follow(next_page, callback=self.parse)` 会自动处理相对 URL 并把控制权交回 parse。
- CSS 扩展语法：`::text` 取文本、`::attr(href)` 取属性。
- 先用 `scrapy shell "https://books.toscrape.com/"` 把选择器试对，再写进 Spider。
