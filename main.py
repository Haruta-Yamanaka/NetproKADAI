# -*- coding:utf-8 -*-
import sys
import pygame
import pygame_gui
from TCPClient import Client
import socket
import pickle
import threading
from TCPServer import Cards,Card
from time import sleep
WIDTH = 1000
HEIGHT = 700
client = Client()
class StartScreen:
    def __init__(self, window_surface, manager):
        # スタートボタンの位置定義
        self.startButton_Width = 200
        self.startButton_Height = 50
        self.startButton_yOffset = 200
        self.startButton_x = (WIDTH - self.startButton_Width) // 2
        self.startButton_y = (HEIGHT - self.startButton_Height + self.startButton_yOffset) // 2

        # タイトルロゴ定義
        self.label_text = "SHINKEI SUIJACK"
        self.label_Width = 1000
        self.label_Height = 200
        self.label_x = (WIDTH - self.label_Width) // 2
        self.label_y = (HEIGHT - self.label_Height - 100) // 2

        self.window_surface = window_surface
        self.manager = manager

        self.setup_ui()

    def setup_ui(self):
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.startButton_x, self.startButton_y), (self.startButton_Width, self.startButton_Height)),
            text='start',
            manager=self.manager
        )
        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.label_x, self.label_y), (self.label_Width, self.label_Height)),
            text=self.label_text,
            manager=self.manager
        )

    def run(self, main):
        # イベント管理
        is_running = True
        while is_running:
            time_delta = main.clock.tick(60) / 1000.0  # 更新用の時計
            for event in pygame.event.get():  # 入力ごとの処理
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:  # ボタンの処理
                    if event.ui_element == self.start_button:
                        print("START!!")
                        main.show_match_screen()
                        is_running = False

                self.manager.process_events(event)

            self.manager.update(time_delta)

            # 画面更新
            self.window_surface.blit(main.background, (0, 0))
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()


class MatchScreen:
    def __init__(self, window_surface, manager):
        # 戻るボタン定義
        self.back_button_Width = 200
        self.back_button_Height = 50
        self.back_button_x = (WIDTH - self.back_button_Width) // 2
        self.back_button_y = HEIGHT - 100

        # ラベル定義
        self.label_text = "Matching now"
        self.label_Width = 1000
        self.label_Height = 200
        self.label_x = (WIDTH - self.label_Width) // 2
        self.label_y = (HEIGHT - self.label_Height - 100) // 2

        self.window_surface = window_surface
        self.manager = manager
        self.connected = False
        self.setup_ui()
        self.time = 0

    def setup_ui(self):
        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.label_x, self.label_y), (self.label_Width, self.label_Height)),
            text=self.label_text,
            manager=self.manager
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.back_button_x, self.back_button_y), (self.back_button_Width, self.back_button_Height)),
            text='Back',
            manager=self.manager
        )
    
    def connect_to_server(self):
        client.socketSetup()
        self.connected = True

    def run(self, main):
        # イベント管理
        is_running = True
        count = 0
        indicator_list = ["", "w", "ww", "www"]
        print("loop_start")

        while is_running:
            time_delta = main.clock.tick(60) / 1000.0  # 更新用の時計
            self.time += time_delta
            if not self.connected:
                print(f"connect_start")
                self.connect_to_server()
                client.setUp()
            else:
                print("start_battle_screen")
                is_running = False
                main.show_battle_screen()

            if self.time > 1:
                self.label.set_text("Matching now" + indicator_list[count % 4])
                count += 1
                self.time = 0

            for event in pygame.event.get():  # 入力ごとの処理
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.back_button:
                        main.show_start_screen()
                        is_running = False


                self.manager.process_events(event)
            self.manager.update(time_delta)

            # 画面更新
            self.window_surface.blit(main.background, (0, 0))
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()


