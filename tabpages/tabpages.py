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

def draw_judgment_grid(surface):
    bias = 90
    pagesize = 15
    baserect = Rect(555, 90, 335, 30)
    pygame.draw.rect(surface, (255, 255, 255), \
        (baserect.left, baserect.top, baserect.width, baserect.height * pagesize), 2)
    for i in range(pagesize):
        pygame.draw.line(surface, (255, 255, 255), \
            (baserect.left, baserect.top + baserect.height * (i + 1)), \
            (555 + 335, bias + 30 * (i + 1)), 2)
    pygame.draw.line(surface, (255, 255, 255),\
        (baserect.left + 75, baserect.top), (baserect.left + 75, baserect.top + baserect.height * pagesize), 2)
    pygame.draw.line(surface, (255, 255, 255), \
        (baserect.left + 173, baserect.top), (baserect.left + 173, baserect.top + baserect.height * pagesize), 2)
    pygame.draw.line(surface, (255, 255, 255), \
        (baserect.left + 245, baserect.top), (baserect.left + 245, baserect.top +baserect.height * pagesize), 2)

# surface 描画対象、 fnt 描画のためのフォント、
# logmsg ログメッセージ、 pagenum 表示ページの指定
def draw_judgement_state(surface, fnt, logmsg, pagenum):
    baserect = Rect(555, 90, 335, 30)  # ログの表示領域の一段分
    pagesize = 15 # ページ当たりのログ数
    pages = 4 #最大ページ数
    judgement_pages = [["" for i in range(pagesize)] for j in range(pages)]
    # 15x5ページ分のリストを用意します judgement_pages[ログ][ページ]

    pygame.draw.rect(surface, (0,0,0), \
        (baserect.left, baserect.top, baserect.width, baserect.height * pagesize))
    # ログ表示領域の背景を黒で初期化

    for i in range(pages):
        for j in range(pagesize):
            if i*pagesize+j < len(logmsg):
                judgement_pages[i][j] = logmsg[i*pagesize+j]
    # ログを、ページに書き写す　１次元配列→２次元配列化
    for i in range(pagesize):
        if len(logmsg) != 0 and i == (len(logmsg) - 1) % pagesize:
        # ログが空じゃなくて、iが指定ページの表示できる範囲内なら描画
            pygame.draw.rect(surface, (100, 0, 0), \
                (baserect.left, baserect.top + baserect.height * i, baserect.width, baserect.height))
            # 一番新しいログは目立つように色を変える
        text1 = fnt.render(judgement_pages[pagenum][i], True, (255, 255, 255))
        surface.blit(text1, (baserect.left+5, baserect.height * i + baserect.top+10 - 3))
        # 描画テキストを生成し描画
    # ４ページあるうちの指定されたページのログを描画する

def draw_tabs(surface, tabnumber, tabimage, atabimage, tabrect):
    baserect = Rect(555, 90, 335, 30)  # ログの表示領域の一段分
    tabsize = [83, 39]
    for i in range(4):
        if i == tabnumber: # 指定されたタブならば、赤いタブ画像
            # surface.blit(tabimage[i], (baserect.left + i * tabsize[0], baserect.top - tabsize[1]))
            surface.blit(tabimage[i], tabrect[i])
        else: #それ以外は緑のタブ画像で表示
            # surface.blit(atabimage[i], (baserect.left+i*tabsize[0], baserect.top - tabsize[1]))
            surface.blit(atabimage[i], tabrect[i])

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


    tabimagelist = []
    tabimagename = []
    for i in range(4):
        tabimagename.append("tab"+str(i+1) + ".png")
    for i in range(4):
        tabimagelist.append(pygame.image.load("./images/" + tabimagename[i]))
    atabimagelist = []
    atabimagename = []
    for i in range(4):
        atabimagename.append("tab" + str(i + 1) + "a.png")
    for i in range(4):
        atabimagelist.append(pygame.image.load("./images/" + atabimagename[i]))
    tabimagerect = []
    for i in range(4):
        tabimagerect.append(Rect(555 + i * 83, 90 - 39, 85, 40))
    # baserect = Rect(555, 90, 335, 30) 描画領域から、タブの位置を逆算してます
    # tab画像の大きさは　83x39で計算　描画は85x40で描画しています。


    players_input = []
    question = []
    input_status = 0 # 1 入力エラー 2 重複エラー 3 正解
    current_tab = 0

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
            # for i in range(len(anslog)):
            #     text = log_font.render(anslog[i], True, (255, 255, 255))
            #     screen.blit(text, (560, 30 * i + 100 - 3))
            draw_judgement_state(screen, log_font, anslog, current_tab)
            draw_tabs(screen, current_tab, tabimagelist, atabimagelist, tabimagerect)
            draw_judgment_grid(screen)
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
                            current_tab = (len(anslog) - 1) // 15
                            turn += 1
                            if judge[0] == 4:
                                input_status = 3
                                gamescene = 2

                    elif gamescene == 2:
                        gamescene = 0
                    else:
                        gamescene = -1
                for i in range(len(tabimagerect)):
                    if gamescene == 1:
                        if tabimagerect[i].collidepoint(event.pos):
                            current_tab = i
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

