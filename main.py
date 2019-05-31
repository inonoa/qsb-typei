import queue as qu
from slackclient import SlackClient
import time
import sys

class QueueWithName:
    def __init__(self, name):
        self.name = name
        self.q = qu.Queue()

qs = [QueueWithName("きゅー")]
hajimete = True

boku = SlackClient(input())

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
                        if rtm["text"][:4] == "enq " and len(rtm["text"])>4:
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
                        if rtm["text"][:9] == "create q ":
                            for qwn in qs:
                                if qwn.name==rtm["text"][9:]:
                                    say("既に同名のキューが存在します。")
                                    break
                            else:
                                qs.append(QueueWithName(rtm["text"][9:]))
                                say("キュー "+rtm["text"][9:]+" を追加しました。")

                # イベント取得間隔は三秒(以上)
                time.sleep(3)

        # 任意の例外で強制終了のメッセージだして(出せない時もあるだろうけど)終了
        except KeyboardInterrupt:
            say("強制終了：予期せぬエラーが発生しました")
            sys.exit()
        except Exception as e:
            print(e)
            say("強制終了：予期せぬエラーが発生しました")
            sys.exit()

    # 繋がらなければ5秒待つ
    time.sleep(5)


# import os
# import time
# from slackclient import SlackClient
# import random
# 
# def postMsg(msg, channel="#memonoa"):
#     sc.api_call(
#         "chat.postMessage",
#         channel=channel,
#         text=msg,
#         icon_emoji=":popco:",
#         username="ボブ子"
#     )
# 
# slack_token = os.environ["SLACK_API_TOKEN"]
# sc = SlackClient(slack_token)
# 
# def bobunemimimmi():
#     postMsg("PandA楽しみー！")
#     bbnmarray = []
#     state = "normal"
#     while True:
#         for rtm in sc.rtm_read():
#             if rtm["type"] == "message" and rtm["channel"] == "C641SPSKC" and "bot_id" not in rtm and "text" in rtm:
#                 '''
#                 if rtm["text"] == "残念":
#                     postMsg("いっけね！")
#                     state = "exceptional"
#                     break
#                 '''
#                 for bbnm in bbnmarray:
#                     if bbnm == rtm["text"]:
#                         if random.randint(1,10)==1:
#                             postMsg("かわいー！")
#                             state = "judging"
#                         else:
#                             postMsg("もう見た")
#                         break
#                 else:
#                     if random.randint(1,10)==1:
#                         postMsg("もう見た")
#                         state = "judging"
#                     else:
#                         postMsg("かわいー！")
#                 bbnmarray.append(rtm["text"])
#         if state == "judging":
#             while True:
#                 for rtm in sc.rtm_read():
#                     if rtm["type"] == "message" and rtm["channel"] == "C641SPSKC" and "bot_id" not in rtm and "text" in rtm:
#                         if rtm["text"] == "残念":
#                             postMsg("いっけね！")
#                             state = "terminal"
#                         else:
#                             state = "normal"
#                         break
#                 if state == "normal" or state == "terminal":
#                     break
#                 time.sleep(1)
#         if state == "terminal":
#             break
#         time.sleep(1)
# 
# if sc.rtm_connect():
#     while True:
#         for rtm in sc.rtm_read():
#             print("hoge")
#             if rtm["type"] == "message" and rtm["channel"] == "C641SPSKC" and "text" in rtm:
#                 if rtm["text"] == "ボブネミミッミ":
#                     bobunemimimmi()
#         time.sleep(1)
# else:
#     print("Connection Failed")