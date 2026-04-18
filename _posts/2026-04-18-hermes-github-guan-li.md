---
layout: post
title: "用 Hermes Agent 管理 GitHub 项目：Issues 与 PR 实战"
date: 2026-04-18 18:00:00 +0800
categories: [Hermes Agent]
tags: [GitHub, Issues, PR, Pull Request, gh CLI, github-pr-workflow]
---

# 用 Hermes Agent 管理 GitHub 项目：Issues 与 PR 实战

还在为 GitHub 操作繁琐而烦恼？Hermes Agent 内置完整的 GitHub 管理技能，支持 Issue 创建、PR 管理、代码审查，配合自然语言对话，让你的 GitHub 工作流事半功倍。

## 准备工作：GitHub 认证

### 方法 1：使用 gh CLI（推荐）

```bash
# 检查认证状态
gh auth status

# 如果未认证，登录
gh auth login
# 选择：GitHub.com → HTTPS → 浏览器登录

# 配置 git 凭证
gh auth setup-git
```

### 方法 2：使用 Hermes 技能

```
你：帮我配置 GitHub 认证
Hermes：好的，我来检查当前的 GitHub 认证状态。

检测结果：
- gh CLI：未安装
- git credential helper：未配置

你有以下选项：
1. 提供 GitHub Personal Access Token（推荐）
2. 配置 SSH Key
3. 安装 gh CLI 并认证

请选择你偏好的方式，或提供你的 Token。
```

### 提取 Token 辅助命令

Hermes 会自动尝试从以下位置读取 Token：

```bash
# 优先级顺序：
# 1. 环境变量 $GITHUB_TOKEN
# 2. ~/.hermes/.env 中的 GITHUB_TOKEN
# 3. ~/.git-credentials 中的 GitHub 凭证
```

## GitHub 认证技能（github-auth）

```bash
# 加载认证技能
/hermes-auth
# 或
hermes chat -s github-auth
```

该技能会自动检测环境并选择最佳认证方式。

## GitHub Issues 管理技能

```bash
# 加载 issues 技能
/github-issues
# 或
hermes chat -s github-issues
```

### 创建 Issue

**自然语言：**
```
你：在当前仓库创建一个 issue，标题是"用户登录偶发超时"，标签是 bug，严重程度是高
Hermes：正在创建 issue...
```

**技能内部执行：**
```bash
gh issue create \
  --title "用户登录偶发超时" \
  --body "## 问题描述\n...\n\n## 环境\n- OS: \n- Version: " \
  --label "bug" \
  --assignee @me
```

### 列出 Issues

```
你：列出所有 open 状态的 bug issue
Hermes：

# Open Bug Issues
──────────────────────────────────────
#42    用户登录偶发超时        [bug, high-priority]
#38    支付回调处理异常        [bug]
#35    移动端页面布局错乱      [bug]

按严重程度排序。
```

### 搜索 Issues

```
你：搜索标题包含"登录"的所有 issue
Hermes：

# 搜索结果：标题包含"登录"
──────────────────────────────────────
#42    用户登录偶发超时        open    [bug]
#41    登录页样式异常          closed  [ui]
#39    登录接口性能优化        open    [enhancement]
```

### Issue 详情和评论

```
你：查看 #42 的详情，并在下面评论"已定位到问题，正在修复"
Hermes：

# Issue #42
──────────────────────────────────────
标题：用户登录偶发超时
状态：open
标签：bug, high-priority
指派：@me

正文：...
──────────────────────────────────────

✓ 已添加评论："已定位到问题，正在修复"
```

### 关闭/重新打开 Issue

```
你：关闭 #35，并说明原因"已在 #42 中统一修复"
Hermes：

✓ Issue #35 已关闭
原因：已在 #42 中统一修复
```

## GitHub PR 工作流技能

```bash
# 加载 PR 技能
/github-pr-workflow
# 或
hermes chat -s github-pr-workflow
```

### 创建 PR

**自然语言：**
```
你：基于当前分支创建一个 PR，目标分支是 main，标题是"fix: 修复登录超时问题"
Hermes：正在创建 PR...
```

**技能内部执行：**
```bash
# 1. 推送分支
git push -u origin HEAD

# 2. 创建 PR
gh pr create \
  --title "fix: 修复登录超时问题" \
  --body "## Summary\n- 修复登录偶发超时问题\n\nCloses #42" \
  --base main
```

### 监控 CI 状态

```
你：检查当前 PR 的 CI 状态
Hermes：

# PR #156 CI Status
──────────────────────────────────────
✓ unit-tests (pytest)     success  2m 34s
⚙ integration-tests       running  1m 12s
⚙ security-scan           pending
⚙ build                   pending
```

### 等待 CI 通过

```
你：等待 CI 全部通过，最多等 10 分钟
Hermes：正在监控 CI 状态...

19:30:01  ✓ unit-tests     success
19:31:23  ✓ integration    success
19:32:45  ✓ security-scan  success
19:33:52  ✓ build          success

✓ 所有 CI 检查通过！（用时 3 分 52 秒）
```

### 自动修复 CI 失败

```
你：CI 失败了，帮我自动修复
Hermes：正在检查失败原因...

## CI 失败分析
──────────────────────────────────────
测试：tests/test_auth.py::test_login_timeout
错误：AssertionError: assert 0.05 < 0.03
原因：超时阈值设置过严
──────────────────────────────────────

正在修复...
✓ 已调整超时阈值为 0.05
✓ 已提交并推送
✓ 触发重新 CI
```

