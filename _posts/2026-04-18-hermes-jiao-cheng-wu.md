---
layout: post
title: "Hermes 教程五：Skill 系统详解"
date: 2026-04-18 18:00:00 +0800
categories: [核心机制]
tags: [Skill系统, 工具调用, 自动化, 技能市场]
---

# Skill 系统详解：Hermes 如何自动调用工具

Hermes 的 Skill 系统是其最强大的功能之一——它让 AI 能够像人类专家一样，根据任务需求自动调用合适的工具链。本文深入解析 Skill 的工作原理、内部架构，以及它与底层 Tool 系统的关系。

## Skill vs Tool：厘清概念

在 Hermes 中，有两个容易混淆的概念：

| 概念 | 说明 | 示例 |
|------|------|------|
| **Tool（工具）** | 模型可直接调用的原子函数 | `ReadFile`、`RunCommand`、`WebSearch` |
| **Skill（技能）** | 封装了特定领域工作流的技能包 | `git-helper`、`pptx-generator`、`code-review` |

**一个 Skill 通常由多个 Tool 组合而成**，并附带领域知识和操作流程。

## Skill 目录结构

所有 Skill 存放在 `~/.hermes/skills/` 目录下：

```
~/.hermes/skills/
├── my-skill/
│   ├── SKILL.md              # 主指令文件（必需）
│   ├── references/           # 参考文档
│   │   ├── api.md
│   │   └── examples.md
│   ├── templates/            # 输出模板
│   │   └── template.md
│   └── assets/               # 辅助资源
└── another-skill/
    └── SKILL.md
```

## SKILL.md 格式

每个 Skill 的核心是 `SKILL.md`，采用 YAML frontmatter + Markdown 内容格式：

```markdown
---
name: git-helper
description: 高效处理 Git 操作，解决合并冲突
version: 1.0.0
platforms: [linux, darwin]   # 可选，限制操作系统；省略则全平台
prerequisites:
  commands: [git, ssh]
  env_vars: [GITHUB_TOKEN]
metadata:
  hermes:
    tags: [git, vcs, developer-tools]
    related_skills: [code-review, ci-helper]
---

# Git Helper

你是一个专业的 Git 助手，擅长：
- 分支管理与冲突解决
- 编写规范的 commit message
- 处理 submodule 和 LFS

当用户请求 git 操作时，优先使用 git 系列工具完成。
```

## Skill 的注册与发现

### 发现机制

`agent/skill_commands.py` 在启动时扫描 `~/.hermes/skills/`：

```python
def build_skill_command_map():
    """Scan ~/.hermes/skills/ and return a mapping of /command -> skill info."""
    skills_dir = get_skills_dir()
    for skill_file in skills_dir.rglob("SKILL.md"):
        # 解析 frontmatter，提取 name、description
        # 注册为斜杠命令
```

扫描结果注入为**用户消息**（而非系统提示词），这是为了保留 Anthropic 的 prompt caching 机制。

### Skill 命令如何工作

当你在对话中输入 `/pptx` 时：

1. `agent/skill_commands.py` 识别这是一个 Skill 命令
2. 加载对应 `SKILL.md` 的完整内容
3. 将 Skill 内容作为用户消息注入对话上下文
4. 模型感知到 Skill 指令，自主决定调用哪些 Tool

### 从 Skill 到 Tool 的调用链

```
用户输入 /pptx
      ↓
skill_commands.py 加载 ~/.hermes/skills/pptx/SKILL.md
      ↓
Skill 指令注入对话（role: user, content: <skill content>）
      ↓
AIAgent 分析任务，决定调用哪些 Tool
      ↓
model_tools.handle_function_call() 执行工具
      ↓
Tool 返回结果，模型组织最终回复
```

## 核心模块解析

### tools/skills_tool.py — 技能列表与查看

提供两个核心工具函数（供 AI 模型调用）：

```python
def skills_list():
    """列出所有技能（仅返回元数据，节省 token）
    
    返回格式：
    - name: 技能名
    - description: 简短描述
    - version: 版本
    - tags: 标签
    """

def skill_view(skill_name: str, path: str = None):
    """加载指定技能的完整内容
    - skill_view("pptx") → 加载主 SKILL.md
    - skill_view("pptx", "references/api.md") → 加载参考文档
    """
```

