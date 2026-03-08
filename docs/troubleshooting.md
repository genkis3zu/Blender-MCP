# トラブルシューティング

| 症状 | 対処法 |
|------|--------|
| Claude CodeがBlenderに接続できない | Blender起動 → N-panel → BlenderMCP → **「Connect to Claude」** を押す |
| 最初のコマンドが失敗する | 既知の挙動。そのまま再試行すれば2回目以降は動く |
| タイムアウトエラーが出る | 指示を小さなステップに分割する |
| オブジェクトが意図しない位置に生成される | `get_scene_info` で座標を把握してから再指示 |
| レンダリング結果が真っ黒 | ライトなし or カメラ向き不正 → `scripts/setup_lighting.py` を実行 |
| 予期しない変更が起きた | Blenderで `Ctrl+Z` → 必要に応じてWIPファイルからリロード |
| Poly Havenが動かない | BlenderMCPタブ → Poly HavenのチェックボックスをONにする |
| Hyper3D生成上限に達した | 無料トライアルの1日上限。翌日リセット or hyper3d.ai で独自キーを取得 |
| `execute_blender_code` で壊れた | `.blend` からリロード（Ctrl+Zより確実） |
| uvx コマンドが見つからない | `uv` 未インストール。Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
