import React, { useEffect, useState } from 'react'
import { BarChart3, MessageSquare, CheckSquare, LayoutDashboard, Settings, Sparkles } from 'lucide-react'

function App() {
  const [stats, setStats] = useState({ feeds: 0, insights: 0, pendingTodos: 0 })
  const [insights, setInsights] = useState([])
  const [selectedInsight, setSelectedInsight] = useState(null)

  useEffect(() => {
    fetch('/api/stats').then(r => r.json()).then(setStats).catch(() => {})
    fetch('/api/insights/top').then(r => r.json()).then(setInsights).catch(() => {})

		fetch('/api/crawler/data').then(r => r.json()).then(data => setStats({ ...stats, crawlerData: data })).catch(() => {})
  }, [])

  const navItem = (icon, label, active = false) => (
    <div className={`flex items-center gap-3 px-4 py-2.5 rounded-xl cursor-pointer transition-colors ${active ? 'bg-apple-blue/20 text-apple-blue' : 'text-apple-gray hover:text-white hover:bg-white/5'}`}>
      {icon}
      <span className="text-sm font-medium">{label}</span>
    </div>
  )

  return (
    <div className="flex h-screen w-full bg-apple-bg overflow-hidden">
      {/* Sidebar */}
      <aside className="w-60 flex-shrink-0 border-r border-white/5 p-4 flex flex-col">
        <div className="flex items-center gap-2 px-2 mb-8">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-apple-blue to-purple-500 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <span className="text-lg font-semibold tracking-tight">GameInsight</span>
        </div>
        <nav className="space-y-1 flex-1">
          {navItem(<LayoutDashboard className="w-4 h-4" />, "Dashboard", true)}
          {navItem(<MessageSquare className="w-4 h-4" />, "Insights")}
          {navItem(<CheckSquare className="w-4 h-4" />, "Todos")}
          {navItem(<BarChart3 className="w-4 h-4" />, "Reports")}
          {navItem(<Settings className="w-4 h-4" />, "Settings")}
        </nav>
      </aside>

      {/* Main */}
      <main className="flex-1 overflow-y-auto p-8">
        <header className="mb-8">
          <h1 className="text-2xl font-semibold">Weekly Insights</h1>
          <p className="text-apple-gray text-sm mt-1">AI-curated player feedback for your game</p>
        </header>

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <StatCard label="Total Feeds" value={stats.feeds} />
          <StatCard label="Valid Insights" value={stats.insights} />
          <StatCard label="Pending Todos" value={stats.pendingTodos} />
        </div>

        {/* Insights Grid */}
        <h2 className="text-lg font-medium mb-4">Top Feedback</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {insights.length === 0 && (
            <EmptyCard message="No insights yet — run a crawl to collect player feedback." />
          )}
          {insights.map((item) => (
            <div
              key={item.id}
              onClick={() => setSelectedInsight(item)}
              className="glass rounded-2xl p-5 cursor-pointer hover:bg-white/5 transition-all duration-300 shadow-soft"
            >
              <div className="flex items-center justify-between mb-3">
                <PlatformBadge platform={item.platform} />
                <span className={`text-xs font-medium px-2 py-1 rounded-full ${sentimentColor(item.sentiment_score)}`}>
                  {sentimentLabel(item.sentiment_score)}
                </span>
              </div>
              <p className="text-sm text-white/90 line-clamp-3 leading-relaxed">{item.summary || item.content}</p>
              <div className="mt-4 flex items-center gap-2">
                {item.player_type && (
                  <span className="text-[11px] px-2 py-0.5 rounded-full bg-white/10 text-white/70">{item.player_type}</span>
                )}
                {item.category && (
                  <span className="text-[11px] px-2 py-0.5 rounded-full bg-apple-blue/20 text-apple-blue">{item.category}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Detail Modal */}
      {selectedInsight && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
          onClick={() => setSelectedInsight(null)}
        >
          <div
            className="glass w-full max-w-2xl rounded-2xl p-6 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <PlatformBadge platform={selectedInsight.platform} />
              <button onClick={() => setSelectedInsight(null)} className="text-apple-gray hover:text-white">Close</button>
            </div>
            <p className="text-base leading-relaxed text-white/95 mb-6">{selectedInsight.summary || selectedInsight.content}</p>
            <div className="flex flex-wrap items-center gap-3 mb-6">
              {selectedInsight.player_type && <Badge>{selectedInsight.player_type}</Badge>}
              {selectedInsight.category && <Badge variant="blue">{selectedInsight.category}</Badge>}
              <Badge variant={sentimentVariant(selectedInsight.sentiment_score)}>
                {sentimentLabel(selectedInsight.sentiment_score)} {selectedInsight.sentiment_score?.toFixed?.(2)}
              </Badge>
            </div>
            <div className="flex items-center gap-3">
              <a
                href={selectedInsight.url}
                target="_blank"
                rel="noreferrer"
                className="text-sm text-apple-blue hover:underline"
              >
                View Source
              </a>
              <button className="ml-auto px-4 py-2 rounded-lg bg-apple-blue text-white text-sm font-medium hover:bg-blue-600 transition-colors">
                Convert to Todo
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function StatCard({ label, value }) {
  return (
    <div className="glass rounded-2xl p-5 shadow-soft">
      <p className="text-apple-gray text-xs font-medium uppercase tracking-wide">{label}</p>
      <p className="text-3xl font-semibold mt-1">{value}</p>
    </div>
  )
}

function EmptyCard({ message }) {
  return (
    <div className="glass rounded-2xl p-6 text-center text-apple-gray text-sm col-span-full">
      {message}
    </div>
  )
}

function PlatformBadge({ platform }) {
  const names = { weibo: 'Weibo', bilibili: 'Bilibili', taptap: 'TapTap', xiaohongshu: '小红书', douyin: '抖音' }
  return (
    <span className="text-xs font-medium text-apple-gray">{names[platform] || platform}</span>
  )
}

function Badge({ children, variant = 'default' }) {
  const styles = {
    default: 'bg-white/10 text-white/80',
    blue: 'bg-apple-blue/20 text-apple-blue',
    green: 'bg-apple-green/20 text-apple-green',
    red: 'bg-apple-red/20 text-apple-red',
    yellow: 'bg-yellow-500/20 text-yellow-400',
  }
  return (
    <span className={`text-xs px-2.5 py-1 rounded-full ${styles[variant] || styles.default}`}>{children}</span>
  )
}

function sentimentColor(score) {
  if (score == null) return 'bg-white/10 text-white/70'
  if (score >= 0.3) return 'bg-apple-green/20 text-apple-green'
  if (score <= -0.3) return 'bg-apple-red/20 text-apple-red'
  return 'bg-yellow-500/20 text-yellow-400'
}

function sentimentLabel(score) {
  if (score == null) return 'Neutral'
  if (score >= 0.3) return 'Positive'
  if (score <= -0.3) return 'Negative'
  return 'Mixed'
}

function sentimentVariant(score) {
  if (score == null) return 'default'
  if (score >= 0.3) return 'green'
  if (score <= -0.3) return 'red'
  return 'yellow'
}

export default App
