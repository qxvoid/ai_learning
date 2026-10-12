# 02 · GitHub 远程仓库与上传项目

> 上一篇你已经能在本地管理版本历史了。但本地仓库只有你这台机器看得见，硬盘坏了就全没了，也没法展示给别人。GitHub 就是把你的 `.git/` 仓库在云端放一份，并加上社交、协作、展示功能。
>
> 这一篇结束时，你的 **MovieLens 电影分析** 和 **Superstore 超市经营分析** 两个项目会真正出现在你的 GitHub 主页上。

---

## 1. 注册与账号安全（5 分钟）

1. 打开 <https://github.com> ，点 Sign up。用一个你长期会用的邮箱（建议和你 `git config user.email` 一致）。
2. 用户名（Username）会成为你仓库地址的一部分，形如 `https://github.com/你的用户名`。想清楚再取，以后作品集、简历都挂它。
3. **两步验证（2FA）必开**：右上头像 → Settings → Password and authentication → Two-factor authentication。GitHub 账号一旦被盗，别人能用你的名字发恶意代码，2FA 是底线。
4. 建议在 Settings → Emails 里开启 “Keep my email addresses private”，它会给你一个 `ID+用户名@users.noreply.github.com` 的隐私邮箱。用这个邮箱来 `git config --global user.email`，你的真实邮箱就不会泄露在提交历史里。

> 本机现状（2026-10-09 实测）：还没有 SSH 密钥（`~/.ssh` 目录不存在），也没有任何凭证助手配置。下面二选一，推荐**新手先用 HTTPS + PAT**，最不容易卡住。

---

## 2. 连接 GitHub 的两种方式：HTTPS+PAT  vs  SSH

Git 要把本地仓库 push 到 GitHub，必须先证明“我是这个仓库的主人”。两种主流方式：

| | HTTPS + PAT | SSH key |
|---|---|---|
| 原理 | 每次 push 输入用户名 + 一串叫 PAT 的密码 | 本地生成一对密钥（公钥+私钥），把公钥给 GitHub |
| 第一次配置 | 建 PAT，然后 Windows 凭证管理器自动记住 | 生成密钥，把公钥贴到 GitHub |
| 之后 push | 无痛，不用再输 | 无痛，不用再输 |
| 适合 | 新手、偶尔换机器 | 长期开发、觉得每次输密码烦 |
| 本机状态 | 可用（推荐先走这条） | 需要先生成密钥，见 2.3 |

> PAT = Personal Access Token，个人访问令牌。它**不是**你的 GitHub 登录密码，而是一串专门给 Git 命令用的“替代密码”。GitHub 早就不再接受账号密码 push 了。

### 2.1 方式 A：HTTPS + PAT（推荐新手）

**第一步：在 GitHub 上生成 PAT**

1. 浏览器登录 GitHub → 右上头像 → Settings → 最左栏最底下 Developer settings → Personal access tokens → **Tokens (classic)** → Generate new token (classic)。
2. Note 随便填，比如 `pc-git`。
3. Expiration 选 90 天或 No expiration（学生建议 1 年以内）。
4. 勾选权限：至少勾 **`repo`**（完整仓库读写）。其它不用勾。
5. 点 Generate token，**立刻把那串 `ghp_xxxxxxxx` 复制下来存好**。页面一关掉就再也看不到第二次了。

**第二步：第一次 push 时输入**

当你第一次 `git push` 时，会弹窗让你登录：

- 用户名：你的 GitHub 用户名。
- 密码：**这里粘贴刚才的 PAT，不是你的登录密码**。

Windows 上 Git 自带的 Git Credential Manager 会把它存进“Windows 凭据管理器”，以后 push 再也不用输。验证它已经记住：

```powershell
git config --global credential.helper
```

若输出 `manager`（或 `manager-core`），说明凭证助手在位，以后 push 自动用 PAT。

> 忘记 PAT / 认证又失败了？见 04 文档“认证失败”一节，一句话重置。

### 2.2 方式 B：SSH key（一次配好，长期无感）

如果你以后每天都用 Git，SSH 更干净。

