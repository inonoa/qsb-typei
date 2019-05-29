import queue as qu
from slackclient import SlackClient
import time
import sys

q = qu.Queue()

boku = SlackClient(input())

q.put("2")
q.put("1")
q.put("0")


while True:
    if boku.rtm_connect():
        try:
            while True:
                for rtm in boku.rtm_read():
                    if rtm.get("type") and rtm["type"] == "message" and\
                        rtm.get("channel") and rtm["channel"] == "C641SPSKC" and\
                            rtm.get("text") and rtm["text"] == "きゅー":
                        if not q.empty():
                            boku.api_call("chat.postMessage",channel="#memonoa",text=q.get()+"を出します")
                        else:
                            boku.api_call("chat.postMessage",channel="#memonoa",text="空ですよ")
                time.sleep(3)
        except KeyboardInterrupt:
            boku.api_call("chat.postMessage",channel="#memonoa",text="強制終了：予期せぬエラーが発生しました")
            sys.exit()
        except Exception as e:
            boku.api_call("chat.postMessage",channel="#memonoa",text="強制終了：予期せぬエラーが発生しました")
            sys.exit()

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