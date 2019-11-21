from pygame.locals import *
import pygame
import sys
import random


def has_duplicates(seq):
    return len(seq) != len(set(seq))

def judgement(yin, ans):
    h=0
    b=0
    for i in range(len(yin)):
        if yin[i] == ans[i]:
            h += 1
        else:
            if yin[i] in ans:
                b += 1
    return([h, b])

def make_question():
    nums = list(range(10))
    return(random.sample(nums, 4))



def main():
    gamescene = 0  # 0 タイトル、1 ゲーム中、2 ゲームオーバー、-1 エラー
    input_pos = 0  # 現在の入力位置　左０１２３右　０，１，２，３の後は０に戻りループ

    pygame.init()  # Pygameを初期化
    screen = pygame.display.set_mode((900, 600))  # 画面を作成
    pygame.display.set_caption("Hit & Blow game")

    # フォントの用意
    # print(pygame.font.get_fonts())  # 使えるフォントの一覧を表示する
    gamemessage = []
    mes_font = pygame.font.SysFont("yumincho", 40)
    gamemessage.append(mes_font.render("エラー：数字が正しくない", True, (255, 0, 0)))
    gamemessage.append(mes_font.render("エラー：数字が重複", True, (255, 0, 0)))
    gamemessage.append(mes_font.render("CONGRATULATIONS", True, (255, 0, 0)))

    title_font = pygame.font.SysFont("arialblack", 50)
    title = title_font.render("Hit & Blow !", True, (255, 0, 0))
    titlepos = [150, 100]

    anslog = []
    log_font = pygame.font.SysFont("yumincho", 20)
    turn = 1

    gamebutton = []
    gamebuttonrect = Rect(200, 250, 200, 50) # 画像の表示位置を表す矩形
    gamebutton.append(pygame.image.load("./images/pushstart.png"))
    gamebutton.append(pygame.image.load("./images/judge.png"))
    gamebutton.append(pygame.image.load("./images/gameover.png"))

    margin = [100, 100] # ＊を表示する位置までのマージン
    imagesize = [100,100] # 画像１個当たりの大きさ

    qfilestr = [] # 画像ファイル名を生成するためのリスト
    qimagelist = []  # 出題用の画像を保存しておくリスト０～９＋＊の画像が収まっている。
    for i in range(10): # 問題の方の画像ファイルは　00.png~99.pngの名前になっている。
        qfilestr.append(str(i)+str(i) + ".png")  # 画像ファイル名を生成
    for i in range(10): # 画像の読み込み
        qimagelist.append(pygame.image.load("./images/" + qfilestr[i]))
    qimagelist.append(pygame.image.load("./images/kome.png")) # ＊の画像の読み込み
    #[00.png, 11.png, 22.png … 99.png, kome.png]
    qbuttonrect = [] #　＊を表示するための矩形を作成　＊のサイズは（１００，１００）
    for i in range(4): #marginの位置から４つ横に画像を並べるためのもの
        qbuttonrect.append(Rect(margin[0] + i * imagesize[1], margin[1], *imagesize))

    nmargin = [50, 350] # 入力ボタンのためのマージン

    filestr  = [] # 画像ファイル名を収めるリスト
    for i in range(10): # 読み込む画像ファイル名のリストを作る
        filestr.append(str(i) + ".png")
    imagelist = [] # 読み込んだ画像のリスト
    for i in range(10):
        imagelist.append(pygame.image.load("./images/" + filestr[i])) #ファイルの読み込み
    buttonrect = [] # 画像ファイルの貼り付け位置が収められたリスト（Rect型）
    for i in range(5): # 0~4の画像の位置
        buttonrect.append(Rect(nmargin[0] + i * imagesize[0], nmargin[1], *imagesize))
    for i in range(5, 10): # 5~9の画像の位置
        buttonrect.append(Rect(nmargin[0] + (i - 5) * imagesize[0], nmargin[1]+imagesize[1], *imagesize))

    players_input = []
    question = []
    input_status = 0 # 1 入力エラー 2 重複エラー 3 正解
    running = True
    # メインループ

    while running:
        screen.fill((100, 100, 100))  # 背景色で塗る
        # この時点では、　screen.blit(gamebutton[gamescene], gamebuttonrect) で済むけど、
        # とりあえずは、if文でわけておく
        if gamescene == 0:
            screen.blit(title, titlepos)
            screen.blit(gamebutton[0], gamebuttonrect)
        elif gamescene == 1:
            for i in range(4): # 入力された数字を表示する領域
                if players_input[i] == -1:
                    screen.blit(qimagelist[10], qbuttonrect[i])
                else:
                    screen.blit(qimagelist[players_input[i]], qbuttonrect[i])

            for i in range(5): # 入力のためのボタンとなる画像０～４
                screen.blit(imagelist[i], buttonrect[i])
            for i in range(5, 10): # 入力のためのボタンとなる画像５～９
                screen.blit(imagelist[i], buttonrect[i])
            screen.blit(gamebutton[1], gamebuttonrect)
            pygame.draw.rect(screen, (255, 0, 0), qbuttonrect[input_pos], 3)
            if input_status > 0:
                screen.blit(gamemessage[input_status-1], (80, 30))
            for i in range(len(anslog)):
                text = log_font.render(anslog[i], True, (255, 255, 255))
                screen.blit(text, (560, 30 * i + 100 - 3))
        elif gamescene == 2:
            screen.blit(gamemessage[input_status - 1], (100, 100))
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
                    if gamescene == 0:
                        question = make_question()
                        print(question)
                        players_input = [-1, -1, -1, -1]
                        gamescene = 1
                        input_status = 0
                        anslog.clear()
                    elif gamescene == 1:
                        if -1 in players_input:
                            input_status = 1
                        elif has_duplicates(players_input):
                            input_status = 2
                        else:
                            judge = judgement(players_input, question)
                            anslog.append("%02d 回目 " % turn + str(players_input) + \
                            "  " + str(judge[0]) + " HIT  " + str(judge[1]) + " BLOW")
                            turn += 1
                            if judge[0] == 4:
                                input_status = 3
                                gamescene = 2
                    elif gamescene == 2:
                        gamescene = 0
                    else:
                        gamescene = -1
                for i in range(len(buttonrect)):
                    if buttonrect[i].collidepoint(event.pos):
                        input_status = 0
                        players_input[input_pos] = i
                        input_pos += 1
                        if input_pos == 4:
                            input_pos = 0


        pygame.display.update()  # 描画処理を実行


if __name__ == "__main__":
    main()

