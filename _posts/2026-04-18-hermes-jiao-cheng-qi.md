---
layout: post
title: "Hermes 教程七：20+必备Skills推荐"
date: 2026-04-18 18:00:00 +0800
categories: [资源推荐]
tags: [社区Skills, 技能市场, 效率工具, 推荐列表]
---

# 社区 Skills 大全：20+ 必备技能推荐

Hermes 的 Skills Hub 拥有丰富的社区技能生态，涵盖开发、运维、数据分析、文档生成等多个领域。本文整理 20+ 实用技能，介绍它们的功能和使用场景，帮你快速找到适合的自动化工具。

## 如何访问 Skills Hub

在 Hermes 中直接搜索：

```
hermes > /skills search <关键词>
hermes > /skills install <技能名>     # 安装技能
hermes > /skills list                  # 查看已安装技能
```

或者在 CLI 中：

```bash
hermes skills search git
hermes skills install code-review
```

## 开发类技能

### 1. `git-helper` ⭐⭐⭐⭐⭐

**功能**：专业的 Git 操作助手，处理分支管理、冲突解决、commit 规范。

**使用场景**：
```
你> /git-helper
你> 帮我解决 main 和 feature/login 分支的冲突
你> 生成规范的 commit message
```

**核心能力**：
- 智能合并冲突分析
- Angular 规范的 commit message 生成
- branch 策略建议

---

### 2. `code-review` ⭐⭐⭐⭐⭐

**功能**：自动化代码审查，检查风格、安全、性能问题。

**使用场景**：
```
你> /code-review
你> 帮我 review 一下 src/auth.py 这个文件
```

**检查维度**：代码风格（ruff/hadolint）、安全漏洞（硬编码凭证/SQL注入）、性能（N+1查询/阻塞IO）。

---

### 3. `api-doc-generator` ⭐⭐⭐⭐

**功能**：根据代码自动生成 API 文档（OpenAPI/Swagger）。

**使用场景**：
```
你> /api-doc-generator
你> 为这个 FastAPI 项目生成 OpenAPI 文档
```

---

### 4. `test-generator` ⭐⭐⭐⭐

**功能**：根据函数签名和文档字符串自动生成单元测试。

**使用场景**：
```
你> /test-generator
你> 为 calculator.py 中的所有函数生成 pytest 测试
```

---

### 5. `sql-optimize` ⭐⭐⭐

**功能**：SQL 查询分析和优化建议。

**使用场景**：
```
你> /sql-optimize
你> 帮我分析这条慢查询：SELECT * FROM orders JOIN users ...
```

---

## 运维类技能

### 6. `docker-helper` ⭐⭐⭐⭐⭐

**功能**：Dockerfile 审查、镜像优化、多阶段构建建议。

**使用场景**：
```
你> /docker-helper
你> 优化一下这个 Dockerfile，让镜像体积减少一半
```

---

### 7. `k8s-debug` ⭐⭐⭐⭐

**功能**：Kubernetes 问题诊断和调试建议。

**使用场景**：
```
你> /k8s-debug
你> pod 一直处于 CrashLoopBackOff 状态，帮我分析
```

---

### 8. `nginx-config` ⭐⭐⭐

**功能**：Nginx 配置检查、安全加固、性能优化。

**使用场景**：
```
你> /nginx-config
你> 帮我检查这个 nginx.conf 有什么安全问题
```

---

### 9. `ci-helper` ⭐⭐⭐⭐

**功能**：CI/CD 流程分析，GitHub Actions / GitLab CI 优化。

**使用场景**：
```
你> /ci-helper
你> 优化一下这个 GitHub Actions workflow，让构建时间减半
```

---

### 10. `deploy-helper` ⭐⭐⭐⭐

**功能**：一键部署助手，支持多环境（测试/预发/生产）切换。

**使用场景**：
```
你> /deploy-helper
你> 部署 v2.1.0 到生产环境
```

**配置项**：
```yaml
skills:
  config:
    deploy_helper:
      server_host: "39.108.142.88"
      deploy_path: "/var/www/app"
```

---

## 文档与写作类技能

### 11. `pptx-generator` ⭐⭐⭐⭐⭐

**功能**：根据主题或数据自动生成 PPTX 幻灯片。

**使用场景**：
```
你> /pptx-generator
你> 帮我做一个介绍微服务架构的 PPT，10页左右
```

---

### 12. `markdown-writer` ⭐⭐⭐⭐

**功能**：专业的 Markdown 写作助手，生成技术文档、博客、README。

**使用场景**：
```
你> /markdown-writer
你> 帮我写一个这个项目的 README.md
```

---

### 13. `api-doc-generator` ⭐⭐⭐⭐

**功能**：自动生成 API 接口文档（Markdown/OpenAPI）。

**使用场景**：
```
你> /api-doc-generator
你> 为这个 Express.js 项目生成 API 文档
```

---

### 14. `changelog-writer` ⭐⭐⭐

**功能**：根据 git commit 历史自动生成 CHANGELOG。

**使用场景**：
```
你> /changelog-writer
你> 为 v1.2.0 生成更新日志
```

---

