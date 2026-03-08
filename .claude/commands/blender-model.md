---
name: blender-model
description: 3Dモデリング作業（STEP 1-3）。シーン確認→形状作成→形状調整を1操作=1指示で実行する。
---

# BlenderMCP: モデリング (STEP 1-3)

このスキルはモデリング作業中に使用する。**1指示 = 1操作** を厳守すること。

## 事前確認（毎回実行）

1. **現在のプロジェクトを確認**: どの `projects/{name}/` で作業中か明示
2. **シーン状態確認**: `get_scene_info` で現在のオブジェクト一覧を取得
3. **最新の保存ファイルを確認**: `projects/{name}/models/wip/` の最新バージョン

## STEP 1: シーン確認

- `get_scene_info` を実行
- 現在のオブジェクト・カメラ・ライトを一覧表示
- 前回の作業状態と矛盾がないか確認

## STEP 2: 形状作成

ユーザーの指示に基づき、**1つずつ** オブジェクトを作成する。

使用ツール:
- `create_object` — プリミティブ（Cube/Sphere/Cylinder/Cone/Torus）
- `modify_object` — 位置・回転・スケール調整

**命名規則を厳守:**
- オブジェクト名: 英語 snake_case（例: `main_body`, `left_arm`）
- 位置は原点 `(0,0,0)` を基準に配置

各オブジェクト作成後:
1. `get_viewport_screenshot` で結果を確認
2. ユーザーに結果を報告し、次の指示を待つ

## STEP 3: 形状調整

複雑な操作は `execute_blender_code` を使用する。

**実行前に必ず:**
1. 現在の .blend を保存（バージョン番号を上げる）
   ```python
   bpy.ops.wm.save_as_mainfile(filepath="projects/{name}/models/wip/{name}_v{NNN}.blend")
   ```
2. 保存完了を確認してからコードを実行

よく使う操作:
- Subdivision Surface モディファイア追加
- Boolean（結合・切り抜き）
- Mirror モディファイア
- 頂点の移動・スケール
- プロポーショナル編集

各操作後:
1. `get_viewport_screenshot` で結果を確認
2. 問題があれば保存した .blend からリロード

## 保存ルール

| タイミング | アクション |
|-----------|----------|
| 新オブジェクト追加後 | バージョン番号を上げて保存 |
| `execute_blender_code` 実行前 | **必ず** バージョン番号を上げて保存 |
| ユーザーが「OK」と言った後 | 保存してから次へ |

## 次のステップへの移行

形状が完成したら:
```
[モデリング完了]
- 作成オブジェクト: {一覧}
- 最新ファイル: projects/{name}/models/wip/{name}_v{NNN}.blend
- 次のステップ: /blender-material でマテリアル・ライト設定へ
```

## 禁止事項
- 複数操作を1ターンでまとめて実行すること
- `get_viewport_screenshot` による確認を省略すること
- 保存なしに `execute_blender_code` を実行すること
- 命名規則を無視すること
- ユーザーの承認なしに形状を大幅変更すること
