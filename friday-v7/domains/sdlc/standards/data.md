# Data

Load when Design Data is `required` or a work-item touches schema.

Both layers, v7 paths: `04 - Data/01 - Model/` (`data-model`) and `04 - Data/02 - Dictionary/` (`data-dict`). Model = concepts/invariants. Dict = columns/types/keys + one-line meaning (units/enum).

Migrations / ORM are runtime SoT if they disagree — patch the vault to match or mark drift. Do not fork a second schema in Design prose.

No database in scope → do not write these files.