## 数据分析类技能

### 15. `data-visualization` ⭐⭐⭐⭐

**功能**：根据数据生成图表建议和 Python/JS 代码。

**使用场景**：
```
你> /data-visualization
你> 我有每日销售数据，帮我选最适合的可视化图表
```

---

### 16. `csv-analyzer` ⭐⭐⭐⭐

**功能**：CSV 文件探索性数据分析，生成统计摘要。

**使用场景**：
```
你> /csv-analyzer
你> 分析一下这个用户行为日志.csv
```

---

### 17. `sql-query-builder` ⭐⭐⭐

**功能**：自然语言转 SQL 查询。

**使用场景**：
```
你> /sql-query-builder
你> 帮我写一条查询：统计每个月的订单总额
```

---

## 效率工具类技能

### 18. `meeting-notes` ⭐⭐⭐⭐

**功能**：生成结构化会议纪要，包括待办事项、负责人、截止日期。

**使用场景**：
```
你> /meeting-notes
你> 根据以下内容生成会议纪要：...
```

---

### 19. `task-decomposer` ⭐⭐⭐⭐

**功能**：将复杂任务拆解为可执行的小任务。

**使用场景**：
```
你> /task-decomposer
你> 帮我把"上线推荐系统"拆解成具体步骤
```

---

### 20. `regex-builder` ⭐⭐⭐

**功能**：自然语言描述转正则表达式。

**使用场景**：
```
你> /regex-builder
你> 帮我写一个匹配中国手机号的正则
```

---

### 21. `cron-parser` ⭐⭐⭐

**功能**：解释 cron 表达式，生成人类可读的调度描述。

**使用场景**：
```
你> /cron-parser
你> 帮我解释一下这个 cron：0 0 */2 * * *
```

---

### 22. `json-formatter` ⭐⭐⭐

**功能**：JSON 格式化、验证、简化（去除冗余字段）。

**使用场景**：
```
你> /json-formatter
你> 帮我把这个 JSON 压缩成一行
```

---

## 安装和管理技能

### 查看已安装技能

```bash
hermes > /skills list
```

### 安装新技能

```bash
hermes > /skills install <技能名>
# 例如
hermes > /skills install pptx-generator
```

### 更新技能

```bash
hermes > /skills update <技能名>
hermes > /skills update --all    # 更新所有技能
```

### 按平台管理技能

```bash
# 只在飞书启用 git-helper
hermes skills enable git-helper --platform feishu

# 在 QQ 禁用 code-review（节省 token）
hermes skills disable code-review --platform qqbot
```

## Bundled Skills（内置技能）

Hermes 安装时会同步一批内置技能到 `~/.hermes/skills/`，来源是 `hermes-agent/bundled/skills/` 目录，通过 `tools/skills_sync.py` 管理：

```python
# 同步内置技能
python -m tools.skills_sync
# 清单保存在 ~/.hermes/skills/.bundled_manifest
```

---

## 技能推荐速查表

| 技能名 | 分类 | 推荐指数 | 主要用途 |
|--------|------|----------|----------|
| `git-helper` | 开发 | ⭐⭐⭐⭐⭐ | Git 操作全覆盖 |
| `code-review` | 开发 | ⭐⭐⭐⭐⭐ | 代码审查 |
| `pptx-generator` | 文档 | ⭐⭐⭐⭐⭐ | 幻灯片生成 |
| `docker-helper` | 运维 | ⭐⭐⭐⭐⭐ | Docker 优化 |
| `k8s-debug` | 运维 | ⭐⭐⭐⭐ | K8s 诊断 |
| `ci-helper` | 运维 | ⭐⭐⭐⭐ | CI/CD 优化 |
| `deploy-helper` | 运维 | ⭐⭐⭐⭐ | 一键部署 |
| `test-generator` | 开发 | ⭐⭐⭐⭐ | 测试生成 |
| `data-visualization` | 数据 | ⭐⭐⭐⭐ | 可视化建议 |
| `meeting-notes` | 效率 | ⭐⭐⭐⭐ | 会议纪要 |
| `task-decomposer` | 效率 | ⭐⭐⭐⭐ | 任务拆解 |
| `sql-optimize` | 开发 | ⭐⭐⭐ | SQL 优化 |
| `api-doc-generator` | 文档 | ⭐⭐⭐⭐ | API 文档 |
| `changelog-writer` | 文档 | ⭐⭐⭐ | 更新日志 |
| `csv-analyzer` | 数据 | ⭐⭐⭐⭐ | 数据分析 |
| `regex-builder` | 开发 | ⭐⭐⭐ | 正则生成 |

## 如何贡献自己的 Skill

1. 编写 `SKILL.md`（参考上文《编写自己的 Skill》教程）
2. 在 GitHub 上创建公开仓库
3. 通过 `/skills publish` 提交到 Skills Hub 审核
4. 审核通过后，所有 Hermes 用户都能搜到并安装你的 Skill

---

掌握这些技能，能让你的日常工作流实现大幅自动化。无论是代码开发、运维部署还是文档写作，把重复的工作交给 Hermes，把精力留给真正的创造性任务。