class BattleScene:
    def __init__(self, window_surface, manager):
        self.window_surface = window_surface
        self.manager = manager
        self.grid_rows = 4
        self.grid_columns = 13
        self.panel_width = 50
        self.panel_height = 100
        self.panel_index_map = {}
        self.now_player_label = "hehe"
        self.panels = self.create_panel_grid()
        self.time = 0
        self.setImages()
        print("client Setup")

    def setImages(self):
        self.image_card = [None] * 52
        for i in range(52):
            if 0 <= i <= 8:
                f = f"image/cards/card_club_0{i+1}.png"
            elif 9 <= i <= 12:
                f = f"image/cards/card_club_{i+1}.png"
            elif 13 <= i <= 21:
                f = f"image/cards/card_diamond_0{i-13+1}.png"
            elif 22 <= i <= 25:
                f = f"image/cards/card_diamond_{i-13+1}.png"
            elif 26 <= i <= 34:
                f = f"image/cards/card_heart_0{i-26+1}.png"
            elif 35 <= i <= 38:
                f = f"image/cards/card_heart_{i-26+1}.png"
            elif 39 <= i <= 47:
                f = f"image/cards/card_spade_0{i-39+1}.png"
            elif 48 <= i <= 51:
                f = f"image/cards/card_spade_{i-39+1}.png"
            self.image_card[i] = pygame.image.load(f)
            self.image_card[i] = pygame.transform.scale(self.image_card[i], (50, 100))

    def create_panel_grid(self):
        #isNowPlayerpanel
        self.isPlayerPanel = pygame_gui.elements.UILabel(
            relative_rect = pygame.Rect((100,530),(820,120)),
            text = self.now_player_label,
            manager=self.manager
        )
        self.image_surface = pygame.image.load('image/cards/card_back.png')
        self.image_surface = pygame.transform.scale(self.image_surface, (50, 100))
        panels = []
        self.cardback_elements = []
        for i in range(self.grid_rows):#4
            row = []
            cardback_row = []
            for j in range(self.grid_columns):#13
                panel = pygame_gui.elements.UIPanel(
                    relative_rect=pygame.Rect((100 + 60 * j, 100 + 110 * i), (50, 100)),
                    manager=self.manager,
                    visible=True
                )
                cardback_element = pygame_gui.elements.UIImage(
                    relative_rect=pygame.Rect((0, 0), (50, 100)),
                    image_surface=self.image_surface,
                    manager=self.manager,
                    container=panel,
                    starting_height=2
                )
                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((0, 0), (50, 100)),
                    text='',
                    manager=self.manager,
                    container=panel,
                    starting_height=1
                )
                row.append(panel)
                cardback_row.append(cardback_element)
                self.panel_index_map[button] = (i + 1, j + 1)
            panels.append(row)
            self.cardback_elements.append(cardback_row)
        return panels

    def draw(self):
        for row in self.panels:
            for panel in row:
                panel.set_position(panel.get_relative_rect().topleft)

    def run(self, main):
        is_running = True
        while is_running:
            if client.is_game_Finish == True:
                self.isPlayerPanel.set_text(client.is_game_winner)
                self.check_card_situation(client.get_cards())
                self.manager.update(time_delta)
                self.window_surface.blit(main.background, (0, 0))
                self.draw()
                self.manager.draw_ui(self.window_surface)
                pygame.display.update()
                is_running = False
                break

            client.TurnTask()

            if client.check_turn() == True:
                self.isPlayerPanel.set_text("your turn")
            else:
                self.isPlayerPanel.set_text("opponent's turn")
            time_delta = main.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    break

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element in self.panel_index_map:
                        print("button_Pressed")
                        if client.check_turn() == True:
                            index = self.panel_index_map[event.ui_element]
                            print("情報を送リます")
                            client.revealCard(index)
                            card_info = client.getCards(index)
                            print(card_info)
                            card_kind = card_info.getNum()  # Cardオブジェクトからカードの番号を取得
                            self.setPanel(index[0] - 1, index[1] - 1, card_kind)


                self.manager.process_events(event)
            self.check_card_situation(client.get_cards())
            self.manager.update(time_delta)

            self.window_surface.blit(main.background, (0, 0))
            self.draw()
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()
        sleep(10)
        pygame.quit()
        sys.exit()

    def setPanel(self, i, j, kind):
        list_card = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        panel_index = list_card.index(kind)
        self.cardback_elements[i][j].set_image(self.image_card[panel_index])

    def setPanel_getted_card(self,i,j,kind):
        list_card = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        panel_index = list_card.index(kind)
        image_path = ""
        if 0 <= panel_index <= 8:
            image_path = f"image/cards/card_club_0{panel_index+1}.png"
        elif 9 <= panel_index <= 12:
            image_path = f"image/cards/card_club_{panel_index+1}.png"
        original_image = pygame.image.load(image_path)
        original_image = pygame.transform.scale(original_image, (50, 100))
        #画像処理(ブラック)
        dark_image = original_image.copy()
        darken_amount = 80
        dark_image_surface = pygame.Surface(dark_image.get_size()).convert_alpha()
        dark_image_surface.fill((0,0,0,darken_amount))
        dark_image.blit(dark_image_surface,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
        #画像セット
        self.cardback_elements[i][j].set_image(dark_image)



    def check_card_situation(self,cards):
        x = 0
        for card in cards.cards:
            if card.getNumber() == "*":
                self.cardback_elements[x//13][x%13].set_image(self.image_surface)
            else:
                if(card.is_card_get() == False):
                    self.setPanel(x//13,x%13,card.getNumber())
                else:
                    self.setPanel_getted_card(x//13,x%13,card.getNumber())

            x += 1
                    
                                    
                





class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('神経衰弱Ⅰ')
        self.window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill(pygame.Color('#FFFFFF'))
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path="UI.json")
        self.clock = pygame.time.Clock()
        self.current_screen = None

    def show_start_screen(self):
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path="UI.json")
        self.current_screen = StartScreen(self.window_surface, self.manager)
        self.current_screen.run(self)

    def show_match_screen(self):
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path="UI.json")
        self.current_screen = MatchScreen(self.window_surface, self.manager)
        print("matchscreen_run_start")
        self.current_screen.run(self)

    def show_battle_screen(self):
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path="UI.json")
        self.current_screen = BattleScene(self.window_surface, self.manager)
        print("aiueo")
        self.current_screen.run(self)

    def run(self):
        self.show_start_screen()

if __name__ == "__main__":
    main = Main()
    main.run()