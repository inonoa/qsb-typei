import queue as qu
from slackclient import SlackClient
import time
import sys

q = qu.Queue()

boku = SlackClient(input())

q.put("2")
q.put("1")
q.put("0")

# 発言
def say(s):
    boku.api_call("chat.postMessage",channel="#memonoa",text=s,icon_emoji=":atcoder_ac:",username="QSB")

# 逮捕
while True:
    # 繋がるならいい感じにやる、つながらなければ5秒待つ
    if boku.rtm_connect():
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
                        if rtm["text"][:3] == "deq":
                            if not q.empty():
                                say(q.get()+"を出します")
                            else:
                                say("空ですよ")

                        # Enqueue(Queueに一つ入れる)
                        elif rtm["text"][:4] == "enq ":
                            ireru = rtm["text"][4:]
                            say(ireru+"を入れます")
                            q.put(ireru)

                # イベント取得間隔は三秒(以上)            
                time.sleep(3)

        # 任意の例外で強制終了のメッセージだして(出せない時もあるだろうけど)終了
        except KeyboardInterrupt:
            say("強制終了：予期せぬエラーが発生しました")
            sys.exit()
        except Exception as e:
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