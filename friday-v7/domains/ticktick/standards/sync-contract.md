# TickTick sync contract

Vault owns roadmap, source identity, Goal. TickTick owns dates, reminders, recurrence, priority, working checklist.

Project lists map 1:1 by persisted TickTick ID. Areas (`Home`, `Health`, `Finance & Admin`) are TickTick-only unless linked.

Queue default 5. Session-sized tasks (45–120m), not 1:1 with every Vault row. Extra IDs go in `ID:` + checklist. Each Vault ID on at most one TickTick task.

Preview before sync, bulk, schedule, archive, abandon, delete. Auth missing = blocker; never claim a partial mutation succeeded.
