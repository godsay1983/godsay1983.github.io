---
layout: post
title: "记忆系统：让 Hermes Agent 记住你的偏好"
date: 2026-04-18 18:00:00 +0800
categories: [Hermes Agent]
tags: [记忆系统, memory, USER.md, MEMORY.md, 偏好]
---

# 记忆系统：让 Hermes Agent 记住你的偏好

你是否遇到过这种情况：每次启动 Hermes Agent 都要重新解释自己的背景和使用习惯？本文详细介绍 Hermes 的双层记忆系统，让你告别重复说明，打造真正懂你的 AI 助手。

## 记忆系统架构

Hermes Agent 采用双层记忆架构：

```
~/.hermes/
├── memories/
│   ├── MEMORY.md    # 代理的记忆（长期）
│   └── USER.md      # 用户画像（长期）
└── sessions/
    └── state.db     # 会话持久化数据库
```

### 两种记忆类型

| 类型 | 文件 | 用途 | 字符上限 |
|------|------|------|---------|
| **代理记忆** | `MEMORY.md` | 环境事实、项目规范、工具技巧 | 2200 |
| **用户画像** | `USER.md` | 用户偏好、沟通风格、工作习惯 | 1375 |

## 配置文件

记忆系统在 `config.yaml` 中的相关配置：

```yaml
memory:
  memory_enabled: true        # 启用记忆功能
  user_profile_enabled: true # 记录用户画像
  memory_char_limit: 2200    # 记忆字符上限
  user_char_limit: 1375      # 用户信息字符上限
  nudge_interval: 10          # 多少轮对话后提醒保存
  flush_min_turns: 6          # 最少对话轮数后允许保存
  provider: ''                # 外置记忆provider（可选）
```

## memory 工具详解

Hermes 提供统一的 `memory` 工具，支持四种操作：

### 1. 添加记忆（add）

```
memory(action="add", entry="你的记忆内容", type="memory|user")
```

**示例对话：**

```
你：我是曹总，IT从业者，平时用飞书联系，请记住我的背景
Hermes：已将你的背景信息保存到用户画像中。
        - 姓名：曹总
        - 职业：IT从业者
        - 联系方式：飞书
```

### 2. 读取记忆（read）

```
memory(action="read", type="memory|user")
```

**示例输出：**

```
=== 用户画像 ===
- 曹总，IT从业者
- 平时用飞书联系
- 偏好简洁的技术回答
- 项目多使用 GitLab
```

### 3. 替换记忆（replace）

通过短字符串匹配找到并替换：

```
memory(action="replace", old="旧的记忆片段", new="新的记忆内容")
```

### 4. 删除记忆（remove）

```
memory(action="remove", entry="要删除的记忆片段")
```

## 实际使用示例

### 场景 1：保存项目环境信息

```
你：我们在用 GitLab 管理代码，Jenkins 做 CI，Nexus 做制品管理
Hermes：已记住你的 DevOps 环境配置：
        - 代码管理：GitLab
        - CI/CD：Jenkins
        - 制品库：Nexus
```

### 场景 2：记录编码规范

```
你：请记住我们项目的 PR 规范：所有 PR 必须有测试，CI 通过后才能合并
Hermes：已记录 PR 规范：
        - 必须包含测试
        - CI 通过是合并前提
```

### 场景 3：更新联系方式

```
你：我换微信号了，新号是 WeChatID123
Hermes：已将联系方式更新为新微信号。
```

## 会话持久化（state.db）

会话数据存储在 SQLite 数据库中：

```bash
~/.hermes/sessions/state.db
```

### 数据库内容

| 表名 | 内容 |
|------|------|
| `messages` | 对话历史记录 |
| `sessions` | 会话元数据 |
| `memory_entries` | 记忆条目 |
| `user_entries` | 用户信息条目 |

### 查看会话历史

```bash
# 列出最近会话
hermes sessions list

# 恢复某个会话
hermes sessions resume <session_id>

# 搜索会话内容
hermes sessions search "GitLab"
```

## 自动记忆保存

Hermes Agent 会根据配置自动提醒保存重要信息：

```yaml
memory:
  nudge_interval: 10      # 每10轮对话检查是否需要保存
  flush_min_turns: 6      # 对话至少6轮后才提示保存
```

当检测到重要信息时，Hermes 会主动提示：

```
💡 我注意到你提到了 [项目规范]，需要我帮你保存到记忆吗？
```

## 外部记忆 Provider

除了内置的记忆系统，Hermes 还支持外置记忆 Provider：

### Supermemory

语义化长期记忆，支持：
- Profile recall
- 语义搜索
- 对话内容自动摄入

### Honcho

AI 原生记忆后端，提供：
-  dialectic reasoning
- 深度用户建模
- 跨会话记忆同步

安装外部 Provider 后，在 `config.yaml` 中配置：

```yaml
memory:
  provider: honcho  # 使用 honcho 作为记忆 provider
```

## 最佳实践

### 1. 定期更新记忆

建议每隔一段时间检查和更新记忆：

```
你：查看我的用户画像
Hermes：当前保存的信息：
        - IT从业者
        - 用飞书联系
        ...
        
你：请帮我补充：最近在学习 Kubernetes
Hermes：已更新用户画像。
```

### 2. 使用简洁的短句

记忆条目建议用短句，便于后续匹配和更新：

```
# ✅ 推荐
- IT从业者
- 用飞书沟通
- 喜欢简洁回答

# ❌ 不推荐
- 我是一名拥有10年工作经验的IT从业者，平时主要使用飞书进行工作沟通
```

### 3. 分类保存

不同类型的信息分开保存：

- **项目信息** → MEMORY.md
- **个人偏好** → USER.md

## 命令行管理

```bash
# 查看记忆状态
hermes memory status

# 关闭外置记忆（使用内置）
hermes memory off

# 重置记忆
hermes memory reset
```

## 安全机制

为了防止记忆注入攻击，Hermes 会对记忆内容进行安全扫描：

- 检测提示注入模式
- 过滤不可见 Unicode 字符
- 阻止读取敏感文件（如 `.env`）的命令

如果保存的内容包含可疑模式，会被拒绝：

```
错误：检测到内容包含威胁模式 'prompt_injection'，
      记忆内容不能包含注入或泄露载荷。
```

## 总结

Hermes Agent 的记忆系统让你只需说明一次：

1. **首次对话** → 介绍自己的背景和偏好
2. **自动保存** → 关键信息自动记录到 USER.md
3. **跨会话复用** → 下次启动自动加载记忆
4. **随时更新** → 用 memory 工具增删改查

这样你的 AI 助手会越来越懂你，工作效率大幅提升！
