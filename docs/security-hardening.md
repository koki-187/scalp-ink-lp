# cima-scalpink.com セキュリティ改善手順

お名前.com「ネットde診断」（2026-11-01）の総合評価 **C（要確認）** への対応。
My Agent Guard のセキュリティ診断（`My-Agent-Works-KICKOFF/tools/mag-security`）の実測結果に基づく。

## 現状（2026-11-02 実測、PR #2 本番反映後）

| リスク | 項目 | 状態 | 直し方 |
|---|---|---|---|
| 中 | HSTS | ヘッダーなし | 手順 4（Cloudflare の HSTS 設定） |
| 中 | クリックジャッキング対策 | なし | 手順 4（Transform Rule。`<meta>` では指定できない） |
| 中 | SPF | なし | 手順 2（Cloudflare の DNS に TXT） |
| 中 | DMARC | なし | 手順 2（Cloudflare の DNS に TXT） |
| 低 | CSP | `<meta>` で指定済み（ヘッダーではない） | 現状で可（PR #2 で対応済み） |
| 低 | X-Content-Type-Options | なし | 手順 4（HSTS 設定の No-Sniff） |
| — | HTTPS・転送・Referrer-Policy・混在コンテンツ・フォーム・.git/.env | 問題なし | — |

GitHub Pages はレスポンスヘッダーを設定できないため、Cloudflare（無料）を前段に置いて直す。
**ネームサーバーを Cloudflare に移すと、お名前.com の DNS 設定は使われなくなる。**
SPF / DMARC も Cloudflare 側に入れる（お名前.com 側に入れても効かない）。

## 手順（所要 30 分＋ネームサーバー反映待ち）

### 1. Cloudflare にサイトを追加する

1. Cloudflare（my-agent.work と同じアカウント）→ **Add a domain** → `cima-scalpink.com` → **Free** プラン
2. 取り込まれた DNS レコードを、お名前.com の「DNS設定」の一覧と1行ずつ見比べる。GitHub Pages の正しい値は次のとおり（[GitHub Docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)）

| TYPE | 名前 | 値 | プロキシ |
|---|---|---|---|
| A | `@` | 185.199.108.153 / .109.153 / .110.153 / .111.153（4件） | オン（オレンジ） |
| CNAME | `www` | `koki-187.github.io` | オン（オレンジ） |

お名前.com 側に、ほかのレコード（TXT の認証用など）があれば同じように追加する。

### 2. なりすましメール対策（SPF / DMARC）を Cloudflare の DNS に追加する

実測で **MX レコードが無い**（このドメインではメールを受け取っていない）ことを確認済み。
予約メールは Apps Script の MailApp（Gmail アカウント）から送っており、このドメインを差出人にしていない（`docs/booking-setup.md`）。
そのため「このドメインからはメールを送らない」設定にする。

| TYPE | 名前 | 内容 |
|---|---|---|
| TXT | `@` | `v=spf1 -all` |
| TXT | `_dmarc` | `v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s` |

将来 info@cima-scalpink.com 等で送信するときは、送信サービスの指定する SPF に置き換え、DMARC を `p=none` から始め直す。

### 3. ネームサーバーを切り替える（ご本人の操作が必要）

1. お名前.com Navi → ドメイン → **ネームサーバーの変更** → cima-scalpink.com → 「他のネームサーバーを利用」
2. Cloudflare が表示した2つのネームサーバーを入力して確定
3. Cloudflare の画面が **Active** になるまで待つ（数時間〜最大 24〜72 時間）
4. Active になったら、ブラウザで https://cima-scalpink.com/ が表示されること、予約フォームから送信できることを確認

### 4. ヘッダーを設定する（Active になってから）

1. **SSL/TLS → Overview** → 暗号化モード **Full**
   （GitHub Pages の証明書は Cloudflare 経由では更新が不安定になることがあるため、まず Full。Full (strict) は証明書を検証するので、エラー 526 が出たら Full に戻す）
2. **SSL/TLS → Edge Certificates** → **Always Use HTTPS** をオン
3. 同じ画面の **HTTP Strict Transport Security (HSTS)** → Enable HSTS
   - Max Age Header: **6 months**（安定を確認したら 12 months）
   - Apply HSTS policy to subdomains: **オフ**（HTTPS 未対応のサブドメインがあると開けなくなるため。必要になったら見直す）
   - Preload: **オフ**
   - **No-Sniff Header: オン**（X-Content-Type-Options: nosniff）
   - **注意**: HSTS を入れたあとは、HTTPS をやめる・Cloudflare を止める・ネームサーバーを戻す操作をしない（Max Age の期間、サイトが開けなくなる）
4. **Rules → Transform Rules → Modify Response Header** → Create rule
   - 名前: `security headers`、適用先: **All incoming requests**
   - Set static: `X-Frame-Options` = `SAMEORIGIN`
   - 「Managed Transforms の Add security headers」は使わない（Referrer-Policy を same-origin に上書きし、廃止済みの Expect-CT も付くため）

### 5. 再診断する

GitHub → My-Agent-Works-KICKOFF → Actions →「MAG セキュリティ診断」→ **Run workflow**
（url: `https://cima-scalpink.com/`、consent: `自社管理（制作・ドメイン登録者）`）。
中リスクの指摘が無くなり、評価が B 以上になることを確認する。翌月1日のネットde診断でも確認する。

## 戻し方

- ヘッダー: Transform Rule を削除。HSTS は Max Age を 0 にして、元の Max Age の期間が過ぎてからネームサーバーを戻す
- DNS: お名前.com でネームサーバーを「お名前.com のネームサーバー」に戻す（戻す前に HSTS を解除すること）
- `<meta>` の CSP / Referrer-Policy: PR #2 のマージコミット 6eff8f9 を revert
