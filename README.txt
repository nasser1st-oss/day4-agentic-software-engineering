Day 4 Student Pack — Agentic Software Engineering
==================================================
Inputs from previous days: .env (OpenRouter key), maintenance_assets.csv,
your Day 1 agent.py (baseline for Lab 4.2).

Lab 4.1 (needs a GitHub account):
  1. Create a new GitHub repo; push your Day 2 scaffold_out/ project.
  2. Copy .github/ from this pack into the repo root; commit & push.
  3. Repo Settings > Secrets and variables > Actions:
     add OPENROUTER_API_KEY.
  4. Branch, change a .py file WITHOUT touching tests, open a PR.
  5. Watch Actions run; read the agent's review comment on the PR.

Lab 4.2:
  1. python guarded_agent.py   (keep Day 1 agent.py as the baseline)
  2. Instructor hands out probe scenarios in class.
  3. Record results in findings_report.md; harden; re-test.

Lab 4.3:
  python perf_test.py   -> performance_report.md + perf_results.json
