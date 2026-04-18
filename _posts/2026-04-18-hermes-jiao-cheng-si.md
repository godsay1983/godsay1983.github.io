---
layout: post
title: "Hermes 教程四：飞书+QQ多平台配置"
date: 2026-04-18 18:00:00 +0800
categories: [平台接入]
tags: [飞书, QQ, 多平台, 网关配置]
---

# 飞书 + QQ 同时在线：Hermes 多平台配置详解

Hermes 的 gateway（网关）架构支持同时接入多个即时通讯平台。本文详细介绍如何同时让飞书（Lark）和 QQ Bot 接入 Hermes，实现一个后端服务同时响应两个平台的消息。

## 架构概览

```
用户 ──► 飞书服务器 ──► Hermes Gateway ──► AIAgent
用户 ──► QQ 服务器  ──► Hermes Gateway ──► AIAgent
                                           │
                                    ~/.hermes/config.yaml
```

Gateway 的核心入口是 `gateway/run.py`，它负责：
- 监听各平台的消息 Webhook
- 统一处理斜杠命令（`/help`、`/model` 等）
- 将消息路由给 AIAgent 处理
- 通过 `SessionStore` 维护会话状态

## 第一步：启动 Gateway

Gateway 通过 `hermes gateway` 命令启动：

```bash
source venv/bin/activate
hermes gateway
```

 Gateway 支持的平台在 `hermes_cli/platforms.py` 中定义：

```python
PLATFORMS = [
    ("cli",        PlatformInfo(label="💻 CLI",             default_toolset="hermes-core")),
    ("telegram",   PlatformInfo(label="✈️ Telegram",        default_toolset="hermes-telegram")),
    ("discord",    PlatformInfo(label="🎮 Discord",        default_toolset="hermes-discord")),
    ("slack",      PlatformInfo(label="💼 Slack",           default_toolset="hermes-slack")),
    ("whatsapp",   PlatformInfo(label="📱 WhatsApp",        default_toolset="hermes-whatsapp")),
    ("feishu",     PlatformInfo(label="🪽 Feishu",          default_toolset="hermes-feishu")),
    ("qqbot",      PlatformInfo(label="💬 QQBot",           default_toolset="hermes-qqbot")),
    ("signal",     PlatformInfo(label="🔐 Signal",           default_toolset="hermes-signal")),
    ("homeassistant", PlatformInfo(label="🏠 HomeAssistant", default_toolset="hermes-homeassistant")),
]
```

## 第二步：配置飞书（Lark/Feishu）

### 创建飞书应用

