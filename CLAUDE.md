# CIMA SKALP INK LP

CIMA SKALP INK のランディングページプロジェクト。

## 技術スタック

- **フレームワーク**: Next.js 14 (App Router)
- **言語**: TypeScript
- **スタイリング**: CSS Modules
- **パッケージマネージャ**: npm

## コマンド

```bash
npm install          # 依存関係のインストール
npm run dev          # 開発サーバー起動 (localhost:3000)
npm run build        # プロダクションビルド
npm run lint         # ESLint 実行
npm run typecheck    # TypeScript 型チェック
```

## ディレクトリ構成

```
src/
├── app/              # Next.js App Router ページ
│   ├── layout.tsx    # ルートレイアウト
│   ├── page.tsx      # トップページ (LP)
│   ├── globals.css   # グローバルスタイル
│   └── page.module.css
├── components/       # 共通コンポーネント
│   ├── Header.tsx
│   ├── Hero.tsx
│   ├── Features.tsx
│   ├── CTA.tsx
│   └── Footer.tsx
public/               # 静的アセット（画像等）
```

## 開発ルール

- コンポーネントは `src/components/` に配置
- スタイルは CSS Modules (`*.module.css`) を使用
- 日本語のLPのため、テキストは日本語で記述
- レスポンシブ対応必須（モバイルファースト）
