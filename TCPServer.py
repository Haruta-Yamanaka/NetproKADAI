import socket
import threading
import random
import pickle

class Player:
    
    def __init__(self,socket,name): #必ず専用のソケットを用意すること
        self.socket = socket
        self.name = name
        self.code = ""
        self.cardList = []#ゲットしたカードを保存するリスト　これがそのまま点数になる
        self.setList = []#裏返したカードを一時的に保存する
        self.cards = Cards
    
    def getName(self):
        return self.name

    def getScore(self):
        return len(self.cardList)
    
    def codeSet(self,code):#クライアントからのコマンドをこちらへ移す
        self.code = code

    def getCode(self):
        return self.code

    def getCode(self):
        return self.code
    
    def getScore(self):
        return len(self.cardList)
    
    def sendMessage(self,message):#クライアントへサーバーからのオブジェクトかメッセージ
        self.socket.sendall(pickle.dumps(message))

    def waitMessage(self,BUFFER_SIZE):
        while self.isMyTurn:
            data = self.socket.recv(BUFFER_SIZE)
            print(data)



#///////////////////ここからカード///////////////////////////////

class Card:
    def __init__(self,number):
        self.number = number
        self.isGet = False  #もうすでに取られているかの判定、最初から取られているはずはないのでFalse
        self.isCovered = True   #裏返されているかの判定、デフォでは裏返されているのでTrue
        
    
    def getNumber(self):    #ここでカードの数字を確認する
        if self.isCovered:
            return "*"
        else:
            return self.number
    
    def Uncover(self):#カードを表にする
        self.isCovered = False


    

    def Cover(self): #カードを裏にする
        self.isCovered = True

    def Get(self):
        self.isGet = True
    
    def isAvailable(self): #今そのカードが取れるかどうかの判定

        if(not self.isGet):
            
            if(self.isCovered):#取られてなくて裏返された状態
                return True
            else:
                return False
        
        else:
            return False
        
    def getNum(self):
        return self.number
    
    def is_card_get(self):
        return self.isGet


#///////////////////ここからカードを管理すCardsクラス///////////////////////////////
    
class Cards:

    def __init__(self,i):
        self.cards = []
        self.i = i
        self.numbers = [
            "A", "2", "3", "4", "5", "6", "7",
            "8", "9", "10", "J", "Q", "K"
        ]

    def sayHello(self):
        print("Hello")
        print(self.rest)

    def createDeck(self):#デッキ構築
        global cards
        self.rest = self.getLength()*4
        for i in range(4):
            for number in self.numbers:
                cd = Card(number)
                self.cards.append(cd)
        random.shuffle(self.cards)

    def showDeck(self):
        str = ""
        str += "\n"
        m = len(self.numbers)
        for i in range(4):
            for card in self.cards[i*m:(i+1)*m]:
                str += card.getNumber() + ", "
            str += "\n"
        print(str)
        return self.cards


    
    def revealCard(self,index,setList,indexList):    #指定のカードを表にする
        
        if self.cards[index].isAvailable():
            self.cards[index].Uncover() #カードをめくる
            setList.append(self.cards[index])
            indexList.append(index)
            return True
        
        else:
            return False
    
    def coverCard(self,number1,number2):#めくったカード二枚を裏にする
        self.cards[number1].Cover()
        self.cards[number2].Cover()

    def getCard(self,list,index1,index2):#ここにプレイヤーのカードリストを入れてプレーヤーのカードにする
        list.append(self.cards[index1])
        self.cards[index1].Get()
        list.append(self.cards[index2])
        self.cards[index2].Get()
        self.rest -=2

    def getRest(self):
        return self.rest
    
    def getLength(self):
        return len(self.numbers)
    
    def getCards(self):
        return self.cards








# グローバル変数
playersSocket= []#全体に送信するとき使いたい
playerList = []
cards = Cards(1) #この引数には一つも意味がないから気にしないで



# TCPサーバーの設定
HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 4096
def handle_client():#ゲームの動き
    global playersSocket, player_scores, cards, BUFFER_SIZE

    try:
        # プレーヤーを追加
        
        #プレイヤーごとにメッセージを送ったり受け付けたりするときに使う。
        p1name = "player1"
        p2name = "player2"
        
        if len(playersSocket)>1:
            p1 = Player(playersSocket[0],p1name)
            p2 = Player(playersSocket[1],p2name)
            playerList.append(p1)
            playerList.append(p2)
            SetUp(p1,p2)
            # ゲームのメインループ
            while cards.getRest()>0:
                TurnTask(p1,BUFFER_SIZE)

                if cards.getRest()>0:
                    
                    TurnTask(p2,BUFFER_SIZE)

                else:

                    break

            showResult(p1,p2)
            
            print("Game Over!")


    except Exception as e:
        print(f"Error: {e}")


