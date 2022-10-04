import pgzrun
from pgzero import clock
from pygame import Rect

WIDTH = 1280
HEIGHT = 720

main_box = Rect(0, 0, 820, 240)
timer_box = Rect(0, 0, 240, 240)
answer_box1 = Rect(0, 0, 495, 165)
answer_box2 = Rect(0, 0, 495, 165)
answer_box3 = Rect(0, 0, 495, 165)
answer_box4 = Rect(0, 0, 495, 165)

main_box.move_ip(50, 40)
timer_box.move_ip(990, 40)
answer_box1.move_ip(50, 338)
answer_box2.move_ip(735, 358)
answer_box3.move_ip(50, 538)
answer_box4.move_ip(735, 538)

answer_boxes = [answer_box1, answer_box2, answer_box3, answer_box4]

score = 0
time_left = 10

q1 = ["What is the capital of France?",
      "London", "Paris", "Berlin", "Tokyo", 2]
q2 = ["梨絵の昔の名前は?",
      "ジャイ子", "たけし", "すねお", "もんくいうこ", 4]

questions = [q1, q2]
# 一番上にある（つまりquestion[0]を取り出して、questionにいれる
# questionにはq1が入っている。次にpopが使われると今度はq2が使われる（q1は取り出されている）
question = questions.pop(0)


# 名前解決をしようとするとうまく表示できなくなる
# pygame zeroは日本語がつかえないっぽい
def draw():
    screen.fill("dim grey")
    screen.draw.filled_rect(main_box, "sky blue")
    screen.draw.filled_rect(timer_box, "sky blue")

    for box in answer_boxes:
        screen.draw.filled_rect(box, "orange")

    #どうすれば日本語になるか検討
    screen.draw.textbox(str(time_left), timer_box, color=("black"))
    screen.draw.textbox(question[0], main_box, color=("black"))

    # 問題文は取り出されているので、回答が取り出される

    index = 1
    for box in answer_boxes:
        screen.draw.textbox(question[index], box, color=("black"))
        index += 1


def game_over():
    global question, time_left
    message = "Game over. You got %s questions correct" % str(score)
    question = [message, "-", "-", "-", "-", "-", 5]
    time_left = 0


def correct_answer():
    global question, score, time_left

    score = score + 1
    if questions:
        # 　問題が残っていたら取り出す処理
        question = questions.pop(0)
        time_left = 10

    else:
        print("End of questions")
        game_over()


def on_mouse_down(pos):
    # 答えのボックスのリストをチェックする
    index = 1
    # index1は押下した場所によって変わる　ボックスのans1を押下したのであれば１でとまる
    # 2,3,と増えていく　ボックスの番号がふえることで
    for box in answer_boxes:
        if box.collidepoint(pos):
            print("Clicked on answer" + str(index))
            # 答えの番号と同じであれば
            if index == question[5]:
                print("You got it correct")
                correct_answer()
            else:
                game_over()
        index += 1


def update_time_left():
    global time_left

    if time_left:
        time_left = time_left - 1

    else:
        game_over()


clock.schedule_interval(update_time_left, 1.0)

pgzrun.go()
