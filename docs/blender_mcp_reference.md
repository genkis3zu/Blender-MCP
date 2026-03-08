# BlenderMCP ツールリファレンス

> 対象: [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) v1.5.5
> 接続: TCP Socket `localhost:9876`

---

## 接続設定

### CLI（1行で完了）
```bash
claude mcp add blender uvx blender-mcp
```

### .mcp.json（Windows）
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

### 接続手順
1. Blender を起動
2. N-panel → BlenderMCP → **「Connect to Claude」** を押す
3. Claude Code で `現在のBlenderシーンの情報を教えて` と入力
4. ハンマーアイコンが表示されシーン情報が返れば接続成功

> 初回コマンドが失敗することがある（既知の挙動）。2回目以降は正常動作。

---

## MCP ツール一覧（13種）

### 情報取得

| ツール | 説明 | 主な用途 |
|--------|------|----------|
| `get_scene_info` | シーン内の全オブジェクト・カメラ・ライト情報 | 操作前の状態確認 |
| `get_object_info` | 指定オブジェクトの詳細（位置・マテリアル・頂点数） | 個別オブジェクト調査 |
| `get_viewport_screenshot` | ビューポートのスクリーンショット取得 | 操作結果の目視確認 |
| `get_render_result` | レンダリング結果画像を取得・表示 | レンダリング確認 |

### オブジェクト操作

| ツール | 説明 | パラメータ例 |
|--------|------|-------------|
| `create_object` | プリミティブ生成 | 種類: Cube/Sphere/Cylinder/Cone/Torus |
| `modify_object` | 位置・回転・スケール・名前変更 | location, rotation, scale, name |
| `delete_object` | オブジェクト削除 | オブジェクト名指定 |
| `set_material` | マテリアル作成・割り当て | color, metallic, roughness |
| `execute_blender_code` | 任意のbpyコードを実行 | Pythonコード文字列 |

> ⚠️ `execute_blender_code` は最も強力だが、実行前に必ず `.blend` を保存すること。

### 出力

| ツール | 説明 | 設定例 |
|--------|------|--------|
| `render_scene` | シーンをレンダリングして画像保存 | 解像度, エンジン, 保存先 |

### 外部連携

| ツール | 説明 | 備考 |
|--------|------|------|
| `search_sketchfab_models` | Sketchfabからモデル検索・ダウンロード | キーワード検索 |
| `get_polyhaven_asset` | Poly HavenからHDRI/テクスチャ/モデル取得 | BlenderMCPタブでON必要 |
| `generate_hyper3d_model` | Hyper3D RodinでAI生成3Dモデル作成 | 無料トライアル: 1日上限あり |

---

## ツール選択ガイド

```
やりたいこと → 使うツール
─────────────────────────
状態を知りたい      → get_scene_info / get_object_info
プリミティブを置く  → create_object
位置・大きさ変更    → modify_object
複雑な操作          → execute_blender_code
色・質感を設定      → set_material
見た目を確認        → get_viewport_screenshot
最終画像を作る      → render_scene → get_render_result
外部モデルを使う    → search_sketchfab_models / get_polyhaven_asset
AIで3Dモデル生成    → generate_hyper3d_model
```
