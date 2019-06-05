import queue as qu
from slackclient import SlackClient
import time
import sys
import os

class QueueWithName:
    def __init__(self, name):
        self.name = name
        self.q = qu.Queue()

qs = [QueueWithName("きゅー")]
hajimete = True

boku = SlackClient(os.environ["SLACK_API_TOKEN"])

# 発言
def say(s):
    boku.api_call("chat.postMessage",channel="#memonoa",text=s,icon_emoji=":atcoder_ac:",username="QSB")

# 逮捕
while True:
    # 繋がるならいい感じにやる、つながらなければ5秒待つ
    if boku.rtm_connect():

        # 挨拶
        if(hajimete):
            say("QSBを起動します。")
            print(qs)
            hajimete = False

        # 任意の例外で同じようなメッセージだして止まるのよろしくないな…
        try:
            # 再犯
            while True:

                # イベントを取得して一つ一つ処理
                for rtm in boku.rtm_read():
                    # 基本的に発言しかとらないので発言の場合だけ処理
                    if rtm.get("type") and rtm["type"] == "message" and\
                        rtm.get("channel") and rtm["channel"] == "C641SPSKC" and rtm.get("text"):

                        # Dequeue(Queueから一つ取り出す)
                        if rtm["text"][:4] == "deq " and len(rtm["text"])>4:
                            for qwn in qs:
                                if qwn.name==rtm["text"][4:]:
                                    if qwn.q.empty():
                                        say("キューが空です。")
                                    else:
                                        say(qwn.q.get()+"を出しました。")
                                    break
                            else:
                                say("そんな名前のキューは無いが？反論がないなら私の勝ちだが？")
                        
                        # peek(Queueの先頭を見る)を実装しようとしたけどそんな関数はなかった？？

                        # Enqueue(Queueに一つ入れる)
                        # これだけ複数入れられる罠(？)がある
                        elif rtm["text"][:4] == "enq " and len(rtm["text"])>4:
                            words = rtm["text"].split()
                            for qwn in qs:
                                if qwn.name==words[1]:
                                    for w in words[2:]:
                                        say(w+"を入れます。")
                                        qwn.q.put(w)
                                    break
                            else:
                                say("そんな名前のキューは無いが？反論がないなら私の勝ちだが？")

                        # new Queue();(キューを追加)
                        elif rtm["text"][:9] == "create q " and len(rtm["text"])>9:
                            for qwn in qs:
                                if qwn.name==rtm["text"][9:]:
                                    say("既に同名のキューが存在します。")
                                    break
                            else:
                                qs.append(QueueWithName(rtm["text"][9:]))
                                say("キュー "+rtm["text"][9:]+" を追加しました。")

                        # Remove(Queueを削除)
                        elif (rtm["text"][:9] == "remove q " or rtm["text"][:9] == "delete q ") and len(rtm["text"])>9:
                            for qwn in qs:
                                if qwn.name==rtm["text"][9:]:
                                    say("キュー "+rtm["text"][9:]+" を削除します。")
                                    qs.remove(qwn)
                                    break
                            else:
                                say("そんな名前のキューは無いが？反論がないなら私の勝ちだが？")
                        
                        # list(Queueの一覧を見る)
                        elif rtm["text"][:6] == "q list":
                            say("キューの一覧を表示します。")
                            s = ""
                            if(len(qs))==0:
                                say(":iie:")
                            else:
                                for qwn in qs:
                                    s += qwn.name + "\n"
                                say(s)

                # イベント取得間隔は三秒(以上)
                time.sleep(3)

        # 任意の例外で強制終了のメッセージだして(出せない時もあるだろうけど)終了
        except KeyboardInterrupt:
            say("強制終了：予期せぬエラーが発生しました")
            sys.exit()
        except Exception as e:
            print(e)
            say("エラーが発生しました。 `nohup.out` をご確認ください。")

    # 繋がらなければ5秒待つ
    time.sleep(5)