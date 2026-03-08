# Glossary / Naming Rules — BlenderMCP

## ブランチ・コミット
- main ブランチ：`main` 固定
- commit 規約：Conventional Commits（feat/fix/docs/chore...）
- PR ラベル例：model, script, docs, guardrail

## 命名規則
- オブジェクト名：英語 snake_case（例: `main_body`, `left_arm`, `top_plate`）
- マテリアル名：用途_色（例: `body_red`, `metal_silver`, `glass_clear`）
- バージョン：`_v001`, `_v002`, `_v003`...
- スクリプト名：動詞_対象（例: `init_scene.py`, `export_stl.py`）

## 単位・座標系
- 単位：メートル（Blenderデフォルト）
- 原点：`(0, 0, 0)` を基準に配置
- Z-up（Blender標準）、エクスポート時に Y-up 変換（GLB等）

## MCP用語
- MCP: Model Context Protocol
- bpy: Blender Python API
- プリミティブ: Cube / Sphere / Cylinder / Cone / Torus
- マニフォールド: 閉じた水密メッシュ（3Dプリント必須条件）

## ファイル配置
- プロンプトテンプレート: `prompts/`
- bpyスクリプト: `scripts/`
- 作業中モデル: `models/wip/`
- 完成モデル: `models/final/`
- プレビュー画像: `renders/preview/`
- 最終レンダリング: `renders/final/`
- エクスポート: `exports/stl/`, `exports/gltf/`, `exports/fbx/`

## エクスポート形式
- STL: 3Dプリント用（Z-up、メートル単位）
- GLB: ゲーム/Web用（Y-up、マテリアル埋め込み）
- FBX: 汎用（他ソフトとの連携）
