---
layout: post
title: "Hermes 教程十一：MCP协议扩展"
date: 2026-04-18 18:00:00 +0800
categories: [Hermes Agent]
tags: [MCP, Model Context Protocol, 外部工具, 扩展, mcp_servers]
---

# MCP 协议：接入 100+ 外部工具的秘诀

Hermes Agent 支持 Model Context Protocol (MCP) 协议，可以连接海量外部工具和服务。本文详细介绍 MCP 的两种接入模式、配置方法，以及如何接入 GitHub、文件系统、Slack 等常用服务。

## MCP 是什么

**Model Context Protocol (MCP)** 是一种标准化协议，让 AI 助手能够调用外部工具和服务。通过 MCP，Hermes 可以：

- 📁 访问本地文件系统（高级功能）
- 🐙 操作 GitHub 仓库
- 📊 查询数据库
- 🔔 发送 Slack/飞书消息
- ☁️ 调用云服务 API
- ...以及 100+ 其他工具

## 两种接入模式

### 1. native-mcp（原生模式）

直接通过 config.yaml 配置，简单快捷：

```yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
  filesystem:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem"]
    env:
      ALLOWED_PATHS: "/home/xxxt-ubuntu/projects"
```

**优点：** 配置简单，直接在 config.yaml 管理
**缺点：** 需要手动安装 npm 包

### 2. mcporter（代理模式）

通过 mcporter 守护进程管理，适合复杂场景：

```bash
# 安装 mcporter
npm install -g @modelcontextprotocol/mcporter

# 启动守护进程
mcporter serve
```

**优点：** 集中管理，工具生态更丰富
**缺点：** 需要额外进程

## config.yaml 中配置 MCP

### 基本配置

```yaml
mcp_servers:
  # 名称自定义
  github:
    # 方式1：通过命令+参数
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    
  filesystem:
    # 方式2：通过 URL（需要 HTTP 服务器）
    url: https://mcp.ml.ink/mcp
    
  database:
    # 方式3：带环境变量
    command: npx
    args: ["-y", "@modelcontextprotocol/server-sqlite"]
    env:
      DATABASE_PATH: "/home/xxxt-ubuntu/data.db"
```

### OAuth 认证配置

某些 MCP Server 需要 OAuth 认证：

```yaml
mcp_servers:
  slack:
    url: https://slack-mcp.example.com/mcp
    auth:
      type: oauth          # 自动处理 OAuth 流程
      client_id: ${SLACK_CLIENT_ID}
      client_secret: ${SLACK_CLIENT_SECRET}
```

### 工具过滤

只启用部分工具，减少干扰：

```yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    tools:
      - create_issue
      - list_issues
      - add_issue_comment
    # 排除：
    # - delete_branch
    # - merge_branch
```

## MCP 命令行操作

### 添加 MCP Server

```bash
# 通过 URL 添加
hermes mcp add github --url "https://mcp.github.com/mcp"

# 通过命令添加
hermes mcp add filesystem --command npx --args "-y @modelcontextprotocol/server-filesystem"

# 通过预设添加
hermes mcp add github --preset github
```

### 列出已配置 Server

```bash
hermes mcp list
```

输出示例：

```
Configured MCP Servers:
─────────────────────────────────────
✓ filesystem  (native)  /home/xxxt-ubuntu/.local/share/mcp/servers/...
✓ github      (native)  npx @modelcontextprotocol/server-github
✓ slack       (url)     https://slack-mcp.example.com/mcp
```

### 测试 Server 连接

```bash
hermes mcp test github
hermes mcp test filesystem --test-file /home/xxxt-ubuntu/test.txt
```

### 配置 Server

```bash
# 配置已有 server
hermes mcp configure github --command npx --args "-y @modelcontextprotocol/server-github"

# 配置工具过滤
hermes mcp configure github --tools create_issue,list_issues
```

### 移除 Server

```bash
hermes mcp remove github
```

## 常用 MCP Server 案例

### 1. GitHub Server

```bash
hermes mcp add github \
  --command npx \
  --args "-y @modelcontextprotocol/server-github"
```

**可用工具：**

| 工具 | 说明 |
|------|------|
| `create_issue` | 创建 Issue |
| `list_issues` | 列出 Issue |
| `get_issue` | 获取 Issue 详情 |
| `create_pull_request` | 创建 PR |
| `search_code` | 代码搜索 |

### 2. 文件系统 Server

```bash
hermes mcp add filesystem \
  --command npx \
  --args "-y @modelcontextprotocol/server-filesystem" \
  --env ALLOWED_PATHS="/home/xxxt-ubuntu/projects"
```

