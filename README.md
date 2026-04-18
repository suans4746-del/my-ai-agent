# GameInsight

> AI 驱动的游戏玩家反馈智能分析系统

GameInsight 自动从 Bilibili、微博、小红书、TapTap、抖音等主流社交平台采集公开的玩家讨论内容，通过 AI 进行语义分析和情感过滤，提纯出有效的设计诉求，并以可视化周报形式推送给游戏策划/设计师。

---

## Tech Stack

| 层 | 技术 |
|----|------|
| 前端 | React 18 + Vite + Tailwind CSS |
| 后端 | Node.js + Express + better-sqlite3 |
| 爬虫 | Python + Playwright + APScheduler |
| AI 分析 | Moonshot API（大语言模型） |
| 数据库 | SQLite |

---

## Project Structure

```
.
├── backend/          # Express API 服务
├── frontend/         # React 前端应用
├── crawler/          # Python 多平台爬虫
├── data/             # SQLite 数据库文件（运行时生成）
└── docs/             # 架构文档 & 设计师使用手册
```

---

## Setup

### Backend

```bash
cd backend
npm install
node server.js
```

默认运行在 `http://localhost:3001`。

### Frontend

```bash
cd frontend
npm install
npm run dev
```

开发服务器默认运行在 `http://localhost:5173`，生产构建产物位于 `frontend/dist/`。

### Crawler

```bash
cd crawler
pip install -r requirements.txt
python main.py --keyword "英雄联盟" --limit 10
```

支持平台：`bilibili`、`weibo`、`xiaohongshu`、`taptap`、`douyin`，使用 `--platform all` 爬取全部平台。

---

## Environment Variables

在项目根目录创建 `.env` 文件：

```env
# 后端
PORT=3001

# AI 分析（Moonshot）
MOONSHOT_API_KEY=your_moonshot_api_key

# 爬虫（可选）
CRAWL_RATE_LIMIT=5
```

---

## Quick Start

1. 启动后端：`cd backend && node server.js`
2. 启动前端：`cd frontend && npm run dev`
3. 运行爬虫：`cd crawler && python main.py`
4. 打开浏览器访问前端地址，查看 Dashboard 周报与待办看板

---

## Documentation

- [系统架构](docs/architecture.md)
- [设计师使用手册](docs/designer-manual.md)
