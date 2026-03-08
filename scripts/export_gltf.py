"""GLTFエクスポートスクリプト（ゲーム/Web用）
選択中のオブジェクトをGLB形式でエクスポートする。
"""
import bpy
import os

# --- 設定 ---
EXPORT_DIR = "//exports/gltf/"  # Blender相対パス
FILENAME = "model_export.glb"

# エクスポートディレクトリを絶対パスに解決
abs_dir = bpy.path.abspath(EXPORT_DIR)
os.makedirs(abs_dir, exist_ok=True)
filepath = os.path.join(abs_dir, FILENAME)

# GLBエクスポート（マテリアル・テクスチャ埋め込み）
bpy.ops.export_scene.gltf(
    filepath=filepath,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
    export_yup=True,
)

print(f"GLB exported to: {filepath}")
