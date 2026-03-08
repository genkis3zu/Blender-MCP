# 命名規則・単位・座標系

## オブジェクト命名

| 対象 | 規則 | 例 |
|------|------|-----|
| オブジェクト | 英語 snake_case | `main_body`, `left_arm`, `top_plate` |
| マテリアル | 用途_色 | `body_red`, `metal_silver`, `glass_clear` |
| コレクション | 英語 PascalCase | `MainStructure`, `Accessories` |

## ファイル命名

| 対象 | 規則 | 例 |
|------|------|-----|
| 作業中 .blend | `{name}_v{NNN}.blend` | `robot_v001.blend`, `robot_v002.blend` |
| 最終 .blend | `{name}_final.blend` | `robot_final.blend` |
| レンダリング | `{name}_{type}_{NNN}.png` | `robot_preview_001.png` |
| エクスポート | `{name}.{ext}` | `robot.stl`, `robot.glb` |
| スクリプト | 動詞_対象.py | `init_scene.py`, `export_stl.py` |

## 単位

- **標準単位**: メートル（Blenderデフォルト）
- **原点**: `(0, 0, 0)` を基準に配置
- **3Dプリント時**: mm単位で設計し、エクスポート時にスケール変換

## 座標系

| 環境 | Up軸 | Forward軸 |
|------|------|-----------|
| Blender | Z-up | -Y forward |
| GLB/glTF（ゲーム） | Y-up | 自動変換 |
| STL（3Dプリント） | Z-up | そのまま |
| FBX（汎用） | エクスポート時に設定 | エクスポート時に設定 |

## Git コミット

- 規約: Conventional Commits
- 形式: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`
- 例: `feat(robot): add arm joint mechanism`
- ガードレール更新: `docs(guardrail): update checklist v1.1`
