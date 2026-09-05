# SDLC — work intake

Turn issues or external PRs into verified, correctly-routed work. Remote tracker changes require explicit confirmation.

## States

Exactly one kind: `bug | enhancement`. Exactly one state:

| State | Meaning |
|---|---|
| needs-triage | Maintainer decision pending |
| needs-info | Waiting for specific reporter facts |
| ready-for-agent | Verified and fully specified for AFK execution |
| ready-for-human | Requires judgement, access, or manual verification |
| wontfix | Already exists or consciously rejected |

Conflicting states → ask before acting.

## Intake

1. Read the full body, comments, labels, author, dates; PR includes diff. Parse prior notes — never re-ask resolved questions.
2. Search by domain concept for an existing implementation; cite where. Check prior ADR/rejection records.
3. Recommend kind + state + why; wait for direction.
4. Verify before grill: bug → reproduce; PR → test its claim. Report `confirmed | failed | insufficient detail` with evidence.
5. Grill only unresolved decisions. Sharpen glossary and record durable choices by normal gates.

## Outcome

- `ready-for-agent`: attach a brief with context, verified evidence, exact outcome/DoD, constraints, scope, and links.
- `ready-for-human`: same, plus why AFK execution is unsafe.
- `needs-info`: established facts + specific unanswered questions. Never “please provide more info”.
- `wontfix`: already implemented → cite it; rejected → reason + durable rejection only if future intake must know.

Quick maintainer override is allowed after confirming remote mutations. Offer a brief before `ready-for-agent` if none exists.
