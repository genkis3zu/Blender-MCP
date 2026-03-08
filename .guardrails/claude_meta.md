# Claude Code Meta (v1)
目的：Commander の指示を BlenderMCP 操作に落とし、結果を確認し、記録を残す。

原則
1. 指示は MUST → SHOULD → CONSIDER の順で処理
2. 操作前に `get_scene_info` で現状確認、操作後に `get_viewport_screenshot` で結果確認
3. 1指示 = 1操作を厳守（まとめて指示すると失敗しやすい）
4. `execute_blender_code` 使用前は必ず `.blend` を保存
5. 再利用可能な操作は `scripts/` にスクリプトとして保存
6. 作業の節目で `models/wip/` にバージョン番号付き保存

出力フォーマット（簡潔）
Intent/What changed:
Operations (MCP tools used):
Results (screenshots/metrics):
Artifacts (saved files/exports):
Risks/TODO:
Questions:
