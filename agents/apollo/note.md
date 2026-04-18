# Apollo Notes

## Current Phase: VERIFICATION of M1

## M1 Deliverables to Verify
1. Backend Express server with SQLite schema (feeds, insights, todos, weekly_reports)
2. Frontend React + Tailwind setup with Apple-style base layout (sidebar + main area)
3. Python Playwright crawler skeleton with platform modules
4. README and docs updated with setup instructions

## Team
- Nina — Backend & Database Verifier
- Oscar — Frontend & UI Verifier
- Pia — Crawler & Documentation Verifier

## My Preliminary Checks (done before scheduling workers)
- ✅ Backend starts on port 3002, all API endpoints respond correctly
- ✅ Frontend builds successfully (vite build completes, dist/ generated)
- ✅ Database schema creates all 4 tables with proper columns and foreign keys
- ✅ Crawler Python imports and runs, saves to shared DB, all 5 platform stubs exist
- ✅ README, PRD.md, designer-manual.md all present

## Issues Found So Far
1. **Missing `glass` class in built CSS?** Need Oscar to verify the glass effect actually renders.
2. **Crawler stubs are pure placeholders** — but M1 only requires "skeleton with platform modules", so this may be acceptable for M1.
3. **Backend `POST /api/crawl` is a pure placeholder** — returns `{queued: true}` but doesn't actually trigger the crawler. Need to check if M1 requires actual crawl triggering.

## M1 Spec Check
Per roadmap: "Backend Express server with SQLite schema", "Frontend React + Tailwind setup with Apple-style base layout", "Python Playwright crawler skeleton with platform modules", "README and docs updated". The word "skeleton" suggests stubs are acceptable for M1.

## Decision Pending
Wait for worker reports before making final verdict.
