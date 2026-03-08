"""3点スタジオ照明セットアップ
Key / Fill / Rim ライトとカメラを配置する。
"""
import bpy
import math

# --- Key Light（主光源）---
bpy.ops.object.light_add(type='AREA', location=(4, -3, 5))
key_light = bpy.context.active_object
key_light.name = "key_light"
key_light.data.energy = 500
key_light.data.size = 2.0
key_light.rotation_euler = (math.radians(55), 0, math.radians(45))

# --- Fill Light（補助光）---
bpy.ops.object.light_add(type='AREA', location=(-3, -2, 3))
fill_light = bpy.context.active_object
fill_light.name = "fill_light"
fill_light.data.energy = 200
fill_light.data.size = 3.0
fill_light.rotation_euler = (math.radians(60), 0, math.radians(-45))

# --- Rim Light（逆光）---
bpy.ops.object.light_add(type='AREA', location=(0, 4, 4))
rim_light = bpy.context.active_object
rim_light.name = "rim_light"
rim_light.data.energy = 300
rim_light.data.size = 1.5
rim_light.rotation_euler = (math.radians(-45), 0, math.radians(180))

# --- Camera ---
bpy.ops.object.camera_add(location=(5, -5, 4))
camera = bpy.context.active_object
camera.name = "studio_camera"
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
bpy.context.scene.camera = camera

print("Studio lighting setup complete: key, fill, rim lights + camera.")
