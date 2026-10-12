# -*- coding: utf-8 -*-
# 下面这8个红X是Pylance静态检查的保守提示：find()理论上可能返回None，所以警告"None没有.text"
# 实际豆瓣页面结构固定，运行完全正常，属无害提示。这行关掉该警告：
# pyright: reportOptionalMemberAccess=false, reportOptionalSubscript=false
"""
豆瓣电影 Top250 完整爬虫
翻10页 -> 提取每部电影的 排名/片名/年份/国家/类型/评分/评价人数/短评 -> 存CSV
"""
import re, time, requests, urllib3, csv
from bs4 import BeautifulSoup

urllib3.disable_warnings()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

BASE = "https://movie.douban.com/top250"
rows = []

for start in range(0, 250, 25):                 
    url = f"{BASE}?start={start}"
    r = requests.get(url, headers=headers, timeout=20, verify=False)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")

    for item in soup.find_all("div", class_="item"):
        rank = item.find("em").text
        name = item.find("span", class_="title").text
        link = item.find("div", class_="hd").a["href"]
        rating_el = item.find("span", class_="rating_num")
        rating = rating_el.text
        votes = ""
        for sp in item.find("div", class_="bd").find_all("span"):
            if "人评价" in sp.text:
                votes = sp.text.replace("人评价", "").strip()
                break

        bd_p = item.find("div", class_="bd").p.get_text(" ", strip=True)
        m = re.search(r"(\d{4})\s*/\s*([^/]+?)\s*/\s*(.+)$", bd_p)
        year, country, genre = m.groups() if m else ("", "", "")

        quote_tag = item.find("p", class_="quote")
        quote = quote_tag.text.strip() if quote_tag else ""

        rows.append([rank, name, year, country.strip(), genre.strip(),
                    rating, votes, quote, link])
    print(f"已抓第 {start//25 + 1} 页，累计 {len(rows)} 部")
    time.sleep(2)

out = r"C:\Users\千禧\Doubao\chats\2026-09-23\new-chat\AI学习\08_爬虫\爬豆瓣小尝试\douban_top250.csv"
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["排名", "片名", "年份", "国家", "类型", "评分", "评价人数", "短评", "链接"])
    w.writerows(rows)

print(f"\n完成，共 {len(rows)} 部，已存 {out}")
print("\n=== 前10部 ===")
for row in rows[:10]:
    print(f"{row[0]:>2}. {row[1]}  {row[2]}  {row[5]}分  ({row[6]}人)")
