# レンダリング・エクスポートプロンプト

## プレビューレンダリング（速度優先）
```
現在のシーンをプレビューレンダリングしてください。
・解像度：640 x 480
・エンジン：EEVEE
・保存先：renders/preview/preview_001.png
```

## 最終レンダリング（品質優先）
```
最終レンダリングを実行してください。
・解像度：1920 x 1080
・エンジン：Cycles
・サンプル数：128
・保存先：renders/final/[model_name]_final.png
```

## STL（3Dプリント用）
```
[object_name] をSTL形式でエクスポートしてください。
・保存先：exports/stl/[file_name].stl
・スケール：1.0（メートル単位）
・軸：Z-up
エクスポート前にメッシュの問題（非マニフォールド等）をチェックして報告してください。
```

## GLB（ゲーム用）
```
[object_name] をGLB形式でエクスポートしてください。
・保存先：exports/gltf/[file_name].glb
・マテリアル・テクスチャを埋め込み
・Y-up座標系
```

## Blenderファイルを保存
```
現在のシーンを models/wip/[model_name]_v001.blend として保存してください。
```

## AI生成（Hyper3D Rodin）
```
Hyper3D Rodinを使って以下の3Dモデルを生成してください：
「[説明：例: a garden gnome with a red hat, cartoonish style]」
生成後、シーンの原点付近に配置してください。
```

## Sketchfabからモデル取得
```
Sketchfabで「[キーワード]」のモデルを検索して、
適切なものをダウンロードしてシーンに追加してください。
```
