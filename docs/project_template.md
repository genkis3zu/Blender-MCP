# 子プロジェクト テンプレート

## 概要

各制作物は `projects/{project_name}/` に独立したデータフォルダを持つ。
共有リソース（スクリプト・プロンプト）はルートの `scripts/`, `prompts/` を使用する。

## ディレクトリ構成

```
projects/{project_name}/
├── README.md           # プロジェクト概要・要件・用途
├── models/
│   ├── wip/            # 作業中 .blend（バージョン番号付き）
│   └── final/          # 完成版 .blend
├── renders/
│   ├── preview/        # プレビュー画像（EEVEE, 640x480）
│   └── final/          # 最終レンダリング（Cycles, 1920x1080）
├── exports/
│   ├── stl/            # 3Dプリント用
│   ├── gltf/           # ゲーム/Web用
│   └── fbx/            # 汎用
└── references/         # 参考画像・スケッチ・仕様メモ
```

## 作成方法

### スクリプトで自動生成
```bash
python scripts/new_project.py {project_name} --use-case {3dprint|game|architecture|general}
```

### README.md テンプレート

子プロジェクトの `README.md` には以下を記載する：

- **プロジェクト名**: 制作物の名前
- **用途**: 3Dプリント / ゲームアセット / 建築 / その他
- **概要**: 何を作るか（1-3行）
- **要件**: サイズ・ポリゴン数・肉厚等の制約
- **ステータス**: WIP / Review / Complete

## 運用ルール

1. 1つの制作物 = 1つの子プロジェクト
2. 複数バリエーションは同一プロジェクト内でバージョン管理
3. 完了した子プロジェクトは README.md のステータスを `Complete` に更新
4. 参考画像は `references/` に集約（散在させない）
