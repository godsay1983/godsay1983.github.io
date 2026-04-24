---
title: "DeepSeek V4 正式发布：百万Token上下文，挑战GPT-4 Turbo"
date: 2026-04-24
tags: [DeepSeek, AI大模型, V4, 百万上下文, 华为芯片]
---

昨晚，DeepSeek 正式发布了 **DeepSeek V4**（代号"海军上将"），这是国产大模型领域的又一重大突破。配合今天收集的 GitLab 周报数据，不得不感叹——AI 军备竞赛正在加速。

## 核心升级：三个"百万"级突破

### 1. 百万 Token 上下文

V4 支持 **100 万 Token 的上下文窗口**，这意味着：

- 可以一次性处理整本书籍、完整代码库
- 长对话记忆不丢失
- 适合法律合同分析、代码库理解、大规模文档处理

### 2. 百万级API调用性能

根据官方文档，V4 在高并发场景下做了专项优化，吞吐量相比 V3 提升显著。

### 3. 华为芯片加持

据 Reuters 报道，DeepSeek V4 将在 **华为昇腾（Ascend）芯片**上运行。这是继英伟达制裁后，国产大模型寻找替代算力方案的重要探索。

## 可用模型一览

| 模型 | 定位 | 特点 |
|------|------|------|
| `deepseek-v4-pro` | 旗舰版 | 性能最强，适合复杂任务 |
| `deepseek-v4-flash` | 轻量版 | 快速响应，适合日常使用 |
| `deepseek-chat` | 兼容模式 | ⚠️ 2026/07/24 弃用 |
| `deepseek-reasoner` | 推理模式 | ⚠️ 2026/07/24 弃用 |

> 老模型 `deepseek-chat` 和 `deepseek-reasoner` 将于 7 月 24 日彻底下线，对应关系：
> - `deepseek-chat` → `deepseek-v4-flash`（非思考模式）
> - `deepseek-reasoner` → `deepseek-v4-flash`（思考模式）

## API 调用示例

和 OpenAI 兼容，迁移成本极低：

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "解释一下什么是RAG"}
    ],
    thinking={"type": "enabled"},  # 开启思考模式
    reasoning_effort="high"
)
print(response.choices[0].message.content)
```

## 技术特性亮点

- **Transformer 架构 + 深度优化**：原生支持 `transformers` 和 `safetensors`
- **8-bit / FP8 量化**：方便本地部署
- **思考模式可控**：可通过 `thinking` 参数灵活开关
- **OpenAI 兼容 API**：无缝迁移，几乎零成本

## 定价参考

目前官方尚未公布详细定价，但根据 `deepseek-v4-flash` 的定位，预计会比 GPT-4 Turbo 便宜 50% 以上——这也是 DeepSeek 一贯的打法。

## 国产大模型竞争格局

| 模型 | 厂商 | 特色 |
|------|------|------|
| DeepSeek V4 | 深度求索 | 极致性价比 + 华为芯片 |
| 智谱 GLM-5 | 智谱AI | 中文优化 + 长上下文 |
| 阿里 Qwen3 | 阿里云 | 开源生态强大 |
| 月之暗面 Kimi K2 | 月之暗面 | 1000万上下文（更长） |
| 百度 文心4 | 百度 | 百度全家桶集成 |

## 怎么看？

DeepSeek V4 的发布再次证明：**国产大模型正在从\"追赶\"转向\"并跑\"甚至\"领跑\"**。百万 Token 上下文 + 华为芯片的组合，让它在当前国际形势下具有特殊战略价值。

对于普通开发者而言，API 兼容 OpenAI 意味着迁移成本极低，值得一试。

---

*Hugging Face 模型已上线：[deepseek-ai/DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)*
