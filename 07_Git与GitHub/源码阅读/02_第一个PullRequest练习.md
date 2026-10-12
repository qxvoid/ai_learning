# 02 · 你的第一个 Pull Request

> 很多人觉得“开源贡献”是大神的专利，其实不是。firstcontributions 这个仓库专门为零基础新手设计，只要改一个字、加一行你的名字，就能走完 Fork → PR → 合并的全流程。
>
> 这一篇带你在真实 GitHub 上完成**人生第一个被合并的 PR**。走完一遍，03 文档里的 fork/PR/upstream 就从纸面变成了肌肉记忆。

---

## 这个练习在练什么

不要求你写代码。它的目的是让你亲手跑一遍开源协作的完整流程：

```
Fork 仓库 → Clone 到本地 → 建分支 → 加一行你的名字 → commit → push → 网页发 PR → 等合并
```

跑通一次，以后给任何真实项目贡献都不慌。

---

## 前置条件

- 已有 GitHub 账号（见 02 文档第 1 节）。
- 已配好本地 Git 身份（`git config user.name` / `user.email`，本机已是 `qxvoid`）。
- 会用 HTTPS+PAT 或 SSH push（见 02 文档第 2 节）。

---

## 分步实操

### 第 1 步：打开练习仓库

浏览器访问：<https://github.com/firstcontributions/first-contributions>

读它的 README（英文，但大意就是“帮我们在 CONTRIBUTORS 列表里加一行你”）。

### 第 2 步：Fork

点页面右上角的 **Fork** 按钮，把这个仓库复制一份到你自己账号下。Fork 完你会进到 `github.com/你的用户名/first-contributions`——这是你的副本，随便改。

### 第 3 步：Clone 你自己的副本到本地

在你想放代码的目录打开 PowerShell：

```powershell
# URL 换成你 fork 后页面上那个绿色 Code 按钮里的地址
git clone https://github.com/你的用户名/first-contributions.git
cd first-contributions
```

### 第 4 步：新建一个分支

**不要直接在 main 上改**（这是练习的重点——养成开分支的习惯）：

```powershell
git switch -c add-你的名字
```

例如 `git switch -c add-jiangyuchen`。

### 第 5 步：编辑文件，加一行你的名字

用 VSCode 打开项目（在当前目录敲 `code .`）。找到仓库里的 `Contributors.md`（或 README 里指引的那个列表文件），在列表末尾**加一行你的 GitHub 用户名**，例如：

```markdown
- [@qxvoid](https://github.com/qxvoid)
```

保存。

### 第 6 步：提交

```powershell
git add Contributors.md
git commit -m "docs: add @qxvoid to contributor list"
```

### 第 7 步：推到你自己的 fork

```powershell
git push -u origin add-你的名字
```

### 第 8 步：在 GitHub 网页发 PR

1. 回到你 fork 的仓库页面（`github.com/你的用户名/first-contributions`）。
2. 页面上方会出现一条黄色横幅：“compare & pull request”，点它。
3. 确认 base 是原作者仓库的 main、head 是你的分支。
4. 标题和说明写一句“Adding myself”，点 **Create pull request**。

### 第 9 步：等待合并

维护者通常会在一段时间后 review 并合并你的 PR。合并成功那一刻，你就成了“这个开源项目的贡献者”。去原仓库的 contributors 列表能看到自己。🎉

---

## 过程中卡住了怎么办

- **push 要密码**：密码栏粘 PAT，不是登录密码（见 02 文档 2.1）。
- **不知道改哪个文件**：回去看 first-contributions 仓库 README，它有带截图的图文教程。
- **PR 被要求改**：维护者留言后，你在本地**同一个分支**改完、commit、再 `git push`，PR 会自动更新。
- **想同步原仓库最新代码**：按 03 文档第 6 节加 `upstream` 再 `git pull upstream main`。

---

## 做完这个练习之后

你已经掌握了开源协作的全套动作。接下来：

1. 把你自己的 MovieLens / Superstore 仓库好好写 README，那是你的长期作品集。
2. 想给真实项目贡献，去这些地方找“新手友好”的议题：
   - 仓库里搜标签 `good first issue` / `help wanted`。
   - <https://github.com/firstcontributions/first-contributions> 本身也列了适合新手的项目。
3. 贡献顺序建议：先修文档错别字 → 补测试 → 改小 bug → 提小功能。不要一上来改核心逻辑。

---

## 来源与延伸

- firstcontributions 官方仓库（带图文教程）：<https://github.com/firstcontributions/first-contributions>
- GitHub 官方 · 关于 Pull Request：<https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests>
- 本模块配套：[03_分支_合并与PullRequest](../文档/03_分支_合并与PullRequest.md)
