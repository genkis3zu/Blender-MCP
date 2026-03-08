---
name: blender-export
description: レンダリング・エクスポート（STEP 6）。最終レンダリング→用途別エクスポート→ファイル整理→プロジェクト完了。
---

# BlenderMCP: レンダリング・エクスポート (STEP 6)

このスキルは最終出力に使用する。レンダリング→エクスポート→整理を順序通りに実行すること。

## 事前確認

1. `/blender-check` (STEP 5) が完了しているか確認
2. 品質チェックで FAIL がないか確認（あれば先に修正）
3. 最新の .blend ファイルを保存

## STEP 6-1: プレビューレンダリング

まずプレビューで最終確認:

```python
import bpy

bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 480
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.filepath = "//projects/{name}/renders/preview/{name}_preview.png"
bpy.ops.render.render(write_still=True)
```

`get_render_result` で結果を表示し、ユーザーに確認。

## STEP 6-2: 最終レンダリング（承認後）

```python
import bpy

bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128
bpy.context.scene.render.filepath = "//projects/{name}/renders/final/{name}_final.png"
bpy.ops.render.render(write_still=True)
```

## STEP 6-3: エクスポート

プロジェクトの用途に応じたフォーマットでエクスポートする。

### 3Dプリント用 → STL

```python
import bpy

bpy.ops.wm.stl_export(
    filepath="projects/{name}/exports/stl/{name}.stl",
    export_selected_objects=True,
    global_scale=1.0,
    forward_axis='Y',
    up_axis='Z',
)
```

### ゲーム用 → GLB

```python
import bpy

bpy.ops.export_scene.gltf(
    filepath="projects/{name}/exports/gltf/{name}.glb",
    export_format='GLB',
    use_selection=True,
    export_apply=True,
    export_yup=True,
)
```

### 建築用 → FBX

```python
import bpy

bpy.ops.export_scene.fbx(
    filepath="projects/{name}/exports/fbx/{name}.fbx",
    use_selection=True,
    global_scale=1.0,
    apply_unit_scale=True,
    axis_forward='-Z',
    axis_up='Y',
)
```

## STEP 6-4: 最終保存

```python
import bpy
bpy.ops.wm.save_as_mainfile(filepath="projects/{name}/models/final/{name}_final.blend")
```

## STEP 6-5: プロジェクト完了報告

```
[プロジェクト完了]
- プロジェクト: projects/{name}/
- 用途: {use_case}
- 成果物:
  - モデル: projects/{name}/models/final/{name}_final.blend
  - レンダリング: projects/{name}/renders/final/{name}_final.png
  - エクスポート: projects/{name}/exports/{format}/{name}.{ext}
- 品質チェック: PASS
```

子プロジェクトの `README.md` のステータスを `Complete` に更新する。

## 禁止事項
- 品質チェック未完了のままエクスポートすること
- プレビューなしに最終レンダリングを実行すること
- エクスポート形式を用途と異なるものにすること
- 最終 .blend の保存を忘れること
- README.md のステータス更新を忘れること
