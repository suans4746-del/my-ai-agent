# GameInsight

> AI 驱动的游戏玩家反馈智能分析系统

GameInsight 是一款面向游戏策划/设计师的智能 Agent 工具，能够自动从主流中文社交媒体平台（微博、小红书、B站、抖音、TapTap）爬取公开的玩家讨论内容，通过 AI 进行语义分析和情感过滤，提纯出有效的设计诉求，生成可视化周报推送至设计师端。

## 核心解决的问题

1. **信息过载** — 玩家反馈分散在 5+ 平台，数量庞大难以人工浏览
2. **噪音过滤** — 从谩骂和情绪化内容中提取有价值的改进建议
3. **优先级排序** — 识别高价值玩家（大V/资深玩家）的诉求，区分新手常见问题
4. **闭环管理** — 设计师可将诉求转为版本迭代待办，完成后自动生成更新日志素材

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18 + Vite + Tailwind CSS |
| 后端 | Node.js + Express + better-sqlite3 |
| 爬虫 | Python + Playwright |
| AI 分析 | Moonshot API |
| 数据库 | SQLite |
| 部署 | 待配置（目标：可公开访问的 Demo 链接） |

## 设计风格

- **Apple Human Interface Guidelines**
- 主色调：深空灰 `#1D1D1F` + 苹果蓝 `#007AFF`
- 圆角 12px、毛玻璃效果、柔和阴影
- 平滑动效（300ms ease-in-out）

---

## 安装与运行

### 前置要求

- **Node.js** >= 18
- **Python** >= 3.10
- **npm** >= 9

### 1. 克隆仓库

```bash
git clone https://github.com/suans4746-del/my-ai-agent.git
cd my-ai-agent
```

### 2. 安装后端依赖

```bash
cd backend
npm install
cd ..
```

后端默认运行在 `http://localhost:3001`。

### 3. 安装前端依赖

```bash
cd frontend
npm install
cd ..
```

前端开发服务器默认运行在 `http://localhost:5173`。

### 4. 安装爬虫依赖

```bash
cd crawler
pip install -r requirements.txt
playwright install
```

> `playwright install` 用于下载浏览器驱动，首次运行需要联网。

---

## 环境变量

在项目根目录创建 `.env` 文件（后端和爬虫均可读取）：

```bash
# 后端端口（可选，默认 3001）
PORT=3001

# 数据库路径（可选，默认 ../data/gameinsight.db）
DB_PATH=./data/gameinsight.db

# Moonshot API Key（AI 分析必需）
MOONSHOT_API_KEY=your_api_key_here

# 爬虫配置
CRAWL_RATE_LIMIT=5
```

> 爬虫模块使用 `python-dotenv`，会自动读取根目录 `.env`。

---

## 如何运行

### 方式一：同时启动前后端（推荐开发）

```bash
npm install   # 根目录安装 concurrently
npm run dev   # 同时启动后端 + 前端开发服务器
```

### 方式二：分别启动

```bash
# 终端 1 — 后端
cd backend && npm run dev

# 终端 2 — 前端
cd frontend && npm run dev
```

### 方式三：生产模式

```bash
# 构建前端
cd frontend && npm run build

# 启动后端（会自动 serve frontend/dist）
cd backend && npm start
```

### 运行爬虫

```bash
cd crawler

# 爬取所有平台
python main.py --keyword "英雄联盟" --limit 10

# 指定平台
python main.py --platform bilibili --keyword "原神" --limit 20

# 查看帮助
python main.py --help
```

---

## 项目结构

```
.
├── README.md              # 项目简介与安装指南
├── PRD.md                 # 产品需求文档
├── package.json           # 根目录 workspace 脚本
├── .env                   # 环境变量（不提交到 Git）
├── docs/
│   ├── designer-manual.md # 设计师使用手册
│   └── architecture.md    # 系统架构文档
├── frontend/              # React + Tailwind 前端
│   ├── src/
│   │   ├── App.jsx        # 主应用组件
│   │   ├── main.jsx       # 入口
│   │   └── index.css      # 全局样式
│   ├── package.json
│   └── vite.config.js
├── backend/               # Node.js / Express 后端
│   ├── server.js          # API 路由与服务器
│   ├── db.js              # SQLite 数据库初始化
│   └── package.json
├── crawler/               # Python Playwright 爬虫
│   ├── main.py            # 爬虫入口与调度
│   ├── requirements.txt   # Python 依赖
│   └── platforms/         # 各平台爬虫实现
│       ├── bilibili.py
│       ├── weibo.py
│       ├── xiaohongshu.py
│       ├── taptap.py
│       └── douyin.py
└── data/                  # SQLite 数据库文件
    └── gameinsight.db
```

---

## API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/stats` | Dashboard 统计数据 |
| GET | `/api/insights/top` | 本周热点诉求 TOP10 |
| GET | `/api/insights/categories` | 诉求分类统计 |
| GET | `/api/todos` | 待办列表 |
| POST | `/api/todos` | 创建待办 |
| PATCH | `/api/todos/:id` | 更新待办状态 |
| POST | `/api/crawl` | 触发爬虫任务（队列模式） |
| GET | `/api/reports/latest` | 最新周报 |

---

## 目标

本项目的交付目标是成为可放入作品集的完整作品，HR 可通过链接直接试用，面试中可现场展示完整工作流。

---

*This project is managed by TheBotCompany AI agents.*
