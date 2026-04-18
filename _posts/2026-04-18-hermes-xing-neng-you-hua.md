---
layout: post
title: "性能优化：加快响应、节省 Token"
date: 2026-04-18 18:00:00 +0800
categories: [Hermes Agent]
tags: [性能优化, Token 节省, context_compressor, 上下文压缩]
---

在使用 Hermes Agent 时，性能优化是一个重要话题。本文介绍如何通过各种技术手段加快响应速度、节省 Token 消耗，让 Hermes 更加高效。

## 上下文压缩原理

Hermes 内置的 `context_compressor.py` 是性能优化的核心组件。其工作原理如下：

### 压缩时机

上下文压缩在以下情况触发：

1. **Token 达到阈值**：当对话消耗的 Token 数量接近模型上下文窗口上限时
2. **对话轮次积累**：经过一定数量的对话交互后
3. **手动触发**：用户可以通过特定命令主动压缩上下文

### 压缩策略

```python
# context_compressor.py 中的关键参数
_MIN_SUMMARY_TOKENS = 200      # 最小摘要长度
_SUMMARY_RATIO = 0.20          # 压缩比：20% 的内容作为摘要
_SUMMARY_TOKENS_CEILING = 2000  # 摘要最大长度
```

### 压缩过程

1. **识别可压缩部分**：对话开头的用户消息和助手回复
2. **调用辅助模型**：使用轻量级模型（如 gpt-3.5-turbo）生成摘要
3. **保留关键信息**：最近的对话、用户偏好、任务状态
4. **替换原始内容**：用摘要替换被压缩的对话历史

### 压缩前缀

压缩后的上下文会带有特殊标记：

```
[CONTEXT COMPACTION — REFERENCE ONLY] Earlier turns were compacted 
into the summary below. This is a handoff from a previous context 
window — treat it as background reference, NOT as active instructions.
```

这个前缀确保模型理解上下文已被压缩，不会重复执行已完成的任务。

## paginator.posts 限制

在处理博客文章列表时，过多的文章会导致响应变慢和 Token 浪费。

### 问题场景

Jekyll 的 `paginator.posts` 默认返回所有文章：

```liquid
{% for post in paginator.posts %}
  {{ post.title }}
{% endfor %}
```

当文章数量超过 100 篇时，每次页面渲染都会消耗大量资源。

### 解决方案

使用 `limit_posts` 变量限制每页文章数量：

```liquid
---
layout: default
limit_posts: 10
---

{% for post in paginator.posts | limit: 10 %}
  <article>
    <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
    <p>{{ post.excerpt }}</p>
  </article>
{% endfor %}
```

### 在 Hermes 中配置

在博客配置文件中添加：

```yaml
# _config.yml
paginate: 10
paginate_path: "/page:num/"
```

## session_search 减少重复

### session_search 的作用

Hermes 使用 SQLite FTS5（全文搜索）存储会话历史，`session_search` 功能可以快速检索历史对话：

```python
# 在 hermes_state.py 中
class SessionDB:
    def search_sessions(self, query: str, limit: int = 10):
        """搜索历史会话"""
        # 使用 FTS5 全文索引
        # 返回相关的历史会话片段
```

### 减少重复的策略

1. **相似问题复用**：当用户提出与历史问题相似的问题时，直接返回已有答案
2. **上下文复用**：在多轮对话中，识别并复用之前的上下文信息
3. **结果缓存**：将常用查询结果缓存，避免重复 API 调用

### 配置示例

```yaml
# ~/.hermes/config.yaml
session:
  search_enabled: true
  cache_results: true
  max_cache_age: 3600  # 缓存 1 小时
```

## 模型选择与速度平衡

### 模型速度对比

| 模型 | 速度 | 智能程度 | 适用场景 |
|------|------|---------|---------|
| claude-3-haiku | 最快 | 中等 | 简单任务、快速响应 |
| claude-3-sonnet | 快 | 中高 | 日常对话、代码生成 |
| claude-3-opus | 较慢 | 最高 | 复杂推理、深度分析 |
| gpt-4 | 较慢 | 高 | 通用任务 |
| gpt-3.5-turbo | 最快 | 中等 | 简单任务、摘要 |

### 在 Hermes 中切换模型

```bash
# 使用 /model 命令切换
/model claude-3-haiku

# 在配置文件中设置默认模型
# ~/.hermes/config.yaml
default_model: anthropic/claude-3-sonnet-4
```

### 智能模型选择策略

```python
# 根据任务复杂度自动选择模型
def select_model(task_type: str) -> str:
    if task_type in ["simple_question", "greeting"]:
        return "claude-3-haiku"
    elif task_type in ["code_generation", "writing"]:
        return "claude-3-sonnet-4"
    elif task_type in ["complex_reasoning", "analysis"]:
        return "claude-3-opus-4"
    return "claude-3-sonnet-4"
```

## Token 节省技巧

### 1. 精简系统提示

```python
# 原始系统提示（约 500 tokens）
SYSTEM_PROMPT = """
你是一个智能助手，可以帮助用户完成各种任务。
你具备以下能力：
1. 回答问题
2. 编写代码
3. 分析数据
4. 写作文章
...
"""

# 精简后（约 150 tokens）
SYSTEM_PROMPT = "你是一个助手，帮助用户完成任务。"
```

### 2. 利用上下文压缩

开启自动上下文压缩，让 Hermes 智能管理上下文：

```yaml
# ~/.hermes/config.yaml
context:
  auto_compress: true
  compression_threshold: 0.8  # 80% 时压缩
```

### 3. 批量操作

将多个相关操作合并为一次请求：

```python
# 低效：多次 API 调用
result1 = chat("总结这篇文章")
result2 = chat("提取关键词")
result3 = chat("翻译成英文")

# 高效：一次调用完成多个任务
result = chat("""对这个文章进行三步处理：
1. 总结主要内容
2. 提取关键词
3. 翻译成英文""")
```

### 4. 使用快捷引用

对于已存在的上下文，使用快捷引用而非重复：

```python
# 低效
chat("根据我们之前讨论的关于博客运营的内容...")

# 高效
chat("基于刚才的博客运营方案，现在帮我写一篇文章")
```

### 5. 控制对话深度

避免过长的多轮对话，将复杂任务分解：

```
复杂任务 → 分解为 3-5 个简单任务
    ↓
每个任务单独完成
    ↓
最终汇总结果
```

## 性能监控

```bash
# 查看当前会话的 Token 使用
/hermes stats

# 查看最近任务的性能数据
hermes --profile
```

## 总结

Hermes 性能优化的核心策略：

| 优化方向 | 方法 | 效果 |
|---------|------|------|
| 上下文管理 | 开启 auto_compress | 节省 30-50% Token |
| 模型选择 | 按任务复杂度选模型 | 速度提升 2-3x |
| 请求优化 | 批量操作、减少调用 | 节省 API 成本 |
| 缓存利用 | session_search 复用 | 避免重复计算 |

合理使用这些优化技巧，可以让 Hermes 在保持高质量输出的同时，大幅提升响应速度和成本效率。
