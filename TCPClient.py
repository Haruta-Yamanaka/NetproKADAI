import socket
import pickle
import threading
from TCPServer import Cards,Card

# TCPクライアントの設定
HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 4096
cards = None
name = None
isMyTurn = True


def setUp(client_socket):
    global cards,name
    isFinish = False
    try:#カード、名前の順に送られる
        while not isFinish:
            # サーバーからのデータを受信して表示
            data = client_socket.recv(BUFFER_SIZE)
            received_object = pickle.loads(data)
            if not data:
                break
            if cards is None:
                cards = received_object
                cards.showDeck()
            elif name is None:
                name = received_object
                print(f"あなたは{name}です")
                isFinish = True

    except KeyboardInterrupt:
        print("\n[*] Client is shutting down.")
        client_socket.close()


def input_handler(client_socket):
    your_input = input(">>>"); #(1)
    client_socket.send(your_input.encode("UTF-8")); #(2)


def receive_handler(client_socket):
    global BUFFER_SIZE, isMyTurn
    str = type("str")
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE); #(3)
            received_object = pickle.loads(data)
            if(type(received_object) == str):
                if(received_object =="Your Turn!"):
                    isMyTurn = True
                    print("あなたの番です。")
                elif (received_object == "Turn End"):
                    isMyTurn = False
                    print("ターン終了です。")
                else:
                    print(received_object)
            else:
                cards = received_object
                cards.showDeck()
                print(getCards())
        except Exception as e:
            continue


def revealCard(client_socket):#カードをめくる処理
    
    #クリックしたらっていう条件分岐を作ってほしい。
    #以下のコードはクリックした後の処理である。

    index = 0 #ここにクリックしたカードのインデックスを代入したい。
    command = getCommand(index)
    sendCommand(command,client_socket)


def getCards():
    global cards
    for card in cards:
        return card
    
def sendCommand(command,client_socket):
    client_socket.send(command.encode("UTF-8"))



def getCommand(index): #選んだインデックスをサーバーに送るコマンドに変換
    diviser = 13
    result = divmod(index,diviser)
    str = str(result[0]+1)+","+str(result[1]+1)
    return str



#グローバル変数の設定


# サーバーに接続
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"[*] Connected to {HOST}:{PORT}")

setUp(client_socket)
while True:
    receiveThread = threading.Thread(target = receive_handler, args= (client_socket,), daemon= True)
    receiveThread.start()
    if isMyTurn:
        inputThread = threading.Thread(target = input_handler, args= (client_socket,), daemon= True)
        inputThread.start()
