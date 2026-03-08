"""シーン初期化スクリプト
デフォルトオブジェクトを削除し、単位系とグリッドを設定する。
"""
import bpy

# 全オブジェクトを削除
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 単位系をメートルに設定
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1.0
bpy.context.scene.unit_settings.length_unit = 'METERS'

# グリッドスケール
bpy.context.space_data.overlay.grid_scale = 1.0 if hasattr(bpy.context, 'space_data') and bpy.context.space_data else None

# 3Dカーソルを原点にリセット
bpy.context.scene.cursor.location = (0, 0, 0)

print("Scene initialized: all objects removed, units set to meters.")
