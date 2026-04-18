---
layout: post
title: "Hermes 教程八：config.yaml深度配置"
date: 2026-04-18 18:00:00 +0800
categories: [Hermes Agent]
tags: [配置, 模型, 人格, toolsets, config.yaml]
---

# Hermes Agent 进阶配置完全指南：模型、人格、工具开关

作为 IT 从业者，你是否想让 Hermes Agent 更贴合自己的使用习惯？本文从实际运行的 `~/.hermes/config.yaml` 出发，深入讲解每个配置项的作用，助你打造专属的 AI 助手。

## 配置文件位置

Hermes Agent 的所有配置集中在两个文件：

- **`~/.hermes/config.yaml`** — 模型、工具集、人格、终端等设置
- **`~/.hermes/.env`** — API 密钥和密钥信息（与 config.yaml 同级目录）

## 完整配置示例

以下是一份生产可用的 `config.yaml`（来自曹总真实运行环境）：

```yaml
model:
  default: MiniMax-M2.7
  provider: minimax-cn
  base_url: https://api.minimaxi.com/anthropic

providers: {}
fallback_providers: []
credential_pool_strategies: {}

toolsets:
  - hermes-cli

agent:
  max_turns: 90
  gateway_timeout: 1800
  restart_drain_timeout: 60
  service_tier: ''
  tool_use_enforcement: auto
  gateway_timeout_warning: 900
  gateway_notify_interval: 600
  verbose: false
  reasoning_effort: medium

display:
  personality: kawaii

terminal:
  backend: local
  modal_mode: auto
  cwd: .
  timeout: 180
  env_passthrough: []
  docker_image: nikolaik/python-nodejs:python3.11-nodejs20
  container_cpu: 1
  container_memory: 5120
  container_disk: 51200
  container_persistent: true
  persistent_shell: true
  lifetime_seconds: 300

browser:
  inactivity_timeout: 120
  command_timeout: 30
  record_sessions: false
  allow_private_urls: false

memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200
  user_char_limit: 1375
  provider: ''
  nudge_interval: 10
  flush_min_turns: 6

compression:
  enabled: true
  threshold: 0.5
  target_ratio: 0.2
  protect_last_n: 20

checkpoints:
  enabled: true
  max_snapshots: 50

custom_providers:
  - name: minimax
    base_url: https://api.minimaxi.com/anthropic
    api_key: ''
    api_mode: anthropic_messages
```

## 模型配置（model / provider / base_url）

```yaml
model:
  default: MiniMax-M2.7    # 使用的模型名称
  provider: minimax-cn     # 提供商标识
  base_url: https://api.minimaxi.com/anthropic  # API 端点
```

### 支持的 Providers

从配置文件中可以看到支持的提供商包括：

| Provider | 说明 |
|----------|------|
| `openai` | OpenAI 系列模型 |
| `anthropic` | Claude 系列 |
| `openrouter` | 路由到任意模型 |
| `minimax-cn` | MiniMax（中国区）|
| `minimax` | MiniMax 国际版 |
| `nous` | Nous Portal |
| `codex` | OpenAI Codex |
| `zai` | Z.AI / GLM |
| `kimi-coding` | Kimi / Moonshot |
| `bedrock` | AWS Bedrock |

### 自定义 Provider 配置

```yaml
custom_providers:
  - name: my-provider
    base_url: https://your-custom-endpoint.com/v1
    api_key: ${MY_API_KEY}  # 引用 .env 中的变量
    api_mode: openai         # 或 anthropic_messages
```

### 备用模型（Fallback）

当主模型不可用时（429/503 错误），自动切换到备用模型：

```yaml
fallback_providers:
  - provider: openrouter
    model: anthropic/claude-sonnet-4
```

## Agent 执行控制

```yaml
agent:
  max_turns: 90              # 单次对话最大轮数
  gateway_timeout: 1800      # 网关超时（秒），0=无限制
  restart_drain_timeout: 60  # 重启时优雅退出超时
  tool_use_enforcement: auto # auto/true/false，强制模型调用工具
  gateway_timeout_warning: 900    # 超时前警告（秒）
  gateway_notify_interval: 600     # 定期状态通知间隔
  reasoning_effort: medium        # 推理努力程度
```

## 工具集开关（toolsets）

