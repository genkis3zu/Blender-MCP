# 標準ワークフロー

## スキル連携フロー

各ステップは Claude Code Skills として実装されており、工程の漏れを防ぐ：

```
/blender-new → /blender-model → /blender-material → /blender-check → /blender-export
   STEP 0         STEP 1-3          STEP 4             STEP 5            STEP 6
```

## 7ステップ・イテレーティブフロー

```
STEP 0: プロジェクト開始（初回のみ）
  └─ ユーザーが自然言語で「何を作りたいか」を伝える
  └─ Claude が要件を整理して確認を返す
  └─ 承認後 → scripts/new_project.py で子プロジェクト生成
  └─ Blender接続確認 + シーン初期化 + 初期 .blend 保存
       │
STEP 1: シーン確認・初期化
  └─ get_scene_info → 現在の状態を把握
  └─ 必要なら scripts/init_scene.py で初期化
       │
STEP 2: 大まかな形を作る
  └─ create_object → プリミティブ（Cube/Sphere/Cylinder等）を配置
  └─ modify_object → 位置・スケール調整
       │
STEP 3: 形状の調整
  └─ execute_blender_code → モディファイア追加、頂点編集、変形
  └─ 例: Subdivision Surface, Boolean, Mirror
       │
STEP 4: マテリアル・ライト設定
  └─ set_material → 色・メタリック・ラフネス設定
  └─ scripts/setup_lighting.py → スタジオ照明
  └─ get_polyhaven_asset → HDRI/テクスチャ（必要時）
       │
STEP 5: ビューポート確認
  └─ get_viewport_screenshot → スクリーンショットで確認
  └─ NG → STEP 2〜4 に戻ってイテレーション
  └─ OK → 次へ
       │
STEP 6: レンダリング・エクスポート
  └─ render_scene → プレビュー or 最終レンダリング
  └─ execute_blender_code → エクスポート（STL/GLB/FBX）
  └─ ファイルを projects/{name}/exports/ に保存
```

---

## イテレーションのコツ

- **1指示 = 1操作** を基本にする（まとめて指示すると失敗しやすい）
- 迷ったら `get_viewport_screenshot` でビジュアル確認してから次の指示
- うまくいった操作はすぐ `scripts/` にスクリプトとして保存
- 失敗したら「元に戻して」より `.blend` ファイルからリロードの方が確実

---

## 保存タイミング

| タイミング | 操作 |
|-----------|------|
| 作業開始前 | `models/wip/{name}_v001.blend` として保存 |
| 大きな変更前 | バージョン番号を上げて保存 `_v002`, `_v003`... |
| `execute_blender_code` 前 | 必ず保存（任意コード実行のため） |
| 作業完了時 | `models/final/{name}_final.blend` として保存 |

---

## レンダリング設定

### プレビュー（速度優先）
- 解像度: 640 x 480
- エンジン: EEVEE
- 保存先: `renders/preview/`

### 最終（品質優先）
- 解像度: 1920 x 1080
- エンジン: Cycles
- サンプル数: 128
- 保存先: `renders/final/`
