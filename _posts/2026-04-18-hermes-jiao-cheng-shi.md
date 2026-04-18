---
layout: post
title: "Hermes 教程十：定时任务自动执行"
date: 2026-04-18 18:00:00 +0800
categories: [Hermes Agent]
tags: [定时任务, cron, 自动化, schedule, 每日任务]
---

# 定时任务：让 Hermes Agent 每天自动执行

不想每天重复同样的工作？Hermes Agent 内置强大的定时任务系统，支持 cron 表达式、间隔执行、一次性任务，让你的 AI 助手成为 24 小时不知疲倦的数字员工。

## 定时任务存储

任务配置文件存储在：

```
~/.hermes/cron/
├── jobs.json          # 任务定义
└── output/            # 任务输出
    └── {job_id}/
        └── {timestamp}.md
```

## cronjob 工具详解

Hermes 提供 `cronjob` 工具，支持完整的 CRUD 操作：

### 1. 创建定时任务（create）

```
cronjob(action="create", name="任务名称", schedule="调度规则", prompt="执行指令", ...)
```

**必填参数：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | 任务名称（唯一标识）| `"daily-gitlab-stats"` |
| `schedule` | 调度规则 | `"0 9 * * *"` |
| `prompt` | 执行指令 | `"统计昨日 GitLab 项目情况"` |

**可选参数：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `deliver` | 送达方式 | `"feishu"` |
| `skills` | 预加载技能 | `["github-issues"]` |
| `enabled` | 是否启用 | `true` |
| `repeat.times` | 重复次数 | `10` |

### 2. 列出所有任务（list）

```
cronjob(action="list")
```

返回所有任务及其状态：

```
ID                  NAME                    SCHEDULE         NEXT RUN              STATUS
─────────────────────────────────────────────────────────────────────────────────────
abc123              daily-gitlab-stats      0 9 * * *        2026-04-19 09:00     active
def456              weekly-report          0 8 * * 1        2026-04-21 08:00     active
ghi789              gitlab-merge-check      every 30m        2026-04-18 19:30     active
```

### 3. 更新任务（update）

```
cronjob(action="update", job_id="abc123", schedule="0 10 * * *", ...)
```

可更新的字段：
- `schedule` — 调度时间
- `prompt` — 执行指令
- `deliver` — 送达方式
- `skills` — 预加载技能
- `enabled` — 启用状态

### 4. 删除任务（remove）

```
cronjob(action="remove", job_id="abc123")
```

## 调度格式详解

Hermes 支持四种调度格式：

### 1. Cron 表达式（标准）

```
┌───────────── 分钟 (0-59)
│ ┌─────────── 小时 (0-23)
│ │ ┌───────── 日 (1-31)
│ │ │ ┌─────── 月 (1-12)
│ │ │ │ ┌───── 星期 (0-7, 0和7都是周日)
│ │ │ │ │
* * * * *
```

**常用示例：**

| 表达式 | 含义 |
|--------|------|
| `0 9 * * *` | 每天 9:00 |
| `0 9 * * 1-5` | 工作日 9:00 |
| `30 8 * * *` | 每天 8:30 |
| `0 */2 * * *` | 每 2 小时 |
| `0 9,18 * * *` | 每天 9:00 和 18:00 |
| `0 0 1 * *` | 每月 1 日午夜 |
| `30 9 * * 1` | 每周一 9:30 |

### 2. 简写间隔

```
every 30m       # 每 30 分钟
every 2h        # 每 2 小时
every 6h        # 每 6 小时
every 1d        # 每 1 天
```

### 3. 持续时间（一次性）

```
30m     # 30 分钟后执行（一次性）
2h      # 2 小时后执行（一次性）
1d      # 1 天后执行（一次性）
```

### 4. ISO 时间戳（指定时间一次性）

```
2026-04-20T10:00:00        # 2026年4月20日 10:00 执行
2026-04-20T14:30:00+08:00  # 指定时区
```

## 送达方式（deliver）

任务执行完成后，结果发送到指定位置：

| 送达方式 | 说明 | 配置 |
|---------|------|------|
| `origin` | 原始方式（默认）| 根据任务创建方式 |
| `local` | 保存到本地文件 | `~/.hermes/cron/output/` |
| `feishu` | 飞书消息 | 需要配置飞书机器人 |
| `qqbot` | QQ 机器人 | 需要配置 QQ 机器人 |
| `telegram` | Telegram | 需要配置 Telegram Bot |

### 飞书送达配置