### tools/skills_hub.py — 技能市场

提供 `/skills` 斜杠命令的完整实现，支持搜索、安装、更新技能：

```bash
hermes > /skills search git
hermes > /skills install pptx-generator
hermes > /skills list
```

底层调用 `unified_search()` 函数搜索技能市场。

### agent/skill_utils.py — 技能元数据工具

```python
def get_disabled_skill_names(platform: str = None) -> Set[str]:
    """从 config.yaml 读取被禁用的技能列表"""

def get_external_skills_dirs() -> List[Path]:
    """读取 config.yaml 中的 skills.external_dirs 配置
    允许指定额外的技能目录"""

def get_all_skills_dirs() -> List[Path]:
    """返回所有技能目录（本地 ~/.hermes/skills/ 优先，然后是外部目录）"""

def skill_matches_platform(frontmatter: Dict) -> bool:
    """检查技能是否与当前操作系统匹配"""
```

### skill_manager_tool.py — 技能管理

供 AI 模型调用的技能管理接口：

```python
def skill_install(skill_identifier: str): ...
def skill_uninstall(skill_name: str): ...
def skill_update(skill_name: str): ...
def skill_list_installed(): ...
```

## 技能与平台隔离

可以为不同平台启用/禁用不同技能：

```bash
# 为飞书平台启用 git-helper
hermes skills enable git-helper --platform feishu

# 为 QQ 平台禁用 web-search
hermes skills disable web-search --platform qqbot
```

这些配置保存在 `~/.hermes/config.yaml`：

```yaml
skills:
  disabled:
    - some-skill
  platform_disabled:
    qqbot:
      - web-search
    feishu:
      - terminal
```

## 技能的渐进式披露（Progressive Disclosure）

为节省 token，技能系统采用三层渐进式加载（参考 Anthropic 规范）：

| 层级 | 内容 | 何时加载 |
|------|------|----------|
| Tier 1 | 元数据（name、description、tags） | `skills_list()` |
| Tier 2 | 主指令（SKILL.md 正文） | `skill_view("name")` |
| Tier 3 | 参考文件（references/、templates/） | 任务需要时 |

这确保 AI 在做技能选择时只看到轻量元数据，实际执行时才加载完整指令。

## 内置核心工具一览

AI 模型可以直接调用的底层工具（在 `tools/` 目录下）：

| 工具 | 文件 | 作用 |
|------|------|------|
| `ReadFile` | `file_tools.py` | 读取文件内容 |
| `WriteFile` | `file_tools.py` | 写入文件 |
| `SearchFiles` | `file_tools.py` | 正则搜索文件内容 |
| `RunCommand` | `terminal_tool.py` | 执行 Shell 命令 |
| `WebSearch` | `web_tools.py` | 搜索引擎查询 |
| `WebExtract` | `web_tools.py` | 提取网页内容 |
| `BrowserUse` | `browser_tool.py` | 浏览器自动化 |
| `ExecuteCode` | `code_execution_tool.py` | 执行代码片段 |
| `DelegateTask` | `delegate_tool.py` | 委托给子 Agent |
| `MCP` | `mcp_tool.py` | 调用 MCP 协议工具 |

## 技能的外部目录

在 `~/.hermes/config.yaml` 中配置：

```yaml
skills:
  external_dirs:
    - /mnt/shared/skills        # 团队共享技能目录
    - ~/company-skills
```

本地技能（`~/.hermes/skills/`）优先于外部目录。

## 小结

| 组件 | 路径 | 职责 |
|------|------|------|
| 技能存储 | `~/.hermes/skills/` | 所有技能文件 |
| 技能市场 | `hermes_cli/skills_hub.py` | 搜索安装更新 |
| 技能元数据 | `agent/skill_utils.py` | 平台匹配、禁用管理 |
| 技能查看工具 | `tools/skills_tool.py` | AI 模型调用接口 |
| 技能管理工具 | `tools/skill_manager_tool.py` | AI 模型管理接口 |
| 斜杠命令注入 | `agent/skill_commands.py` | Skill → 用户消息 |

Skill 系统让 Hermes 拥有了"专家能力"——每个 Skill 都是一个垂直领域的操作手册，AI 加载后就能像专家一样工作。
