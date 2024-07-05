import socket
import pickle
import threading
from TCPServer import Cards,Card

class Client:
    # TCPクライアントの設定
    def __init__(self):
            
        self.HOST = 'localhost'
        self.PORT = 12345
        self.BUFFER_SIZE = 4096
        self.client_socket = None
        self.cards = None
        self.name = None
        self.isMyTurn = True


    def setUp(self):
        self.isFinish = False
        try:#カード、名前の順に送られる
            while not self.isFinish:
                # サーバーからのデータを受信して表示
                data = self.client_socket.recv(self.BUFFER_SIZE)
                received_object = pickle.loads(data)
                if not data:
                    break
                if self.cards is None:
                    self.cards = received_object
                    self.cards.showDeck()
                elif self.name is None:
                    self.name = received_object
                    print(f"あなたは{self.name}です")
                    self.isFinish = True

        except KeyboardInterrupt:
            print("\n[*] Client is shutting down.")
            self.client_socket.close()

    def TurnTask(self):
        receiveThread = threading.Thread(target = self.receive_handler, args= (self.client_socket,), daemon= True)
        receiveThread.start()
        if self.isMyTurn:
            inputThread = threading.Thread(target = self.input_handler, args= (self.client_socket,), daemon= True)
            inputThread.start()


    def input_handler(self,client_socket):
        your_input = input(">>>"); #(1)
        client_socket.send(your_input.encode("UTF-8")); #(2)


    def receive_handler(self,client_socket):
        str = type("str")
        while True:
            try:
                data = client_socket.recv(self.BUFFER_SIZE); #(3)
                received_object = pickle.loads(data)
                if(type(received_object) == str):
                    if(received_object =="Your Turn!"):
                        self.isMyTurn = True
                        print("あなたの番です。")
                    elif (received_object == "Turn End"):
                        self.isMyTurn = False
                        print("ターン終了です。")
                    else:
                        print(received_object)
                else:
                    self.cards = received_object
                    self.cards.showDeck()
            except Exception as e:
                continue


    def revealCard(self):#カードをめくる処理
        #クリックしたらっていう条件分岐を作ってほしい。
        #以下のコードはクリックした後の処理である。

        tupple = (1,1) #ここにクリックしたカードから返されたタプルを代入したい
        command = self.getCommand(tupple)
        self.sendCommand(command,self.client_socket)


    def getCards(self):
        for card in self.cards:
            return card
        
    def sendCommand(self,command,client_socket):
        client_socket.send(command.encode("UTF-8"))



    def getCommand(self,tupple): #選んだインデックスをサーバーに送るコマンドに変換
        tupple = tupple
        str = str(tupple[0])+","+str(tupple[1])
        return str

    def socketSetup(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        print(f"[*] Connected to {self.HOST}:{self.PORT}")

#グローバル変数の設定


# サーバーに接続


cl = Client()
cl.socketSetup()

cl.setUp()
while True:
    cl.TurnTask()