**第一步：生成密钥对**（本机还没有，下面命令会新建）：

```powershell
ssh-keygen -t ed25519 -C "你的GitHub邮箱@example.com"
```

一路回车（密码 passphrase 可留空，也可设一个更安全）。它会在 `C:\Users\千禧\.ssh\` 下生成两个文件：

- `id_ed25519`：**私钥，永远不要给任何人，不要上传**。
- `id_ed25519.pub`：公钥，待会贴给 GitHub。

**第二步：把公钥贴到 GitHub**：

```powershell
# 用记事本打开公钥并全选复制
notepad $env:USERPROFILE\.ssh\id_ed25519.pub
```

然后 GitHub → Settings → SSH and GPG keys → New SSH key：Title 填 `我的PC`，Key 粘贴 `.pub` 文件全部内容，保存。

**第三步：测试连接**：

```powershell
ssh -T git@github.com
```

第一次会问 `Are you sure you want to continue connecting`，输 `yes`。成功会看到：`Hi 你的用户名! You've successfully authenticated...`。

之后远程地址要用 SSH 格式：`git@github.com:用户名/仓库.git`，而不是 HTTPS 格式。

> 选了 HTTPS 就不用做这一节。两种方式连的是同一个 GitHub，只是“怎么证明你是你”不同。

---

## 3. 远程仓库的五个核心命令

先记住一张关系图：

```
   你的电脑                                   GitHub 云端
 ┌───────────┐   git push   ┌───────────────────────┐
 │  本地仓库  │ ──────────▶ │  远程仓库 (origin)      │
 │ .git/     │ ◀────────── │  github.com/你/项目     │
 └───────────┘  git pull   └───────────────────────┘
```

| 命令 | 作用 | 类比 |
|---|---|---|
| `git remote add origin <url>` | 给本地仓库起个别名叫 `origin`，指向云端地址 | 存一个网址书签 |
| `git push -u origin main` | 把本地 main 推上云端，并绑定跟踪关系 | 第一次上传 + 记地址 |
| `git pull` | 把云端新提交拉回本地并合并 | 同步别人/别处的改动 |
| `git fetch` | 只下载云端改动，**不自动合并**到你的工作区 | 先看一眼别人改了啥 |
| `git clone <url>` | 把整个云端仓库下载到新文件夹 | 复制别人的项目 |

> **fetch vs pull 的区别**（面试常问）：`git pull = git fetch + git merge`。`fetch` 只把远程更新下载到 `origin/main` 这个远程跟踪分支，你的本地文件一动不动，你可以先 `git log main..origin/main` 看清楚再决定怎么合并；`pull` 则立刻把远程改动合并进你当前分支，万一有冲突会当场炸出来。**不确定时先 `fetch`，看清楚再 `merge`。**（本机已用本地裸仓库实测过这套流程。）

---

## 4. 在 GitHub 上新建一个空远程仓库

1. GitHub 首页右上 `+` → New repository。
2. Repository name：仓库名，比如 `movielens-analysis`。
3. Description：一句话介绍，比如“MovieLens 电影评分数据 EDA”。
4. Public（公开，作品集要公开）还是 Private（私有）：**作品集选 Public**。
5. **不要**勾选 “Add a README”、“Add .gitignore”、“Choose a license”——因为你本地已经有项目了，勾了会让云端和本地历史不一致，第一次 push 会冲突。这些我们在本地补。
6. 点 Create repository。建好后 GitHub 会给你一个页面，上面有 HTTPS 地址，形如：
   `https://github.com/你的用户名/movielens-analysis.git`，复制它。

---

## 5. 把 MovieLens 项目上传（完整分步）

