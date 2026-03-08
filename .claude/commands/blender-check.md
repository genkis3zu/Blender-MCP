---
name: blender-check
description: 品質確認・レビュー（STEP 5）。スクリーンショット確認→用途別品質チェック→修正指示を実行する。
---

# BlenderMCP: 品質確認・レビュー (STEP 5)

このスキルはモデルの品質確認とレビューに使用する。用途に応じたチェックを漏れなく実行すること。

## STEP 5-1: ビジュアル確認

複数アングルからスクリーンショットを取得する:

1. **正面**: `get_viewport_screenshot`
2. **必要に応じて** `execute_blender_code` でカメラ角度を変更し追加撮影:
   - 背面
   - 側面
   - 上面（トップダウン）

各スクリーンショットをユーザーに提示し、見た目の問題を報告。

## STEP 5-2: 用途別品質チェック

プロジェクトの README.md から用途を確認し、該当するチェックを **全項目** 実行する。

### 3Dプリント用（use-case: 3dprint）

`execute_blender_code` で以下を検証:

```python
import bpy, bmesh

obj = bpy.context.active_object
bm = bmesh.new()
bm.from_mesh(obj.data)

# 非マニフォールドチェック
non_manifold = [e for e in bm.edges if not e.is_manifold]
print(f"Non-manifold edges: {len(non_manifold)}")

# 寸法確認
dims = obj.dimensions
print(f"Dimensions: {dims.x*1000:.1f}mm x {dims.y*1000:.1f}mm x {dims.z*1000:.1f}mm")

# 頂点数・面数
print(f"Vertices: {len(bm.verts)}, Faces: {len(bm.faces)}")

bm.free()
```

チェック結果を報告:
| チェック項目 | 基準 | 結果 |
|-------------|------|------|
| 非マニフォールド | 0 | {数値} |
| 最小肉厚 | ≥1.5mm | {確認結果} |
| オーバーハング | ≤45° | {確認結果} |
| 寸法 | 実寸確認 | {X}mm × {Y}mm × {Z}mm |

### ゲームアセット用（use-case: game）

```python
import bpy

obj = bpy.context.active_object
poly_count = len(obj.data.polygons)
vert_count = len(obj.data.vertices)
print(f"Polygons: {poly_count}, Vertices: {vert_count}")

# 原点位置確認
origin = obj.location
bbox_min_z = min(v.co.z for v in obj.data.vertices)
print(f"Origin Z: {origin.z:.3f}, Bbox min Z: {bbox_min_z:.3f}")
```

| チェック項目 | 基準 | 結果 |
|-------------|------|------|
| ポリゴン数 | キャラ≤5000 / 小物≤500 | {数値} |
| 原点位置 | 底面中心 | {確認結果} |
| UV展開 | 重なりなし | {確認結果} |

### 建築・工業モデル用（use-case: architecture）

| チェック項目 | 基準 | 結果 |
|-------------|------|------|
| スケール | 1単位=1m | {確認結果} |
| 寸法精度 | 小数点2桁 | {確認結果} |

## STEP 5-3: 問題報告

チェック結果をまとめて報告する:

```
[品質チェック結果]
- 用途: {use_case}
- PASS: {通過した項目}
- FAIL: {不合格の項目と具体的な問題}
- 推奨修正: {修正方法の提案}
```

## STEP 5-4: 修正 or 承認

- **問題あり**: 修正内容を提案し、`/blender-model` に戻って修正
- **問題なし**: ユーザーに承認を求める

承認後:
```
[STEP 5 完了 — 品質確認OK]
- 最新ファイル: projects/{name}/models/wip/{name}_v{NNN}.blend
- 次のステップ: /blender-export でレンダリング・エクスポートへ
```

## 禁止事項
- 用途別チェックをスキップすること
- チェック結果を数値なしで報告すること
- 問題を検出しても報告せず次に進むこと
- ユーザーの承認なしに STEP 6 へ進むこと
