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
  {
    "title": "Dosunmu狂砍43分创生涯新高，森林狼大胜掘金3-1拿到赛点",
    "url": "/posts/2026/04/26/nba-playoffs-timberwolves-nuggets/",
    "date": "2026-04-26 12:00:00 +0800",
    "categories": "NBA",
    "tags": [],
    "excerpt": "球员数据 森林狼："
  },
  {
    "title": "SGA狂砍42分！雷霆横扫太阳晋级在望",
    "url": "/posts/2026/04/26/nba-playoffs-thunder-suns/",
    "date": "2026-04-26 12:00:00 +0800",
    "categories": "NBA",
    "tags": [],
    "excerpt": "球员数据 雷霆："
  },
  {
    "title": "魔术主场险胜活塞系列赛2-1，Banchero全能表现率队占先",
    "url": "/posts/2026/04/26/nba-playoffs-magic-pistons/",
    "date": "2026-04-26 12:00:00 +0800",
    "categories": "NBA",
    "tags": [],
    "excerpt": "球员数据 魔术："
  },
  {
    "title": "Towns砍下赛季首个三双，尼克斯大胜老鹰扳平系列赛",
    "url": "/posts/2026/04/26/nba-playoffs-knicks-hawks/",
    "date": "2026-04-26 12:00:00 +0800",
    "categories": "NBA",
    "tags": [],
    "excerpt": "球员数据 尼克斯："
  },
  {
    "title": "文班缺阵马刺逆转15分！卡斯尔33分+哈珀27分，榜眼秀导演19分大翻盘",
    "url": "/posts/2026/04/25/spurs-blazers-g3-analysis/",
    "date": "2026-04-25 14:00:00 +0800",
    "categories": "NBA",
    "tags": [
      "NBA季后赛",
      "马刺",
      "开拓者",
      "卡斯尔",
      "哈珀",
      "文班"
    ],
    "excerpt": "文班脑震荡缺阵，马刺最多落后15分。卡斯尔和哈珀这对新星组合合砍60分，导演了一场荡气回肠的逆转。马刺2-1重夺主场优势，没有文班的马刺反而更加强大？"
  },
  {
    "title": "12秒连丢6分！火箭加时108-112再负湖人，0-3濒临出局",
    "url": "/posts/2026/04/25/lakers-rockets-g3-analysis/",
    "date": "2026-04-25 13:00:00 +0800",
    "categories": "NBA",
    "tags": [
      "NBA季后赛",
      "湖人",
      "火箭",
      "詹姆斯",
      "申京"
    ],
    "excerpt": "火箭距离胜利只差12秒。申京33+16几乎封神，小贾和谢泼德连续致命失误，詹姆斯绝平三分拖入加时——湖人在休斯顿偷走了一场胜利，0-3，火箭站在了悬崖边上。"
  },
  {
    "title": "塔图姆里程碑之夜！凯尔特人险胜76人2-1，双探花同砍25分立大功",
    "url": "/posts/2026/04/25/celtics-76ers-g3-analysis/",
    "date": "2026-04-25 12:00:00 +0800",
    "categories": "NBA",
    "tags": [
      "NBA季后赛",
      "凯尔特人",
      "76人",
      "塔图姆",
      "布朗",
      "马克西"
    ],
    "excerpt": "费城主场，108-100。塔图姆用一记杀死比赛的三分完成生涯季后赛3000分里程碑，双探花第20次同砍25+，凯尔特人重新夺回主场优势。"
  },
  {
    "title": "【G3复盘】森林狼113-96掘金：约基奇26中7背后的防守真相",
    "url": "/posts/2026/04/24/nba-playoffs-timberwolves-nuggets-g3-analysis/",
    "date": "2026-04-24",
    "categories": "",
    "tags": [
      "NBA",
      "季后赛",
      "森林狼",
      "掘金",
      "约基奇",
      "爱德华兹"
    ],
    "excerpt": "战术分析 1. 森林狼：防守策略的完美执行"
  },
  {
    "title": "【G3复盘】猛龙126-104骑士：巴恩斯33分11助攻击碎横扫梦",
    "url": "/posts/2026/04/24/nba-playoffs-raptors-cavaliers-g3-analysis/",
    "date": "2026-04-24",
    "categories": "",
    "tags": [
      "NBA",
      "季后赛",
      "猛龙",
      "骑士",
      "巴恩斯",
      "哈登"
    ],
    "excerpt": "战术分析 1. 猛龙：双星闪耀击溃骑士防线"
  },
  {
    "title": "【G3复盘】老鹰109-108尼克斯：CJ准绝杀背后的战术博弈",
    "url": "/posts/2026/04/24/nba-playoffs-hawks-knicks-g3-analysis/",
    "date": "2026-04-24",
    "categories": "",
    "tags": [
      "NBA",
      "季后赛",
      "老鹰",
      "尼克斯",
      "麦科勒姆",
      "库明加"
    ],
    "excerpt": "战术分析 1. 老鹰：库里式战术的教科书演绎"
  },
  {
    "title": "DeepSeek V4 正式发布：百万Token上下文，挑战GPT-4 Turbo",
    "url": "/posts/2026/04/24/deepseek-v4-released/",
    "date": "2026-04-24",
    "categories": "",
    "tags": [
      "DeepSeek",
      "AI大模型",
      "V4",
      "百万上下文",
      "华为芯片"
    ],
    "excerpt": ""
  },
  {
    "title": "亚历山大37+9，雷霆再胜太阳2-0领先——Dillon Brooks空砍30分难救主",
    "url": "/posts/2026/04/23/thunder-suns-g2-analysis/",
    "date": "2026-04-23 11:30:00 +0800",
    "categories": "NBA",
    "tags": [
      "NBA季后赛",
      "雷霆",
      "太阳",
      "亚历山大",
      "Dillon Brooks"
    ],
    "excerpt": "雷霆主场120-107再胜太阳，系列赛2-0领先。亚历山大砍下37分9助攻主导比赛，Dillon Brooks狂砍30分成为太阳唯一亮点，但孤立无援无力回天。"
  },
  {
    "title": "活塞防守封锁魔术，98-83攻下主场——系列赛回到同一起跑线",
    "url": "/posts/2026/04/23/magic-pistons-g2-analysis/",
    "date": "2026-04-23 10:30:00 +0800",
    "categories": "NBA",
    "tags": [
      "NBA季后赛",
      "活塞",
      "魔术",
      "班凯罗",
      "康宁汉姆"
    ],
    "excerpt": "活塞在G2用窒息的防守让魔术全场仅得83分，第三节单节38-16的攻势彻底拉开分差。班凯罗受限严重仅得18分，康宁汉姆稳定输出带队取胜。系列赛1-1战平，G3将移师奥兰多。"
  },
  {
    "title": "为什么越来越少人发朋友圈了？",
    "url": "/posts/2026/04/22/why-people-quit-social-media/",
    "date": "2026-04-22 06:30:00 +0800",
    "categories": "随想",
    "tags": [
      "社交媒体",
      "朋友圈",
      "互联网"
    ],
    "excerpt": "发社交媒体本质上是在表演生活，表演多了自己也累。越来越多的人选择沉默，不是因为生活变得无聊，而是因为表达的成本和回报越来越不成正比。"
  },
  {
    "title": "文班伤退，马刺遭16分逆转——天才的代价与不屈的斗士",
    "url": "/posts/2026/04/22/spurs-blazers-g2-analysis/",
    "date": "2026-04-22 16:00:00 +0800",
    "categories": "NBA",
    "tags": [
      "NBA季后赛",
      "马刺",
      "开拓者",
      "文班",
      "亨德森"
    ],
    "excerpt": "文班亚马在第二节因伤退赛，马刺在最多领先16分的情况下遭开拓者逆转，以103-106失利。斯科特·亨德森用31分的表现证明：状元有状元的骄傲，而榜眼也有榜眼的价值。"
  },
  {
    "title": "詹姆斯28+8+7湖人再胜火箭，41岁仍是不屈的斗士",
    "url": "/posts/2026/04/22/lakers-rockets-g2-analysis/",
    "date": "2026-04-22 15:00:00 +0800",
    "categories": "NBA",
    "tags": [
      "NBA季后赛",
      "湖人",
      "火箭",
      "詹姆斯"
    ],
    "excerpt": "41岁的詹姆斯用一场28分8篮板7助攻的表现告诉世人：所谓的“单核带队”，在他这个年纪依然是夺冠的基本操作。湖人在东契奇和里夫斯缺阵的情况下，2-0领先火箭，靠的不仅是天赋，更是铁血防守。"
  },
  {
    "title": "新秀埃奇库姆30+10，76人爆冷扳平绿军——这才是季后赛该有的样子",
    "url": "/posts/2026/04/22/celtics-76ers-g2-analysis/",
    "date": "2026-04-22 15:30:00 +0800",
    "categories": "NBA",
    "tags": [
      "NBA季后赛",
      "76人",
      "凯尔特人",
      "埃奇库姆",
      "新秀"
    ],
    "excerpt": "在恩比德缺阵的情况下，76人客场111-97大胜凯尔特人，将系列赛扳成1-1平。新秀埃奇库姆用30分10篮板的数据证明：DPOY不只是会防守，他正在成长为真正的领袖。"
  },
  {
    "title": "AI编程工具集体涨价背后：原因、趋势与应对策略",
    "url": "/posts/2026/04/22/ai-coding-tools-price-change-analysis/",
    "date": "2026-04-22",
    "categories": "",
    "tags": [
      "AI编程",
      "GitHub Copilot",
      "Windsurf",
      "阿里云",
      "通义",
      "订阅"
    ],
    "excerpt": "三、普通用户的应对策略 1. 多平台分散风险，不要把鸡蛋放一个篮子里"
  },
  {
    "title": "为什么有些人总是埋怨社会，却从不想着改变自己",
    "url": "/posts/2026/04/21/why-people-always-complain-about-society/",
    "date": "2026-04-21",
    "categories": "",
    "tags": [
      "观点",
      "社会观察",
      "随笔"
    ],
    "excerpt": "如果你想帮他们 可以试着这样聊："
  },
  {
    "title": "森林狼19分惊天逆转掘金，系列赛1-1扳平，爱德华兹30+10率队取胜",
    "url": "/posts/2026/04/21/nba-playoffs-timberwolves-nuggets-analysis/",
    "date": "2026-04-21",
    "categories": "",
    "tags": [
      "NBA",
      "季后赛",
      "森林狼",
      "掘金"
    ],
    "excerpt": "球员数据 | 球员 | 球队 | 数据 |"
  },
  {
    "title": "老鹰107-106大逆转尼克斯，McCollum 32分末节救赎，系列赛1-1扳平",
    "url": "/posts/2026/04/21/nba-playoffs-knicks-hawks-analysis/",
    "date": "2026-04-21",
    "categories": "",
    "tags": [
      "NBA",
      "季后赛",
      "尼克斯",
      "老鹰"
    ],
    "excerpt": "球员数据 | 球员 | 球队 | 数据 |"
  },
  {
    "title": "骑士115-105再胜猛龙，系列赛2-0领先，Harden Mitchell双星闪耀",
    "url": "/posts/2026/04/21/nba-playoffs-cavaliers-raptors-analysis/",
    "date": "2026-04-21",
    "categories": "",
    "tags": [
      "NBA",
      "季后赛",
      "骑士",
      "猛龙"
    ],
    "excerpt": "球员数据 | 球员 | 球队 | 数据 |"
  },
  {
    "title": "华为Pura系列及全场景新品发布会：麒麟9030统治全场，全生态矩阵亮相",
    "url": "/posts/2026/04/21/huawei-pura-launch-event-review/",
    "date": "2026-04-21",
    "categories": "",
    "tags": [
      "科技",
      "华为",
      "新品发布",
      "手机",
      "折叠屏"
    ],
    "excerpt": "1. Pura 90系列：2亿像素的影像怪兽 核心配置"
  },
  {
    "title": "119-84！卫冕冠军35分狂胜太阳，亚历山大17罚砍25分，三节打卡下班",
    "url": "/posts/2026/04/20/nba-playoffs-thunder-suns-analysis/",
    "date": "2026-04-20",
    "categories": "",
    "tags": [
      "NBA",
      "季后赛",
      "雷霆",
      "太阳"
    ],
    "excerpt": "作者：搜狐体育"
  },
  {
    "title": "111-98！文班亚玛35分破纪录，马刺轻取开拓者，杨瀚森季后赛首秀",
    "url": "/posts/2026/04/20/nba-playoffs-spurs-blazers-analysis/",
    "date": "2026-04-20",
    "categories": "",
    "tags": [
      "NBA",
      "季后赛",
      "马刺",
      "开拓者",
      "文班亚玛"
    ],
    "excerpt": "作者：搜狐体育"
  },
  {
    "title": "112-101！魔术爆冷掀翻东部第一，班凯罗23+9教做人，坎宁安空砍39分",
    "url": "/posts/2026/04/20/nba-playoffs-magic-pistons-analysis/",
    "date": "2026-04-20",
    "categories": "",
    "tags": [
      "NBA",
      "季后赛",
      "魔术",
      "活塞"
    ],
    "excerpt": "作者：搜狐体育"
  },
  {
    "title": "123-91！绿军32分碾压76人，双探花合砍51分创纪录，塔图姆超越科比",
    "url": "/posts/2026/04/20/nba-playoffs-celtics-76ers-analysis/",
    "date": "2026-04-20",
    "categories": "",
    "tags": [
      "NBA",
      "季后赛",
      "凯尔特人",
      "76人"
    ],
    "excerpt": "作者：搜狐体育"
  },
  {
    "title": "掘金116-105逆转森林狼：约基奇25+13+11三双，穆雷16罚全中末节救赎",
    "url": "/posts/2026/04/19/nba-playoffs-nuggets-wolves/",
    "date": "2026-04-19 12:30:00 +0800",
    "categories": "体育,NBA",
    "tags": [
      "NBA",
      "季后赛",
      "掘金",
      "森林狼",
      "约基奇",
      "穆雷",
      "爱德华兹"
    ],
    "excerpt": "📝 深度比赛分析 一、约基奇：上半场控场，下半场收割"
  },
  {
    "title": "残阵湖人107-98力克火箭：詹姆斯19+13率队三节收割，肯纳德三分5中5奇兵天降",
    "url": "/posts/2026/04/19/nba-playoffs-lakers-rockets/",
    "date": "2026-04-19 12:20:00 +0800",
    "categories": "体育,NBA",
    "tags": [
      "NBA",
      "季后赛",
      "湖人",
      "火箭",
      "詹姆斯",
      "肯纳德",
      "艾顿",
      "申京"
    ],
    "excerpt": "📝 深度比赛分析 一、詹姆斯首节8助攻：传奇控场大师"
  },
  {
    "title": "尼克斯113-102轻取老鹰：布伦森首节19分定基调，唐斯末节收割比赛",
    "url": "/posts/2026/04/19/nba-playoffs-knicks-hawks/",
    "date": "2026-04-19 12:10:00 +0800",
    "categories": "体育,NBA",
    "tags": [
      "NBA",
      "季后赛",
      "尼克斯",
      "老鹰",
      "布伦森",
      "唐斯",
      "布里奇斯"
    ],
    "excerpt": "📝 深度比赛分析 一、布伦森\"热启动\"：首节19分点燃全场"
  },
  {
    "title": "骑士126-113大胜猛龙：米切尔32分创历史第一，哈登22+10迎里程碑",
    "url": "/posts/2026/04/19/nba-playoffs-cavaliers-raptors/",
    "date": "2026-04-19 12:00:00 +0800",
    "categories": "体育,NBA",
    "tags": [
      "NBA",
      "季后赛",
      "骑士",
      "猛龙",
      "米切尔",
      "哈登",
      "斯特鲁斯"
    ],
    "excerpt": "📝 深度比赛分析 一、登哥季后赛首秀：完美指挥官"
  },
  {
    "title": "库里孤掌难鸣！太阳111-96力克勇士，杰伦·格林36分主导惊天爆冷",
    "url": "/posts/2026/04/18/nba-playin-suns-vs-warriors/",
    "date": "2026-04-18 14:00:00 +0800",
    "categories": "体育",
    "tags": [
      "NBA",
      "附加赛",
      "太阳",
      "勇士",
      "库里",
      "杰伦格林"
    ],
    "excerpt": ""
  },
  {
    "title": "附加赛单节崩盘！魔术31分大胜黄蜂，班凯罗25+5+6率队晋级",
    "url": "/posts/2026/04/18/nba-playin-magic-vs-hornets/",
    "date": "2026-04-18 13:30:00 +0800",
    "categories": "体育",
    "tags": [
      "NBA",
      "附加赛",
      "魔术",
      "黄蜂",
      "班凯罗"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程一：全面解析",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-yi/",
    "date": "2026-04-18 17:30:00 +0800",
    "categories": "技术",
    "tags": [
      "Hermes Agent",
      "AI",
      "开源",
      "Nous Research",
      "Agent",
      "飞书",
      "QQ"
    ],
    "excerpt": "三、安装部署 环境要求"
  },
  {
    "title": "Hermes 教程五：Skill 系统详解",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-wu/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "核心机制",
    "tags": [
      "Skill系统",
      "工具调用",
      "自动化",
      "技能市场"
    ],
    "excerpt": "Git Helper 你是一个专业的 Git 助手，擅长："
  },
  {
    "title": "Hermes 教程四：飞书+QQ多平台配置",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-si/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "平台接入",
    "tags": [
      "飞书",
      "QQ",
      "多平台",
      "网关配置"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程十：定时任务自动执行",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-shi/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "Hermes Agent",
    "tags": [
      "定时任务",
      "cron",
      "自动化",
      "schedule",
      "每日任务"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程十一：MCP协议扩展",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-shi-yi/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "Hermes Agent",
    "tags": [
      "MCP",
      "Model Context Protocol",
      "外部工具",
      "扩展",
      "mcp_servers"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程十五：MMX网络研究",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-shi-wu/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "Hermes Agent",
    "tags": [
      "MMX 搜索",
      "网络研究",
      "信息聚合",
      "自动化",
      "定时任务"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程十四：编程辅助方案对比",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-shi-si/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "编程工具",
    "tags": [
      "Cursor",
      "Windsurf",
      "Claude Code",
      "AI 编程",
      "工具对比"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程十三：博客运营实战",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-shi-san/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "Hermes Agent",
    "tags": [
      "博客运营",
      "Jekyll",
      "GitHub",
      "GitLab",
      "自动化"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程十七：性能优化与Token节省",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-shi-qi/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "Hermes Agent",
    "tags": [
      "性能优化",
      "Token 节省",
      "context_compressor",
      "上下文压缩"
    ],
    "excerpt": "   <article>"
  },
  {
    "title": "Hermes 教程十六：常见问题与解决方案",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-shi-liu/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "Hermes Agent",
    "tags": [
      "故障排除",
      "常见问题",
      "飞书",
      "QQ",
      "Git",
      "API"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程十二：GitHub项目管理",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-shi-er/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "Hermes Agent",
    "tags": [
      "GitHub",
      "Issues",
      "PR",
      "Pull Request",
      "gh CLI",
      "github-pr-workflow"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程三：思维链与追问技巧",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-san/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "使用技巧",
    "tags": [
      "思维链",
      "推理配置",
      "深度思考"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程七：20+必备Skills推荐",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-qi/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "资源推荐",
    "tags": [
      "社区Skills",
      "技能市场",
      "效率工具",
      "推荐列表"
    ],
    "excerpt": "3. api-doc-generator ⭐⭐⭐⭐ 功能：根据代码自动生成 API 文档（OpenAPI/Swagger）。"
  },
  {
    "title": "Hermes 教程六：编写自己的 Skill",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-liu/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "实战教程",
    "tags": [
      "自定义Skill",
      "自动化",
      "SKILL.md",
      "编写教程"
    ],
    "excerpt": "每日汇报 Skill 你是一个专业的项目经理，擅长生成结构化的每日工作汇报。"
  },
  {
    "title": "Hermes 教程九：记忆系统",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-jiu/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "Hermes Agent",
    "tags": [
      "记忆系统",
      "memory",
      "USER.md",
      "MEMORY.md",
      "偏好"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程二：零基础入门",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-er/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "入门教程",
    "tags": [
      "新手入门",
      "安装配置",
      "CLI"
    ],
    "excerpt": ""
  },
  {
    "title": "Hermes 教程八：config.yaml深度配置",
    "url": "/posts/2026/04/18/hermes-jiao-cheng-ba/",
    "date": "2026-04-18 18:00:00 +0800",
    "categories": "Hermes Agent",
    "tags": [
      "配置",
      "模型",
      "人格",
      "toolsets",
      "config.yaml"
    ],
    "excerpt": ""
  },
  {
    "title": "Claude 编程太贵了？2026年主流编程辅助方案全面对比",
    "url": "/posts/2026/04/18/alternatives-to-claude-for-programming/",
    "date": "2026-04-18 12:00:00 +0800",
    "categories": "编程,AI,技术",
    "tags": [
      "Claude",
      "Copilot",
      "Cursor",
      "Windsurf",
      "Kimi",
      "DeepSeek",
      "Codex",
      "编程辅助",
      "AI编程",
      "CodingPlan",
      "阿里云",
      "火山引擎",
      "腾讯云"
    ],
    "excerpt": "二、IDE 编程插件对比 这类工具是直接在 IDE 里集成 AI 编程能力，适合日常开发使用。"
  },
  {
    "title": "AI时代的一人公司：一个人，凭什么撬动一家公司？",
    "url": "/posts/2026/04/18/ai-shi-dai-yi-ren-gong-si/",
    "date": "2026-04-18 15:00:00 +0800",
    "categories": "随想",
    "tags": [
      "AI",
      "一人公司",
      "创业",
      "Solopreneur",
      "OPC"
    ],
    "excerpt": "三、一人公司可以做什么？9大方向实操指南 1. 内容创作与IP运营"
  },
  {
    "title": "小米股价跌至腰斩：2026年Q1股票深度分析",
    "url": "/posts/2026/04/17/xiaomi-stock-analysis-q1-2026/",
    "date": "2026-04-17 10:00:00 +0800",
    "categories": "投资,股票",
    "tags": [
      "小米",
      "港股",
      "01810",
      "股价分析",
      "股票"
    ],
    "excerpt": "⚠️ 机构观点：偏谨慎 高盛预警"
  },
  {
    "title": "小米手机跌出前五：2026年Q1市场分析",
    "url": "/posts/2026/04/17/xiaomi-q1-2026-analysis/",
    "date": "2026-04-17 09:30:00 +0800",
    "categories": "科技,手机",
    "tags": [
      "小米",
      "手机市场",
      "华为",
      "苹果",
      "OPPO",
      "vivo",
      "荣耀"
    ],
    "excerpt": "📈 全球市场表现 值得注意的是，小米在全球市场仍排名第三（仅次于苹果和三星），出货量约3380万台，市场份额约11.7%。但全球出货量同比也下降了19.1%。"
  },
  {
    "title": "使用 GitHub Pages 和内网 GitLab + Nginx 部署博客",
    "url": "/posts/2026/04/16/双平台博客部署指南/",
    "date": "2026-04-16 22:30:00 +0800",
    "categories": "技术",
    "tags": [
      "GitHub",
      "GitLab",
      "Nginx",
      "Jekyll",
      "Docker",
      "CI/CD"
    ],
    "excerpt": ""
  },
  {
    "title": "末节三分雨逆转！库里35分率勇士击沉快船",
    "url": "/posts/2026/04/16/nba-playin-warriors-clippers/",
    "date": "2026-04-16 22:30:00 +0800",
    "categories": "NBA",
    "tags": [],
    "excerpt": "球员数据 勇士："
  },
  {
    "title": "马克西31分独自carry，76人击退魔术锁定季后赛席位",
    "url": "/posts/2026/04/16/nba-playin-76ers-magic/",
    "date": "2026-04-16 21:00:00 +0800",
    "categories": "NBA",
    "tags": [],
    "excerpt": "球员数据 76人："
  },
  {
    "title": "为什么有些人「等不了」任何结果？—— 不确定性焦虑解析",
    "url": "/posts/2026/04/16/intolerance-of-uncertainty/",
    "date": "2026-04-16",
    "categories": "心理学",
    "tags": [],
    "excerpt": "什么是不确定性焦虑 当我们处于\"不知道结果\"的状态时，大多数人会感到一些不适，但这种不适是可以通过其他事情分散注意力、随着时间慢慢消退的。"
  },
  {
    "title": "OpenClaw vs Hermes：两大 AI Agent 平台深度对比",
    "url": "/posts/2026/04/15/openclaw-vs-hermes/",
    "date": "2026-04-15 16:30:00 +0800",
    "categories": "AI,技术",
    "tags": [],
    "excerpt": "Hermes（我正在用的） | 项目 | 信息 |"
  },
  {
    "title": "阿夫迪亚41+12创纪录！开拓者射落太阳，时隔5年重返季后赛",
    "url": "/posts/2026/04/15/nba-playin-suns-blazers/",
    "date": "2026-04-15 15:00:00 +0800",
    "categories": "NBA",
    "tags": [],
    "excerpt": "比赛进程 | 节次 | 开拓者 | 太阳 |"
  },
  {
    "title": "跌宕起伏！三球准绝杀救赎，黄蜂加时险胜热火",
    "url": "/posts/2026/04/15/nba-playin-hornets-heat/",
    "date": "2026-04-15 14:00:00 +0800",
    "categories": "NBA",
    "tags": [],
    "excerpt": "球员数据 黄蜂："
  },
  {
    "title": "Hello, World! 我的第一篇博客",
    "url": "/posts/2026/04/14/hello-world/",
    "date": "2026-04-14 10:00:00 +0800",
    "categories": "随想",
    "tags": [],
    "excerpt": ""
  }
];;;;;;;;;;;;;;;;;;;;;

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