> 你的项目实际位置（相对 `AI学习\` 根目录）：
>
> - MovieLens：`05_实战项目\01_MovieLens电影分析_任务书.ipynb`，数据在 `05_实战项目\ml-latest-small\`，还有一个 `ml-latest-small.zip`。
>
> 下面命令里把 `你的用户名` 换成你的 GitHub 用户名，把仓库 URL 换成你上一步复制的。

### 5.1 进项目目录，建仓库

```powershell
cd "C:\Users\千禧\Doubao\chats\2026-09-23\new-chat\AI学习\05_实战项目"
git init
```

> 注意：这会把整个 `05_实战项目` 变成一个 Git 仓库。如果你想让 MovieLens 和 Superstore **各自是独立仓库**（推荐，作品集分开展示），那就别在 `05_实战项目` 根目录 init，而是先给每个项目单独建文件夹。更干净的做法见 5.3。

### 5.2 先写 .gitignore，别把大数据包传上去

`ml-latest-small.zip` 这种压缩包不该进 Git（GitHub 单文件硬上限 100MB，而且数据可重新下载）。在 `05_实战项目\` 里建一个 `.gitignore`，把本模块的 [Python_gitignore模板](Python_gitignore模板) 内容粘进去，并确认至少有：

```gitignore
*.zip
ml-latest-small.zip
.ipynb_checkpoints/
__pycache__/
.venv/
```

小体积的 CSV（`ml-latest-small\*.csv` 总共才几 MB）可以传，方便别人 clone 下来就能跑。

### 5.3（推荐）每个项目一个独立仓库

作品集最好一个项目一个仓库，链接干净。操作：

```powershell
# 1. 在合适位置（比如你的代码目录）建项目文件夹
mkdir movielens-analysis
cd movielens-analysis

# 2. 把任务书 notebook 和数据复制进来（不是移动，是复制，原 05 目录不动）
copy "..\..\AI学习\05_实战项目\01_MovieLens电影分析_任务书.ipynb" .
# 数据若想带上：
# copy "..\..\AI学习\05_实战项目\ml-latest-small\*.csv" .

# 3. 把本模块的 Python_gitignore模板 复制成当前目录的 .gitignore
# 4. 初始化并提交
git init
git add .
git commit -m "feat: init movielens EDA project"
```

> 路径按你自己的实际目录调整。原则：**原 `AI学习\05_实战项目\` 里的一个文件都不要动、不要删**，我们只是复制一份到独立项目文件夹里做作品集。

### 5.4 关联远程并首次推送

```powershell
# 关联远程（URL 换成你在 GitHub 上建好的仓库地址）
git remote add origin https://github.com/你的用户名/movielens-analysis.git

# 确认远程地址对不对
git remote -v

# 首次推送：-u 把本地 main 和云端 main 绑在一起，以后直接 git push 即可
git push -u origin main
```

第一次 push 会弹窗要凭证：用户名填 GitHub 用户名，密码填 **PAT**（见 2.1）。成功后刷新 GitHub 仓库页面，文件已经躺在上面了。

### 5.5 以后每天的同步循环

本地改完代码后：

```powershell
git add .
git commit -m "feat: 补充评分分布分析"
git push          # 因为已经 -u 绑过，不用再加 origin main
```

---

## 6. 把 Superstore 项目上传

完全一样的套路，只是仓库名和文件不同：

```powershell
mkdir superstore-analysis
cd superstore-analysis

# 复制任务书和数据（原目录不动）
copy "..\..\AI学习\05_实战项目\02_Superstore超市经营分析_任务书.ipynb" .
copy "..\..\AI学习\05_实战项目\superstore\Superstore.csv" .

# .gitignore 同样用本模块模板

git init
git add .
git commit -m "feat: init superstore EDA project"

