---
layout: default
title: 文章搜索
permalink: /search/
---
<style>
.search-container { margin: 2rem 0; }
.search-input {
  width: 100%;
  padding: 0.8rem 1rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  font-size: 1rem;
}
.search-input:focus { outline: none; border-color: var(--accent); }
#search-results { margin-top: 1.5rem; }
.search-result {
  padding: 1rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  margin-bottom: 0.8rem;
  background: var(--bg-secondary);
}
.search-result a { font-size: 1.1rem; font-weight: bold; color: var(--accent); }
.search-result .date { color: var(--text-muted); font-size: 0.9rem; margin-left: 0.5rem; }
.search-result .excerpt { color: var(--text-muted); margin-top: 0.3rem; font-size: 0.95rem; }
.no-results { color: var(--text-muted); padding: 2rem; text-align: center; }
</style>

<h2>🔍 文章搜索</h2>
<div class="search-container">
  <input type="text" id="search-input" class="search-input" placeholder="输入关键词搜索标题、分类或标签..." autofocus>
</div>
<div id="search-results" class="no-results">输入关键词开始搜索...</div>

<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.min.js"></script>
<script>
// 文章数据（由 scripts/generate-search-index.js 生成，Jekyll 构建时自动更新）
var searchData = [
  {"title":"掘金116-105逆转森林狼：约基奇25+13+11三双，穆雷16罚全中末节救赎","url":"/posts/2026/04/19/nba-playoffs-nuggets-wolves/","date":"2026-04-19","categories":"['体育', 'NBA']","tags":['NBA', '季后赛', '掘金', '森林狼', '约基奇', '穆雷', '爱德华兹'],"excerpt":" !掘金vs森林狼(/images/nba-2026-april19/nw.jpg) 🏀 比分：丹佛掘金 116 - 105 明尼苏达森林狼"},
  {"title":"残阵湖人107-98力克火箭：詹姆斯19+13率队三节收割，肯纳德三分5中5奇兵天降","url":"/posts/2026/04/19/nba-playoffs-lakers-rockets/","date":"2026-04-19","categories":"['体育', 'NBA']","tags":['NBA', '季后赛', '湖人', '火箭', '詹姆斯', '肯纳德', '艾顿', '申京'],"excerpt":" !湖人vs火箭(/images/nba-2026-april19/lr.jpg) 🏀 比分：洛杉矶湖人 107 - 98 休斯顿火箭"},
  {"title":"尼克斯113-102轻取老鹰：布伦森首节19分定基调，唐斯末节收割比赛","url":"/posts/2026/04/19/nba-playoffs-knicks-hawks/","date":"2026-04-19","categories":"['体育', 'NBA']","tags":['NBA', '季后赛', '尼克斯', '老鹰', '布伦森', '唐斯', '布里奇斯'],"excerpt":" !尼克斯vs老鹰(/images/nba-2026-april19/nk.jpg) 🏀 比分：纽约尼克斯 113 - 102 亚特兰大老鹰"},
  {"title":"骑士126-113大胜猛龙：米切尔32分创历史第一，哈登22+10迎里程碑","url":"/posts/2026/04/19/nba-playoffs-cavaliers-raptors/","date":"2026-04-19","categories":"['体育', 'NBA']","tags":['NBA', '季后赛', '骑士', '猛龙', '米切尔', '哈登', '斯特鲁斯'],"excerpt":" !骑士vs猛龙(/images/nba-2026-april19/cr.jpg) 🏀 比分：克利夫兰骑士 126 - 113 多伦多猛龙"},
  {"title":"库里孤掌难鸣！太阳111-96力克勇士，杰伦·格林36分主导惊天爆冷","url":"/posts/2026/04/18/nba-playin-suns-vs-warriors/","date":"2026-04-18","categories":"['体育']","tags":['NBA', '附加赛', '太阳', '勇士', '库里', '杰伦格林'],"excerpt":" 北京时间4月18日，NBA附加赛第二轮，西部最后一张季后赛门票争夺战。太阳主场以 111-96 力克勇士，成功晋级季后赛，首轮将对阵雷霆。 这场比赛的胜负手很清晰：库里一人扛着勇士走，而太阳全民皆兵，杰伦·格林如同天神下凡。"},
  {"title":"附加赛单节崩盘！魔术31分大胜黄蜂，班凯罗25+5+6率队晋级","url":"/posts/2026/04/18/nba-playin-magic-vs-hornets/","date":"2026-04-18","categories":"['体育']","tags":['NBA', '附加赛', '魔术', '黄蜂', '班凯罗'],"excerpt":" 北京时间4月18日，NBA附加赛第二轮，东部第八争夺战上演一场一边倒的较量。魔术主场以 121-90 大胜黄蜂，狂胜31分，以东部第8身份晋级季后赛，首轮将对阵活塞。 黄蜂在9-10名附加赛中奇迹般逆转击败猛龙，但面对真正的高强度对抗，这支年轻的球队彻底露馅。"},
  {"title":"Hermes 教程一：全面解析","url":"/posts/2026/04/18/hermes-jiao-cheng-yi/","date":"2026-04-18","categories":"['技术']","tags":['Hermes Agent', 'AI', '开源', 'Nous Research', 'Agent', '飞书', 'QQ'],"excerpt":" 在 AI Agent 领域，有一个项目在 GitHub 上已经悄悄突破了 97,900 Stars，被称为\"真正会自己成长的 AI 分身\"——它就是 Hermes Agent，来自开源 AI 研究机构 Nous Research。 本文从我作为实际使用者的角度，深度解析 Hermes Agent 的来龙去脉、核心架构、安装部署与使用教程。"},
  {"title":"Hermes 教程五：Skill 系统详解","url":"/posts/2026/04/18/hermes-jiao-cheng-wu/","date":"2026-04-18","categories":"['核心机制']","tags":['Skill系统', '工具调用', '自动化', '技能市场'],"excerpt":" Hermes 的 Skill 系统是其最强大的功能之一——它让 AI 能够像人类专家一样，根据任务需求自动调用合适的工具链。本文深入解析 Skill 的工作原理、内部架构，以及它与底层 Tool 系统的关系。 在 Hermes 中，有两个容易混淆的概念："},
  {"title":"Hermes 教程四：飞书+QQ多平台配置","url":"/posts/2026/04/18/hermes-jiao-cheng-si/","date":"2026-04-18","categories":"['平台接入']","tags":['飞书', 'QQ', '多平台', '网关配置'],"excerpt":" Hermes 的 gateway（网关）架构支持同时接入多个即时通讯平台。本文详细介绍如何同时让飞书（Lark）和 QQ Bot 接入 Hermes，实现一个后端服务同时响应两个平台的消息。 用户 ──► 飞书服务器 ──► Hermes Gateway ──► AIAgent"},
  {"title":"Hermes 教程十：定时任务自动执行","url":"/posts/2026/04/18/hermes-jiao-cheng-shi/","date":"2026-04-18","categories":"['Hermes Agent']","tags":['定时任务', 'cron', '自动化', 'schedule', '每日任务'],"excerpt":" 不想每天重复同样的工作？Hermes Agent 内置强大的定时任务系统，支持 cron 表达式、间隔执行、一次性任务，让你的 AI 助手成为 24 小时不知疲倦的数字员工。 任务配置文件存储在："},
  {"title":"Hermes 教程十一：MCP协议扩展","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-yi/","date":"2026-04-18","categories":"['Hermes Agent']","tags":['MCP', 'Model Context Protocol', '外部工具', '扩展', 'mcp_servers'],"excerpt":" Hermes Agent 支持 Model Context Protocol (MCP) 协议，可以连接海量外部工具和服务。本文详细介绍 MCP 的两种接入模式、配置方法，以及如何接入 GitHub、文件系统、Slack 等常用服务。 Model Context Protocol (MCP) 是一种标准化协议，让 AI 助手能够调用外部工具和服务。通过 MCP，Hermes 可以："},
  {"title":"Hermes 教程十五：MMX网络研究","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-wu/","date":"2026-04-18","categories":"['Hermes Agent']","tags":['MMX 搜索', '网络研究', '信息聚合', '自动化', '定时任务'],"excerpt":" Hermes Agent 提供了强大的网络搜索和研究能力，特别是 MMX 搜索功能，可以帮助用户高效地收集和整理网络信息。本文详细介绍如何用 Hermes 进行网络研究，以及如何实现多源信息聚合。 Hermes 内置的 MMX 搜索是核心研究工具，使用 --q 参数指定搜索查询："},
  {"title":"Hermes 教程十四：编程辅助方案对比","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-si/","date":"2026-04-18","categories":"['编程工具']","tags":['Cursor', 'Windsurf', 'Claude Code', 'AI 编程', '工具对比'],"excerpt":" 随着 AI 编程工具的快速发展，开发者有了更多选择。本文从功能、价格、使用体验等维度对比主流 AI 编程辅助工具，并探讨如何在 Hermes Agent 中集成这些工具。 | 工具 | 价格 | 核心特点 | 适用场景 |"},
  {"title":"Hermes 教程十三：博客运营实战","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-san/","date":"2026-04-18","categories":"['Hermes Agent']","tags":['博客运营', 'Jekyll', 'GitHub', 'GitLab', '自动化'],"excerpt":" 用 Hermes 运营个人博客是一件非常高效的事情。本文详细介绍如何用 Hermes 实现博客文章从创作到发布的完整流程，以及如何配置双平台自动推送。 Hermes 内置了 blog/jekyll-blog-troubleshooting Skill，专门用于 Jekyll 博客的常见问题诊断和日常维护。常用的博客管理操作包括："},
  {"title":"Hermes 教程十七：性能优化与Token节省","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-qi/","date":"2026-04-18","categories":"['Hermes Agent']","tags":['性能优化', 'Token 节省', 'context_compressor', '上下文压缩'],"excerpt":" 在使用 Hermes Agent 时，性能优化是一个重要话题。本文介绍如何通过各种技术手段加快响应速度、节省 Token 消耗，让 Hermes 更加高效。 Hermes 内置的 context_compressor.py 是性能优化的核心组件。其工作原理如下："},
  {"title":"Hermes 教程十六：常见问题与解决方案","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-liu/","date":"2026-04-18","categories":"['Hermes Agent']","tags":['故障排除', '常见问题', '飞书', 'QQ', 'Git', 'API'],"excerpt":" 使用 Hermes Agent 的过程中，可能会遇到一些常见问题。本文汇总了高频问题及其解决方案，帮助你快速排查和修复。 症状：飞书机器人无法接收或发送消息"},
  {"title":"Hermes 教程十二：GitHub项目管理","url":"/posts/2026/04/18/hermes-jiao-cheng-shi-er/","date":"2026-04-18","categories":"['Hermes Agent']","tags":['GitHub', 'Issues', 'PR', 'Pull Request', 'gh CLI', 'github-pr-workflow'],"excerpt":" 还在为 GitHub 操作繁琐而烦恼？Hermes Agent 内置完整的 GitHub 管理技能，支持 Issue 创建、PR 管理、代码审查，配合自然语言对话，让你的 GitHub 工作流事半功倍。 bash"},
  {"title":"Hermes 教程三：思维链与追问技巧","url":"/posts/2026/04/18/hermes-jiao-cheng-san/","date":"2026-04-18","categories":"['使用技巧']","tags":['思维链', '推理配置', '深度思考'],"excerpt":" Hermes Agent 不仅仅是一个问答机器人，它的思维链（Chain-of-Thought）系统让你可以控制 AI 的思考深度——从快速响应到深度推理，按需切换。这对于复杂分析、多步规划、代码调试等场景至关重要。 Hermes 通过 reasoning_effort 参数控制模型的内部思考量。这个概念源自 Anthropic 的 Claude 模型推理机制——模型在生成最终回答前，会在内部进行"},
  {"title":"Hermes 教程七：20+必备Skills推荐","url":"/posts/2026/04/18/hermes-jiao-cheng-qi/","date":"2026-04-18","categories":"['资源推荐']","tags":['社区Skills', '技能市场', '效率工具', '推荐列表'],"excerpt":" Hermes 的 Skills Hub 拥有丰富的社区技能生态，涵盖开发、运维、数据分析、文档生成等多个领域。本文整理 20+ 实用技能，介绍它们的功能和使用场景，帮你快速找到适合的自动化工具。 在 Hermes 中直接搜索："},
  {"title":"Hermes 教程六：编写自己的 Skill","url":"/posts/2026/04/18/hermes-jiao-cheng-liu/","date":"2026-04-18","categories":"['实战教程']","tags":['自定义Skill', '自动化', 'SKILL.md', '编写教程'],"excerpt":" Hermes 的 Skill 系统不仅仅用来安装社区技能，更重要的是你可以自己编写 Skill，把日常重复的工作流封装成可复用的自动化脚本。本文从零讲解如何编写一个真正可用的自定义 Skill。 一个 Skill 最少只需要一个文件："},
  {"title":"Hermes 教程九：记忆系统","url":"/posts/2026/04/18/hermes-jiao-cheng-jiu/","date":"2026-04-18","categories":"['Hermes Agent']","tags":['记忆系统', 'memory', 'USER.md', 'MEMORY.md', '偏好'],"excerpt":" 你是否遇到过这种情况：每次启动 Hermes Agent 都要重新解释自己的背景和使用习惯？本文详细介绍 Hermes 的双层记忆系统，让你告别重复说明，打造真正懂你的 AI 助手。 Hermes Agent 采用双层记忆架构："},
  {"title":"Hermes 教程二：零基础入门","url":"/posts/2026/04/18/hermes-jiao-cheng-er/","date":"2026-04-18","categories":"['入门教程']","tags":['新手入门', '安装配置', 'CLI'],"excerpt":" Hermes Agent 是由 Nous Research 开发的新一代 AI 助手框架，支持 CLI、飞书、QQ 等多平台运行，同时内置 Skill 技能系统、思维链推理、MCP 工具调用等强大功能。本文手把手带你从零开始，5 分钟内跑通第一个对话。 - Python 3.11+"},
  {"title":"Hermes 教程八：config.yaml深度配置","url":"/posts/2026/04/18/hermes-jiao-cheng-ba/","date":"2026-04-18","categories":"['Hermes Agent']","tags":['配置', '模型', '人格', 'toolsets', 'config.yaml'],"excerpt":" 作为 IT 从业者，你是否想让 Hermes Agent 更贴合自己的使用习惯？本文从实际运行的 ~/.hermes/config.yaml 出发，深入讲解每个配置项的作用，助你打造专属的 AI 助手。 Hermes Agent 的所有配置集中在两个文件："},
  {"title":"Claude 编程太贵了？2026年主流编程辅助方案全面对比","url":"/posts/2026/04/18/alternatives-to-claude-for-programming/","date":"2026-04-18","categories":"['编程', 'AI', '技术']","tags":['Claude', 'Copilot', 'Cursor', 'Windsurf', 'Kimi', 'DeepSeek', 'Codex', '编程辅助', 'AI编程', 'CodingPlan', '阿里云', '火山引擎', '腾讯云'],"excerpt":" 近期收到不少朋友反馈：Claude 的付费方案越来越贵，而且 Anthropic 的服务在国内访问越来越困难。作为一个长期关注 AI 编程工具的观察者，我花了些时间系统梳理了目前市面上主流的编程辅助方案，写成这篇文章，希望能给正在选型的朋友一些参考。 本文不吹不黑，数据均来自各平台官方定价页面，结论仅供参考。"},
  {"title":"AI时代的一人公司：一个人，凭什么撬动一家公司？","url":"/posts/2026/04/18/ai-shi-dai-yi-ren-gong-si/","date":"2026-04-18","categories":"['随想']","tags":['AI', '一人公司', '创业', 'Solopreneur', 'OPC'],"excerpt":" 2026年，一句过去听起来像笑话的话正在变成现实：\"一个人，一台电脑，几个AI智能体，就能开一家公司。\" 这不是科幻。"},
  {"title":"小米股价跌至腰斩：2026年Q1股票深度分析","url":"/posts/2026/04/17/xiaomi-stock-analysis-q1-2026/","date":"2026-04-17","categories":"['投资', '股票']","tags":['小米', '港股', '01810', '股价分析', '股票'],"excerpt":" | 指标 | 数据 | |------|------|"},
  {"title":"小米手机跌出前五：2026年Q1市场分析","url":"/posts/2026/04/17/xiaomi-q1-2026-analysis/","date":"2026-04-17","categories":"['科技', '手机']","tags":['小米', '手机市场', '华为', '苹果', 'OPPO', 'vivo', '荣耀'],"excerpt":" 2026年第一季度，中国智能手机市场出货量约为 6900-6980万台，同比下降约1%-3.3%。然而，市场整体微降的背后，是国产手机品牌格局的剧烈洗牌——小米以约870万台的出货量跌至第六，同比暴跌35%，这是小米近年来首次季度出货量跌出中国前五。 | 品牌 | Omdia 出货量 | 市场份额 | 同比变化 |"},
  {"title":"使用 GitHub Pages 和内网 GitLab + Nginx 部署博客","url":"/posts/2026/04/16/双平台博客部署指南/","date":"2026-04-16","categories":"技术","tags":['GitHub', 'GitLab', 'Nginx', 'Jekyll', 'Docker', 'CI/CD'],"excerpt":" 折腾了大半天，终于把双平台博客自动部署整明白了。记录一下过程，方便以后查阅，也给有类似需求的朋友一个参考。 我们的目标很简单："},
  {"title":"末节三分雨逆转！库里35分率勇士击沉快船","url":"/posts/2026/04/16/nba-playin-warriors-clippers/","date":"2026-04-16","categories":"['NBA']","tags":[],"excerpt":" 金州勇士客场以 126-121 战胜洛杉矶快船，在生死战中上演末节大逆转！库里砍下全场最高的35分，并在末节连续命中关键三分球点燃反击号角。勇士赢得惊险，将与菲尼克斯太阳争夺西部最后一张季后赛门票。 快船在主场痛失好局，赛季结束——伦纳德时代或许正式落幕。"},
  {"title":"马克西31分独自carry，76人击退魔术锁定季后赛席位","url":"/posts/2026/04/16/nba-playin-76ers-magic/","date":"2026-04-16","categories":"['NBA']","tags":[],"excerpt":" 费城76人主场以 109-97 战胜奥兰多魔术，在当家球星恩比德缺阵的情况下，成功锁定东部第7号种子，晋级季后赛——首轮将挑战苦主波士顿凯尔特人。 魔术输球后仍有机会，将与黄蜂再战一场，争夺东部最后一张季后赛门票。"},
  {"title":"为什么有些人「等不了」任何结果？—— 不确定性焦虑解析","url":"/posts/2026/04/16/intolerance-of-uncertainty/","date":"2026-04-16","categories":"心理学","tags":[],"excerpt":" —— 不确定性焦虑解析 ---"},
  {"title":"OpenClaw vs Hermes：两大 AI Agent 平台深度对比","url":"/posts/2026/04/15/openclaw-vs-hermes/","date":"2026-04-15","categories":"['AI', '技术']","tags":[],"excerpt":" 最近在玩 AI Agent，发现两个很有意思的平台：OpenClaw 和 Hermes。两者都支持 Skill/插件扩展，都走开源路线，但定位差异很大。今天来深度对比一下，顺便也记录我折腾博客的过程。 > ⚠️ 特别说明： 本文中提到的 \"Hermes\" 是我本地运行的 AI Agent 助手（基于 Hermes Agent 开源项目），并非那个搞加密货币的 Hermes代币，两者没有任何关系。"},
  {"title":"阿夫迪亚41+12创纪录！开拓者射落太阳，时隔5年重返季后赛","url":"/posts/2026/04/15/nba-playin-suns-blazers/","date":"2026-04-15","categories":"['NBA']","tags":[],"excerpt":" 西部附加赛首轮，波特兰开拓者客场以 114-110 险胜菲尼克斯太阳，夺得西部第7号种子，时隔5年重返季后赛！ 这场胜利含金量极高——开拓者本场在客场完成以下克上，以下克上击败了拥有主场优势、常规赛多赢3场的太阳。"},
  {"title":"跌宕起伏！三球准绝杀救赎，黄蜂加时险胜热火","url":"/posts/2026/04/15/nba-playin-hornets-heat/","date":"2026-04-15","categories":"['NBA']","tags":[],"excerpt":" 东部附加赛首轮，夏洛特黄蜂主场历经加时，以 127-126 险胜迈阿密热火，夺得队史附加赛首胜，继续保留季后赛希望。 这场比赛堪称本赛季最精彩的附加赛之一——双方17次交替领先，最大分差仅8分，从第一节一直激战到加时赛最后一秒。"},
  {"title":"Hello, World! 我的第一篇博客","url":"/posts/2026/04/14/hello-world/","date":"2026-04-14","categories":"['随想']","tags":[],"excerpt":" 大家好，我是曹总。这是我用 Jekyll + GitHub Pages 创建的个人博客。 以后我会在这里分享一些技术笔记和思考。"},
];;

