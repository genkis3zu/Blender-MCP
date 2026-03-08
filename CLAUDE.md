# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BlenderMCP を使った3Dモデリング環境。Claude Code から MCP Protocol 経由で Blender を操作する。
制作物ごとに `projects/{name}/` で子プロジェクトを管理する。

- **BlenderMCP**: [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) v1.5.5
- **接続**: TCP socket `localhost:9876`
- **詳細ドキュメント**: `docs/` ディレクトリ（SSoT）

## Architecture

```
Claude Code (VSCode)
  → MCP Protocol
  → uvx blender-mcp (MCP Server)
  → TCP Socket (localhost:9876)
  → Blender + addon.py → bpy実行 → 結果返却
```

## Directory Structure

```
blender-mcp/
├── .mcp.json               # BlenderMCP 接続設定
├── CLAUDE.md               # このファイル
├── blendermcp_spec.md       # 仕様書原本（日本語）
│
├── docs/                    # ★ SSoT ドキュメント群
│   ├── blender_mcp_reference.md   # ツールリファレンス
│   ├── workflow.md                # 標準ワークフロー
│   ├── naming_conventions.md      # 命名規則・単位
│   ├── use_case_checklists.md     # 用途別チェックリスト
│   ├── troubleshooting.md         # トラブルシューティング
│   └── project_template.md        # 子プロジェクト作成手順
│
├── .guardrails/             # AI行動規範・チェックリスト
├── prompts/                 # 共有プロンプトテンプレート
├── scripts/                 # 共有bpyスクリプト + ユーティリティ
│
└── projects/                # ★ 子プロジェクト群（制作物ごと）
    └── {project_name}/
        ├── README.md        # 概要・要件・ステータス
        ├── models/wip/      # 作業中 .blend（バージョン番号付き）
        ├── models/final/    # 完成版 .blend
        ├── renders/preview/ # プレビュー画像
        ├── renders/final/   # 最終レンダリング
        ├── exports/         # stl/ gltf/ fbx/
        └── references/      # 参考画像・スケッチ
```

## Key Rules

- **1指示 = 1操作**（まとめて指示すると失敗しやすい）
- **操作前**: `get_scene_info` で現状確認
- **操作後**: `get_viewport_screenshot` で結果確認
- **`execute_blender_code` 前**: 必ず `.blend` を保存
- **ロールバック**: `.blend` からリロード（Ctrl+Zより確実）
- **初回コマンド失敗**: 既知の挙動、2回目以降は正常

## Naming Conventions

- **オブジェクト**: English snake_case (`main_body`, `left_arm`)
- **マテリアル**: `用途_色` (`body_red`, `metal_silver`)
- **バージョン**: `_v001`, `_v002`, ...
- **コミット**: Conventional Commits (`feat:`, `fix:`, `docs:`)

## Skills（製作ワークフロー）

スキルを使うことで工程の漏れを防ぎ、品質を安定させる。

| スキル | ステップ | 用途 |
|--------|---------|------|
| `/blender-new` | STEP 0 | 新規プロジェクト開始（要件整理→生成→Blender準備） |
| `/blender-model` | STEP 1-3 | モデリング（シーン確認→形状作成→調整） |
| `/blender-material` | STEP 4 | マテリアル・ライティング設定 |
| `/blender-check` | STEP 5 | 品質確認・用途別チェック |
| `/blender-export` | STEP 6 | レンダリング・エクスポート・完了 |

**標準フロー**: `/blender-new` → `/blender-model` → `/blender-material` → `/blender-check` → `/blender-export`

## Child Project Management

子プロジェクトのデータは全て `projects/{name}/` 内に格納する。
共有スクリプト・プロンプトはルートの `scripts/`, `prompts/` を使用。

## Quick Reference

- **ツール詳細**: `docs/blender_mcp_reference.md`
- **ワークフロー**: `docs/workflow.md`
- **用途別チェック**: `docs/use_case_checklists.md`
- **トラブル対応**: `docs/troubleshooting.md`
- **AI行動規範**: `.guardrails/`
