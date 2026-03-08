"""子プロジェクト自動生成スクリプト
Usage: python scripts/new_project.py <project_name> [--use-case <type>]

Creates a new child project under projects/<project_name>/ with
standard directory structure and README.md template.
"""
import argparse
import os
import sys

USE_CASE_REQUIREMENTS = {
    "3dprint": {
        "label": "3Dプリント",
        "requirements": [
            "- 最小肉厚: 1.5mm (FDM)",
            "- 非マニフォールド: ゼロ必須",
            "- オーバーハング: 45度以下推奨",
            "- エクスポート: STL (Z-up, メートル単位)",
        ],
    },
    "game": {
        "label": "ゲームアセット",
        "requirements": [
            "- ポリゴン数: キャラ ~5000 / 小物 ~500",
            "- UV展開: 重なりなし",
            "- 原点: 底面中心",
            "- エクスポート: GLB (Y-up, マテリアル埋め込み)",
        ],
    },
    "architecture": {
        "label": "建築・工業モデル",
        "requirements": [
            "- スケール: 1単位 = 1メートル",
            "- 寸法精度: 小数点2桁",
            "- エクスポート: FBX / STL",
        ],
    },
    "general": {
        "label": "汎用",
        "requirements": [
            "- 用途に応じて要件を追記してください",
        ],
    },
}

DIRS = [
    "models/wip",
    "models/final",
    "renders/preview",
    "renders/final",
    "exports/stl",
    "exports/gltf",
    "exports/fbx",
    "references",
]


def create_project(name: str, use_case: str):
    project_root = os.path.join("projects", name)

    if os.path.exists(project_root):
        print(f"ERROR: Project '{name}' already exists at {project_root}")
        sys.exit(1)

    # Create directories
    for d in DIRS:
        path = os.path.join(project_root, d)
        os.makedirs(path, exist_ok=True)
        # Add .gitkeep to empty dirs
        gitkeep = os.path.join(path, ".gitkeep")
        open(gitkeep, "w").close()

    # Generate README.md
    uc = USE_CASE_REQUIREMENTS.get(use_case, USE_CASE_REQUIREMENTS["general"])
    requirements = "\n".join(uc["requirements"])

    readme = f"""# {name}

## 用途
{uc['label']}

## 概要
<!-- 何を作るかを1-3行で記述 -->

## 要件
{requirements}

## ステータス
WIP
"""

    readme_path = os.path.join(project_root, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"Project created: {project_root}/")
    print(f"  Use case: {uc['label']}")
    print(f"  Directories: {len(DIRS)} created")
    print(f"  README: {readme_path}")


def main():
    parser = argparse.ArgumentParser(description="Create a new BlenderMCP child project")
    parser.add_argument("name", help="Project name (snake_case recommended)")
    parser.add_argument(
        "--use-case",
        choices=["3dprint", "game", "architecture", "general"],
        default="general",
        help="Project use case (default: general)",
    )
    args = parser.parse_args()
    create_project(args.name, args.use_case)


if __name__ == "__main__":
    main()
