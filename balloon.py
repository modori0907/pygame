# from pgzero import clock, actor
# from pygame import Rect
from random import randint

import pgzrun

WIDTH = 800
HEIGHT = 600

baloon = Actor("balloon")
baloon.pos = 400, 300

bird = Actor("bird-up")
bird.pos = randint(800, 1600), randint(10, 200)

house = Actor("house")
house.pos = randint(800, 1600), 450

tree = Actor("tree")
tree.pos = randint(800, 1600), 450

bird_up = True
up = False
game_over = False
score = 0
# 画面尾更新回数を記録する
number_of_updates = 0

scores = []


def update_high_scores():
    global score, scores
    filename = r"high-scores.txt"
    scores = []
    # 現在のハイスコアを呼び出す処理
    with open(filename, "r") as file:
        line = file.readline()
        # high_scoresをリストにしている
        high_scores = line.split()
        # はいすこあを全部取り出してそれぞれ比較している
        for high_score in high_scores:
            if (score > int(high_score)):
                scores.append(str(score) + " ")
                score = int(high_score)
            else:
                scores.append(str(high_score) + " ")
    with open(filename, "w") as file:
        for high_score in scores:
            file.write(high_score)


def display_high_scores():
    screen.draw.text("HIGH SCORES", (350, 150), color="black")
    y = 175
    position = 1
    for high_score in scores:
        screen.draw.text(str(position) + ". " + high_score, (350, y), color="black")
        y += 25
        position += 1


# 風景の描画
def draw():
    screen.blit("background", (0, 0))
    if not game_over:
        baloon.draw()
        bird.draw()
        house.draw()
        tree.draw()
        screen.draw.text("Score: " + str(score), (700, 5), color="black")
    else:
        display_high_scores()


# マウスが押された時の関数
def on_mouse_down():
    global up
    up = True
    baloon.y -= 50


# マウスが離された時の関数
def on_mouse_up():
    global up
    up = False


# 鳥の動き
def flap():
    global bird_up
    if bird_up:
        bird.image = "bird-down"
        bird_up = False
    else:
        bird.image = "bird-up"
        bird_up = True


def update():
    global game_over, score, number_of_updates
    if not game_over:
        if not up:
            # 気球が下がる処理 global upがTrueでない場合（つまり、マウスを押していない時）
            baloon.y += 1
        if bird.x > 0:
            # 画面左上が座標(0, 0)
            bird.x -= 4
            """
            update()関数は毎秒60回実行されている、この関数を呼び呼び出すたびに鳥の画像を変更してしまうと
            画像がぼやけてしまうので、関数が１０回呼び出されたら画像をか会えるように変更している
            """

            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            bird.x = randint(800, 1600)
            bird.y = randint(10, 200)
            score += 1
            number_of_updates = 0

        if house.right > 0:
            house.x -= 2
        else:
            house.x = randint(800, 1600)
            score += 1

        if tree.right > 0:
            tree.x -= 2
        else:
            tree.x = randint(800, 1600)
            score += 1

        if baloon.top < 0 or baloon.bottom > 560:
            game_over = True
            update_high_scores()

        # 衝突の判別
        if baloon.collidepoint(bird.x, bird.y) or \
                baloon.collidepoint(house.x, house.y) or \
                baloon.collidepoint(tree.x, tree.y):
            game_over = True
            update_high_scores()


pgzrun.go()
