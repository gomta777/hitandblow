from pygame.locals import *
import pygame
import sys
import random



def main():
    gamestate = 0  # 0 タイトル、1 ゲーム中、2 ゲームオーバー、-1 エラー
    pygame.init()  # Pygameを初期化
    screen = pygame.display.set_mode((900, 600))  # 画面を作成
    pygame.display.set_caption("Hit & Blow game")
    # フォントの用意
    # print(pygame.font.get_fonts())  # 使えるフォントの一覧を表示する
    font1 = pygame.font.SysFont("yumincho", 20)
    font2 = pygame.font.SysFont("meiryomeiryomeiryouimeiryouiitalic", 50)

    gamebutton = []
    gamebuttonrect = Rect(200, 250, 200, 50) # 画像の表示位置を表す矩形
    gamebutton.append(pygame.image.load("./images/pushstart.png"))
    gamebutton.append(pygame.image.load("./images/judge.png"))
    gamebutton.append(pygame.image.load("./images/gameover.png"))



    running = True
    # メインループ

    while running:
        screen.fill((100, 100, 100))  # 背景色で塗る

        if gamestate == 0:
            screen.blit(gamebutton[0], gamebuttonrect)
        elif gamestate == 1:
            screen.blit(gamebutton[1], gamebuttonrect)
        elif gamestate ==2:
            screen.blit(gamebutton[2], gamebuttonrect)
        else:
            print("error")


        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                running = False
                pygame.quit()  # pygameのウィンドウを閉じる
                sys.exit()  # システム終了
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if gamebuttonrect.collidepoint(event.pos):
                    if gamestate == 0:
                        gamestate = 1
                    elif gamestate == 1:
                        gamestate = 2
                    elif gamestate == 2:
                        gamestate = 0
                    else:
                        gamestate = -1

        pygame.display.update()  # 描画処理を実行

if __name__ == "__main__":
    main()