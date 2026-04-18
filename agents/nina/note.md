# Nina Notes

## Task
Verify the GameInsight backend: Express server, SQLite schema, API endpoints, and database integrity.

## Files to Check
- backend/server.js
- backend/db.js
- backend/package.json

## Deliverables Expected (per M1)
1. Backend Express server with SQLite schema (feeds, insights, todos, weekly_reports)
2. All REST API endpoints working
3. Proper error handling
4. Database foreign keys and constraints

## Checklist
- [ ] Schema has all 4 tables: feeds, insights, todos, weekly_reports
- [ ] feeds table has correct columns
- [ ] insights table has correct columns with foreign key to feeds
- [ ] todos table has correct columns with foreign key to insights
- [ ] weekly_reports table has correct columns
- [ ] All API endpoints exist and return correct data
- [ ] Backend serves built frontend correctly
- [ ] Database uses WAL mode and foreign keys enabled
