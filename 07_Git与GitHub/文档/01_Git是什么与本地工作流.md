# 01 · Git 是什么与本地工作流

> 你以前备份代码大概是这样的：`project/`、`project_备份/`、`project_final/`、`project_final_真的最终版/`。
> Git 要解决的就是这件事，但它不是“多存几份文件夹”，而是给项目建了一个**只增不改、内容寻址的快照数据库**。这一篇讲清楚它到底存了什么，以及你每天会敲的那 5 条命令为什么是这 5 条。

---

## 1. 版本控制到底在控制什么

先纠正一个直觉误区：**Git 不保存“文件之间的差异（diff）”，它保存“每个时刻的完整快照（snapshot）”。**

这是 Git 和老一代版本控制（SVN、CVS）最本质的区别，也是它快的原因：

- 如果一个文件没改，Git 不会再存一份副本，而是**存一个指向上一次已存副本的链接**。
- 如果改了，就把新内容存成一个新对象。
- 所谓“一次提交（commit）”，就是给**当时整个项目所有文件的状态**拍一张快照，并给它一个指纹（哈希）。

类比你熟悉的东西：这很像 C++ 里的**不可变二叉树持久化结构（persistent data structure）**——每次修改不改动旧树，只新建被改动的节点，旧节点仍然被旧版本引用着，所以你能瞬间回到任何历史版本。

### 1.1 内容寻址（content-addressed）是什么

Git 给每个对象算一个 SHA-1 哈希（40 个十六进制字符，简写前 7 位），比如 `462c29f005bbd2983e54f58d0eab4185cc73cfef`。

- 对象存进去时，**文件名就是它内容的哈希**。
- 内容一样 → 哈希一样 → 全局只存一份。
- 内容哪怕只改一个字节 → 哈希完全不同 → 变成一个新对象。

这带来一个免费性质：**Git 能自动发现任何“偷偷改动过历史”的行为**，因为哈希对不上。你以后看到的 `commit 462c29f`，那个 `462c29f` 就是这次快照内容的指纹。

---

## 2. 三区模型（本篇最重要的一张图）

Git 里一个文件在任意时刻一定处于以下三个区域之一：

```
 ┌──────────────┐   git add    ┌──────────────┐   git commit   ┌──────────────┐
 │   工作区      │ ───────────▶ │   暂存区      │ ─────────────▶ │   版本库      │
 │  Working     │              │  Staging /   │                │  Repository  │
 │  Directory   │ ◀─────────── │  Index       │ ◀───────────── │  (.git/ 目录) │
 └──────────────┘  checkout    └──────────────┘   reset HEAD~1  └──────────────┘
   你眼睛看到的        git add 决定"下次提交"          已定格的历史
   文件夹里的文件      要包含哪些改动                 每个 commit 一个快照
```

用大白话：

1. **工作区**：你在资源管理器里能看到、能编辑的那些文件。
2. **暂存区（Index）**：一个“购物车”。`git add` 不是把文件存进历史，而是**把当前改动放进购物车**，告诉你“下次结账（commit）我要这些”。
3. **版本库（`.git/` 目录）**：真正的仓库。`git commit` 把购物车里的东西打成一张快照，永久存进 `.git/`。

> 为什么要有暂存区这个“多余”的中间层？因为你可能改了 5 个文件，但只想把“修登录 bug”和“改文档”分成两次干净的提交。有了暂存区，你可以先 `git add login.py` 提交一次，再 `git add README.md` 提交第二次。这就是它的价值：**让每次提交只做一件事**。

### 2.1 `git status` 就是在回答“我现在各区长什么样”

跑一次你就明白上面那张图在说什么：

```powershell
git status
```

典型输出会分三段：

- `Changes to be committed`：在暂存区（购物车里），下次 commit 会带走。
- `Changes not staged for commit`：在工作区改了，但还没 `add`。
- `Untracked files`：Git 从没见过的新文件，连工作区“被跟踪”的资格都还没有。

---

## 3. 安装复查与首次配置

### 3.1 复查安装

```powershell
git --version
```

本机实测输出：`git version 2.53.0.windows.2`。若提示“无法将 git 识别为 cmdlet”，去 <https://git-scm.com/download/win> 下载安装包，安装时大部分选项保持默认即可，注意：

- “Choosing the default editor” 选 VSCode 或你顺手的编辑器。
- “Adjusting your PATH environment” 选默认的 “Git from the command line and also from 3rd-party software”。
- “Choosing the default branch name” 选让 `main` 成为默认（本仓库已经是 `main`）。

### 3.2 身份配置（每次提交都会带上你是谁）

Git 每次提交都要记录作者。先看本机现状：

```powershell
git config --global user.name
git config --global user.email
```

本机实测：`user.name = qxvoid`，`user.email = 2854640226@qq.com`，**已经配置好了**。

如果你要改成自己 GitHub 想用的身份（把下面换成你自己的）：

```powershell
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱@example.com"
```

几个要点：

