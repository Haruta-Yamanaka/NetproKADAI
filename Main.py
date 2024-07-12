import tkinter
import random

CARD_WIDTH = 50
CARD_HEIGHT = 70


class Main:
    def __init__(self, master):
        self.master = master

        # 選択中のカード
        self.first_card_id = None
        self.second_card_id = None

        # キャンバスのサイズ
        self.width = CARD_WIDTH*13  # 横に13枚並べるためのサイズ
        self.height = CARD_HEIGHT*4  # 縦に4枚並べるためのサイズ
        # 未獲得のカードを管理するリスト
        self.remain_card_ids = []

        self.createWidgets()  # キャンバス作成
        self.createCards()  # カードを作成
        self.layoutCards()  # カードを並べる
        self.setEvents()  # イベントの受付設定

    def createWidgets(self):
        '''アプリに必要なウィジェットを作成する'''

        self.canvas = tkinter.Canvas(
            self.master,
            width=self.width,
            height=self.height,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack()

    def createCards(self):
        '''神経衰弱に使用するカードを作成する'''

        numbers = [
            "A", "2", "3", "4", "5", "6", "7",
            "8", "9", "10", "J", "Q", "K"
        ]

        # 13枚*4のカードをcardsに保持
        self.cards = [number for _ in range(4) for number in numbers]

        # カードの並びをシャッフルする
        random.shuffle(self.cards)
        print(self.cards[0])

    def layoutCards(self):
        '''カードをキャンバス上に並べる'''

        for i, number in enumerate(self.cards):
            # 水平方向と垂直方向の位置
            h = i % 13
            v = i // 13

            # カードを表現する長方形の座標を計算
            x1 = h * CARD_WIDTH
            x2 = (h + 1) * CARD_WIDTH
            y1 = v * CARD_HEIGHT
            y2 = (v + 1) * CARD_HEIGHT

            # カードの中心に数字を描画
            self.canvas.create_text(
                x1 + CARD_WIDTH / 2, y1 + CARD_HEIGHT / 2,
                text = number,
                font=("", 40)
            )

            # 長方形を数字の上に描画して数字を隠す
            fig_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="blue",
                tag=number
            )

            # 未獲得のカードとしてリストに追加
            self.remain_card_ids.append(fig_id)

    def setEvents(self):
        '''アプリに必要なイベントの設定を行う'''

        # クリック時にfaceupCardが実行されるように設定
        self.canvas.bind("<ButtonPress>", self.selectCard)

    def selectCard(self, event):
        '''選択されたカードに対する処理'''

        # ３枚同時に選択された場合は何もしない
        if self.first_card_id is not None and self.second_card_id is not None:
            return

        # クリックされたカードに対応する図形IDを取得
        card_fig_ids = self.canvas.find_closest(event.x, event.y)
        card_fig_id = card_fig_ids[0]

        # クリックされた図形が未獲得カードでない場合は何もしない
        if not card_fig_id in self.remain_card_ids:
            return

        # 同じ図形がクリックされた場合は何もしない
        if card_fig_id == self.first_card_id:
            return

        # 取得したIDの図形を塗りつぶし無しにする（数字が見えるようになる）
        self.canvas.itemconfig(card_fig_id, fill="")

        if self.first_card_id is None:
            # １枚目に選択したカードとして覚えておく
            self.first_card_id = card_fig_id
        else:
            # ２枚目に選択したカードとして覚えておく
            self.second_card_id = card_fig_id

            # 図形IDから表向きにされたカードの数字を取得する
            first_number = self.canvas.gettags(self.first_card_id)[0]
            second_number = self.canvas.gettags(self.second_card_id)[0]

            if first_number == second_number:
                # 選んだカードが同じ数字だった場合

                self.earnCards()
            else:
                # 選んだカードが異なる数字だった場合

                # 一時的にクリックを無効にする
                self.canvas.unbind("")

                # 1000ミリ秒後にカードを裏向きにする
                self.master.after(1000, self.reverseCards)
    def reverseCards(self):
        #'''めくったカードを元に戻す'''

        # カードを表す長方形に色をつける（数字が隠れる）
            self.canvas.itemconfig(self.first_card_id, fill="blue")
            self.canvas.itemconfig(self.second_card_id, fill="blue")

        # 選択中のカードの図形IDをNoneに設定
            self.first_card_id = None
            self.second_card_id = None

        # 再度クリック時にselectCardが実行されるように設定
            self.canvas.bind("<ButtonPress>", self.selectCard)
    def earnCards(self):
        '''めくったカードを獲得済みにする'''

        # 揃ったカードの色をグレーにする
        self.canvas.itemconfig(self.first_card_id, fill="gray")
        self.canvas.itemconfig(self.second_card_id, fill="gray")

        # カードの長方形を最背面に移動する（数字が見えるようになる）
        self.canvas.lower(self.first_card_id, "all")
        self.canvas.lower(self.second_card_id, "all")

        # 未獲得カードのリストから獲得されたカードを削除する
        self.remain_card_ids.remove(self.first_card_id)
        self.remain_card_ids.remove(self.second_card_id)

        # 選択中のカードの図形IDをNoneに設定
        self.first_card_id = None
        self.second_card_id = None
        # 未獲得カードのリストに要素がなくなったらゲームクリア
        if len(self.remain_card_ids) == 0:
            self.canvas.create_text(
                self.width / 2, self.height / 2,
                font=("", 80),
                text="GAME CLEAR!!!",
                fill="red"
            )


app = tkinter.Tk()
Main(app)
app.mainloop()

