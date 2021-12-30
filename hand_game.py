import cv2
import mediapipe as mp
import time
import random

cap = cv2.VideoCapture(0)#鏡頭
mpHands = mp.solutions.hands#讀取手
hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

game=0#遊戲頁面(模式)
end=False#結束程式

def Play(reball,xball,yball,pause,score):#遊戲過程
    if reball:#抽目標球位置
        xball,yball=(random.random()*0.7+0.15), (random.random()*0.6+0.25)
        reball=False
    else:
        cv2.putText(img, f"Score : {int(score)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 3)
        cv2.putText(img, "stop", (550, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 3)
        cv2.circle(img, (int(xball*imgWidth), int(yball*imgHeight)), 10, (0, 0, 255), cv2.FILLED)#顯示目標球
    if xball-0.03<lmX8<xball+0.03 and yball-0.03<lmY8<yball+0.03 and not pause:#碰到球
        score+=1
        reball=True
    if 0.85<lmX8 and lmY8<0.12:#按停止
        pause=True
    return reball,xball,yball,pause,score
while True:
    ret, img = cap.read()
    img=cv2.flip(img,1)
    if ret:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)

        imgHeight = img.shape[0]
        imgWidth = img.shape[1]

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                for i, lm in enumerate(handLms.landmark):
                    if i == 8:#讀取食指位置
                        cv2.circle(img, (int(lm.x * imgWidth), int(lm.y * imgHeight)), 10, (150, 0, 0), cv2.FILLED)
                        #cv2.circle(圖片, (x位置), y位置), 大小, 顏色, 狀態(填滿))
                        lmX8=lm.x#紀錄
                        lmY8=lm.y
                        break
        
        if game == 0:#首頁
            cv2.putText(img, "Free Game | Challenge", (15, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (0, 100, 255), 5)
            #cv2.putText(圖片, 文字, (x位置, y位置), 字體, 大小, 顏色, 粗細)
            cv2.putText(img, "End", (550, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 100, 255), 3)
            
            try:#若有讀到手
                if 0.05<lmX8<0.45 and 0.1<lmY8<0.2:#選Free Game
                    game=1
                elif 0.55<lmX8<0.95 and 0.1<lmY8<0.2:#選Challenge
                    game=2
                    cstart=False#正式開始(讀完秒)
                    t=time.time()#遊戲開始時間
                elif 0.85<lmX8 and 0.86<lmY8:#點選End
                    end=True
                if end:#再次確認是否關閉遊戲
                    cv2.putText(img, "Yes | N0", (210, 290), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (0, 100, 255), 5)
                    if 0.28<lmX8<0.46 and 0.5<lmY8<0.62:#選Yes
                        break
                    elif 0.54<lmX8<0.72 and 0.5<lmY8<0.62:#選No
                        end=False
            except:
                pass
            reball=True#重新抽目標球
            xball=yball=0
            score=0#分數
            pause=False#暫停
        elif game == 1:
            reball,xball,yball,pause,score=Play(reball,xball,yball,pause,score)
            if pause:#再次確認
                cv2.putText(img, "Yes | N0", (210, 290), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (0, 100, 255), 5)
                if 0.28<lmX8<0.46 and 0.5<lmY8<0.62:#遊戲結束
                    game=0
                elif 0.54<lmX8<0.72 and 0.5<lmY8<0.62:#遊戲繼續
                    pause=False
        elif game == 2:
            if cstart:#讀完秒，正式開始
                reball,xball,yball,pause,score=Play(reball,xball,yball,pause,score)
                if pause:
                    cv2.putText(img, "Yes | N0", (210, 290), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (0, 100, 255), 5)
                    tgameP=t+30-time.time()#暫停時間
                    if 0.28<lmX8<0.46 and 0.5<lmY8<0.62:
                        game=0
                    elif 0.54<lmX8<0.72 and 0.5<lmY8<0.62:
                        pause=False
                        t+=tgame-tgameP
                else:#計時
                    tgame=t+30-time.time()
                cv2.putText(img, f"Time : %.3f"%(tgame), (260, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 3)
                if tgame<=0:
                    tgame=0
                    game=3
            else:#讀秒
                tstart=int(t+4-time.time())
                if tstart<=0:
                    cstart=True
                    t=time.time()
                cv2.putText(img, f"{(tstart)}", (280, 240), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 100, 255), 10)
        elif game==3:#challenge顯示結果
            cv2.putText(img, f"score: {(score)}", (160, 240), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 100, 255), 8)
            cv2.putText(img, "Back", (30, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 100, 255), 3)
            if lmX8<0.2 and 0.86<lmY8:
                game=0
        cv2.imshow('Hand Game', img)#顯示文字圖案
    if cv2.waitKey(1) == ord('q'):#關閉遊戲
        break