- `--global` 表示这台机器上所有仓库都用这个身份，**只配一次**。
- 如果某个仓库想用不同身份（比如工作仓库），进到那个仓库目录里去掉 `--global` 再配一次，仓库级会覆盖全局。
- 用 `git config user.name`（不带 `--global`）看“当前仓库实际生效的值”，它会优先显示仓库级配置。
- **邮箱会公开**在你推到 GitHub 的每一次提交里。如果你不想暴露 QQ 邮箱，可以在 GitHub 申请一个隐私邮箱（形如 ` ID+用户名@users.noreply.github.com`），再用它来 `git config --global user.email`。

### 3.3 换行符（Windows 用户强烈建议现在就设）

Windows 的换行是 `CRLF`（`\r\n`），Mac/Linux 是 `LF`（`\n`）。不统一会导致整个文件每一行都“被改动”，diff 惨不忍睹。设一次：

```powershell
git config --global core.autocrlf true
```

含义：提交时把 CRLF 转成 LF 存进仓库， checkout 时再转回 CRLF。这样仓库里永远是 LF，跨平台协作不打架。详见 04 文档。

---

## 4. 第一个仓库：init / status / add / commit / log

下面所有命令我都在一个临时目录里真实跑通过。你可以**在一个空目录里自己跟着敲一遍**感受，不要直接在你的真实项目目录里 `git init`（上传项目的专门步骤见 02 文档）。

### 4.1 初始化

```powershell
# 先建一个练习目录并进去
mkdir git-practice
cd git-practice

git init
```

输出类似：`Initialized empty Git repository in .../git-practice/.git/`。

> 本质：Git 在这个目录下建了一个隐藏的 `.git/` 文件夹，刚才说的“版本库”就住在这里。目录本身**没有任何魔法**，你删掉 `.git/` 这个文件夹，这个项目就变回一个普通文件夹——Git 历史全部消失，但工作区文件完好。
>
> 因为本机设了 `init.defaultBranch=main`，新仓库的初始分支直接叫 `main`，不用再手动改名。

### 4.2 看状态

```powershell
git status
```

现在是 “No commits yet”，因为还没有任何提交。

### 4.3 新建一个文件，观察三区变化

用 VSCode 或记事本建一个 `hello.py`，内容：

```python
print("hello git")
```

然后：

```powershell
git status        # 看到 hello.py 在 Untracked files（未跟踪）
git add hello.py  # 放进暂存区（购物车）
git status        # 现在它变成 Changes to be committed（new file）
```

把这两条 `status` 的输出对比着看，你就彻底理解三区了。

### 4.4 提交

```powershell
git commit -m "feat: add hello.py"
```

输出会显示 `[main (root-commit) xxxxxxx] feat: add hello.py` 和 `1 file changed`。

> `-m` 后面是提交说明。建议遵循“约定式提交”：`feat:` 新功能、`fix:` 修 bug、`docs:` 改文档、`chore:` 杂项、`refactor:` 重构、`test:` 测试。详见 <https://www.conventionalcommits.org/zh-hans/>。写说明用一句话讲清“这次改动为了什么”，不是“我改了哪几行”。

### 4.5 提交后再看状态

```powershell
git status
```

现在应该是 `nothing to commit, working tree clean`——工作区和暂存区都干净，所有改动都已定格进版本库。

### 4.6 改一个文件，体验“已跟踪文件”的流转

编辑 `hello.py` 第二行：

```python
print("hello git, version 2")
```

```powershell
git status        # hello.py 出现在 Changes not staged（改了但没 add）
git diff          # 看工作区相对暂存区改了什么（下面单独讲）
git add hello.py  # 放进购物车
git diff --cached # 看暂存区相对上次提交将提交什么
git commit -m "feat: bump greeting to version 2"
```

### 4.7 看历史（log）

最常用的三个：

```powershell
git log                      # 完整历史：谁、什么时候、说明、完整哈希
git log --oneline            # 每行一条：短哈希 + 说明，日常最爱
git log --oneline --graph --all   # 带分支图形，看分叉/合并一目了然
```

本机实测的 `--oneline` 样子：

```
462c29f feat: add hello.py
```

---

## 5. 常用命令速记（本篇涉及的）

| 想干嘛 | 命令 | 落在哪个区 |
|---|---|---|
| 把目录变成 Git 仓库 | `git init` | 创建 `.git/` |
| 看状态 | `git status` | 只读 |
| 看工作区改了啥 | `git diff` | 工作区 vs 暂存区 |
| 看暂存了啥 | `git diff --cached` | 暂存区 vs 上次提交 |
| 新文件/改动放进暂存区 | `git add <文件>` 或 `git add .` | 工作区 → 暂存区 |
| 定格一次快照 | `git commit -m "说明"` | 暂存区 → 版本库 |
| 看历史 | `git log --oneline --graph --all` | 只读 |

> `git add .` 里的 `.` 表示“当前目录下所有改动”。**养成习惯：`add` 之后、`commit` 之前一定 `git status` 看一眼购物车里是不是只有你想提交的东西。**

