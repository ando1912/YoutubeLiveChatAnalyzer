YoutubeLiveChatAnalyzer

---
# 概要
- Youtubeのライブ配信のコメントを取得~~分析~~するプログラム

# 使い方
## コマンドライン
```
python src\livechat_to_csv.py video_id
```
|name|type|remarks|
|:-:|:-:|:-:|
|video_id|str|Youtubeの動画ID|

## 出力csvのデータ形式

|name|type|remarks|
|:--|:--|:--|
|datetime|str|日時|
|timestamp|int|チャット投稿時刻（unixタイムスタンプ、ミリ秒）|
|elapsedTime|str|経過時間|
|type|str|"superChat","textMessage","superSticker","newSponsor"|
|id|str|チャットの固有ID|
|autor_name|str|ユーザー名|
|isChatSponsor|bool|メンバーシップ加入者|
|message|str|チャット文|
|amountValue|float|スパチャ金額|
|amountString|str|スパチャ通貨単位+金額|
|currency|str|ISO4217の通貨記号|

# 今後の展望
- 瞬間チャット数が増えた瞬間などの視聴者の感情分析をしてみたい
  - チャット文章から感情の分類
  - 面白い、心配、からかい、叫び etc...
