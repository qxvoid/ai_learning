# 03 · 分支、合并与 Pull Request

> 分支是 Git 被称为“分布式版本控制”的灵魂。很多人学 Git 卡在分支上，是因为他们以为分支是“把整个项目复制一份”。**根本不是。**
>
> Git 的分支极其廉价——它本质只是一个**41 字节的文件，里面存着某个 commit 的哈希**。建一个分支就是新建一个指针，切换分支就是移动这个指针。你在 C++ 竞赛里管的是内存指针，Git 分支管的是 commit 指针。这一篇把这个心智模型讲透。

---

## 1. 分支的本质：一个会移动的指针

回忆 01 篇：每个 commit 都是一次快照，并且**记录着它的父 commit 是谁**。所以所有 commit 天然连成一条链：

```
A ← B ← C ← D   (main 分支指着 D)
```

`main` 不是什么特殊的东西，它只是一个指针，指向当前最新的 commit `D`。

现在你想开发一个新功能，又不想弄坏 main：

```powershell
git switch -c feature/login     # 新建并切换到 feature/login
```

发生了什么？Git 新建了一个叫 `feature/login` 的指针，也指向 `D`，然后把你工作区切过去：

```
A ← B ← C ← D
             ↑↑
          main  feature/login   (两个指针都在 D)
```

你在 `feature/login` 上做一次 commit `E`：

```
A ← B ← C ← D ← E
             ↑     ↑
           main   feature/login   (只有 feature/login 往前走了，main 不动)
```

**这就是分支的全部魔法**：分支 = 一个会随你 commit 自动前移的指针。没有复制文件，没有拷贝项目，建 1000 个分支也只占几 KB。

> `git switch` 是较新 Git（2.23+）推荐的切换命令，语义清晰。老教程里的 `git checkout` 一身兼两职（切分支 + 恢复文件），容易混。本机 Git 2.53 两个都支持，本模块统一用 `switch`。

---

## 2. 分支的日常命令

```powershell
git branch                    # 列出本地分支，* 号是当前所在
git switch main               # 切回 main
git switch -c feature/xxx     # 新建并切到 feature/xxx（-c = create）
git branch -d feature/xxx     # 删除已合并的分支
git branch -D feature/xxx    # 强制删除没合并的分支（小心）
git switch -                  # 切回上一个分支（像 cd -）
```

本机实测的分支图（`git log --oneline --graph --all`）：

```
* 548dc9d feat: feature x version
| * a048cb8 feat: main version
|/
* 473330b feat: change greeting on dev
* 462c29f feat: add hello.py
```

这张图就是分叉：`main` 和 `feature/x` 从 `473330b` 各自往前走了一格。

---

## 3. merge：把两条分支缝在一起

你在 `feature/login` 上把功能做完了，想合回 `main`：

```powershell
git switch main               # 先切回被合并的目标分支
git merge feature/login       # 把 feature/login 合进来
```

分两种情况：

### 3.1 Fast-forward（快进）——没有分叉

如果从你切出 `feature/login` 之后，`main` 一步没动过，Git 根本不需要“合并”，直接把 `main` 指针往前挪到 `feature/login` 即可。历史是一条直线，干净。本机实测就是这种：`Updating 462c29f..473330b, Fast-forward`。

### 3.2 真正的三方合并 + 冲突——两条线都往前走了

如果 `main` 在你开发期间也有了新提交（比如别人改了同一行），Git 会尝试自动合并。**它能自动合就自动合，合不上就报冲突，让你手动解决。**

本机实测制造冲突的过程：在 `feature/x` 把某文件改成一句话，切回 `main` 把同一文件改成另一句话，再 `git merge feature/x`：

```
Auto-merging hello.py
CONFLICT (content): Merge conflict in hello.py
Automatic merge failed; fix conflicts and then commit the result.
```

`git status --short` 会显示 `UU hello.py`（UU = both modified，两边都改了）。打开那个文件，会看到 Git 标出来的冲突区：

```
<<<<<<< HEAD
print("from main")
=======
print("from feature x")
>>>>>>> feature/x
```

- `<<<<<<< HEAD` 到 `=======` 之间是你当前分支（main）的版本。
- `=======` 到 `>>>>>>> feature/x` 是对方分支的版本。

**解决冲突 = 你手动把这段改成最终想要的样子，并删掉那三行尖括号标记。** 比如想合并两版：

```python
print("from main and feature x merged")
```

然后：

```powershell
git add hello.py              # 告诉 Git 冲突已解决
git commit                    # 完成合并（会自动生成一条 merge commit 说明）
```

**如果你后悔了，不想合并了**，随时：

```powershell
git merge --abort             # 一键回到合并前的干净状态
```

> 冲突不可怕，它就是 Git 在说“这地方我猜不准你想要啥，你来看一眼”。解决完 `add` + `commit` 就好。

---

## 4. fetch 与 pull（再强调一次）

```powershell
git fetch origin        # 下载 origin 上的新提交，但不动你的本地文件
git pull                # = git fetch origin + git merge origin/当前分支
```

工作流建议：

```powershell
git fetch origin
git log --oneline main..origin/main   # 看看远程比你多了啥
# 看清楚了，再决定：
git merge origin/main                  # 手动合
# 或者图省事直接：
git pull
```

