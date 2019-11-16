import sys
import random

def has_not_duplicates(seq):
    return len(seq) == len(set(seq))

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
    turn = 1
    ans = make_question()
    print("Hit＆Blowゲーム！")

    while True:
        print("第%02d手目" % turn)
        print("４桁の重複しない数字を入力してください。")
        print("->", end="")
        hit = 0
        blow = 0
        tmp = input()
        your_input = []
        for i in tmp:
            your_input.append(int(i))
        if has_not_duplicates(your_input):
            hit, blow = judgement(your_input, ans)
            print("hit = "+str(hit)+", blow = " + str(blow))
            if hit == 4:
                print("おめでとう! %02d手目で正解です :" % turn)
                break
            else:
                turn += 1



if __name__ == "__main__":
        main()