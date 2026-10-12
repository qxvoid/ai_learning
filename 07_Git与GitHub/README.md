# 07 · Git 与 GitHub

> 这个模块要解决两件事：第一，把你已经写好的项目（MovieLens、Superstore EDA）安全地放到 GitHub 上，变成可展示的作品集；第二，获得一项被严重低估的能力——**读懂别人的开源项目源码**。
>
> 你是 C++ 竞赛出身，习惯从内存模型和底层原理理解东西。Git 恰好是少数“搞懂底层就一通百通”的工具：它本质上是一个**内容寻址的对象数据库**，分支只是一个 41 字节的指针。一旦你接受这个心智模型，所有命令都是这个模型的自然推论，不用背。

---

## 这个模块学完后你能做到什么

1. 在本地用 Git 管理任何一个项目的版本历史，知道每一次改动谁、什么时候、为什么进去。
2. 把本地项目首次推送到 GitHub，并在以后每天 `add / commit / push` 同步。
3. 用分支 + Pull Request 参与开源，而不是只能围观。
4. 遇到“提交错了、文件删了、冲突了、认证失败了”不慌，知道怎么回退和排查。
5. 拿到一个陌生高星仓库，能按固定套路在半天内搞清楚它的架构和入口，而不是打开 `main.py` 瞎点。

---

## 学习顺序（严格按编号来）

| 顺序 | 文件 | 你将学会 | 建议时长 |
|---|---|---|---|
| 1 | [文档/01_Git是什么与本地工作流.md](文档/01_Git是什么与本地工作流.md) | 三区模型、对象数据库、`init/status/add/commit/log`、`.gitignore` | 2–3 小时，边读边敲 |
| 2 | [文档/02_GitHub远程仓库与上传项目.md](文档/02_GitHub远程仓库与上传项目.md) | 注册、HTTPS+PAT / SSH 二选一、`push/pull/clone`、把 MovieLens 和 Superstore 真正传上去 | 2–3 小时 |
| 3 | [文档/03_分支_合并与PullRequest.md](文档/03_分支_合并与PullRequest.md) | 分支本质是指针、merge 与冲突、fetch vs pull、PR、fork、GitHub Flow | 2 小时 |
| 4 | [文档/04_常见问题与速查表.md](文档/04_常见问题与速查表.md) | reset/revert/reflog 撤销全家桶、CRLF、中文乱码、认证失败、大文件、VSCode 内置 Git | 随时查，不必通读 |
| 5 | [文档/Python_gitignore模板](文档/Python_gitignore模板) | 直接复制成项目里的 `.gitignore` | 5 分钟 |
| 6 | [源码阅读/00_源码阅读方法论.md](源码阅读/00_源码阅读方法论.md) | 读源码读什么、怎么读、读不下去怎么办 | 1 小时 |
| 7 | [源码阅读/01_高星项目阅读路线.md](源码阅读/01_高星项目阅读路线.md) | 由易到难的 9 个仓库 + 每个的切入点 | 长期路线，按需取用 |
| 8 | [源码阅读/02_第一个PullRequest练习.md](源码阅读/02_第一个PullRequest练习.md) | 在 firstcontributions 上走完人生第一个 PR | 1 小时 |

> 建议节奏：第 1、2 篇必须当天动手做完（把 Superstore 传上去），第 3 篇配合第 8 篇的 firstcontributions 实操。源码阅读路线是“毕业后”的长期菜单，不要试图一周啃完 PyTorch。

---

## 环境检查清单（已在本机实测，2026-10-09）

打开 PowerShell（开始菜单搜 “PowerShell”），逐条运行。下面“实测结果”一列是这台机器上的真实状态，你照着核对自己的即可。

| 检查项 | 命令 | 本机实测结果 | 说明 |
|---|---|---|---|
| Git 是否安装 | `git --version` | `git version 2.53.0.windows.2` | 已装。若提示找不到命令，去 https://git-scm.com/download/win 下载安装包，一路下一步即可 |
| 用户身份（姓名） | `git config --global user.name` | `qxvoid` | **已配置**。若为空，见 01 文档“首次配置”一节 |
| 用户身份（邮箱） | `git config --global user.email` | `2854640226@qq.com` | **已配置**。注意：这个邮箱会公开出现在你所有提交里，建议用 GitHub 账号绑定的邮箱 |
| 默认分支名 | `git config --global init.defaultBranch` | `main` | 新仓库默认分支就是 `main`，和 GitHub 一致 |
| 换行符策略 | `git config --global core.autocrlf` | （空，未设置） | Windows 上建议设为 `true`，见 04 文档“CRLF”一节 |
| SSH 密钥 | `Test-Path "$env:USERPROFILE\.ssh"` | `False`（无 `.ssh` 目录） | **还没有 SSH 密钥**。想用 SSH 方式连接 GitHub 才需要生成，见 02 文档 |
| VSCode 命令 | `code --version` | 应输出版本号 | 已装 VSCode。VSCode 自带 Git 图形界面，见 04 文档 |

### 三个关键认知（先知道，后面细讲）

- **本机已经配好了 `user.name` / `user.email`**，所以你本地提交不会再被拦。但你要自己确认这两个值是不是你 GitHub 账号想用的身份——尤其是邮箱。想改就跑 `git config --global user.email "你的邮箱@example.com"`。
- **你还没有 GitHub 账号，也没有 SSH 密钥**，这都正常，02 文档会带你一步步建。
- **本模块不会替你上传任何东西**。所有 `git push` 都是你自己在自己的 PowerShell 里执行；文档只给命令和原理。

---

## 目录结构

```
07_Git与GitHub/
├── README.md                        ← 你在这里
├── 文档/
│   ├── 01_Git是什么与本地工作流.md
│   ├── 02_GitHub远程仓库与上传项目.md
│   ├── 03_分支_合并与PullRequest.md
│   ├── 04_常见问题与速查表.md
│   └── Python_gitignore模板
└── 源码阅读/
    ├── 00_源码阅读方法论.md
    ├── 01_高星项目阅读路线.md
    └── 02_第一个PullRequest练习.md
```

---

## 来源与延伸

- Pro Git 中文官方书：<https://git-scm.com/book/zh/v2>（本模块原理部分的主干来源）
- Git 官方文档（中文）：<https://git-scm.com/docs/zh>
- GitHub 官方文档（中文）：<https://docs.github.com/zh>
- GitHub 官方 .gitignore 模板集合：<https://github.com/github/gitignore>
- firstcontributions（人生第一个 PR）：<https://github.com/firstcontributions/first-contributions>
- git-flight-rules（踩坑大全）：<https://github.com/k88hudson/git-flight-rules>
- Oh Shit, Git!?!（出错自救）：<https://ohshitgit.com/>
- 约定式提交：<https://www.conventionalcommits.org/zh-hans/>
- GitHub Markdown 写法：<https://docs.github.com/zh/get-started/writing-on-github>

> 星数说明：源码阅读路线里的 star 数均于 2026-10-09 通过 `api.github.com` 实时核实（会随时间增长，读文档时以仓库页面为准）。
