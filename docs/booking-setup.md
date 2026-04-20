# 予約フォーム通知 セットアップ手順（5分で完了）

## 採用アーキテクチャ

```
[予約者] → [サイトのフォーム] → [Google Apps Script Web App]
                                       ├─ Google Sheets に記録
                                       ├─ CIMA様メールに即時通知
                                       └─ 予約者に自動返信メール
```

**すべて無料、Googleアカウント1つで完結、APIキー不要、1日100通まで送信可能。**

---

## ステップ 1: Google Sheet を作成

1. [sheets.google.com](https://sheets.google.com) で新規スプレッドシート作成
2. 名前を「**SCALP INK 予約管理**」に変更
3. 1行目に以下のヘッダーを入力:

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| 受信日時 | お名前 | 電話番号 | メール | 希望日時 | メニュー | メッセージ | ステータス |

---

## ステップ 2: Apps Script に以下のコードを貼り付け

1. スプレッドシート上部メニュー「**拡張機能 → Apps Script**」
2. 既存の `myFunction` を全削除し、下のコードを貼り付け

```javascript
// CIMA様の受信通知メールアドレス（★要変更）
const NOTIFY_EMAIL = 'navigator.koki@gmail.com';
// 店舗名（自動返信メールの差出名）
const SHOP_NAME = 'THE SCALP INK by CIMA';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('シート1')
               || SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    const now = new Date();
    const tz = 'Asia/Tokyo';
    const ts = Utilities.formatDate(now, tz, 'yyyy-MM-dd HH:mm:ss');

    // 予約一覧シートに追加
    sheet.appendRow([
      ts,
      data.name || '',
      data.phone || '',
      data.email || '',
      data.date || '',
      data.menu || '',
      data.message || '',
      '未対応'
    ]);

    // CIMA様への通知メール
    const subject = '【新規予約】' + (data.name || '名前未入力') + ' 様';
    const body = [
      '新しい予約リクエストが届きました。',
      '',
      '受信日時: ' + ts,
      'お名前: ' + (data.name || '(未入力)'),
      '電話番号: ' + (data.phone || '(未入力)'),
      'メール: ' + (data.email || '(未入力)'),
      '希望日時: ' + (data.date || '(未指定)'),
      'メニュー: ' + (data.menu || '(未選択)'),
      'メッセージ: ' + (data.message || '(なし)'),
      '',
      '─────────────',
      '予約管理シート: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl()
    ].join('\n');
    MailApp.sendEmail({ to: NOTIFY_EMAIL, subject: subject, body: body });

    // 予約者への自動返信
    if (data.email) {
      const replyBody = [
        (data.name || 'お客') + ' 様',
        '',
        SHOP_NAME + へのご予約リクエスト、ありがとうございます。',
        '以下の内容で受付いたしました。',
        '',
        '希望日時: ' + (data.date || '(未指定)'),
        'メニュー: ' + (data.menu || '(未選択)'),
        '',
        '現在、東京と沖縄の2拠点で施術を行っており、',
        'スケジュール確認後、24時間以内に担当者よりご連絡いたします。',
        'お急ぎの場合はLINE @045ovoxr までお問い合わせください。',
        '',
        '──────',
        SHOP_NAME,
        'https://cima-scalpink.com/'
      ].join('\n');
      MailApp.sendEmail({
        to: data.email,
        subject: '【' + SHOP_NAME + '】予約リクエストを受付けました',
        body: replyBody
      });
    }

    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput('SCALP INK Booking API OK');
}
```

3. 上部の「**保存**」（フロッピーアイコン）

---

## ステップ 3: Web App としてデプロイ

1. 右上「**デプロイ → 新しいデプロイ**」
2. 種類「**ウェブアプリ**」を選択
3. 設定:
   - 説明: `Booking API v1`
   - 次のユーザーとして実行: `自分（navigator.koki@gmail.com）`
   - **アクセスできるユーザー: `全員`** ← 重要！
4. 「**デプロイ**」をクリック
5. 初回は Google の承認ダイアログが表示 → 「詳細」→「安全でないページに移動」→「許可」
6. 完了画面に表示される **ウェブアプリ URL** をコピー

例: `https://script.google.com/macros/s/AKfycbxxxxxxxx/exec`

---

## ステップ 4: サイト側にURLを設定

index.html の先頭の `BOOKING_API_URL` 変数に、コピーしたURLを貼り付けてください。

```javascript
// サイト上 index.html 冒頭の <script> 内
const BOOKING_API_URL = 'https://script.google.com/macros/s/AKfycbxxxxxxxx/exec';
```

または、チャットで「URL: https://script.google.com/macros/s/...」とお送りいただければ私が設定します。

---

## 動作確認

1. サイトの予約フォームに入力 → 送信
2. スプレッドシートに新しい行が追加されていることを確認
3. CIMA様のメール（`navigator.koki@gmail.com`）に通知が届くことを確認
4. 予約者のメールに自動返信が届くことを確認（予約者がメール入力した場合）

---

## トラブルシューティング

| 症状 | 原因 | 対応 |
|---|---|---|
| フォーム送信後 CORS エラー | Apps Script の URL が古い | 再デプロイしてURL更新 |
| メールが届かない | スパム判定 | メーラーのスパムフォルダ確認、送信元を連絡先に追加 |
| 承認でブロック | Google 初回承認 | 詳細 → 移動 → 許可 を繰り返す |
| 送信上限 (1日100通) | Google 個人アカ制限 | ほぼ問題ない枠だが、超過時は Workspace アカウントへ |

---

## 将来の拡張

- **LINE通知追加**: LINE Messaging API チャネルを作成し、Apps Script から `UrlFetchApp.fetch('https://api.line.me/v2/bot/message/push', ...)` でpush送信を追加可能
- **予約カレンダー**: Google Calendar に予約を自動登録
- **SMS通知**: Twilio などの有料サービスで対応可能
