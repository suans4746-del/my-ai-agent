# Pia Notes

## Task
Verify the GameInsight crawler framework and documentation.

## Files to Check
- crawler/main.py
- crawler/requirements.txt
- README.md
- PRD.md
- docs/designer-manual.md

## Deliverables Expected (per M1)
1. Python Playwright crawler skeleton with platform modules
2. 5 platform stubs (Weibo, Bilibili, TapTap, Xiaohongshu, Douyin)
3. Rate limiting (5s between platforms)
4. Data anonymization (author_hash)
5. README with setup instructions
6. PRD and designer manual present

## Checklist
- [ ] Python script imports successfully
- [ ] All 5 platform functions exist as stubs
- [ ] run_all() iterates through all platforms
- [ ] 5-second sleep between platforms (rate limiting)
- [ ] save_feed() hashes author for anonymization
- [ ] get_db() connects to shared SQLite database
- [ ] requirements.txt has needed packages
- [ ] README has complete setup instructions
- [ ] PRD.md exists and is meaningful
- [ ] designer-manual.md exists and is meaningful
