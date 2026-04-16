import express from 'express';
import cors from 'cors';
import path from 'path';
import db from './db.js';

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Health check
app.get('/api/health', (req, res) => {
  res.json({ ok: true });
});

// Dashboard stats
app.get('/api/stats', (req, res) => {
  const feeds = db.prepare('SELECT COUNT(*) as count FROM feeds').get();
  const insights = db.prepare('SELECT COUNT(*) as count FROM insights').get();
  const todos = db.prepare("SELECT COUNT(*) as count FROM todos WHERE status != 'done'").get();
  res.json({ feeds: feeds.count, insights: insights.count, pendingTodos: todos.count });
});

// Weekly top insights
app.get('/api/insights/top', (req, res) => {
  const rows = db.prepare(`
    SELECT i.*, f.platform, f.url
    FROM insights i
    JOIN feeds f ON i.feed_id = f.id
    ORDER BY i.ai_analyzed_at DESC
    LIMIT 10
  `).all();
  res.json(rows);
});

// Insight categories summary
app.get('/api/insights/categories', (req, res) => {
  const rows = db.prepare(`
    SELECT category, COUNT(*) as count
    FROM insights
    GROUP BY category
  `).all();
  res.json(rows);
});

// Todos
app.get('/api/todos', (req, res) => {
  const rows = db.prepare(`
    SELECT t.*, i.summary as insight_summary
    FROM todos t
    LEFT JOIN insights i ON t.insight_id = i.id
    ORDER BY t.created_at DESC
  `).all();
  res.json(rows);
});

app.post('/api/todos', (req, res) => {
  const { insight_id, title, notes, priority } = req.body;
  const result = db.prepare(
    'INSERT INTO todos (insight_id, title, notes, priority) VALUES (?, ?, ?, ?)'
  ).run(insight_id || null, title, notes || '', priority || 'medium');
  res.json({ id: result.lastInsertRowid });
});

app.patch('/api/todos/:id', (req, res) => {
  const { status } = req.body;
  db.prepare("UPDATE todos SET status = ?, updated_at = datetime('now') WHERE id = ?")
    .run(status, req.params.id);
  res.json({ success: true });
});

// Trigger crawl (placeholder - calls crawler later)
app.post('/api/crawl', (req, res) => {
  res.json({ queued: true, message: 'Crawl job queued' });
});

// Weekly report
app.get('/api/reports/latest', (req, res) => {
  const report = db.prepare('SELECT * FROM weekly_reports ORDER BY generated_at DESC LIMIT 1').get();
  res.json(report || null);
});

// Serve built frontend
const frontendDist = path.join(process.cwd(), '..', 'frontend', 'dist');
app.use(express.static(frontendDist));
app.get('*', (req, res) => {
  res.sendFile(path.join(frontendDist, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`GameInsight backend listening on http://localhost:${PORT}`);
});