```yaml
# 在 ~/.hermes/.env 中配置
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_ENCRYPT_KEY=your_encrypt_key
FEISHU_VERIFICATION_TOKEN=your_verification_token
```

创建任务时指定：

```
cronjob(action="create",
        name="daily-report",
        schedule="0 9 * * *",
        prompt="生成每日报告",
        deliver="feishu")
```

## 实际案例：每日 GitLab 统计

### 任务创建

```
你：帮我创建一个每天早上9点自动统计 GitLab 项目的定时任务
Hermes：好的，我来创建这个定时任务。需要确认几个问题：

1. 统计哪些项目？（全部还是指定项目）
2. 需要统计哪些指标？（commits、MRs、issues、成员变动）
3. 结果发送到飞书还是本地？

你：统计所有项目，统计 commits 和 MRs，发送到飞书
Hermes：
```

### 创建任务的命令

```bash
hermes chat -c "
cronjob(action='create',
        name='daily-gitlab-stats',
        schedule='0 9 * * *',
        prompt='统计昨日所有 GitLab 项目的 commits 和 MR 情况，生成简洁报告',
        deliver='feishu',
        skills=['gitlab-stats'])
"
```

### 查看任务输出

```bash
# 查看任务输出目录
ls ~/.hermes/cron/output/

# 查看具体输出
cat ~/.hermes/cron/output/daily-gitlab-stats/2026-04-18_09-00-00.md
```

### 示例输出

```markdown
# GitLab 每日统计报告 - 2026-04-18

## 概览
- 总项目数：15
- 活跃项目：12

## Commits 排行
| 项目 | commits |
|------|---------|
| backend-api | 23 |
| frontend-web | 18 |
| mobile-app | 12 |

## MR 情况
- 新建 MR：8
- 合并 MR：6
- 待审查：2

## 建议
- backend-api 项目提交活跃，建议关注代码质量
- mobile-app 有 2 个 MR 超过 3 天未审查
```

## 技能参数传递（skills）

定时任务可以预加载技能，确保任务执行时使用正确的工具：

```bash
hermes chat -c "
cronjob(action='create',
        name='github-issue-triage',
        schedule='every 30m',
        prompt='检查 GitHub issues，标记需要分类的工单',
        skills=['github-issues', 'github-auth'])
"
```

### 多个技能

```yaml
skills:
  - github-issues    # GitHub 工单管理
  - github-auth      # GitHub 认证
  - gitlab-stats     # GitLab 统计
```

## 任务管理

### 暂停任务

```
cronjob(action="update", job_id="abc123", enabled=false)
```

或使用快捷命令：

```bash
hermes cron pause abc123
```

### 恢复任务

```bash
hermes cron resume abc123
```

### 手动触发任务

立即执行任务（不等下次调度时间）：

```
cronjob(action="trigger", job_id="abc123")
```

### 查看任务状态

```bash
hermes cron list
hermes cron status abc123
```

### 查看任务历史

```bash
hermes cron history abc123
```

## 完整示例对话

```
你：帮我创建一个每周一早上8点发送周报的定时任务
Hermes：好的！我来帮你创建周报定时任务。

请告诉我：
1. 周报内容需要包含哪些？（项目进度、待办事项、风险项？）
2. 报告格式偏好？（详细版/简洁版）
3. 通过什么渠道发送？（飞书/邮件/本地）

你：要包含项目进度和待办事项，用飞书发送
Hermes：

任务已创建！

📅 **周报定时任务**
- 名称：weekly-report
- 调度：每周一 08:00
- 内容：项目进度 + 待办事项
- 送达：飞书

下次执行：2026-04-21 08:00

你想现在手动触发一次测试吗？
```

## 注意事项

1. **调度时区**：任务按配置的时区执行，默认使用系统时区
2. **执行超时**：默认 10 分钟，可通过 `HERMES_CRON_TIMEOUT` 环境变量调整
3. **错误处理**：任务失败会记录错误信息，可通过 `hermes cron history` 查看
4. **并发控制**：同一任务不会并发执行，下次调度会等待前一次完成

## 总结

Hermes Agent 的定时任务系统让你的 AI 助手自动化：

- ✅ Cron 表达式 + 简写格式，使用灵活
- ✅ 支持飞书、QQ 等多种送达方式
- ✅ 技能预加载，执行更智能
- ✅ 完整的 CRUD 管理
- ✅ 输出持久化到本地

设置好定时任务后，你就可以专注于更有价值的工作了！
