#!/usr/bin/env python3
import argparse, json, yaml, re, os
from datetime import datetime, timedelta
from util import commit_msgs_since, changed_files_since, count_files_in

def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=".guardrails/config.yaml")
    ap.add_argument("--spec", default=".guardrails/metrics.yaml")
    args = ap.parse_args()

    cfg = load_yaml(args.config)
    spec = load_yaml(args.spec)
    days = cfg["metrics_window_days"]
    msgs = commit_msgs_since(days)
    files = changed_files_since(days)

    docs_files = set(cfg["paths"]["docs_files"])
    conv_re = re.compile(cfg["naming"]["conventional_regex"])
    guardrail_prefix = cfg["naming"]["guardrail_commit_prefix"]

    # docs_update_rate
    code_commits = max(len(msgs), 1)
    docs_changed = sum(1 for f in files if f in docs_files)
    docs_update_rate = min(docs_changed / code_commits, 1.0)

    # conventional_commits_ratio
    conv_hits = sum(1 for m in msgs if conv_re.match(m or ""))
    conv_ratio = conv_hits / max(len(msgs), 1)

    # guardrail_commit_count
    gr_count = sum(1 for m in msgs if m.startswith(guardrail_prefix))

    # script_reuse_count
    script_count = count_files_in("scripts", ".py")

    # model_version_count
    model_count = count_files_in("models/wip", ".blend")

    result = {
        "window_days": days,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "metrics": {
            "docs_update_rate": round(docs_update_rate, 3),
            "conventional_commits_ratio": round(conv_ratio, 3),
            "guardrail_commit_count": gr_count,
            "script_reuse_count": script_count,
            "model_version_count": model_count,
        },
        "thresholds": cfg["thresholds"],
    }

    # 判定
    verdict = []
    thr = cfg["thresholds"]
    if result["metrics"]["docs_update_rate"] < thr["docs_update_rate_min"]:
        verdict.append("docs_update_rate below threshold")
    if result["metrics"]["conventional_commits_ratio"] < thr["conventional_commits_ratio_min"]:
        verdict.append("conventional_commits ratio low")

    result["verdict"] = "NG" if verdict else "OK"
    result["notes"] = verdict

    # 出力
    out_json = spec["report"]["out_json"]
    out_md = spec["report"]["out_md"]
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    open(out_json, "w", encoding="utf-8").write(
        json.dumps(result, ensure_ascii=False, indent=2)
    )

    md = [
        f"# Guardrail Metrics ({days}d)",
        f"- generated: {result['generated_at']}",
        f"- verdict: **{result['verdict']}**",
        "## numbers",
        *[f"- {k}: {v}" for k, v in result["metrics"].items()],
        "## notes" if verdict else "## notes\n- none",
    ]
    open(out_md, "w", encoding="utf-8").write("\n".join(md))
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
