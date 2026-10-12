# -*- coding: utf-8 -*-
"""
云南民族大学官网「通知公告」爬虫演示
完整流程：翻页抓取 -> 解析(日期/标题/链接) -> 存CSV -> pandas分析 -> matplotlib画图
"""
import re, time, requests, urllib3
from bs4 import BeautifulSoup
from requests.compat import urljoin
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

urllib3.disable_warnings()
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = "https://www.ymu.edu.cn/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Referer": BASE,
}
OUT_DIR = r"C:\Users\千禧\Doubao\chats\2026-09-23\new-chat\AI学习\08_爬虫\爬学校通知"


def parse_list_page(html, page_url):
    """解析一页列表：返回(通知行列表, 下一页URL)"""
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for a in soup.find_all("a", href=True):
        if "info/" not in a["href"]:
            continue
        text = a.get_text(strip=True)
        m = re.match(r"^(\d{2})\.(\d{2})(\d{4})(.*)$", text)  # 标题开头的 09.292026
        if not m:
            continue
        mm, dd, yyyy, title = m.groups()
        rows.append({
            "日期": f"{yyyy}-{mm}-{dd}",
            "标题": title.strip(),
            "链接": urljoin(page_url, a["href"]),
        })
    next_url = None
    for a in soup.find_all("a", href=True):
        if a.get_text(strip=True) == "下页":
            next_url = urljoin(page_url, a["href"])
    return rows, next_url


all_rows = []
url = BASE + "tzgg.htm"
for page in range(15):                       # 最多抓15页，慢速礼貌抓取
    r = requests.get(url, headers=HEADERS, timeout=20, verify=False)
    r.encoding = r.apparent_encoding
    rows, next_url = parse_list_page(r.text, url)
    all_rows.extend(rows)
    print(f"第{page+1:2d}页  {url}  -> {len(rows)}条")
    if not next_url or next_url == url:
        break
    url = next_url
    time.sleep(1)                            # 每停1秒，不给学校服务器添负担

df = pd.DataFrame(all_rows).drop_duplicates(subset=["链接"])
df["日期"] = pd.to_datetime(df["日期"])
df = df.sort_values("日期", ascending=False).reset_index(drop=True)
csv_path = OUT_DIR + r"\通知列表.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"\n共抓到 {len(df)} 条，已存 {csv_path}")
print("\n=== 最近10条通知 ===")
print(df.head(10)[["日期", "标题"]].to_string(index=False))

# 按标题关键词分类
def classify(t):
    if any(k in t for k in ["招标", "采购", "磋商", "竞价"]): return "招标/采购"
    if any(k in t for k in ["中标", "成交", "结果公告", "结果公示"]): return "中标/结果"
    if any(k in t for k in ["招聘", "聘用", "岗位"]): return "招聘"
    if any(k in t for k in ["公示", "公示"]): return "公示"
    if ("学术" in t) or ("讲座" in t): return "学术/讲座"
    return "其他"

df["类别"] = df["标题"].apply(classify)
print("\n=== 通知类型分布 ===")
print(df["类别"].value_counts().to_string())

df["月份"] = df["日期"].dt.to_period("M").astype(str)
monthly = df.groupby("月份").size()

# 画图：左=类别分布，右=每月数量
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
df["类别"].value_counts().plot.barh(ax=axes[0], color="#4C72B0")
axes[0].set_title("通知类型分布")
axes[0].set_xlabel("条数")
monthly.plot.bar(ax=axes[1], color="#DD8452")
axes[1].set_title("每月发布通知数量")
axes[1].set_ylabel("条数")
plt.tight_layout()
png_path = OUT_DIR + r"\通知分析.png"
plt.savefig(png_path, dpi=120)
print(f"\n图已保存: {png_path}")
