---
name: blender-material
description: マテリアル・ライティング設定（STEP 4）。質感と照明を設定し、ビジュアル品質を確立する。
---

# BlenderMCP: マテリアル・ライティング (STEP 4)

このスキルはマテリアルとライティングの設定に使用する。

## 事前確認（毎回実行）

1. `get_scene_info` で現在のオブジェクト一覧を取得
2. 各オブジェクトにマテリアルが未設定か確認
3. ライトの有無を確認

## マテリアル設定

### 基本マテリアル

`set_material` を使用して1オブジェクトずつ設定する。

パラメータ:
- **color**: ベースカラー（色名 or #RRGGBB）
- **metallic**: 0.0（非金属）〜 1.0（金属）
- **roughness**: 0.0（光沢）〜 1.0（マット）

**マテリアル命名規則**: `用途_色`
- 例: `body_red`, `metal_silver`, `glass_clear`, `rubber_black`

### 高度なマテリアル

`set_material` で対応できない場合は `execute_blender_code` を使用:
- ノードベースマテリアル（Principled BSDF の詳細設定）
- テクスチャマッピング
- 透過・発光・SSS

**`execute_blender_code` 使用前に必ず .blend を保存すること。**

### Poly Haven テクスチャ（必要時）

`get_polyhaven_asset` でリアルなテクスチャを取得:
- 石壁: `stone_wall`
- 錆びた金属: `rusted_metal`
- 木の床: `wooden_floor`

> Poly Haven使用前に BlenderMCPタブでONにする必要あり。

## ライティング設定

### スタジオ照明（推奨デフォルト）

`execute_blender_code` で `scripts/setup_lighting.py` の内容を実行:
- Key Light: エリアライト（主光源）
- Fill Light: エリアライト（補助光）
- Rim Light: エリアライト（逆光）
- Camera: 正面斜め上からの視点

### HDRI 環境光（必要時）

`get_polyhaven_asset` で HDRI を取得:
- スタジオ: `studio`
- 屋外: `forest`, `sunset`
- 室内: `interior`

## 確認フロー

マテリアルとライトを設定したら:

1. `get_viewport_screenshot` でビジュアル確認
2. ユーザーに結果を報告:
   ```
   [マテリアル・ライト設定完了]
   - マテリアル: {オブジェクト名: マテリアル名} の一覧
   - ライト: {ライト構成の説明}
   - スクリーンショット: （表示）
   ```
3. 調整が必要なら修正、OKなら保存

## 次のステップへの移行

```
[STEP 4 完了]
- 最新ファイル: projects/{name}/models/wip/{name}_v{NNN}.blend
- 次のステップ: /blender-check で品質確認へ
```

## 禁止事項
- マテリアル名を命名規則に従わず設定すること
- ライト設定後のスクリーンショット確認を省略すること
- 保存なしに高度なマテリアル操作を実行すること
