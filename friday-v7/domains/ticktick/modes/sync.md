# TickTick — sync

One mapped project by default. All projects only when explicit. Missing mapping → setup.

Compare Vault sources vs TickTick. Validate source keys, coverage (one Vault ID ≤ one task), session-size, queue cap.

Dry-run groups: Create · Refresh Goal · Complete · Abandon · Conflict · No-op. Apply only the approved non-conflict set. Unique `sortOrder`. Failed TickTick write blocks its Vault patch.

No full-backlog mirror, delete, auto-reopen, or title overwrite.
