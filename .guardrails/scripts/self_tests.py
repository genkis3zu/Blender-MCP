#!/usr/bin/env python3
import sys, os, yaml

REQUIRED = [
    ".guardrails/checklist.md",
    ".guardrails/claude_meta.md",
    ".guardrails/codex_meta.md",
    ".guardrails/config.yaml",
    ".guardrails/metrics.yaml",
    ".guardrails/role.md",
    ".guardrails/glossary.md",
    ".guardrails/system_architecture.md",
]

def must_exist():
    missing = [p for p in REQUIRED if not os.path.exists(p)]
    if missing:
        print("MISSING:", ", ".join(missing))
        return False
    return True

def checklist_format_ok():
    txt = open(".guardrails/checklist.md", encoding="utf-8").read()
    required_keywords = [
        "Context Block",
        "get_scene_info",
        "get_viewport_screenshot",
        "snake_case",
        "質問は最大3件",
    ]
    ok = all(k in txt for k in required_keywords)
    if not ok:
        print("CHECKLIST weak: required keyword not found")
    return ok

def config_yaml_ok():
    try:
        yaml.safe_load(open(".guardrails/config.yaml", encoding="utf-8"))
        return True
    except Exception as e:
        print("CONFIG YAML invalid:", e)
        return False

def project_structure_ok():
    dirs = ["prompts", "scripts", "models/wip", "models/final",
            "renders/preview", "renders/final",
            "exports/stl", "exports/gltf", "exports/fbx"]
    missing = [d for d in dirs if not os.path.isdir(d)]
    if missing:
        print("MISSING DIRS:", ", ".join(missing))
        return False
    return True

if __name__ == "__main__":
    ok = must_exist() and checklist_format_ok() and config_yaml_ok() and project_structure_ok()
    sys.exit(0 if ok else 1)
