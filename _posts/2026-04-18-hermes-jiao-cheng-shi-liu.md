---
layout: post
title: "Hermes 教程十六：常见问题与解决方案"
date: 2026-04-18 18:00:00 +0800
categories: [Hermes Agent]
tags: [故障排除, 常见问题, 飞书, QQ, Git, API]
---

使用 Hermes Agent 的过程中，可能会遇到一些常见问题。本文汇总了高频问题及其解决方案，帮助你快速排查和修复。

## 飞书/QQ 连接失败排查

### 飞书连接问题

**症状**：飞书机器人无法接收或发送消息

**排查步骤**：

1. 检查 Webhook 配置是否正确
```bash
# 查看飞书 Webhook 配置
cat ~/.hermes/config.yaml | grep -A5 feishu
```

2. 验证 Webhook URL 是否有效
```bash
curl -X POST "你的飞书Webhook地址" \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"test"}}'
```

3. 检查防火墙和网络设置
```bash
# 测试 Hermes Gateway 端口
telnet localhost 8080
netstat -tlnp | grep 8080
```

4. 查看日志定位问题
```bash
tail -f ~/.hermes/logs/hermes.log
```

### QQ 连接问题

**症状**：QQ 机器人无响应或消息发送失败

**排查步骤**：

1. 确认 QQ 机器人已启用
2. 检查 `platforms/qqbot` 配置
3. 验证 OneBot 协议连接（如果使用 go-cqhttp 等中间件）

## Skill 不生效的原因

### 常见原因

**1. Skill 文件路径错误**

Skill 应放在 `~/.hermes/skills/` 目录下：

```bash
ls -la ~/.hermes/skills/
# 确保你的 skill 文件在这里
```

**2. Skill 没有可执行权限**

```bash
chmod +x ~/.hermes/skills/your-skill.sh
```

**3. Skill 名称拼写错误**

```bash
# 正确调用方式
/hermes skill jekyll-blog-troubleshooting

# 注意斜杠和名称匹配
```

**4. Skill 脚本语法错误**

```bash
# 测试 skill 脚本是否能正常运行
bash -x ~/.hermes/skills/your-skill.sh
```

**5. 平台禁用**

某些 Skill 可能被特定平台禁用：

```bash
# 检查 skills_config
hermes skills --platform telegram
```

## 消息发送失败（MEDIA: 大写）

### 问题描述

发送图片或其他媒体消息时失败，提示 "MEDIA" 相关错误。

### 原因

在 Telegram 等平台，发送媒体需要使用正确的 API 格式：

```python
# 错误 ❌
{"photo": "https://example.com/image.jpg"}

# 正确 ✅
{"photo": "https://example.com/image.jpg", "caption": "图片描述"}
```

### 解决方案

1. 检查消息格式是否正确
2. 确保图片 URL 可访问
3. 媒体文件需要先通过 Telegram API 上传获取 file_id
4. 使用 Hermes 内置的 send_photo、send_document 等专用方法

## Git Push Non-Fast-Forward 解决

### 问题描述

```bash
error: failed to push some refs to 'https://github.com/xxx/xxx.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally.
```

### 解决方案

**方案一：先拉取再推送（推荐）**

```bash
git pull --rebase origin main
git push origin main
```

**方案二：强制推送（谨慎使用）**

```bash
git push origin main --force
# ⚠️ 注意：这会覆盖远程历史，慎用！
```

**方案三：使用 workdir 工具避免冲突**

在 Hermes 中操作 Git 时，先确保工作目录是最新的：

```bash
cd /home/xxxt-ubuntu/blog
git fetch origin
git status  # 检查是否有未提交的更改
```

### 预防措施

1. 每次开始新任务前先 `git pull`
2. 频繁小提交，避免大量更改堆积
3. 使用 `git stash` 暂存本地更改再 pull

## API Key 错误处理

### 常见 API Key 问题

**1. Key 不存在或为空**

```bash
# 检查环境变量
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# 检查配置文件
cat ~/.hermes/.env | grep API
```

**2. Key 格式错误**

```bash
# OpenAI Key 应以 sk- 开头
# Anthropic Key 应以 claude- 开头
```

**3. Key 权限不足**

某些模型需要特定权限或订阅：

- Claude Pro/Claude Max 需要相应订阅
- GPT-4 需要 API 访问权限
- 某些模型有地域限制

### 解决方案

```bash
# 重新配置 API Key
hermes auth --provider openai --api-key "你的新key"

# 或直接编辑 .env 文件
nano ~/.hermes/.env
```

## 环境变量不生效

### 问题描述

修改了 `.env` 文件或系统环境变量，但不生效。

### 排查步骤

**1. 确认文件位置**

```bash
# Hermes 读取的环境变量文件
ls -la ~/.hermes/.env
```

**2. 检查变量格式**

```bash
# 正确格式
OPENAI_API_KEY=sk-xxxxx
ANTHROPIC_API_KEY=claude-xxxxx

# 错误格式（带引号）
OPENAI_API_KEY="sk-xxxxx"  # ❌
ANTHROPIC_API_KEY='sk-xxxxx'  # ❌
```

**3. 重启 Hermes**

环境变量修改后需要重启 Hermes 服务：

```bash
# 停止现有服务
pkill -f hermes

# 重新启动
hermes run
```

**4. 手动导出测试**

```bash
# 在当前 shell 中测试
export OPENAI_API_KEY="sk-xxxxx"
hermes run
```

### 常见错误汇总

| 错误类型 | 原因 | 解决方案 |
|---------|------|---------|
| API Key 无效 | Key 过期或格式错误 | 重新获取并配置 |
| 认证失败 | Provider 账号问题 | 检查订阅状态 |
| 连接超时 | 网络问题 | 检查代理/防火墙 |
| 权限不足 | 模型访问权限 | 升级订阅或切换模型 |

## 总结

遇到问题时，排查顺序建议：

1. **检查日志** — 大多数问题都能在日志中找到线索
2. **验证配置** — 确认 config.yaml 和 .env 配置正确
3. **测试网络** — 确保 API 可访问
4. **重启服务** — 有时简单的重启能解决大部分临时性问题

如果以上方法都无法解决，建议在 GitHub Issues 或社区中寻求帮助，提供完整的日志和配置信息以便快速定位问题。
