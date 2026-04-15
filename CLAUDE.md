# CIMA SCALP INK — Claude作業ルール

## プロジェクト概要
- サイト: https://cima-scalpink.com
- GitHub: https://github.com/koki-187/scalp-ink-lp
- メインブランチ: `master`（本番デプロイ）
- ファイル: `index.html`（JP版）、`en/index.html`（EN版）

---

## リモートコントロール作業ルール（iOS / ブラウザ版Claude共通）

### ブランチ運用
| 状況 | 使用ブランチ | push先 |
|------|-------------|--------|
| デスクトップ通常作業 | `master` | `origin/master` |
| iOS・ブラウザからの軽微な修正 | `master` | `origin/master` |
| iOS・ブラウザからの大規模変更 | `remote/ios` | `origin/remote/ios` → PR → master |

### 必須ルール

1. **push前に必ずpullする**
   ```bash
   git pull origin master
   git push origin master
   ```

2. **force pushは絶対禁止**（設定でブロック済み）

3. **作業完了後は必ずpushする**（iOS/デスクトップ間の同期のため）

4. **競合が発生した場合**
   - 作業を `remote/work` ブランチに退避
   - デスクトップ版で `master` に merge

### iOS/ブラウザ作業がデスクトップに与える影響
- **同じ `master` ブランチを使う限り、変更は共有される**（これは正常動作）
- デスクトップ側は次回作業前に `git pull` を実行すれば最新状態になる
- 「デスクトップ版の構築が壊れる」ことはない（force pushがブロックされているため）

---

## SMP シミュレーター実装状況（v9.3）

### 実装済み7項目
- ① 30cm距離固定 → 面積×500ドット×3回計算・cm²表示
- ② 黄色ペンin-app描画ツール（`#drawingCanvas` overlay）
- ③ ユーザーが自ら黄色枠を囲う操作フロー
- ④ 黄色枠内をSMPドットで充填（BFS flood fill）
- ⑤ 処理後に黄色線のみ削除（`_cleanPhotoPixels` 復元）
- ⑥ ビフォーアフター表示
- ⑦ ±30,000ドット絶対値スライダー

### 主要技術
- `detectYellowRegion()`: R>150, G>140, B<110判定 + 4px dilation + BFS flood fill
- `onDensitySlider(val)`: `_baseDotsCache` ± offset（最低10,000ドット）
- Canvas merge: `capCv` + `drawingCanvas` → `mergedCv` → API送信
- Yellow removal: `yellowMask[i]` の画素を `_cleanPhotoPixels` で上書き復元

---

## 禁止事項（設定でブロック済み）
- `git push --force`
- `git push -f`
- `git reset --hard`
- `rm -rf`
- `sudo`
