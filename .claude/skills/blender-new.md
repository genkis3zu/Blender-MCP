---
name: blender-new
description: 新規3Dモデリングプロジェクトを開始する。要件整理→確認→プロジェクト生成→Blender準備を順序通りに実行する。
---

# BlenderMCP: 新規プロジェクト開始 (STEP 0)

このスキルは新規制作を開始する際に使用する。全ステップを順序通りに実行すること。

## STEP 0-1: 要件整理

ユーザーの入力から以下を抽出し、**確認を返す**。推測で埋めず、不明な点は質問する（最大3件）。

```
[要件整理]
- プロジェクト名: {snake_case で提案}
- 用途: {3dprint / game / architecture / general}
- 概要: {1-2行で要約}
- サイズ/スケール: {数値 + 単位}
- スタイル: {キーワード}
- 制約: {用途に応じた制約を明示}
  - 3dprint: 最小肉厚1.5mm, マニフォールド必須
  - game: 目標ポリゴン数, UV展開要件
  - architecture: 寸法精度, 単位系
```

**必ず「この内容で進めてよいですか？」と確認を求める。承認なしに次へ進まないこと。**

## STEP 0-2: プロジェクト生成（承認後のみ）

```bash
python scripts/new_project.py {project_name} --use-case {use_case}
```

生成されたディレクトリ構成を報告する：
- `projects/{name}/README.md`
- `projects/{name}/models/wip/`
- `projects/{name}/models/final/`
- `projects/{name}/renders/preview/`
- `projects/{name}/renders/final/`
- `projects/{name}/exports/stl/`, `gltf/`, `fbx/`
- `projects/{name}/references/`

## STEP 0-3: Blender準備

以下を順序通りに実行する：

1. **接続確認**: `get_scene_info` を実行してBlender接続を確認
   - 失敗した場合: 「Blenderで Connect to Claude を押してください」と案内
   - 初回失敗は既知の挙動。再試行する
2. **シーン初期化**: `execute_blender_code` で `scripts/init_scene.py` の内容を実行
3. **初期保存**: `execute_blender_code` で以下を実行
   ```python
   bpy.ops.wm.save_as_mainfile(filepath="projects/{name}/models/wip/{name}_v001.blend")
   ```

## STEP 0-4: 制作開始宣言

以下を報告して完了：

```
[プロジェクト開始]
- プロジェクト: projects/{name}/
- 用途: {use_case}
- 初期ファイル: projects/{name}/models/wip/{name}_v001.blend
- 次のステップ: /blender-model でモデリング開始
```

## 禁止事項
- 承認なしにプロジェクト生成に進むこと
- 要件整理をスキップすること
- Blender接続確認を省略すること
- 初期 .blend 保存を忘れること
