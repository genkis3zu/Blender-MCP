# System Architecture (v1.0.0)

## Overview

BlenderMCP × Claude Code 3Dモデリング環境のシステムアーキテクチャ。
Claude Code から MCP Protocol 経由で Blender を操作する。

---

## 1. Communication Flow

```
Claude Code (VSCode)
│
│  自然言語で指示（例：「ドラゴンのモデルを作って」）
│
▼
[Claude Code] MCPツールを選択・実行
│
│ MCP Protocol
▼
uvx blender-mcp（MCPサーバー）
│
│ TCP Socket（localhost:9876）
▼
Blender + addon.py
bpyスクリプト実行 → シーンに反映 → 結果返却
```

---

## 2. MCP Tools (v1.5.5)

| ツール名 | 説明 | カテゴリ |
|----------|------|----------|
| `get_scene_info` | シーン内のオブジェクト・カメラ・ライト情報を取得 | 情報取得 |
| `get_object_info` | 指定オブジェクトの詳細（位置・マテリアル・頂点数） | 情報取得 |
| `get_viewport_screenshot` | ビューポートのスクリーンショットを取得 | 情報取得 |
| `get_render_result` | レンダリング結果画像を取得 | 情報取得 |
| `create_object` | 基本プリミティブ生成（Cube/Sphere/Cylinder/Cone/Torus） | 操作 |
| `modify_object` | 位置・回転・スケール・名前を変更 | 操作 |
| `delete_object` | オブジェクトを削除 | 操作 |
| `set_material` | マテリアル作成・割り当て（色・Metallic・Roughness） | 操作 |
| `execute_blender_code` | 任意のBlender Pythonコードを直接実行（最汎用） | 操作 |
| `render_scene` | シーンをレンダリングして画像保存 | 出力 |
| `search_sketchfab_models` | Sketchfabからモデル検索・ダウンロード | 外部連携 |
| `get_polyhaven_asset` | Poly HavenからHDRI/テクスチャ/モデル取得 | 外部連携 |
| `generate_hyper3d_model` | Hyper3D RodinでAI生成3Dモデル作成 | 外部連携 |

> ⚠️ `execute_blender_code` は任意コードを実行できる。使用前に `.blend` を保存すること。

---

## 3. Project Directory Structure

```
blender-mcp/
├── .mcp.json                   # BlenderMCP 接続設定
├── CLAUDE.md                   # Claude Code への常設指示書
├── blendermcp_spec.md          # 仕様書（日本語）
├── .guardrails/                # AI行動規範・チェックリスト
│
├── prompts/                    # プロンプトテンプレート集
│   ├── 01_scene_setup.md
│   ├── 02_modeling.md
│   ├── 03_materials.md
│   ├── 04_lighting.md
│   └── 05_export.md
│
├── scripts/                    # 再利用bpyスクリプト
│   ├── init_scene.py
│   ├── setup_lighting.py
│   ├── export_stl.py
│   └── export_gltf.py
│
├── models/                     # .blend ファイル
│   ├── wip/                    # 作業中（v001, v002...）
│   └── final/                  # 完成版
│
├── renders/                    # レンダリング出力
│   ├── preview/
│   └── final/
│
└── exports/                    # エクスポートファイル
    ├── stl/                    # 3Dプリント用
    ├── gltf/                   # ゲーム/Web用
    └── fbx/                    # 汎用
```

---

## 4. Standard Workflow

```
STEP 1: シーン確認・初期化
  └─ get_scene_info → 状態把握
       │
STEP 2: 大まかな形を作る
  └─ create_object → プリミティブ配置
       │
STEP 3: 形状の調整
  └─ modify_object / execute_blender_code → 変形・モディファイア
       │
STEP 4: マテリアル・ライト設定
  └─ set_material / execute_blender_code → 質感・照明
       │
STEP 5: ビューポート確認
  └─ get_viewport_screenshot → 確認 → NG なら STEP 2〜4 に戻る
       │
STEP 6: レンダリング・エクスポート
  └─ render_scene → exports/ に出力
```

---

## 5. Key Constraints

- **1指示 = 1操作**: まとめて指示すると失敗しやすい
- **初回コマンド失敗**: 既知の挙動。2回目以降は正常動作
- **ロールバック**: `Ctrl+Z` より `.blend` ファイルからのリロードが確実
- **単位**: メートル（Blenderデフォルト）、原点 `(0,0,0)` 基準
- **接続前提**: Blender側で「Connect to Claude」を押してから使用
