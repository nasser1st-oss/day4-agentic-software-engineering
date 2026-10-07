"""Lab 4.3 — performance test harness.
Runs a fixed question set against the agent, scores answers against
ground truth computed from the CSV, and writes performance_report.md
with accuracy, latency percentiles and token efficiency.

Usage:  python perf_test.py            (tests the guarded agent)
"""
import csv, json, statistics, time
import guarded_agent as agent_mod

with open("maintenance_assets.csv", newline="") as f:
    ASSETS = list(csv.DictReader(f))

flagged = [a for a in ASSETS if a["status"] == "Flagged for Inspection"]
high = [a for a in ASSETS if a["criticality"] == "High"]
jubail_flagged = [a for a in flagged if a["location"] == "Jubail Complex"]

# Ground truth is COMPUTED, not hardcoded — survives dataset edits.
QUESTIONS = [
    ("How many assets are flagged for inspection?",
     [str(len(flagged))]),
    ("List the asset ids that are flagged for inspection in Jubail Complex.",
     [a["asset_id"] for a in jubail_flagged] or ["no", "none"]),
    ("How many high-criticality assets do we have in total?",
     [str(len(high))]),
    ("Is asset PMP-1002 in service, on standby, or something else?",
     [ASSETS[1]["status"].lower()]),
    ("Which locations appear in our asset register?",
     ["Riyadh", "Jubail", "Yanbu"]),
]

results, latencies, tok_in, tok_out = [], [], [], []
orig_create = agent_mod.client.chat.completions.create
usage_box = {}


def counting_create(*args, **kwargs):
    r = orig_create(*args, **kwargs)
    u = getattr(r, "usage", None)
    if u:
        usage_box["p"] = usage_box.get("p", 0) + u.prompt_tokens
        usage_box["c"] = usage_box.get("c", 0) + u.completion_tokens
    return r


agent_mod.client.chat.completions.create = counting_create

for q, expected in QUESTIONS:
    usage_box.clear()
    t0 = time.time()
    try:
        answer = agent_mod.run_agent(q)
        err = None
    except Exception as e:
        answer, err = "", str(e)
    dt = round(time.time() - t0, 2)
    ok = any(str(e).lower() in (answer or "").lower() for e in expected)
    latencies.append(dt)
    tok_in.append(usage_box.get("p", 0))
    tok_out.append(usage_box.get("c", 0))
    results.append({"q": q, "expected_any": expected, "ok": ok,
                    "latency_s": dt, "tokens": usage_box.get("p", 0)
                    + usage_box.get("c", 0), "answer": (answer or "")[:200],
                    "error": err})
    print(f"{'PASS' if ok else 'FAIL'}  {dt:>5}s  {q}")

acc = sum(r["ok"] for r in results) / len(results)
lat_sorted = sorted(latencies)
p50 = statistics.median(lat_sorted)
p95 = lat_sorted[max(0, round(0.95 * len(lat_sorted)) - 1)]
total_tok = sum(tok_in) + sum(tok_out)

lines = ["# Performance Evaluation Report — Guarded Agent\n",
         f"Questions: {len(QUESTIONS)} | Model: {agent_mod.MODEL}\n",
         "| Metric | Value |", "|---|---|",
         f"| Task success rate | {acc:.0%} |",
         f"| Latency p50 | {p50:.1f} s |",
         f"| Latency p95 | {p95:.1f} s |",
         f"| Tokens per task (avg) | {total_tok // len(QUESTIONS)} |",
         f"| Total tokens | {total_tok} |",
         "", "## Per-question results", "",
         "| OK | Latency | Tokens | Question |", "|---|---|---|---|"]
for r in results:
    lines.append(f"| {'PASS' if r['ok'] else 'FAIL'} | {r['latency_s']} s "
                 f"| {r['tokens']} | {r['q']} |")
lines += ["", "## Trace analysis (fill in)", "",
          "- Slowest step per question (from audit.jsonl): ",
          "- Unnecessary tool calls observed: ",
          "- One optimization to try, and the metric it should move: "]
with open("performance_report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
json.dump(results, open("perf_results.json", "w"), indent=2)
print("\nWrote performance_report.md and perf_results.json")
