---
layout: post
title: "用 Hermes 做网络研究：MMX 搜索与信息聚合"
date: 2026-04-18 18:00:00 +0800
categories: [Hermes Agent]
tags: [MMX 搜索, 网络研究, 信息聚合, 自动化, 定时任务]
---

Hermes Agent 提供了强大的网络搜索和研究能力，特别是 MMX 搜索功能，可以帮助用户高效地收集和整理网络信息。本文详细介绍如何用 Hermes 进行网络研究，以及如何实现多源信息聚合。

## MMX 搜索使用

Hermes 内置的 MMX 搜索是核心研究工具，使用 `--q` 参数指定搜索查询：

```bash
# 基本搜索
mmx search --q "一人公司 创业模式"

# 限制结果数量
mmx search --q "AI 编程工具对比" --limit 10

# 指定搜索来源
mmx search --q "Hermes Agent 使用教程" --source web
```

MMX 搜索的优势在于：
- 快速返回结构化的搜索结果
- 自动去重和排序
- 支持多种搜索来源（网页、新闻、学术等）

## 多源信息聚合方法

进行深度研究时，需要从多个来源收集信息。Hermes 提供以下聚合方法：

### 方法一：分步骤搜索

```python
# 第一步：搜索核心概念
mmx search --q "一人公司 definition"

# 第二步：搜索实践案例
mmx search --q "一人公司 成功案例 2025"

# 第三步：搜索工具和方法
mmx search --q "一人公司 tools 自动化"
```

### 方法二：使用 context_compressor 保持上下文

在进行长篇研究时，Hermes 的 context_compressor 会自动压缩早期对话，保留关键信息：

```python
# 上下文压缩会自动：
# 1. 识别已解决的搜索任务
# 2. 提取关键结论和链接
# 3. 清理冗余的中间结果
# 4. 保留最新的研究进展
```

### 方法三：并行多查询

```bash
# 同时搜索多个相关主题
mmx search --q "一人公司 LLC vs 工作室"
mmx search --q "sole proprietorship benefits"
mmx search --q "一个人可以做的互联网生意"
```

## 搜索结果的解析处理

MMX 搜索返回的结果需要进一步解析和处理。推荐的工作流：

```
搜索结果（原始）
    ↓
提取关键信息（标题、URL、摘要）
    ↓
去重和分类（按主题、按可信度）
    ↓
深度读取（针对重要来源）
    ↓
汇总报告（结构化的研究报告）
```

### 实用技巧

1. **使用 read_file 读取重要页面**：结合搜索结果中的 URL，用 read_file 工具深度抓取内容
2. **使用 search_files 搜索本地已有信息**：避免重复搜索，节省时间和 API 调用
3. **及时保存中间结果**：用 write_file 将搜索发现写入笔记文件

## 案例：研究一人公司

以下是使用 Hermes 研究"一人公司"主题的实际案例：

### 第一阶段：概念探索

```
搜索：什么是一人公司
结果：
- 一人公司（sole proprietorship）是最简单的企业形式
- 业主对公司债务承担无限责任
- 适合自由职业者和小规模经营者
```

### 第二阶段：深入研究

```
搜索：一人公司 vs 有限责任公司
结果：
- 有限责任公司（LLC）提供资产保护
- 一人公司注册简单、成本低
- 风险和便利性需要权衡
```

### 第三阶段：实践方法

```
搜索：一人公司如何运营
结果：
- 使用工具： invoicing软件、会计软件、项目管理工具
- 外包策略：非核心业务外包
- 自动化：使用AI工具提高效率
```

### 最终汇总

基于三个阶段的研究，汇总成结构化的研究报告，包括：
- 一人公司的定义和特点
- 与其他企业形式的对比
- 运营一人公司的工具推荐
- 适合一人公司的商业模式

## 定时信息收集方案

对于需要持续追踪的课题，可以配置定时任务自动收集信息。

### 创建定时搜索任务

在 `/home/xxxt-ubuntu/.hermes/cron/` 下创建自动搜索脚本：

```python
# cron/market_research.py
import subprocess
import json
from datetime import datetime

TOPICS = [
    "AI 编程工具 最新动态",
    "一人公司 创业趋势",
    "远程工作 工具推荐"
]

def run_scheduled_search():
    results = {}
    for topic in TOPICS:
        result = subprocess.run(
            ['mmx', 'search', '--q', topic, '--limit', '5'],
            capture_output=True, text=True
        )
        results[topic] = {
            'timestamp': datetime.now().isoformat(),
            'data': result.stdout
        }
    
    # 保存结果到研究笔记
    with open('/home/xxxt-ubuntu/research/latest.json', 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    run_scheduled_search()
```

### 配置 crontab

```bash
# 每天早上 9 点自动运行研究任务
0 9 * * * python3 /home/xxxt-ubuntu/.hermes/cron/market_research.py

# 每周一早上 9 点汇总上周研究
0 9 * * 1 python3 /home/xxxt-ubuntu/.hermes/cron/weekly_summary.py
```

## 总结

用 Hermes 做网络研究的核心优势：

| 功能 | 传统方式 | Hermes 方式 |
|------|---------|-------------|
| 搜索速度 | 多次搜索、手动整理 | 一命令返回结构化结果 |
| 信息聚合 | 复制粘贴、容易丢失 | 自动保存、统一管理 |
| 持续追踪 | 手动定期搜索 | cron 自动化 |
| 上下文管理 | 搜索多了容易混淆 | 自动压缩、智能保留 |

MMX 搜索配合 Herme's context_compressor 和 cron 定时任务，可以构建一个半自动化的网络研究系统，大大提高信息收集效率。
