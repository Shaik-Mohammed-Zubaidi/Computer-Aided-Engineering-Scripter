"""
harness.py  – evaluate natural-language→Abaqus agent.

• Reads prompts from prompts.csv
• Generates code with generate_abaqus_script()
• Executes each script with `abaqus cae noGUI=...`
• Records:
    ─ success / fail (exit-code & ***ERROR scan)
    ─ wall-clock latency (generation + execution)
    ─ token cost (if OpenAI responses include usage)
Outputs results.csv + summary.json
"""
import csv, json, subprocess, tempfile, time, pathlib, re
from agent import generate_abaqus_script        # your function

PROMPTS_CSV = "prompts.csv"
RESULTS_CSV = "results.csv"
SUMMARY_JSON = "summary.json"
ABAQUS = ["abaqus", "cae", "noGUI="]           # tweak path if needed

def run_script(code: str) -> bool:
    """Return True if script executes without ABAQUS errors."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
    cp = subprocess.run(ABAQUS + [tmp.name],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, timeout=300)
    ok = cp.returncode == 0 and "***ERROR" not in cp.stdout
    pathlib.Path(tmp.name).unlink(missing_ok=True)
    return ok

def main():
    rows, passes, total, gen_secs, exe_secs = [], 0, 0, 0.0, 0.0
    with open(PROMPTS_CSV, newline="") as fp:
        reader = csv.reader(fp)
        for prompt, intent in reader:          # intent column is free-text description
            total += 1
            t0 = time.perf_counter()
            code = generate_abaqus_script(prompt)
            gen_secs += time.perf_counter() - t0

            t1 = time.perf_counter()
            success = run_script(code)
            exe_secs += time.perf_counter() - t1

            passes += success
            rows.append({"prompt": prompt, "intent": intent, "success": success})

    # write results
    with open(RESULTS_CSV, "w", newline="") as fp:
        csv.DictWriter(fp, fieldnames=rows[0].keys()).writerows(rows)

    summary = {
        "total": total,
        "passed": passes,
        "pass_rate": passes / total,
        "avg_gen_latency_s": gen_secs / total,
        "avg_exec_latency_s": exe_secs / total,
    }
    json.dump(summary, open(SUMMARY_JSON, "w"), indent=2)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
