# BlenderMCP × Claude Code 3Dモデリング仕様書

> **対象リポジトリ**: [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) v1.5.5  
> **前提**: Blender側のAddon（addon.py）は設定済み・接続ポート: `9876`

---

## 目次

1. [アーキテクチャ概要](#1-アーキテクチャ概要)
2. [Claude Code 接続設定](#2-claude-code-接続設定)
3. [ディレクトリ・ファイル構成](#3-ディレクトリファイル構成)
4. [標準ワークフロー](#4-標準ワークフロー)
5. [プロンプト集](#5-プロンプト集)
6. [用途別チェックリスト](#6-用途別チェックリスト)
7. [トラブルシューティング](#7-トラブルシューティング)

---

## 1. アーキテクチャ概要

### 1.1 通信フロー

```
VSCode + Claude Code
│
│  「ドラゴンがいるダンジョンシーンを作って」
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

### 1.2 MCPツール一覧（v1.5.5）

| ツール名 | 説明 |
|---|---|
| `get_scene_info` | シーン内のオブジェクト・カメラ・ライト情報を取得 |
| `get_object_info` | 指定オブジェクトの詳細（位置・マテリアル・頂点数など） |
| `execute_blender_code` | 任意のBlender Pythonコードを直接実行（最汎用） |
| `create_object` | 基本プリミティブ（Cube/Sphere/Cylinder/Cone/Torus等）を生成 |
| `modify_object` | 位置・回転・スケール・名前を変更 |
| `delete_object` | オブジェクトを削除 |
| `set_material` | マテリアルを作成・割り当て（色・Metallic・Roughness） |
| `render_scene` | シーンをレンダリングして画像保存 |
| `get_render_result` | レンダリング結果画像を取得・表示 |
| `get_viewport_screenshot` | Blenderビューポートのスクリーンショットを取得 |
| `search_sketchfab_models` | Sketchfabからモデルを検索・ダウンロード |
| `get_polyhaven_asset` | Poly HavenからHDRI/テクスチャ/モデルを取得 |
| `generate_hyper3d_model` | Hyper3D RodinでAI生成3Dモデルを作成 |

> ⚠️ `execute_blender_code` は任意コードを実行できる強力なツール。実行前に必ず `.blend` を保存すること。

---

## 2. Claude Code 接続設定

### 2.1 Claude Code CLI（推奨・1行で完了）

```bash
claude mcp add blender uvx blender-mcp
```

### 2.2 .mcp.json（プロジェクト単位の設定）

プロジェクトルートに `.mcp.json` を作成する。

**Windows**
```json
{
  "mcpServers": {
    "blender": {
      "command": "cmd",
      "args": ["/c", "uvx", "blender-mcp"]
    }
  }
}
```

**Mac / Linux**
```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    }
  }
}
```

**テレメトリを無効にする場合**
```json
{
  "mcpServers": {
    "blender": {
      "command": "cmd",
      "args": ["/c", "uvx", "blender-mcp"],
      "env": { "DISABLE_TELEMETRY": "true" }
    }
  }
}
```

> ⚠️ `uv` が未インストールの場合、先にインストールすること。  
> Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` を実行後、PATHを通す。

### 2.3 接続確認

Blenderで **「Connect to Claude」** を押してから Claude Code に入力：

```
現在のBlenderシーンの情報を教えて
```

🔨 ハンマーアイコンが表示され、シーン情報が返ってくれば接続成功。

> 💡 最初のコマンドが失敗することがある（既知の挙動）。2回目以降は正常に動く。

---

## 3. ディレクトリ・ファイル構成

### 3.1 推奨プロジェクト構造

```
my-3d-project/
├── .mcp.json                   # BlenderMCP 接続設定
├── CLAUDE.md                   # Claude Code への常設指示書 ★重要
├── README.md
│
├── prompts/                    # プロンプトテンプレート集（コピペ用）
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
└── exports/                    # 最終エクスポートファイル
    ├── stl/                    # 3Dプリント用
    ├── gltf/                   # ゲーム用
    └── fbx/                    # 汎用
```

### 3.2 CLAUDE.md テンプレート

> プロジェクトルートに置くと Claude Code が毎回自動で読み込む。  
> 用途に合わせて書き換えて使う。

```markdown
# プロジェクト概要
このプロジェクトは [作るものの説明] を制作するための3Dモデリング環境。

# ツール
- BlenderMCPを使ってBlenderを操作する（localhost:9876）
- 操作前に必ずget_scene_infoで現在の状態を確認すること
- 複雑な操作はexecute_blender_codeを使う

# 命名規則
- オブジェクト名：英語スネークケース（例: main_body, left_arm）
- マテリアル名：用途_色（例: body_red, metal_silver）

# 単位・スケール
- 単位：メートル（Blenderデフォルト）
- 原点(0,0,0)を基準に配置

# 保存ルール
- 作業の節目ごとに models/wip/ にバージョン番号付きで保存
- 例: models/wip/model_v001.blend

# 用途固有のルール（3Dプリントの場合は以下を追加）
# - 最小肉厚 1.5mm 厳守
# - 非マニフォールドエッジは修正してからエクスポート
# - エクスポート先: exports/stl/
```

---

## 4. 標準ワークフロー

```
STEP 1: シーン確認・初期化
  └─ 「現在のシーン情報を確認して」
  └─ 「シーンをクリアして作業環境を整えて」
       │
       ▼
STEP 2: 大まかな形を作る
  └─ 「胴体になる円柱を追加して」
  └─ 「頭部に球体を乗せて」
       │
       ▼
STEP 3: 形状の調整
  └─ 「上部を少し細くして」
  └─ 「Subdivisionを追加してなめらかに」
       │
       ▼
STEP 4: マテリアル・ライト設定
  └─ 「光沢のある赤色マテリアルを設定して」
  └─ 「スタジオ照明を設定して」
       │
       ▼
STEP 5: ビューポート確認
  └─ 「ビューポートのスクリーンショットを撮って」
       │
  確認OK? ─── NG → STEP 2〜4 に戻る
       │ OK
       ▼
STEP 6: レンダリング・エクスポート
  └─ 「renders/final/ にレンダリング保存して」
  └─ 「exports/stl/ に STL でエクスポートして」
```

**イテレーションのコツ**
- 1指示 = 1操作を基本にする（まとめて指示すると失敗しやすい）
- 迷ったら `get_viewport_screenshot` でビジュアル確認してから次の指示
- うまくいった操作はすぐ `scripts/` にスクリプトとして保存
- 失敗したら「元に戻して」より「`models/wip/xxx.blend` からリロードして」の方が確実

---

## 5. プロンプト集

> `[ ]` の部分を書き換えて使う。そのままコピペでも動く。

### 5.1 シーン管理

**シーン確認**
```
現在のBlenderシーンの情報を取得して。オブジェクト名・位置・マテリアルを一覧で教えて。
```

**シーン初期化**
```
Blenderシーンを初期化してください。
デフォルトのCube・ライト・カメラをすべて削除して、
単位系をメートル、グリッドスケールを1.0に設定してください。
```

**ビューポート確認**
```
現在のBlenderビューポートのスクリーンショットを撮って見せて。
```

---

### 5.2 オブジェクト操作

**オブジェクトを追加する**
```
以下のオブジェクトを追加してください：
・種類：[Cube / Sphere / Cylinder / Cone / Torus]
・位置：([X], [Y], [Z])
・サイズ：半径 [N] m
・名前：[object_name]
```

**複数オブジェクトを整列配置する**
```
[object_name] と同じオブジェクトを [N] 個、
[X/Y/Z] 軸方向に [間隔]m 間隔で並べてください。
名前は [prefix]_001, _002, _003... とつけてください。
```

**形状を変形する**
```
[object_name] の形状を以下のように変形してください：
・上部を [N]% 縮小してなだらかな丸みを持たせる
・Subdivision Surface モディファイアをレベル2で追加してスムーズに見せる
execute_blender_code を使って実行してください。
```

**オブジェクトを結合する**
```
[object_name_1] と [object_name_2] を結合して1つのメッシュにしてください。
結合後の名前は [new_name] にしてください。
```

---

### 5.3 マテリアル設定

**基本マテリアル**
```
[object_name] にマテリアルを設定してください：
・ベースカラー：[色名 または #RRGGBB]
・メタリック：[0.0〜1.0]（1.0=金属）
・ラフネス：[0.0〜1.0]（0.0=光沢あり、1.0=マット）
・マテリアル名：[mat_name]
```

**複数オブジェクトに一括適用**
```
シーン内の以下のオブジェクト全てに [mat_name] を適用してください：
[object_1], [object_2], [object_3]
```

**Poly Havenのテクスチャを使う**（要: Poly Haven有効化）
```
Poly Havenから [テクスチャ名] のマテリアルを取得して [object_name] に適用してください。
例：「stone_wall」「rusted_metal」「wooden_floor」
```

---

### 5.4 ライティング

**スタジオ照明**
```
プロダクト撮影風のスタジオ照明を設定してください。
3点照明（Key/Fill/Rim）でシーン全体が見やすくなるように。
カメラは正面斜め上から見下ろす角度に設定してください。
```

**Poly Haven HDRI**（要: Poly Haven有効化）
```
Poly HavenからHDRI「[hdri_name]」を取得して環境光として設定してください。
例：「studio」「forest」「sunset」
```

---

### 5.5 レンダリング

**プレビューレンダリング（速度優先）**
```
現在のシーンをプレビューレンダリングしてください。
・解像度：640 x 480
・エンジン：EEVEE
・保存先：renders/preview/preview_001.png
```

**最終レンダリング（品質優先）**
```
最終レンダリングを実行してください。
・解像度：1920 x 1080
・エンジン：Cycles
・サンプル数：128
・保存先：renders/final/[model_name]_final.png
```

---

### 5.6 AI生成機能（v1.5+）

**Hyper3D Rodinで3Dモデルを生成**
```
Hyper3D Rodinを使って以下の3Dモデルを生成してください：
「[説明：例: a garden gnome with a red hat, cartoonish style]」
生成後、シーンの原点付近に配置してください。
```
> 💡 無料トライアルは1日あたりの生成数に上限あり。超えた場合は翌日リセット。

**Sketchfabからモデルを検索・取得**
```
Sketchfabで「[キーワード]」のモデルを検索して、
適切なものをダウンロードしてシーンに追加してください。
```

---

### 5.7 エクスポート

**STL（3Dプリント用）**
```
[object_name] をSTL形式でエクスポートしてください。
・保存先：exports/stl/[file_name].stl
・スケール：1.0（メートル単位）
・軸：Z-up
エクスポート前にメッシュの問題（非マニフォールド等）をチェックして報告してください。
```

**GLB（ゲーム用）**
```
[object_name] をGLB形式でエクスポートしてください。
・保存先：exports/gltf/[file_name].glb
・マテリアル・テクスチャを埋め込み
・Y-up座標系
```

**Blenderファイルを保存**
```
現在のシーンを models/wip/[model_name]_v001.blend として保存してください。
```

---

## 6. 用途別チェックリスト

### 6.1 3Dプリント用モデル

| チェック項目 | 基準 | 確認プロンプト |
|---|---|---|
| 最小肉厚 | FDM: 1.5mm以上 | 「肉厚が1.5mm未満の箇所を検出して」 |
| 非マニフォールド | ゼロ（必須） | 「非マニフォールドエッジを修正して」 |
| オーバーハング | 45度以下推奨 | 「サポートが必要な角度の面を確認して」 |
| スケール | 実寸確認必須 | 「モデルの実寸法（mm単位）を教えて」 |
| エクスポート | STL形式 | 「exports/stl/ にSTLでエクスポートして」 |

### 6.2 ゲームアセット

| チェック項目 | 基準 | 確認プロンプト |
|---|---|---|
| ポリゴン数 | キャラ: 〜5000 / 小物: 〜500 | 「ポリゴン数を [N] 以下に最適化して」 |
| UV展開 | 重なりなし | 「UVを自動展開してアトラスにまとめて」 |
| 原点位置 | 底面中心 | 「原点をオブジェクトの底面中心に移動して」 |
| エクスポート | GLB形式 | 「exports/gltf/ にGLBでエクスポートして」 |

### 6.3 建築・工業モデル

| チェック項目 | 基準 | 確認プロンプト |
|---|---|---|
| スケール | 1単位 = 1メートル | 「単位をミリメートルに変更して調整して」 |
| 寸法精度 | 小数点2桁 | 「幅[N]mm × 高さ[N]mm で作成して」 |
| 断面ビュー | 図面用 | 「フロント/サイド/トップビューをレンダリングして」 |
| エクスポート | FBX / STL | 「exports/fbx/ にFBXでエクスポートして」 |

---

## 7. トラブルシューティング

| 症状 | 対処法 |
|---|---|
| Claude CodeがBlenderに接続できない | Blenderを起動 → N-panel → BlenderMCP → **「Connect to Claude」** を押す |
| 最初のコマンドが失敗する | 既知の挙動。そのまま再試行すれば2回目以降は動く |
| タイムアウトエラーが出る | 指示を小さなステップに分割する |
| オブジェクトが意図しない位置に生成される | 「現在のシーン情報を確認して」で座標を把握してから再指示 |
| レンダリング結果が真っ黒 | ライトなし or カメラ向き不正。「スタジオ照明を設定して」から再実行 |
| 予期しない変更が起きた | Blenderで `Ctrl+Z` → 必要に応じてWIPファイルからリロード |
| Poly Havenが動かない | BlenderMCPタブ → Poly HavenのチェックボックスをONに |
| Hyper3D生成上限に達した | 無料トライアルの1日上限。翌日リセット or hyper3d.ai で独自キーを取得 |

---

*参照: [github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp)*