---

## 6. .gitignore：让 Git 假装这些文件不存在

不是所有文件都该进版本库。数据集、虚拟环境、缓存、密钥、IDE 配置——这些要么体积大、要么是个人环境、要么是秘密。`.gitignore` 告诉 Git 哪些路径**不要跟踪**。

在项目根目录建一个 `.gitignore`（注意开头有个点，没有文件名）：

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Jupyter
.ipynb_checkpoints/

# 数据（你的 EDA 项目数据别传 GitHub）
*.csv
*.zip
data/

# 密钥与环境
.env
*.env
config.local.py

# 操作系统垃圾
Thumbs.db
Desktop.ini

# 编辑器
.vscode/
.idea/
```

> 本模块给了一份**可直接复制的完整版**：[文档/Python_gitignore模板](Python_gitignore模板)。你的 MovieLens / Superstore 项目尤其需要它——`ml-latest-small.zip` 有几百 MB，GitHub 单文件 100MB 限制，数据集不该传。

### 6.1 .gitignore 的两条铁律（踩过坑才知道痛）

1. **`.gitignore` 只对“未跟踪”的文件生效。** 如果一个文件已经被 `git add` 跟踪了，后来才写进 `.gitignore`，Git **仍然会跟踪它**。这时候要先把它从暂存区删掉（但保留硬盘上的文件）：
   ```powershell
   git rm --cached 误入的文件.csv
   git commit -m "chore: stop tracking dataset"
   ```
   本机实测：`git rm --cached secret.env` 后，该文件从暂存区消失（状态 `D`），但硬盘上文件还在（状态变回 `??`）。
2. **想验证某文件为啥被忽略 / 没被忽略**：
   ```powershell
   git check-ignore -v 某个文件.csv
   ```
   会告诉你它被哪条 `.gitignore` 规则命中。本机实测输出形如 `.gitignore:1:*.csv  某个文件.csv`。

---

## 7. Windows / PowerShell 专属注意点

1. **路径用反斜杠 `\` 或正斜杠 `/` 都行**，但命令里有空格时整体加引号：`cd "C:\Users\千禧\My Projects"`。
2. **PowerShell 里没有 `&&`**（老版本）。要连着写就用 `;` 或者分行；本模块所有命令都按单条给出，你逐条粘贴即可。
3. **别在一个 Git 仓库里面再 `git clone` 另一个仓库**。实测时我不小心这么干，Git 会警告 `adding embedded git repository`，并把内层仓库记成一个叫 `gitlink` 的奇怪引用。如果你不小心 clone 错了位置，用 `git rm --cached 那个目录` 撤掉。
4. **文件名中文**：现代 Git for Windows 默认能正常显示中文文件名。如果 `git status` 里中文文件名变成一堆 `\351\234...` 转义，跑一次：
   ```powershell
   git config --global core.quotepath false
   ```
5. **编辑器**：`git commit` 不带 `-m` 时会唤起默认编辑器写说明。建议 `git config --global core.editor "code --wait"`，以后提交说明直接用 VSCode 写。
6. **换行符乱码/整文件变红**：见 04 文档“CRLF”一节，跑 `git config --global core.autocrlf true` 通常就好。

---

## 8. 动手检验（不做等于没学）

在你的 `AI学习\07_Git与GitHub\` 目录下**不要**建练习仓库（那是放文档的地方）。而是另开一个临时目录，完成：

1. `git init` 一个新仓库。
2. 建 `a.txt`、`b.txt`，分别 `add` + `commit` 成两次提交。
3. 改 `a.txt`，用 `git diff` 看改动，再 `git add`，用 `git diff --cached` 再看一次，体会两者区别。
4. `git log --oneline --graph --all` 看到两条历史。
5. 写一个 `.gitignore` 忽略 `*.log`，建一个 `test.log`，确认 `git status` 里**看不到**它。
6. 用 `git check-ignore -v test.log` 验证它被哪条规则命中。

全部能跑通，你就掌握了本地版本控制的 90%。剩下的 10%（撤销、分支）在 03、04 篇。

---

## 来源与延伸

- Pro Git 中文 · 起步：<https://git-scm.com/book/zh/v2/起步-关于版本控制>
- Pro Git 中文 · Git 基础（三区模型、记录每次更新）：<https://git-scm.com/book/zh/v2/Git-基础-记录每次更新到仓库>
- Pro Git 中文 · Git 内部原理（对象数据库、内容寻址）：<https://git-scm.com/book/zh/v2/Git-内部原理>
- Git 官方 · gitignore 文档：<https://git-scm.com/docs/gitignore>
- GitHub 官方 · 忽略文件：<https://docs.github.com/zh/get-started/getting-started-with-git/ignoring-files>
- 约定式提交：<https://www.conventionalcommits.org/zh-hans/>

> 本篇命令均在 Windows 11 / PowerShell 5.1 / Git 2.53.0 实测通过（2026-10-09）。
