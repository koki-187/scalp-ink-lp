# cima-scalpink.com セキュリティ改善手順

お名前.com「ネットde診断」（2026-11-01）の総合評価 **C（要確認）** への対応。
My Agent Guard のセキュリティ診断（`My-Agent-Works-KICKOFF/tools/mag-security`）で 2026-11-02 に実測した結果に基づく。

## 実測結果（2026-11-02）

| リスク | 項目 | 状態 | 直す場所 |
|---|---|---|---|
| 中 | HSTS | ヘッダーなし | ① Cloudflare |
| 中 | CSP | なし | このリポジトリ（PR #2 で `<meta>` を追加済み） |
| 中 | クリックジャッキング対策 | なし | ① Cloudflare（`<meta>` では指定できない） |
| 中 | SPF | なし | ② お名前.com の DNS |
| 中 | DMARC | なし | ② お名前.com の DNS |
| 低 | X-Content-Type-Options | なし | ① Cloudflare |
| 低 | Referrer-Policy | なし | このリポジトリ（PR #2 で追加済み） |
| — | HTTPS・http→https 転送・混在コンテンツ・フォーム送信先・.git/.env | 問題なし | — |

GitHub Pages はレスポンスヘッダーを設定できないため、HSTS・クリックジャッキング対策・nosniff は
**このリポジトリだけでは直せない**。

## ② DNS（SPF / DMARC）— 5分、費用なし

実測で **MX レコードが無い**（このドメインではメールを受け取っていない）ことを確認した。
予約メールは Google Apps Script（Gmail）から送っており、このドメインを差出人にしていない。
そのため「このドメインからはメールを送らない」と宣言するのが最も安全。

お名前.com Navi → ドメイン → **DNS設定／転送設定** → cima-scalpink.com → **DNSレコード設定を利用する** で、次の2件を追加する。

| ホスト名 | TYPE | VALUE |
|---|---|---|
| （空欄） | TXT | `v=spf1 -all` |
| `_dmarc` | TXT | `v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s` |

**注意**: 将来このドメインのアドレス（info@cima-scalpink.com 等）でメールを送るときは、送信サービスが案内する SPF に置き換え、DMARC を `p=none` から始め直す。

## ① ヘッダー（HSTS・クリックジャッキング・nosniff）— Cloudflare 無料プランで対応

GitHub Pages のまま、Cloudflare をプロキシとして前段に置く。

1. Cloudflare（無料）にサイト `cima-scalpink.com` を追加し、既存の DNS レコード（GitHub Pages の A / CNAME）が取り込まれたことを確認
2. お名前.com でネームサーバーを Cloudflare が指定する2つに変更（反映に最大24〜72時間。**ここだけはご本人の操作が必要**）
3. Cloudflare の SSL/TLS を **Full** にする（GitHub Pages の「Enforce HTTPS」は有効のまま）
4. Rules → **Transform Rules → Modify Response Header** で、全リクエストに次を「Set static」で追加

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
```

5. 再診断: My-Agent-Works-KICKOFF の Actions →「MAG セキュリティ診断」→ Run workflow（URL: `https://cima-scalpink.com/`）

②と①が終わり PR #2 がマージされると、中リスクの指摘は無くなる見込み（翌月1日のネットde診断で確認）。

## 戻し方

- PR #2: コミットを revert（各ページ3行の削除）
- DNS: 追加した TXT 2件を削除
- Cloudflare: お名前.com のネームサーバーを元（お名前.com 既定）に戻す
