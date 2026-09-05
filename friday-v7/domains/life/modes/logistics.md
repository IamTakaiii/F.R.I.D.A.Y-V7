# Life — logistics

Travel planning: itinerary, bookings, visas, transport, lodging, budget snapshot, packing, and backup choices.

The trip hub is `trip-plan`. Read or create it first; it holds the current route through the trip, not every transaction or task detail.

## Truth rules

- Booking status is `open | held | confirmed | cancelled`; only `confirmed` with cited evidence. Never invent confirmation numbers, schedules, opening hours, prices, or visa rules.
- Label estimates `Assumed`; record currency and date checked. Time-sensitive facts need a source and checked date.
- Include transit and recovery buffer; an itinerary with no feasible movement time is not done.
- Every high-impact risk has a trigger, backup, and decision deadline.

## Persist

`trip-plan` is the canonical trip card at `01 - Plan/Trip - <slug>.md`. Long execution lists → `personal-tasks`; transactions → `personal-budget`; heavy risk register → `personal-risk`. Link them from the trip plan; do not duplicate their rows.

Done: dates/bases coherent · open booking deadlines owned · budget snapshot reconciles · backup named · path cited.
