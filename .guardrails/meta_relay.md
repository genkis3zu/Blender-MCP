# meta_relay.md
## Context Relay Protocol (v2)

### 目的
ClaudeCode / Codex / Commander 間でコンテキストが途中で薄まったり消えたりしないように、
各エージェントが **「受け取った文脈を再宣言し、次に明示的に渡す」** ことを義務化する。

---

## 共通フォーマット

### 1. Context Block（各AIの冒頭に必ず付ける）

すべての出力は、先頭にこのブロックを持つ：

```text
[Context Block]
From: <ClaudeCode | Codex | Commander>
BasedOn: <何を元にしたか（前の出力・対象ファイル・スクリーンショットなど）>
Summary: <これまでの経緯を1〜3行で要約>
Objective: <今回のラウンドで達成したい目的を1行で>
```

### 2. Relay Header（各AIの末尾に必ず付ける）

```text
[Relay Header]
NextTarget: <ClaudeCode | Codex | Commander>
ExpectedFocus: <次のエージェントが見るべきポイント>
CarryContextFrom: <Summary を1行に圧縮>
```

---

## ルール
1. **Context Block（冒頭）必須**
2. **Relay Header（末尾）必須**
3. Summary は毎回"自分の言葉で再構築"
4. BasedOn は前ラウンドの出力を正しく参照
5. Objective は1行で明確
