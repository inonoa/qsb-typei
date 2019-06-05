import queue as qu
from slackclient import SlackClient
import time
import sys
import os

class IQ:
    def __init__(self, name):
        self.name = name
        self.q = qu.Queue()
        self.top = None
    def enq(self,put):
        if self.top==None:
           self.top = put
        else:
            self.q.put(put)
    def deq(self,):
        if self.top==None:
            say("キューが空です。")
        else:
            whatwastop = self.top
            self.top = self.q.get()
            say(whatwastop+"を出しました。")
    def peek(self,):
        if self.top==None:
            return ":null:"
        else:
            return self.top

qs = [IQ("きゅー")]
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
                            for iq in qs:
                                if iq.name==rtm["text"][4:]:
                                    iq.deq()
                                    break
                            else:
                                say("そんな名前のキューは無いが？反論がないなら私の勝ちだが？")
                        
                        # peek(Queueの先頭を見る)を実装しようとしたけどそんな関数はなかった？？→オブジェクト指向は便利(ほんま？)
                        if rtm["text"][:5] == "peek " and len(rtm["text"])>5:
                            for iq in qs:
                                if iq.name==rtm["text"][5:]:
                                    say("先頭は"+iq.peek()+"です。")
                                    break
                            else:
                                say("そんな名前のキューは無いが？反論がないなら私の勝ちだが？")

                        # Enqueue(Queueに一つ入れる)
                        # これだけ複数入れられる罠(？)がある
                        elif rtm["text"][:4] == "enq " and len(rtm["text"])>4:
                            words = rtm["text"].split()
                            for iq in qs:
                                if iq.name==words[1]:
                                    for w in words[2:]:
                                        say(w+"を入れます。")
                                        iq.enq(w)
                                    break
                            else:
                                say("そんな名前のキューは無いが？反論がないなら私の勝ちだが？")

                        # new Queue();(キューを追加)
                        elif rtm["text"][:9] == "create q " and len(rtm["text"])>9:
                            for iq in qs:
                                if iq.name==rtm["text"][9:]:
                                    say("既に同名のキューが存在します。")
                                    break
                            else:
                                qs.append(IQ(rtm["text"][9:]))
                                say("キュー "+rtm["text"][9:]+" を追加しました。")

                        # Remove(Queueを削除)
                        elif (rtm["text"][:9] == "remove q " or rtm["text"][:9] == "delete q ") and len(rtm["text"])>9:
                            for iq in qs:
                                if iq.name==rtm["text"][9:]:
                                    say("キュー "+rtm["text"][9:]+" を削除します。")
                                    qs.remove(iq)
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
                                for iq in qs:
                                    s += iq.name + "\n"
                                say(s)
                        
                        # kill qsb (殺す)
                        elif rtm["text"] == "kill qsb":
                            say("この後亡くなったんだよね…")
                            sys.exit()

                # イベント取得間隔は三秒(以上)
                time.sleep(3)
                print(3)

        # 任意の例外で強制終了のメッセージだして(出せない時もあるだろうけど)終了
        except KeyboardInterrupt:
            say("強制終了：予期せぬエラーが発生しました")
            sys.exit()
        except Exception as e:
            print(e)
            say("エラーが発生しました。 `nohup.out` をご確認ください。")

    # 繋がらなければ5秒待つ
    time.sleep(5)