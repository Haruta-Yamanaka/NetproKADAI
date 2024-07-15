# ネップロ最終制作課題

## 概要  
Pythonのsocketとpygame-guiを用いて作成した  
一対一通信の神経衰弱アプリです。  

## 役割分担
riporippo ... **GUI作成＆連携**   
Haruta-Yamanaka ... **通信機能＆ゲーム内部**     

## プログラム解説
* **main.py**  
  GUIを表示するスクリプト  
  TCPClient.pyのClinetクラスを作って  
  card情報をもらい、画面更新を行います。  
 ![classes_main](https://github.com/user-attachments/assets/6e4ff6ae-a999-4b6c-a711-d871813e5a04)　　
* **main2.py**  
  main.pyと一緒です。  
  TCPClient2.pyのClientクラスを使っています。    
* **TCPClient.py**  
  serverとやりとりをします  
  GUIからの入力を受け付けて、server側に送り  
  結果をserverから受け取って、main.pyに情報を提供する役割を担っています。  
  ![classes_Client](https://github.com/user-attachments/assets/7ada9fab-85f6-4648-b755-8a9a7b1a1019)  
* **TCPClinet2.py**  
  TCPClient.pyと一緒です。  
* **TCPServer.py**
  二つのクライアントからの接続確立  
  ゲーム進行機能、cardクラスやplayerクラス  
  などの定義を行うスクリプト
  ゲームの根幹を担います。  
  ![classes_tcpserver](https://github.com/user-attachments/assets/1783c6c2-66d8-43c6-b3b2-09e3c47b305e)  

### クラス図全体とパッケージ  
![packages_Server](https://github.com/user-attachments/assets/2be096e5-41e1-493d-aefe-60e16a39cb69)  
![classes_Server](https://github.com/user-attachments/assets/41045b35-9ab1-47a5-b9d7-e023962c79fa)  
## ゲームの進行方法  
1. Serverを起動
2. main.py,main2.pyを起動し、GUI画面のstartボタンを押す
   ![image](https://github.com/user-attachments/assets/9735e202-5669-4bed-a1e4-b5f9436aaa2f)  
3. 接続が確立されると、対戦画面に遷移するのでプレイ
   ![image](https://github.com/user-attachments/assets/58193462-78f8-4a80-9d00-e315fdf6fae5)  
4. ゲームが終わると、勝ち負けが表示され、10秒後にウィンドウが強制終了  
   ![image](https://github.com/user-attachments/assets/066409df-9cf3-4edd-a749-81e8985cbb33)  

