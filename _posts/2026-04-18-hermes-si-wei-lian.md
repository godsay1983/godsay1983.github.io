---
layout: post
title: "让 AI 想清楚再回答：Hermes 的思维链与追问技巧"
date: 2026-04-18 18:00:00 +0800
categories: [使用技巧]
tags: [思维链, 推理配置, 深度思考]
---

# 让 AI 想清楚再回答：Hermes 的思维链与追问技巧

Hermes Agent 不仅仅是一个问答机器人，它的思维链（Chain-of-Thought）系统让你可以控制 AI 的思考深度——从快速响应到深度推理，按需切换。这对于复杂分析、多步规划、代码调试等场景至关重要。

## 什么是 Reasoning Effort

Hermes 通过 `reasoning_effort` 参数控制模型的内部思考量。这个概念源自 Anthropic 的 Claude 模型推理机制——模型在生成最终回答前，会在内部进行更深度或更浅层的推理。

配置层级：

| 级别 | 说明 | 适用场景 |
|------|------|----------|
| `off` | 关闭推理思考 | 简单问答、快速查询 |
| `low` | 轻度思考 | 普通对话、简单任务 |
| `medium` | 中度思考 | 编程辅助、一般分析 |
| `high` | 深度思考 | 复杂规划、调试、深度分析 |

## 如何设置 Reasoning Effort

### 方法一：CLI 斜杠命令（会话级）

在 `hermes >` 交互提示符下：

```
hermes > /reasoning high
```

系统会显示当前设置：

```
Reasoning effort: high
```

可用值：`off`、`low`、`medium`、`high`，或用 `show` 查看当前推理内容。

### 方法二：配置文件（持久化）

编辑 `~/.hermes/config.yaml`：

```yaml
agent:
  reasoning_effort: high

display:
  show_reasoning: true    # 在终端实时显示模型的思考过程
```

重启 hermes 或下次启动时自动生效。

### 方法三：API 级别动态控制

在 Python 代码中创建 Agent 时：

```python
from run_agent import AIAgent

agent = AIAgent(
    model="anthropic/claude-sonnet-4-20250514",
    reasoning_effort="high"
)
```

## 查看模型的思考过程

设置 `display.show_reasoning: true` 后，每次对话都会在终端看到模型的分步思考，例如：

```
┏━━━ Reasoning (high) ━━━
分析这个问题需要分三步：
1. 首先理解用户的需求是什么
2. 然后搜索相关的代码模式
3. 最后组合成最佳方案
→ 第一步：用户需要一个函数来...
→ 第二步：找到现有实现...
→ 最终方案：...
━━━━━━━━━━━━━━━━━━━━
```

这个思考过程有助于你判断模型是否真正理解了问题。

## 追问技巧：让 AI 更精确

Hermes 支持多轮对话中的追问，以下是几个高效追问策略：

### 1. 指定思考步骤

```
用户：帮我优化这个 SQL 查询

hermes > 追问：请先分析这个查询的执行计划，告诉我哪里有性能问题，再给出优化建议
```

### 2. 限制回答范围

```
用户：介绍一下 Kubernetes

hermes > 追问：只介绍与网络相关的部分，其他略过
```

### 3. 要求提供多个方案

```
用户：帮我选型一个缓存方案

hermes > 追问：分别给出 Redis、Memcached、本地缓存三种方案的优缺点和适用场景
```

## 源代码中的 Reasoning 实现

理解 Hermes 的思维链如何与模型交互，有助于更精确地配置。

### 消息格式中的 Reasoning

推理内容存储在 assistant 消息的 `reasoning` 字段中：

```python
# run_agent.py 中的消息格式
messages = [
    {"role": "system", "content": "你是一个有帮助的助手"},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "...", "reasoning": "内部思考链..."},
    {"role": "tool", "tool_call_id": "...", "content": "..."},
]
```

### 核心循环

```python
# run_agent.py 核心循环
while api_call_count < self.max_iterations and self.iteration_budget.remaining > 0:
    response = client.chat.completions.create(
        model=model, messages=messages, tools=tool_schemas
    )
    if response.tool_calls:
        for tool_call in response.tool_calls:
            result = handle_function_call(tool_call.name, tool_call.args, task_id)
            messages.append(tool_result_message(result))
        api_call_count += 1
    else:
        return response.content
```

当模型输出 `tool_calls` 时，说明它正在调用工具（文件读写、终端命令等），这也是一种"思考外化"的表现。

## reasoning_effort 的底层原理

在 `hermes_cli/setup.py` 中可以看到：

```python
def _current_reasoning_effort(config: Dict[str, Any]) -> str:
    agent_cfg = config.get("agent", {})
    return str(agent_cfg.get("reasoning_effort") or "").strip().lower()

def _set_reasoning_effort(config: Dict[str, Any], effort: str) -> None:
    agent_cfg = config.setdefault("agent", {})
    agent_cfg["reasoning_effort"] = effort
```

这个配置最终会传递给模型 provider，影响模型的思考 token 预算。

## 子 Agent 的独立推理控制

如果你使用 `delegate_tool` 委托子 Agent 处理任务，主 Agent 和子 Agent 可以有独立的 `reasoning_effort`：

```yaml
# config.yaml
delegation:
  reasoning_effort: medium   # 子 agent 用 medium，不影响主 agent
```

## 实战案例

### 场景一：代码调试

```
你> 这个 Python 程序报错了：
   TypeError: 'NoneType' object is not iterable

hermes (reasoning=high)> 我来分析这个错误：
   第一步：理解错误类型 —— NoneType 说明某处返回了 None
   第二步：搜索代码中可能返回 None 的地方
   第三步：追踪变量流向，找到根源
   → 问题出在 filter() 后的结果没有做空值处理
   → 建议添加：if result is not None: ...
```

### 场景二：架构设计

```
你> 帮我设计一个微服务架构

hermes (reasoning=high)> 在给出具体方案前，我需要考虑：
   - 服务拆分粒度（按业务域 vs 按技术域）
   - 通信协议（同步 HTTP/gRPC vs 异步消息队列）
   - 数据一致性策略（最终一致 vs 强一致）
   - 部署和运维复杂度
   → 推荐：领域驱动设计 + 事件溯源 + Kubernetes
```

## 小结

| 功能 | 命令/配置 |
|------|----------|
| 设置推理深度 | `/reasoning high` |
| 显示思考过程 | `display.show_reasoning: true` |
| 持久化配置 | `~/.hermes/config.yaml` |
| 子 Agent 推理 | `delegation.reasoning_effort` |

合理使用思维链配置，能让 Hermes 在简单任务上快速响应，在复杂任务上深度思考，真正做到"该快就快，该深就深"。
