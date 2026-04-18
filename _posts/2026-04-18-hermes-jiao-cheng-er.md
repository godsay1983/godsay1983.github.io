---
layout: post
title: "Hermes 教程二：零基础入门"
date: 2026-04-18 18:00:00 +0800
categories: [入门教程]
tags: [新手入门, 安装配置, CLI]
---

# 零基础入门：5分钟跑通 Hermes Agent

Hermes Agent 是由 Nous Research 开发的新一代 AI 助手框架，支持 CLI、飞书、QQ 等多平台运行，同时内置 Skill 技能系统、思维链推理、MCP 工具调用等强大功能。本文手把手带你从零开始，5 分钟内跑通第一个对话。

## 环境要求

- Python 3.11+
- Git
- 网络正常（用于拉取模型 API）

## 第一步：克隆代码仓库

```bash
cd ~
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
```

## 第二步：创建虚拟环境并安装依赖

```bash
python3 -m venv venv
source venv/bin/activate      # 激活虚拟环境（以后每次使用都要执行）
pip install -e .
```

> **注意**：`source venv/bin/activate` 这条命令非常重要。每次运行 Hermes 之前都必须先激活虚拟环境，否则会报模块找不到的错误。

## 第三步：配置 API Key

Hermes 支持 OpenAI、Anthropic、AWS Bedrock 等多种模型 provider。最简单的入门方式是使用 OpenAI兼容接口：

```bash
# 创建环境变量文件
cat > ~/.hermes/.env << 'EOF'
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://api.openai.com/v1
EOF
```

如果你使用 Anthropic 的 Claude 模型：

```bash
cat > ~/.hermes/.env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
EOF
```

## 第四步：运行交互式 CLI

```bash
source venv/bin/activate
hermes
```

正常情况下，你会看到类似这样的启动画面（带颜色 banner）：

```
╔══════════════════════════════════════════╗
║           Hermes Agent v0.7.x            ║
╚══════════════════════════════════════════╝
```

直接输入你的问题即可，例如：

```
you> 帮我写一个 Python 快速排序函数
```

## 核心文件结构一览

```
hermes-agent/
├── run_agent.py          # AIAgent 核心类 —— 对话循环
├── model_tools.py         # 工具编排层
├── toolsets.py            # 工具集定义
├── cli.py                 # HermesCLI 交互式命令行
├── hermes_cli/            # CLI 子命令模块
│   ├── main.py            # 入口，所有 hermes 子命令
│   ├── config.py          # 配置加载和迁移
│   ├── commands.py        # 斜杠命令定义
│   ├── setup.py           # 交互式配置向导
│   └── skills_hub.py      # /skills 技能市场
├── tools/                 # 工具实现（每个文件一个工具）
│   ├── registry.py         # 工具注册中心
│   ├── file_tools.py      # 文件读写搜索
│   ├── terminal_tool.py   # 终端命令执行
│   ├── web_tools.py       # 网页搜索
│   ├── delegate_tool.py   # 子 Agent 委托
│   └── mcp_tool.py        # MCP 客户端
└── gateway/               # 消息平台网关
    ├── run.py             # 主循环和斜杠命令
    └── platforms/         # 适配器（飞书、QQ、Telegram 等）
```

## 常用 CLI 命令

在 `hermes >` 交互提示符下：

| 命令 | 说明 |
|------|------|
| `/help` | 显示所有可用命令 |
| `/model <name>` | 切换模型 |
| `/reasoning low/medium/high` | 设置思维深度 |
| `/skills` | 查看已安装的技能 |
| `/exit` 或 `Ctrl+C` | 退出 |

## 思维链推理：让 AI 想清楚再回答

Hermes 支持调整模型的推理深度：

```
hermes > /reasoning high
```

开启后，模型会在回答前展示内部思考过程（Chain-of-Thought），适合处理复杂分析任务。在 `~/.hermes/config.yaml` 中也可以持久化配置：

```yaml
agent:
  reasoning_effort: high
display:
  show_reasoning: true    # 在终端显示思考过程
```

## 快速验证是否正常运行

```bash
source venv/bin/activate
hermes -c "1+1等于几？"
```

如果返回了正确的答案，说明环境配置成功。

## 常见问题

**Q：报错 "No module named 'hermes_agent'"**
> 确认已经执行了 `source venv/bin/activate`

**Q：报 API Key 相关错误**
> 检查 `~/.hermes/.env` 文件是否正确配置，API Key 不能有前后空格

**Q：如何查看详细日志？**
```bash
hermes --verbose
```

## 下一步

- 阅读 [《让 AI 想清楚再回答：Hermes 的思维链与追问技巧》](/blog/hermes-si-wei-lian) 了解推理配置
- 阅读 [《飞书 + QQ 同时在线：Hermes 多平台配置详解》](/blog/hermes-feishu-qq) 接入即时通讯
- 阅读 [《Skill 系统详解：Hermes 如何自动调用工具》](/blog/hermes-skill-xi-tong) 解锁技能系统
