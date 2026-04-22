from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('JP',     r'C:\Windows\Fonts\msgothic.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('JP-B',   r'C:\Windows\Fonts\msgothic.ttc', subfontIndex=1))

GOLD  = colors.HexColor('#C9A84C')
DARK  = colors.HexColor('#111111')
LGOLD = colors.HexColor('#F9F5EC')
SUB   = colors.HexColor('#888880')
WHITE = colors.white
GREEN = colors.HexColor('#3A9E68')
RED   = colors.HexColor('#D04040')

output = r'C:\Users\reale\Desktop\scalp_report.pdf'
doc = SimpleDocTemplate(output, pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=20*mm, bottomMargin=20*mm)

W = A4[0] - 36*mm

def S(name, fn='JP', fs=10, fc=DARK, sb=4, sa=3, li=0, lb=16):
    return ParagraphStyle(name, fontName=fn, fontSize=fs, textColor=fc,
                          spaceBefore=sb, spaceAfter=sa, leftIndent=li, leading=lb)

sTitle = S('t',  fn='JP-B', fs=20, fc=GOLD, sb=0, sa=2, lb=26)
sSub   = S('su', fs=9,  fc=SUB, sb=0, sa=12, lb=13)
sH1    = S('h1', fn='JP-B', fs=13, fc=GOLD, sb=12, sa=4, lb=19)
sH2    = S('h2', fn='JP-B', fs=10, fc=DARK, sb=8, sa=3, lb=15)
sBody  = S('b',  fs=9.5, lb=16, sa=3)
sSmall = S('sm', fs=8.2, fc=SUB, lb=13, sa=2)

def hr():
    return HRFlowable(width='100%', thickness=0.7, color=GOLD, spaceAfter=5, spaceBefore=3)

def p(txt, st=None):
    return Paragraph(txt, st or sBody)

def mkTable(data, widths, extra=None):
    base = [
        ('FONTNAME',     (0,0), (-1,-1), 'JP'),
        ('FONTNAME',     (0,0), (-1, 0), 'JP-B'),
        ('FONTSIZE',     (0,0), (-1,-1), 9),
        ('LEADING',      (0,0), (-1,-1), 14),
        ('BACKGROUND',   (0,0), (-1, 0), GOLD),
        ('TEXTCOLOR',    (0,0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [LGOLD, WHITE]),
        ('GRID',         (0,0), (-1,-1), 0.4, colors.HexColor('#DDD8C8')),
        ('TOPPADDING',   (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0), (-1,-1), 5),
        ('LEFTPADDING',  (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
    ]
    if extra:
        base.extend(extra)
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle(base))
    return t

def secH(txt):
    return [Spacer(1,3), p(txt, sH1), hr()]

story = []

# Cover
story += [
    Spacer(1, 8*mm),
    p('THE SCALP INK', S('brand', fn='JP-B', fs=10, fc=GOLD, sb=0, sa=3)),
    p('料金体系・特典ルール 設計書', sTitle),
    p('Pricing &amp; Referral Program Design Document　|　2026年4月', sSub),
    hr(),
    Spacer(1, 2*mm),
]

# 1. 料金体系
story += secH('1.  施術実態に基づく料金体系')
story.append(p('「1 DOT = ¥1」の透明会計を軸に、実際の施術発数（30,000〜50,000発）と整合した価格設定。'))
story.append(Spacer(1, 3*mm))
story.append(mkTable([
    ['プラン', 'ドット数目安', '価格', '対象・用途'],
    ['体験施術',        '3,000発',    '¥3,000',  '初回体験・部分確認'],
    ['全頭ライト',      '〜30,000発', '¥30,000', '薄め・初期薄毛'],
    ['全頭スタンダード', '〜40,000発', '¥40,000', '標準的な全頭施術'],
    ['全頭ヘビー',      '〜50,000発', '¥50,000', '濃いめ・広範囲対応'],
    ['スポット補修',    '応相談',      '¥9,800〜', '傷跡・部分集中'],
    ['タッチアップ',    '実測値',      '¥1/発',   '年1〜2回メンテナンス'],
], [30*mm, 32*mm, 26*mm, None]))
story.append(Spacer(1,2*mm))
story.append(p('※ ドット数はカウンセリング時診断。専用カウント機器により1発単位で計測・リアルタイム表示。', sSmall))

# 2. 初回割引
story += secH('2.  初回限定割引')
story.append(mkTable([
    ['項目', '内容'],
    ['対象',       '新規ユーザーのみ（初回施術時）'],
    ['割引額',     '全プラン ¥3,000 OFF'],
    ['適用条件',   '施術当日に適用・事前申告不要'],
    ['有効期限',   'カウンセリングから3ヶ月以内の初回施術'],
    ['紹介特典との関係', '選択制（どちらか一方のみ適用・非併用）'],
], [40*mm, None]))
story.append(Spacer(1,2*mm))
story.append(p('【選択制の根拠】紹介特典（¥5,000相当）は初回割引（¥3,000）より顧客メリットが大きいため、紹介コード使用時は紹介特典を自動優先適用することで管理もシンプルになる。'))

# 3. 紹介特典
story += secH('3.  紹介特典プログラム')
story.append(p('3-1.  紹介者（既存ユーザー）への特典', sH2))
story.append(mkTable([
    ['項目', '内容'],
    ['対象',          '施術完了済みユーザーのみ（未施術者は紹介者になれない）'],
    ['特典内容',      '5,000発プレゼント（¥5,000相当）'],
    ['付与タイミング', '被紹介者の施術＋支払い完了後'],
    ['使用用途',      '次回タッチアップ・追加施術に充当'],
    ['有効期限',      '付与日から12ヶ月'],
    ['累積',          '制限なし（何人紹介してもOK・発数は累積可能）'],
    ['不正防止',      '本人・同居家族への紹介は無効'],
], [40*mm, None]))
story.append(Spacer(1,3*mm))
story.append(p('3-2.  被紹介者（新規ユーザー）への特典', sH2))
story.append(mkTable([
    ['項目', '内容'],
    ['対象',          '紹介コードを提示した新規ユーザー'],
    ['特典内容',      '5,000発プレゼント（施術時にドット数へ加算）'],
    ['付与タイミング', '施術当日'],
    ['初回割引との関係', '非併用 / 紹介特典を自動優先（¥5,000 > ¥3,000）'],
], [40*mm, None]))

# 4. 併用可否
story += secH('4.  特典併用可否マトリクス')
story.append(mkTable([
    ['ユーザー区分', '初回割引 ¥3,000', '被紹介特典 5,000発', '紹介者特典 5,000発'],
    ['紹介なし（新規）',   'YES',      'NO',           '対象外'],
    ['紹介あり（新規）',   'NO（除外）','YES',          '対象外'],
    ['既存ユーザー（紹介者）', '対象外', '対象外',      'YES（施術後付与）'],
], [44*mm, 34*mm, 36*mm, None], [
    ('TEXTCOLOR', (1,1),(1,1), GREEN), ('FONTNAME', (1,1),(1,1), 'JP-B'),
    ('TEXTCOLOR', (2,1),(2,1), RED),
    ('TEXTCOLOR', (1,2),(1,2), RED),
    ('TEXTCOLOR', (2,2),(2,2), GREEN), ('FONTNAME', (2,2),(2,2), 'JP-B'),
    ('TEXTCOLOR', (3,3),(3,3), GREEN), ('FONTNAME', (3,3),(3,3), 'JP-B'),
]))

# 5. 紹介フロー
story += secH('5.  紹介フロー（オペレーション手順）')
story.append(mkTable([
    ['STEP', '担当', '内容'],
    ['①', '既存ユーザー', 'LINEや口頭で友人にサロンを紹介'],
    ['②', '新規ユーザー', 'カウンセリング予約時に「〇〇さんの紹介」と申告'],
    ['③', 'スタッフ',   '紹介者名を台帳に記録・被紹介者へ5,000発加算を告知'],
    ['④', '新規ユーザー', '施術＋お会計完了（カウント機器で発数・金額リアルタイム確認）'],
    ['⑤', 'スタッフ',   '紹介者台帳に5,000発を加算・LINE等で通知'],
    ['⑥', '紹介者',    '次回来店時に5,000発を充当（有効期限12ヶ月以内）'],
], [13*mm, 34*mm, None]))

# 6. ビジネス妥当性
story += secH('6.  ビジネス観点での妥当性検証')
story.append(p('6-1.  新規顧客1人獲得コスト比較', sH2))
story.append(mkTable([
    ['獲得チャネル', '一般的な獲得コスト', '当サロンの負担', '評価'],
    ['Web広告（Meta / Google）', '¥15,000〜¥50,000', '広告費全額',          '高コスト'],
    ['紹介プログラム',           '¥10,000相当',       '5,000発×2名分',      '最大1/5'],
    ['SNS自然流入',             '実質ほぼ¥0',        'なし',                '最低コスト'],
], [50*mm, 38*mm, 36*mm, None], [
    ('TEXTCOLOR', (3,1),(3,1), RED),   ('FONTNAME', (3,1),(3,1), 'JP-B'),
    ('TEXTCOLOR', (3,2),(3,2), GREEN), ('FONTNAME', (3,2),(3,2), 'JP-B'),
    ('TEXTCOLOR', (3,3),(3,3), GREEN), ('FONTNAME', (3,3),(3,3), 'JP-B'),
]))
story.append(Spacer(1,3*mm))
story.append(p('6-2.  LTV（顧客生涯価値）への貢献', sH2))
for item in [
    '紹介特典の「次回タッチアップに使える」仕組みが既存ユーザーの再来店を促進する',
    '紹介行動自体がユーザーのサービス愛着の証であり、口コミブランディングに直結する',
    '紹介数ランク制（3人→+3,000発、5人→+5,000発等）を追加するとリテンション効果が倍増',
]:
    story.append(p('◆  ' + item))
story.append(Spacer(1,3*mm))
story.append(p('6-3.  リスクと対策', sH2))
story.append(mkTable([
    ['リスク', '対策'],
    ['本人・家族への自己紹介で不正取得', '予約時に紹介者名と連絡先を記録・照合'],
    ['施術キャンセル後の特典要求',       '付与タイミングを「支払い完了後」に固定'],
    ['有効期限切れトラブル',             '付与時にLINE通知＋期限3ヶ月前にリマインド'],
    ['特典の二重取り',                   '予約システムで紹介コード入力時に初回割引を自動除外'],
], [62*mm, None]))

# 7. 拡張案
story += secH('7.  今後の拡張案')
story.append(mkTable([
    ['施策', '内容', '優先度'],
    ['SNSシェア特典',    'Instagramタグ投稿で+1,000発（施術後限定）', '高'],
    ['回数券・定期プラン', '年間タッチアップ2回セット割引',            '高'],
    ['ランク紹介制',     '3人紹介で+3,000発、5人で+5,000発ボーナス', '中'],
    ['誕生日特典',       '誕生月の施術で+2,000発プレゼント',          '中'],
    ['モニター募集',     'ビフォーアフター掲載同意で30%OFF',          '低'],
], [44*mm, None, 18*mm]))
story.append(Spacer(1,5*mm))
story.append(hr())
story.append(p('本設計書は THE SCALP INK 内部資料です。内容は営業状況に応じて随時改定します。', sSmall))

doc.build(story)
import shutil, os
dest_dir = u'H:\\\u30de\u30a4\u30c9\u30e9\u30a4\u30d6\\\u2605\u2605\u2605\u30d7\u30e9\u30a4\u30d9\u30fc\u30c8\u7528\u2605\u2605\u2605\\\U0001f603scalp inc\U0001f603'
dest = os.path.join(dest_dir, '\u6599\u91d1\u30fb\u7279\u5178\u30eb\u30fc\u30eb\u8a2d\u8a08\u66f8.pdf')
shutil.copy2(output, dest)
print('PDF saved to desktop and project folder')