1. 访问 [https://open.feishu.cn/](https://open.feishu.cn/)（国际版用 [https://open.larksuite.com/](https://open.larksuite.com/)）
2. 创建企业自建应用
3. 获取 `App ID` 和 `App Secret`

### 交互式配置

```bash
hermes setup
# 选择 "Feishu / Lark"
```

会触发 `_setup_feishu()` 函数（位于 `hermes_cli/gateway.py`），流程包括：

```python
def _setup_feishu():
    # 1. 输入 App ID 和 Secret
    # 2. 选择域名：feishu (中国) 或 lark (国际)
    # 3. 配置消息接收 Webhook 地址
    # 4. 启用机器人能力
    # 5. 申请权限：im:message, im:message.receive_v1
```

### 手动配置

直接在 `~/.hermes/config.yaml` 中添加：

```yaml
feishu:
  app_id: cli_xxxxxxxxxxxxx
  app_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  domain: feishu   # 或 lark（国际版）
  default_room_id: oc_chat_xxxxxxxx   # 默认群/会话 ID
```

Webhook 地址默认为 `http://127.0.0.1:8765/feishu/webhook`，需要在飞书后台配置。

### 验证飞书连通性

```python
from gateway.platforms.feishu import probe_bot
probe_bot(app_id, app_secret, domain="feishu")
```

## 第三步：配置 QQ Bot

### 创建 QQ 机器人

1. 前往 [QQ 开放平台](https://q.qq.com/) 创建机器人
2. 获取 App ID

### 交互式配置（支持二维码扫码）

```bash
hermes setup
# 选择 "QQ Bot"
```

QQ Bot 配置调用 `_setup_qqbot()`（`hermes_cli/gateway.py`），支持**二维码扫码登录**方式，适合个人开发者：

```python
def _setup_qqbot():
    # 调用 QQ 平台接口获取二维码
    # _qqbot_render_qr(url) 显示二维码
    # _qqbot_qr_flow() 等待扫码确认
    credentials = _qqbot_qr_flow()
```

### 手动配置

```yaml
qqbot:
  app_id: "1234567890"
  token: "your_qq_bot_token"
  secret: "your_qq_bot_secret"
```

### 二维码登录流程

如果你选择 QR 码认证方式（适合个人 Bot）：

```bash
# 触发扫码流程
from gateway.platforms.qqbot import QQAdapter, check_qq_requirements
# 会弹出一个二维码图片，需要用 QQ 扫描确认
```

## 第四步：同时启用多平台

在 `~/.hermes/config.yaml` 中：

```yaml
gateway:
  enabled_platforms:
    - feishu
    - qqbot
  port: 8765           # Webhook 服务端口
  host: "0.0.0.0"      # 监听地址
```

配置示例：

```yaml
feishu:
  app_id: cli_xxxxxxxxxxxxx
  app_secret: xxxxxxxx
  domain: feishu

qqbot:
  app_id: "1234567890"
  token: "your_token"

gateway:
  enabled_platforms:
    - feishu
    - qqbot
  port: 8765
```

启动：

```bash
hermes gateway
```

## 多平台工具集隔离

可以为不同平台启用不同的工具集：

```yaml
platform_toolsets:
  feishu: [hermes-feishu, hermes-core]
  qqbot: [hermes-qqbot, hermes-core]
```

在 `hermes_cli/tools_config.py` 中按平台启用/禁用工具：

```bash
hermes tools enable web-search --platform feishu
hermes tools disable terminal --platform qqbot
```

## 斜杠命令在网关中的处理

Gateway 的斜杠命令通过 `GATEWAY_KNOWN_COMMANDS` 管理（`hermes_cli/commands.py`）：

```python
# 当收到 /reasoning high 这样的命令时
# gateway/run.py 调用 resolve_command() 解析
if canonical == "reasoning":
    return await self._handle_reasoning(event)
```

这保证了 CLI 和 Gateway 的命令行为一致。

## 平台特定的环境变量

| 平台 | 必需环境变量 |
|------|------------|
| 飞书 | `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `FEISHU_DOMAIN` |
| QQ | `QQ_APP_ID`, `QQ_APP_TOKEN`, `QQ_APP_SECRET` |
| 飞书首页会话 | `FEISHU_HOME_CHANNEL` |
| QQ 首页会话 | `QQBOT_HOME_CHANNEL` |

在 `cron/scheduler.py` 中定义了平台到环境变量的映射：

```python
PLATFORM_ENV_VARS = {
    "feishu": "FEISHU_HOME_CHANNEL",
    "qqbot": "QQBOT_HOME_CHANNEL",
}
```

## 常见问题

**Q：两个平台消息会串吗？**

不会。`SessionStore`（`gateway/session.py`）按平台和会话 ID 隔离对话上下文。

**Q：如何给不同平台配置不同技能？**

```bash
hermes skills enable git-helper --platform feishu
hermes skills disable web-search --platform qqbot
```

**Q：飞书 Webhook 收不到消息？**
- 确认公网可访问（内网用 ngrok 暴露）
- 检查 `FEISHU_APP_ID`/`SECRET` 是否正确
- 确认已启用"接收消息"权限

## 部署建议

生产环境推荐使用 systemd 服务：

```bash
# /etc/systemd/system/hermes-gateway.service
[Unit]
Description=Hermes Gateway
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/.hermes
ExecStart=/home/ubuntu/hermes-agent/venv/bin/hermes gateway
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable hermes-gateway
sudo systemctl start hermes-gateway
```

## 小结

| 步骤 | 命令 |
|------|------|
| 启动网关 | `hermes gateway` |
| 配置飞书 | `hermes setup` → 选择 Feishu |
| 配置 QQ | `hermes setup` → 选择 QQ Bot |
| 按平台管理工具 | `hermes tools --platform feishu` |
| 按平台管理技能 | `hermes skills --platform feishu` |

这样你就拥有了一个同时响应飞书和 QQ 消息的 AI 助手后端，所有对话都通过同一个 AIAgent 处理，共享配置和技能系统。