# 先在 GitHub 网页建好空仓库 superstore-analysis，再：
git remote add origin https://github.com/你的用户名/superstore-analysis.git
git push -u origin main
```

> Superstore.csv 只有几 MB，可以传。如果你以后项目里出现 >50MB 的文件，先想想该不该传，真要传见 04 文档“大文件”。

---

## 7. 写一个像样的 README（作品集的门面）

别人点开你的仓库，**第一眼看到的就是 README.md**。它会渲染在仓库主页。一个 EDA 项目的 README 至少要有：

````markdown
# MovieLens 电影评分数据分析

基于 MovieLens Latest Small 数据集（约 10 万条评分）的探索性数据分析。

## 技术栈
Python · pandas · matplotlib · seaborn · Jupyter Notebook

## 数据集
MovieLens Latest Small：https://grouplens.org/datasets/movielens/
本仓库附带清洗后的数据 CSV，clone 即可运行。

## 分析内容
- 评分分布与用户活跃度
- 高分电影类型 Top10
- 评分随时间的趋势

## 如何运行
```powershell
# 建议先建虚拟环境
pip install pandas matplotlib seaborn jupyter
jupyter notebook
```

## 作者
你的名字 · 数据来源 GroupLens
````

Markdown 常用语法（GitHub 渲染）：

| 写法 | 效果 |
|---|---|
| `# 一级` `## 二级` | 标题 |
| `**加粗**` `*斜体*` | 粗体/斜体 |
| `- 列表` | 无序列表 |
| `` `代码` `` | 行内代码 |
| ``` 三个反引号包代码块 ``` | 代码块（标注语言如 ```python） |
| `[文字](url)` | 链接 |
| `![说明](图片路径)` | 图片（把截图放进仓库的 `docs/` 或 `assets/` 文件夹） |
| `> 引用` | 引用块 |
| `\| 列1 \| 列2 \|` | 表格 |

官方完整语法：<https://docs.github.com/zh/get-started/writing-on-github>。

> 作品集加分项：把 notebook 跑出来的关键图保存成 PNG，在 README 里用 `![](docs/评分分布.png)` 展示。空仓库 + 一个 notebook 是“课程作业”，README + 图表 + 清晰结构是“作品集”。

---

## 8. License（开源许可证）

License 告诉别人“你可以拿我的代码干嘛”。学生作品集建议在仓库根目录放一个 `LICENSE` 文件：

- 最简单：GitHub 仓库页 → Add file → Create new file → 文件名打 `LICENSE` → 右边会出现 “Choose a license template” 按钮 → 选 **MIT License** → 填你的名字。
- MIT 的意思：随便用、随便改、随便商用，只要保留我的版权声明。对想扩散影响力的学生项目最友好。

没有 License 的默认含义是：**保留所有权利，别人理论上不能复制你的代码**。

---

## 9. Release（打版本快照）

当你一个项目做到“能拿得出手”的节点，打一个 Release：

1. 仓库页右侧 → Releases → Draft a new release。
2. Choose a tag → 输入 `v1.0.0` → 点 “Create new tag”。
3. Release title 写“第一版：完成核心 EDA”，描述列一下这版做了什么。
4. 发布。

以后别人可以直接下载这个时间点的完整代码，也能看到你的项目在“版本化前进”。

> 命令行等价操作：`git tag -a v1.0.0 -m "第一版"` 然后 `git push origin v1.0.0`。标签本质是指向某个 commit 的命名指针，详见 03 文档。

---

## 10. 常见卡点速查（详细版见 04 文档）

- `git push` 卡住要密码 → 密码那栏粘 PAT，不是登录密码。
- `remote origin already exists` → 远程名字加错了，先 `git remote remove origin` 再加。
- `fatal: refusing to merge unrelated histories` → 本地和云端是两条不相关历史（比如云端勾了 README），用 `git pull origin main --allow-unrelated-histories` 合并一次，再 push。
- 传错了大文件想撤 → 见 04 文档“大文件”。

---

## 来源与延伸

- GitHub 官方文档（中文）· 新建仓库：<https://docs.github.com/zh/get-started/quickstart/hello-world>
- GitHub 官方 · 使用 HTTPS 克隆与 PAT：<https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens>
- GitHub 官方 · 生成 SSH 密钥：<https://docs.github.com/zh/authentication/connecting-to-github-with-ssh>
- Pro Git 中文 · 远程仓库：<https://git-scm.com/book/zh/v2/Git-基础-远程仓库的使用>
- GitHub 官方 · Markdown 写法：<https://docs.github.com/zh/get-started/writing-on-github>
- 选择开源许可证：<https://choosealicense.com/>

> 本机实测（2026-10-09）：Git 2.53.0，全局身份已配为 `qxvoid` / `2854640226@qq.com`，尚无 SSH 密钥。`remote add / push / clone / fetch` 流程已用本地裸仓库模拟验证通过。**本模块不会替你 push 到任何真实仓库。**