---

## 5. Pull Request（PR）：开源协作的核心仪式

本地 merge 是“我自己的两个分支合并”。但如果你**没有权限直接往别人仓库 push**，怎么贡献？答案就是 Fork + Pull Request。

### 5.1 PR 的完整流程

1. **Fork**：在别人仓库页面点 Fork，把它复制一份到你自己账号下。现在你有了一份完全可控的副本。
2. **Clone 你自己的副本**到本地：
   ```powershell
   git clone https://github.com/你的用户名/某仓库.git
   ```
3. **在本地建分支改代码**：
   ```powershell
   git switch -c fix/typo
   # 改代码...
   git add .
   git commit -m "fix: 修正 README 错别字"
   git push -u origin fix/typo
   ```
4. **在 GitHub 网页发起 PR**：push 后仓库主页会出现一个 “Compare & pull request” 按钮，点它，写清楚“我改了什么、为什么”，提交。
5. **维护者评审（review）**：对方可能在 PR 里留言“这里再改一下”。你就在本地同一个分支继续改、commit、push——PR 会**自动更新**，不用重新发。
6. **对方合并**：你的代码正式进上游仓库。🎉

### 5.2 为什么不直接在 main 上改

因为 PR 的本质是**一次代码评审请求**：它给别人一个检查你改动的地方，留下讨论记录。直接往 main push 就跳过了这道关卡。团队里 main 通常是受保护分支，根本不让直推。

---

## 6. Fork 之后：和上游保持同步

你 Fork 的副本会随时间落后于原仓库（原仓库一直在更新）。要给它加一个“上游”地址：

```powershell
# 先看你现在有哪些远程（origin 指向你自己的 fork）
git remote -v

# 把原仓库加为 upstream
git remote add upstream https://github.com/原作者/某仓库.git

# 以后想同步原仓库最新代码：
git switch main
git fetch upstream
git merge upstream/main       # 把上游 main 合进你的本地 main
git push origin main          # 再把同步后的结果推到你自己的 fork
```

> `origin` = 你自己的 fork（你有写权限）；`upstream` = 原作者仓库（你通常只有读权限）。这个命名是社区惯例。

---

## 7. 标签（Tag）：给重要节点起名字

分支是会动的指针，标签是**钉死在某个 commit 上的书签**，通常用来标记版本号（v1.0、v2.3.1）。

```powershell
git tag v1.0.0                          # 轻量标签（就一个名字）
git tag -a v1.0.0 -m "第一版正式发布"     # 附注标签（带说明、打标签人信息，推荐）
git tag -l                              # 列所有标签
git push origin v1.0.0                  # 标签默认不会被 push 带走，要单独推
git push origin --tags                  # 一次推全部标签
```

本机实测：附注标签 `git show v0.1.1` 会显示 Tagger、日期、说明。Release（见 02 文档）就是基于标签在 GitHub 上打的。

---

## 8. GitHub Flow：一套被验证过的协作流程

这是 GitHub 官方推荐的轻量分支模型，适合大多数项目（包括你的个人项目）：

```
main（永远可发布）
 ├── feature/用户登录     ← 从 main 切出，做完发 PR，评审通过合回 main
 ├── fix/登录按钮错位     ← 从 main 切出，修完发 PR
 └── docs/补README
```

规则只有 5 条：

1. `main` 里的代码永远是可运行、可发布的。
2. **任何新工作都从 `main` 切出新分支**，分支名见名知意（`feat/`、`fix/`、`docs/`）。
3. 小步提交，常 push 到同名远程分支做备份。
4. 做完立刻发 PR，找人评审（个人项目可以自己 review）。
5. 评审通过就合并回 `main`，删掉已合并的分支。

> 更重的团队模型（Git Flow：develop/release/hotfix 多层分支）等你以后进团队再学。个人作品集用 GitHub Flow 足够，别过度设计。

---

## 9. 给你个人项目的建议工作流

你的 EDA 项目可以这样用分支：

```powershell
# 第一次：main 是主干
git switch -c eda/评分分布      # 切个分支做评分分析
# 写 notebook...
git commit -m "feat: 完成评分分布图"
git push -u origin eda/评分分布
# 在 GitHub 发个 PR 自己看一眼 diff，没问题合并到 main
git switch main
git pull
git branch -d eda/评分分布
```

这样 main 永远是“当前能看的版本”，每个分析模块独立分支、独立提交历史。

---

## 来源与延伸

- Pro Git 中文 · 分支何谓（分支本质是指针）：<https://git-scm.com/book/zh/v2/Git-分支-分支是什么>
- Pro Git 中文 · 分支新建与合并：<https://git-scm.com/book/zh/v2/Git-分支-分支的新建与合并>
- Pro Git 中文 · 分支管理与远程分支：<https://git-scm.com/book/zh/v2/Git-分支-分支管理>
- GitHub 官方 · 关于 Pull Request：<https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests>
- GitHub 官方 · Fork 一个仓库并同步上游：<https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests/working-with-forks>
- GitHub Flow 原文：<https://docs.github.com/zh/get-started/quickstart/github-flow>

> 本篇分支/合并/冲突/abort/标签命令均在本机 Git 2.53.0 实测通过（2026-10-09）。