def TurnTask(player,BUFFER_SIZE):#プレイヤーそれぞれのターン処理
    global cards
    setList = []
    indexList = []
    isContinue = True
    
    TurnStart(player)
    
    while isContinue:
    
        try:
            data = player.socket.recv(BUFFER_SIZE)
            data = data.decode()
            if "," not in data:
                player.sendMessage("正しい値を入れてください。")
                continue
            else:
                try:
                    code = data.split(",")
                    code.reverse()
                    index = 0
                    m = 0
                    for i in code:
                            if(int(i)>13 or int(i)<1):
                                index = -13
                            else:
                                index += (int(i)-1) * cards.getLength()**m
                                m += 1
                        
                    if index<0 or index >= len(cards.cards) or len(code)>2 or len(code)<1:
                        player.sendMessage("正しい値を入れてください。\n")
                        continue
                    else:
                        if(cards.revealCard(index,setList,indexList)):
                            
                            send_game_state(playerList)#変化があったら全体に送信
                            print(len(setList))

                            if(len(setList)<=1):

                                player.sendMessage("もう一枚めくってください\n")
                                continue

                            else: #２枚カードをめくったときの処理

                                if(setList[0].getNumber() == setList[1].getNumber()):
                                    getCard(player,indexList[0],indexList[1])
                                    print(f"残り{cards.getRest()}枚です")
                                    send_game_state(playerList)
                                    setList.clear()#カードを手に入れるためにリスト内のものは全削除
                                    indexList.clear()
                                    isContinue = False
                                else:

                                    print("ターン終了処理")
                                    cards.coverCard(indexList[0],indexList[1])
                                    setList.clear()
                                    indexList.clear()
                                    isContinue = False
                                    
                                
                                isContinue = False
                        else:
                                player.sendMessage("もう一度引き直してください。\n")
                                player.sendMessage(cards)
                except ValueError:
                        player.sendMessage("数字を入力してください\n")
                        continue
        
        except Exception as e:
            player.socket.send("無効なコードです。行の番号、列の番号の順にお願いします。")
        
        
    TurnEnd(player)



    
def getCard(player,index1,index2):#指定のプレイヤーが指定のカードを取得する
    global cards
    cards.getCard(player.cardList,index1,index2)
    player.sendMessage(f"{cards.cards[index1].getNumber()}を獲得！")

def TurnStart(player):#ターンを始めるときの処理
    print(f"{player.name}のターンを始めます。")
    player.sendMessage("Your Turn!")

def TurnEnd(player):#ターンエンド時の処理
    print(f"{player.name}のターンを終了します。")
    player.sendMessage("Turn End")

def SetUp(p1,p2):#ゲームの準備　カード用意したりとか名前とかカード送ったりとか
    global cards
    p1Turn = True
    p2Turn = False
    cards.createDeck()
    p1.sendMessage(cards)
    p2.sendMessage(cards)
    p1.sendMessage(p1.getName())
    p2.sendMessage(p2.getName())
    p1.sendMessage(p1Turn)
    p2.sendMessage(p2Turn)


def send_game_state(playerList):#カードの状態を両プレイヤーに送る
    global cards
    for player in playerList:
        player.sendMessage(cards)


def showResult(p1,p2): #結果を表示
    p1Score = p1.getScore()
    p2Score = p2.getScore()
    if(p1Score > p2Score):
        p1.sendMessage("You Win!")
        p2.sendMessage("You Lose...")
    elif(p1Score < p2Score):
        p1.sendMessage("You Lose...")
        p2.sendMessage("You Win!")
    else:
        p1.sendMessage("Draw")
        p2.sendMessage("Draw")

def main():
    global playersSocket
    # TCPサーバーソケットの作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)
    print(f"[*] Listening on {HOST}:{PORT}")
    try:
        while True:
            # クライアントからの接続を待機
            client_socket, addr = server_socket.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            playersSocket.append(client_socket)
            # クライアントを処理するスレッドを開始
            handle_client()

    except KeyboardInterrupt:
        print("\n[*] Server is shutting down.")
        server_socket.close()

if __name__ == "__main__":
    main()