var fuse = new Fuse(searchData, {
  keys: ['title', 'categories', 'tags', 'excerpt'],
  threshold: 0.3,
  includeMatches: true,
  minMatchCharLength: 1
});

function renderResults(results) {
  var html = '';
  if (results.length === 0) {
    html = '<div class="no-results">没有找到相关文章 😅</div>';
  } else {
    results.forEach(function(r) {
      var d = r.item;
      html += '<div class="search-result">';
      html += '<div><a href="' + d.url + '">' + d.title + '</a> <span class="date">' + d.date + '</span></div>';
      if (d.excerpt) html += '<div class="excerpt">' + d.excerpt.substring(0, 120) + (d.excerpt.length > 120 ? '...' : '') + '</div>';
      html += '</div>';
    });
  }
  document.getElementById('search-results').innerHTML = html;
}

function doSearch(query) {
  if (!query.trim()) {
    document.getElementById('search-results').innerHTML = '<div class="no-results">输入关键词开始搜索...</div>';
    return;
  }
  var results = fuse.search(query);
  renderResults(results);
}

document.addEventListener('DOMContentLoaded', function() {
  var params = new URLSearchParams(window.location.search);
  var q = params.get('q');
  if (q) {
    document.getElementById('search-input').value = q;
    doSearch(q);
  }
  document.getElementById('search-input').addEventListener('input', function(){ doSearch(this.value); });
  document.getElementById('search-input').addEventListener('keypress', function(e){
    if(e.key==='Enter'){ doSearch(this.value); }
  });
});
</script>
