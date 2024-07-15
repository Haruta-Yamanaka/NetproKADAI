# スケベすぎるネトプロ最終課題
#概要
Pythonのsocketとpygame-guiを用いて作成した
一対一通信の神経衰弱アプリです。

#役割分担
riporippo ... GUI作成＆連携
Haruta-Yamanaka ... 通信機能＆ゲーム内部

#プログラム解説
#main.py
GUIを表示するスクリプト
TCPClient.pyのClinetクラスを作って
card情報をもらい、画面更新を行います。
classes_main　　
#main2.py
main.pyと一緒です。
TCPClient2.pyのClientクラスを使っています。
#TCPClient.py
serverとやりとりをします
GUIからの入力を受け付けて、server側に送り
結果をserverから受け取って、main.pyに情報を提供する役割を担っています。
classes_Client
TCPClinet2.py
TCPClient.pyと一緒です。
TCPServer.py 二つのクライアントからの接続確立
ゲーム進行機能、cardクラスやplayerクラス
などの定義を行うスクリプト ゲームの根幹を担います。
classes_tcpserver
#クラス図全体とパッケージ
packages_Server
classes_Server

#ゲームの進行方法
Serverを起動
main.py,main2.pyを起動し、GUI画面のstartボタンを押す image
接続が確立されると、対戦画面に遷移するのでプレイ image
ゲームが終わると、勝ち負けが表示され、10秒後にウィンドウが強制終了
image