**可用工具：**

| 工具 | 说明 |
|------|------|
| `read_file` | 读取文件 |
| `write_file` | 写入文件 |
| `list_directory` | 列出目录 |
| `move_file` | 移动文件 |

### 3. PostgreSQL Server

```bash
hermes mcp add postgres \
  --command npx \
  --args "-y @modelcontextprotocol/server-postgres" \
  --env DATABASE_URL="postgresql://user:pass@localhost:5432/mydb"
```

**可用工具：**

| 工具 | 说明 |
|------|------|
| `query` | 执行 SQL 查询 |
| `list_tables` | 列出表 |

### 4. Slack Server

```yaml
mcp_servers:
  slack:
    url: https://slack-mcp.example.com/mcp
    auth:
      type: oauth
```

**可用工具：**

| 工具 | 说明 |
|------|------|
| `send_message` | 发送消息 |
| `create_channel` | 创建频道 |
| `list_messages` | 获取消息 |

### 5. Google Mail Server

```bash
hermes mcp add gmail \
  --command npx \
  --args "-y @modelcontextprotocol/server-gmail"
```

## MCP 工具使用示例

配置好 MCP Server 后，直接用自然语言调用：

```
你：在 GitHub 上创建一个 issue，标题是"登录页面加载慢"，标签是 bug
Hermes：正在通过 GitHub MCP 创建 issue...

✓ Issue 创建成功
- 标题：登录页面加载慢
- 标签：bug
- 链接：https://github.com/owner/repo/issues/123
```

```
你：查询数据库中用户表的总记录数
Hermes：正在执行查询...

SELECT COUNT(*) FROM users;
✓ 查询结果：1,234 条记录
```

## 第三方 MCP Server 生态

主流 MCP Server 注册表：

| 平台 | 地址 |
|------|------|
| MCP Servers 官方列表 | github.com/modelcontextprotocol/servers |
| Smithery | smithery.ai |

### 推荐的 Server

```bash
# 开发工具
@modelcontextprotocol/server-github
@modelcontextprotocol/server-filesystem
@modelcontextprotocol/server-brave-search
@modelcontextprotocol/server-slack
@modelcontextprotocol/server-postgres
@modelcontextprotocol/server-sqlite

# 云服务
aws/@modelcontextprotocol/server-aws-kb-retrieval
@modelcontextprotocol/server-google-maps

# 通信
@modelcontextprotocol/server-sendgrid
@modelcontextprotocol/server-twilio
```

## 工具级别控制

### 启用/禁用特定工具

```bash
# 禁用某个 server 的特定工具
hermes mcp configure github \
  --tools create_issue,list_issues

# 排除工具
hermes mcp configure github \
  --exclude-tools delete_repository,force_push
```

### 查看可用工具

```bash
hermes mcp tools github
hermes tools list --platform cli | grep mcp
```

## 安全考虑

### 1. 限制访问路径

```yaml
mcp_servers:
  filesystem:
    env:
      ALLOWED_PATHS: "/home/xxxt-ubuntu/projects:/tmp/read-only"
```

### 2. 工具白名单

```yaml
mcp_servers:
  github:
    tools:
      - create_issue
      - list_issues
      - add_issue_comment
      # 不包含危险操作：
      # - delete_repository
      # - merge_branch
```

### 3. 环境变量隔离

MCP Server 的环境变量与主机隔离，防止泄露敏感信息。

## 故障排除

### Server 无法连接

```bash
# 诊断 MCP 配置
hermes mcp list

# 测试连接
hermes mcp test <server-name>

# 查看日志
tail -f ~/.hermes/logs/hermes.log | grep mcp
```

### 工具调用超时

增加超时配置：

```yaml
mcp_servers:
  slow-server:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-slow"]
    timeout: 120  # 120秒超时
```

### npx 加载慢

预先安装包：

```bash
npm install -g @modelcontextprotocol/server-github
```

然后配置：

```yaml
mcp_servers:
  github:
    command: /usr/local/bin/node
    args: ["/usr/local/lib/node_modules/@modelcontextprotocol/server-github"]
```

## 总结

MCP 协议让 Hermes Agent 的能力无限扩展：

- ✅ 标准化协议，接入简单
- ✅ 100+ 官方及社区 Server
- ✅ 工具级别精细控制
- ✅ 支持 OAuth 认证
- ✅ 安全的环境隔离

通过合理配置 MCP Server，你的 Hermes 可以成为真正的超级助手，掌控一切！
