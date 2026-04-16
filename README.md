# GameInsight

> AI 驱动的游戏玩家反馈智能分析系统

GameInsight 是一款面向游戏策划/设计师的智能 Agent 工具，能够自动从主流中文社交媒体平台（微博、小红书、B站、抖音、TapTap、百度贴吧）爬取公开的玩家讨论内容，通过 AI 进行语义分析和情感过滤，提纯出有效的设计诉求，生成可视化周报推送至设计师端。

## 核心解决的问题

1. **信息过载** — 玩家反馈分散在 7+ 平台，数量庞大难以人工浏览
2. **噪音过滤** — 从谩骂和情绪化内容中提取有价值的改进建议
3. **优先级排序** — 识别高价值玩家（大V/资深玩家）的诉求，区分新手常见问题
4. **闭环管理** — 设计师可将诉求转为版本迭代待办，完成后自动生成更新日志素材

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React + Tailwind CSS |
| 后端 | Node.js / Express |
| 爬虫 | Python + Playwright |
| AI 分析 | Moonshot API |
| 数据库 | SQLite |
| 部署 | 待配置（目标：可公开访问的 Demo 链接） |

## 设计风格

- **Apple Human Interface Guidelines**
- 主色调：深空灰 `#1D1D1F` + 苹果蓝 `#007AFF`
- 圆角 12px、毛玻璃效果、柔和阴影
- 平滑动效（300ms ease-in-out）

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/suans4746-del/my-ai-agent.git
cd my-ai-agent

# 2. 安装后端依赖
cd backend && npm install && cd ..

# 3. 安装前端依赖
cd frontend && npm install && cd ..

# 4. 安装爬虫依赖
cd crawler && pip install -r requirements.txt && cd ..

# 5. 启动开发环境
# （详见各目录下的 README）
```

## 项目结构

```
.
├── README.md              # 项目简介
├── PRD.md                 # 产品需求文档
├── docs/
│   └── designer-manual.md # 设计师使用手册
├── frontend/              # React + Tailwind 前端
├── backend/               # Node.js / Express 后端
└── crawler/               # Python Playwright 爬虫
```

## 目标

本项目的交付目标是成为可放入作品集的完整作品，HR 可通过链接直接试用，面试中可现场展示完整工作流。

---

*This project is managed by TheBotCompany AI agents.*
