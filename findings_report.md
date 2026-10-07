# Lab 4.2 — Red-Team Findings Report  (template)

Pair: ______________   Date: ______________

## 1. Attack surface map (before testing)
| # | Untrusted input path | Reaches the model as | Worst realistic outcome |
|---|---|---|---|
| 1 | User question | user message | |
| 2 | CSV `notes` field via search results | tool result | |
| 3 | | | |

## 2. Probe results (scenarios provided by the instructor)
| # | Scenario id | Baseline agent result | Guarded agent result | Rail that blocked it |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

Blocked rate — baseline: ____ / ____     guarded: ____ / ____

## 3. What still got through, and the fix applied
- Finding:
- Rail strengthened (file/line):
- Re-test result:

## 4. Response runbook (if this were production)
- [ ] Kill switch: delete/rotate the API key at openrouter.ai/keys
- [ ] Preserve audit.jsonl before any restart
- [ ] Identify blast radius from the audit trail (which tools ran?)
- [ ] Root cause -> new rail or policy entry -> regression probe added
- Owner on call: ______________