```yaml
toolsets:
  - hermes-cli        # Hermes 内置 CLI 命令
  # - browser         # 浏览器自动化
  # - vision          # 视觉理解
  # - web             # 网页搜索
  # - terminal        # 终端执行
  # - file            # 文件操作
```

### 可用工具集列表

| 工具集 | 说明 |
|--------|------|
| `hermes-cli` | Hermes 内置命令（默认开启）|
| `browser` | Playwright 浏览器自动化 |
| `vision` | 图片理解和分析 |
| `web` | 网页搜索和内容提取 |
| `terminal` | 沙箱终端执行 |
| `file` | 文件读写搜索操作 |
| `code_execution` | Python/JS 代码执行 |
| `mcp` | MCP 协议外部工具 |

### 平台特定工具集

```yaml
platform_toolsets:
  cli:
    - hermes-cli
  telegram:
    - hermes-telegram
  discord:
    - hermes-discord
  whatsapp:
    - hermes-whatsapp
  qqbot:
    - hermes-qqbot
```

## 12 种人格配置（personalities）

Hermes Agent 内置 12 种不同风格的人格，通过 `display.personality` 切换：

```yaml
personalities:
  helpful: You are a helpful, friendly AI assistant.
  concise: You are a concise assistant. Keep responses brief and to the point.
  technical: You are a technical expert. Provide detailed, accurate technical information.
  creative: You are a creative assistant. Think outside the box and offer innovative solutions.
  teacher: You are a patient teacher. Explain concepts clearly with examples.
```

### 全部 12 种人格详解

| 人格名称 | 风格描述 | 适用场景 |
|---------|---------|---------|
| `helpful` | 乐于助人的友好助手 | 通用对话 |
| `concise` | 简洁明了，直击要点 | 快速问答 |
| `technical` | 技术专家，详细准确 | 技术问题 |
| `creative` | 创新思维，跳出框框 | 头脑风暴 |
| `teacher` | 耐心教导，举例说明 | 学习辅导 |
| `kawaii` | 可爱风格 ✨ ٩(◕‶◕｡)۶ | 轻松互动 |
| `catgirl` | 猫娘风格 "nya~" | 趣味对话 |
| `pirate` | 海盗风格 "Arrr!" | 冒险故事 |
| `shakespeare` | 莎士比亚文风 | 文学创作 |
| `surfer` | 冲浪风格 "Duuude!" | 轻松聊天 |
| `noir` | 黑色电影侦探风格 | 推理分析 |
| `uwu` | 可爱卖萌风格 | 轻松娱乐 |
| `philosopher` | 哲学家风格 | 深度思考 |
| `hype` | 激情满满风格 | 激励场景 |

### 切换人格

```yaml
display:
  personality: technical  # 切换到技术人格
```

或在对话中直接说"切换到创意模式"。

## 代理 / Proxy 设置

Hermes Agent 支持通过环境变量配置代理：

```bash
# 在 ~/.hermes/.env 中配置
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=http://proxy.example.com:8080
NO_PROXY=localhost,127.0.0.1,.local
```

对于需要代理的 API 端点，可以在 `custom_providers` 中配置：

```yaml
custom_providers:
  - name: openai-via-proxy
    base_url: http://your-proxy.com/v1
    api_key: ${OPENAI_API_KEY}
```

## 记忆配置（memory）

```yaml
memory:
  memory_enabled: true        # 启用记忆功能
  user_profile_enabled: true   # 记录用户画像
  memory_char_limit: 2200     # 记忆字符上限
  user_char_limit: 1375       # 用户信息字符上限
  nudge_interval: 10          # 记忆提醒间隔（轮）
  flush_min_turns: 6          # 最少对话轮数后保存
```

## 配置管理命令

```bash
# 查看当前配置
hermes config

# 编辑配置文件
hermes config edit

# 设置特定值
hermes config set model.default "claude-sonnet-4"
hermes config set display.personality "technical"

# 重新运行安装向导
hermes config wizard
```

## 总结

通过深度配置 `config.yaml`，你可以：

- 切换不同的 AI 模型和提供商
- 自定义人格风格
- 精细控制工具集权限
- 配置代理和备用方案
- 调整记忆和压缩策略

曹总的经验是：先用 `hermes config edit` 查看完整配置，根据实际需求逐项调整。配置修改后下次启动自动生效，无需重启服务。