### 合并 PR

```
你：squash 合并这个 PR，并删除分支
Hermes：

✓ Squash 合并 PR #156
✓ 已删除远程分支 fix/login-timeout
✓ 已切换回 main 分支
```

## 完整对话示例

### 场景：Bug 处理流程

```
你：我发现一个 bug，用户注册后邮件验证链接打不开
Hermes：明白了，我来帮你处理这个 bug。请提供更多信息：

1. 邮件验证链接的格式是什么？（能举个例子吗）
2. 是所有用户都这样，还是部分用户？
3. 有日志吗？具体报错信息是什么？

你：链接格式是 /verify?token=xxx，部分用户有问题，日志显示 Token 验证失败
Hermes：好的，我来：

1. 先搜索是否已有相关 issue
2. 创建新的 bug issue
3. 创建分支开始修复
```

```
你：搜索现有 issue
Hermes：

# 搜索结果："邮件验证" OR "verify" OR "token"
──────────────────────────────────────
#38    支付回调处理异常        [bug]          ← 不相关
#41    登录页样式异常          [closed]       ← 不相关
未找到相关 issue
```

```
你：创建一个新 issue，标题是"注册邮件验证链接失效"
Hermes：正在创建 issue...

✓ Issue #43 已创建
标题：注册邮件验证链接失效
标签：bug
指派：@me
链接：https://github.com/godsay1983/project/issues/43
```

```
你：创建分支并修复这个问题
Hermes：

1. 创建修复分支
   ✓ git checkout -b fix/email-verify

2. 分析问题
   邮件验证链接：/verify?token=xxx
   Token 使用 URL 编码，但后端解码有问题

3. 修复代码（src/auth/email_verify.py）
   - 修改 token 解码逻辑
   - 添加错误处理

4. 提交
   ✓ git commit -m "fix: 修复邮件验证链接 token 解码问题"

5. 推送
   ✓ git push -u origin fix/email-verify
```

```
你：创建 PR 并等待 CI
Hermes：

✓ PR #157 已创建
标题：fix: 修复邮件验证链接 token 解码问题
目标分支：main
链接：https://github.com/godsay1983/project/pull/157

正在监控 CI...
✓ unit-tests     success
✓ integration    success
✓ security-scan  success
```

```
你：合并这个 PR
Hermes：

✓ Squash 合并 PR #157
✓ 关联 Issue #43 已自动关闭
✓ 已删除分支 fix/email-verify

🎉 Bug #43 已修复并合并！
```

## 常用命令速查表

### Issue 操作

| 操作 | 命令 |
|------|------|
| 列出所有 open issue | `gh issue list --state open` |
| 列出我的 issue | `gh issue list --assignee @me` |
| 按标签筛选 | `gh issue list --label bug` |
| 创建 issue | `gh issue create --title "..." --body "..."` |
| 查看 issue | `gh issue view 42` |
| 添加评论 | `gh issue comment 42 --body "..."` |
| 关闭 issue | `gh issue close 42` |

### PR 操作

| 操作 | 命令 |
|------|------|
| 列出我的 PR | `gh pr list --author @me` |
| 创建 PR | `gh pr create --title "..." --body "..."` |
| 查看 PR | `gh pr view 42` |
| 查看 PR diff | `gh pr diff 42` |
| 添加评论 | `gh pr comment 42 --body "..."` |
| 请求审查 | `gh pr edit 42 --add-reviewer username` |
| 合并 PR | `gh pr merge --squash --delete-branch` |
| CI 状态 | `gh pr checks` |
| 等待 CI | `gh pr checks --watch` |

## Skill 组合使用

```bash
# 同时加载多个技能
hermes chat -s github-auth -s github-issues -s github-pr-workflow

# 指定技能执行命令
/hermes-issues 创建 issue
/github-pr-workflow 创建 PR
```

### Webhook 集成

结合 webhook 功能，GitHub 事件自动触发 Hermes：

```bash
# 订阅 GitHub issues 事件
hermes webhook subscribe github-issues \
  --skills github-issues \
  --deliver feishu

# 测试 webhook
hermes webhook test github-issues
```

## 故障排除

### gh CLI 未认证

```bash
# 检查状态
gh auth status

# 重新认证
gh auth logout
gh auth login
```

### Token 权限不足

确保 Token 包含所需 scopes：

| 操作 | 最小 Scope |
|------|-----------|
| 读取 public repo | `repo:public_repo` |
| 读取 private repo | `repo` |
| 管理 PR | `repo` |
| 触发 Actions | `workflow` |

### API 限流

GitHub API 有速率限制：

- 未认证：60 请求/小时
- 已认证：5000 请求/小时

使用 `gh` CLI 会自动处理认证和限流。

## 总结

Hermes Agent 让 GitHub 管理变得轻松：

- ✅ **自然语言操作** — 告别记忆繁琐命令
- ✅ **完整工作流** — Issue → Branch → PR → CI → Merge
- ✅ **自动修复 CI** — 失败时智能分析和修复
- ✅ **多技能协作** — github-auth + github-issues + github-pr-workflow
- ✅ **Webhook 集成** — 事件自动触发处理

现在就试试 `/github-issues` 或 `/github-pr-workflow`，体验高效的 GitHub 管理吧！
