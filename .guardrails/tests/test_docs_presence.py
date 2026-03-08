import os

def test_required_docs_exist():
    for p in ["CLAUDE.md", "blendermcp_spec.md", ".mcp.json"]:
        assert os.path.exists(p), f"missing required doc: {p}"

def test_project_directories_exist():
    dirs = [
        "prompts", "scripts",
        "models/wip", "models/final",
        "renders/preview", "renders/final",
        "exports/stl", "exports/gltf", "exports/fbx",
    ]
    for d in dirs:
        assert os.path.isdir(d), f"missing required directory: {d}"
