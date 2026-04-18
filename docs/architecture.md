# GameInsight 系统架构文档

本文档描述 GameInsight 的高层级系统架构、数据流与各组件职责。

---

## 1. 架构概览

GameInsight 采用经典的三层架构：

```
┌─────────────────────────────────────────────────────────────┐
│                        前端层 (Frontend)                      │
│              React 18 + Vite + Tailwind CSS                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Dashboard   │  │ Insight     │  │ Todo Kanban         │  │
│  │ (周报视图)   │  │ Detail      │  │ (待办看板)           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP / REST
┌──────────────────────────▼──────────────────────────────────┐
│                        后端层 (Backend)                      │
│              Node.js + Express + better-sqlite3              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ API Routes  │  │ Insight     │  │ Report Generator    │  │
│  │             │  │ Aggregator  │  │ (周报生成器)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ SQLite
┌──────────────────────────▼──────────────────────────────────┐
│                      数据层 (Data Layer)                     │
│                         SQLite                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ feeds       │  │ insights    │  │ todos               │  │
│  │ (原始数据)   │  │ (AI分析结果) │  │ (设计师待办)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ HTTP / Playwright
┌──────────────────────────┴──────────────────────────────────┐
│                      爬虫层 (Crawler)                        │
│              Python + Playwright + APScheduler               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ │
│  │ Bilibili│ │ Weibo   │ │ Xiaohong│ │ TapTap  │ │ Douyin │ │
│  │         │ │         │ │ shu     │ │         │ │        │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Moonshot   │
                    │  AI API     │
                    └─────────────┘
```

---

## 2. 组件职责

### 2.1 前端层 (Frontend)

| 模块 | 职责 |
|------|------|
| Dashboard | 展示统计数据、热点诉求卡片、情感分布 |
| Insight Detail | 卡片点击展开，展示原文、AI 摘要、来源链接 |
| Todo Kanban | 三列看板（待处理 / 设计中 / 已完成），支持状态流转 |
| Settings | 游戏关键词、目标平台配置 |

- **技术选型**：React 18 Hooks + Vite 构建 + Tailwind CSS 样式
- **状态管理**：React useState/useEffect（当前规模无需 Redux）
- **API 通信**：原生 fetch，后端 API 前缀 `/api/*`

### 2.2 后端层 (Backend)

| 模块 | 职责 |
|------|------|
| API Routes | RESTful 接口，处理前端请求 |
| Insight Aggregator | 聚合 feeds 与 insights 数据，生成排行榜 |
| Report Generator | 按周汇总数据，生成 Markdown/PDF 报告 |
| Crawl Trigger | 接收手动触发请求，调用爬虫进程 |

- **技术选型**：Node.js + Express + better-sqlite3（同步 SQLite，适合单机部署）
- **部署模式**：生产环境 serve 静态前端 dist，开发环境代理到 Vite dev server

### 2.3 爬虫层 (Crawler)

| 模块 | 职责 |
|------|------|
| main.py | 入口调度，参数解析，数据库写入 |
| Platform Modules | 各平台独立实现 `crawl(keyword, limit)` 接口 |
| Rate Limiter | 平台间间隔 5 秒，防止被封 |

- **技术选型**：Python + Playwright（浏览器自动化，绕过反爬）
- **扩展性**：新增平台只需在 `platforms/` 下新增模块并在 `__init__.py` 注册

### 2.4 AI 分析层

| 模块 | 职责 |
|------|------|
| 情感分析 | 判断玩家情绪：正面 / 负面 / 混合 |
| 诉求提取 | 从长文本中提取具体的设计建议或痛点 |
| 玩家身份识别 | 根据资料判断 KOL / 资深玩家 / 新手 |
| 自动分类 | 按 UI/UX、数值平衡、剧情、BUG、新功能建议归类 |

- **技术选型**：Moonshot API（大语言模型，支持中文语义理解）
- **调用时机**：爬虫采集后批量调用，结果写入 `insights` 表

---

## 3. 数据流

### 3.1 日常采集流程

```
1. Scheduler 触发爬虫任务
        │
        ▼
2. Crawler 依次访问各平台搜索页
        │
        ▼
3. 提取公开内容 → 写入 feeds 表
        │
        ▼
4. AI Engine 读取未分析 feeds
        │
        ▼
5. 调用 Moonshot API 分析
        │
        ▼
6. 结果写入 insights 表
        │
        ▼
7. 前端 Dashboard 轮询/刷新展示
```

### 3.2 设计师交互流程

```
1. 设计师打开 Dashboard
        │
        ▼
2. 浏览 AI 提纯后的诉求卡片
        │
        ▼
3. 点击卡片查看详情（原文 + AI 分析）
        │
        ▼
4. 点击「转为待办」→ 创建 todo
        │
        ▼
5. 在 Todo Kanban 中管理状态
        │
        ▼
6. 标记「已完成」→ 自动生成更新日志草稿
```

---

## 4. 数据库 Schema

### feeds — 原始采集数据

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| platform | TEXT | 来源平台 |
| url | TEXT | 原帖链接 |
| content | TEXT | 原始内容 |
| author_hash | TEXT | 作者 ID 的 SHA256 前16位（匿名化） |
| published_at | TEXT | 发布时间 |
| collected_at | TEXT | 采集时间 |
| game_keyword | TEXT | 匹配的关键词 |

### insights — AI 分析结果

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| feed_id | INTEGER FK | 关联 feeds |
| summary | TEXT | AI 提炼的诉求摘要 |
| sentiment_score | REAL | 情感分值 -1 ~ +1 |
| category | TEXT | 分类标签 |
| player_type | TEXT | 玩家身份标签 |
| ai_analyzed_at | TEXT | 分析时间 |

### todos — 设计师待办

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| insight_id | INTEGER FK | 关联 insights（可为空） |
| title | TEXT | 待办标题 |
| status | TEXT | pending / designing / done |
| notes | TEXT | 备注 |
| priority | TEXT | high / medium / low |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

---

## 5. 安全与合规

- **数据匿名化**：所有用户 ID 存储为 SHA256 哈希，不可逆推原始身份
- **公开内容-only**：爬虫仅访问无需登录即可见的公开页面
- **限速策略**：平台间爬取间隔 >= 5 秒，单平台请求频率遵守 robots.txt
- **删除机制**：提供 API 支持按 author_hash 删除该用户的所有数据

---

## 6. 扩展方向

| 方向 | 说明 |
|------|------|
| 新增平台 | 在 `crawler/platforms/` 添加新模块即可 |
| 替换 AI 引擎 | 修改调用层，可切换至 OpenAI / Claude / 本地模型 |
| 多游戏支持 | `game_keyword` 字段已预留，前端增加游戏切换器 |
| 实时推送 | 后端增加 WebSocket，爬虫完成后主动推送 |
| 用户系统 | 增加设计师账号体系，支持多项目隔离 |

---

*Last updated: 2024*
