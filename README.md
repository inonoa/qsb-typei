# QSB Type-I
Queue in Slack Bot.

## 使用法
*キューを作る/消す*
- `create q hoge` : hogeキューを作る
- `delete q hoge` : hogeキューを消す

*キューにモノを入れる/出す*
- `enq hoge fuga` : hogeキューにfugaを入れる
- `deq hoge` : hogeキューの先頭の要素を出す

## 欲しいかもしれないやつ
- `q peak hoge` : hogeキューの先頭を表示(出すわけではない)
- `q count hoge` : hogeキューに入っている要素数を表示
- `q list` : 全てのキューの名前と先頭の要素を表示

(先頭の要素だけが見れるのが良いと思ってるので先頭以外の中身を見る機能は入れません)