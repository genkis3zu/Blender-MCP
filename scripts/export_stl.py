"""STLエクスポートスクリプト（3Dプリント用）
選択中のオブジェクトをSTL形式でエクスポートする。
使用前にオブジェクトを選択しておくこと。
"""
import bpy
import os

# --- 設定 ---
EXPORT_DIR = "//exports/stl/"  # Blender相対パス
FILENAME = "model_export.stl"

# エクスポートディレクトリを絶対パスに解決
abs_dir = bpy.path.abspath(EXPORT_DIR)
os.makedirs(abs_dir, exist_ok=True)
filepath = os.path.join(abs_dir, FILENAME)

# 非マニフォールドチェック
obj = bpy.context.active_object
if obj and obj.type == 'MESH':
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.object.mode_set(mode='OBJECT')

    non_manifold_count = sum(1 for v in obj.data.vertices if v.select)
    if non_manifold_count > 0:
        print(f"WARNING: {non_manifold_count} non-manifold vertices detected in '{obj.name}'.")
    else:
        print(f"Mesh check passed: '{obj.name}' is manifold.")

# STLエクスポート
bpy.ops.wm.stl_export(
    filepath=filepath,
    export_selected_objects=True,
    global_scale=1.0,
    forward_axis='Y',
    up_axis='Z',
)

print(f"STL exported to: {filepath}")
