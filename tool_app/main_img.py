import tkinter
import PIL
import cv2
from PIL import Image, ImageTk, ImageOps  # 画像関連
from pathlib import Path
import datetime
# import schedule
import time
import sys
import numpy as np
import pandas as pd
import torch
from facenet_pytorch import MTCNN
from hsemotion.facial_emotions import HSEmotionRecognizer


def get_path():
    """
    このプロジェクトを管理している親フォルダーの絶対リンクを取得する。
    parents[1]は1個前を取得するので、階層を変えるとその数に合わせて変更の必要がある。
    """
    folder_path = Path(__file__).resolve().parents[1]
    return folder_path


def mk_dir(folder_path):
    """
    写真保存用と結果保存用ののディレクトリとそのパスを作成する
    """
    str_date = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    default_path = folder_path / "photos" / str(str_date)
    photos_path = default_path / "images"
    table_path = default_path / "result"
    Path(default_path).mkdir()
    Path(photos_path).mkdir()
    Path(table_path).mkdir()
    return photos_path, table_path


class CameraApplication(tkinter.Frame):
    def __init__(self, photos_path: str, table_path: str, master=None):
        # （tkinter.Frame）の初期化
        super().__init__(master)
        # カメラ --------------------------------------------------------------
        # USBカメラの設定(idは、webカメラ非接続時: 0 = 内蔵、webカメラ接続時: 0 = web)
        camera_id = 0
        self.cap = cv2.VideoCapture(camera_id)
        # 撮影制御用(True:撮影中  False:停止中)
        self.cap_flg = False

        # 基本情報 ------------------------------------------------------------
        # 他の処理用
        self.root = root
        # タイトル
        root.title('表情認識カメラアプリ')
        # ウィンドサイズ
        root.geometry('1600x1200')

        # 構成要素 -------------------------------------------------------------
        # ラベル-1
        label_cam = tkinter.Label(root, text='インタビュイーの感情')
        label_cam.pack()
        # ラベル-2
        self.label_quality = tkinter.Label(root, text='画質')
        self.label_quality.pack()

        # スタート/ストップボタン
        button_1 = tkinter.Button(
            text='START/STOP', width=30, command=self.start_stop)
        button_1.pack(side=tkinter.BOTTOM)

        # 終了ボタン
        button_2 = tkinter.Button(
            text='QUIT', width=30, command=self.quit_app)
        button_2.pack(side=tkinter.BOTTOM)

        # キャンバス(画像表示)
        self.canvas_cam = tkinter.Canvas(
            self.master, width=1280, height=960, bg='black')
        self.id = self.canvas_cam.create_text(
            640, 360, text="Some Text", fill="white",
            font=("Helvetica 120 bold"))
        self.canvas_cam.pack()

        # canvasのサイズ取得
        self.canvas_cam.update()
        self.canvas_w = self.canvas_cam.winfo_width()
        self.canvas_h = self.canvas_cam.winfo_height()

        # 顔認識用のセッティング ----------------------------------------------------
        # 使用するプロセッサーの確認
        use_cuda = torch.cuda.is_available()
        device = 'cuda' if use_cuda else 'cpu'

        # 人の顔の切り出し用の関数
        self.mtcnn = MTCNN(keep_all=False, post_process=False,
                           min_face_size=40, device=device)

        # 利用する顔認識モデル
        model_name = 'enet_b0_8_best_vgaf'
        # model_name = 'enet_b0_8_best_afew'
        # model_name='enet_b0_8_va_mtl'
        # model_name='enet_b2_8'
        self.fer = HSEmotionRecognizer(model_name=model_name, device=device)

        # 感情を表す文字・顔文字の辞書
        self.char = {
            'Anger': "ネガティブ",     # 怒り
            'Contempt': "ネガティブ",  # 軽蔑
            'Disgust': "ネガティブ",   # 嫌悪感
            'Fear': "ネガティブ",      # 恐れ
            'Happiness': "幸福",  # 幸福
            'Neutral': "真顔",   # ニュートラル
            'Sadness': "ネガティブ",   # 悲しみ
            'Surprise': "驚き",   # 驚き
            "Unknown": "顔が認識できない"
        }
        """
        驚き : http://www.kaomoji.com/kao/text/odoroku.htm
        幸せ : http://www.kaomoji.com/kao/text/yorokobu.htm
        真顔 : http://www.kaomoji.com/kao/text/bisyou.htm
        ネガティブ : http://www.kaomoji.com/kao/text/fumann.htm
        "Unknown" : 
        """
        self.kaomoji = {
            'Anger': "（￣へ￣； ムムム",     # 怒り
            'Contempt': "（￣へ￣； ムムム",  # 軽蔑
            'Disgust': "（￣へ￣； ムムム",   # 嫌悪感
            'Fear': "（￣へ￣； ムムム",      # 恐れ
            'Happiness': "(@^∇^@) わぁーい",  # 幸福
            'Neutral': "（￣ー￣）フッ",   # ニュートラル
            'Sadness': "（￣へ￣； ムムム",   # 悲しみ
            'Surprise': "(°д°;;) ナント！",   # 驚き
            "Unknown": "メ（一o一) バツ！"  # 認識できなかった時
        }

        # 得られたスコアを記録するテーブルを作成
        cols = [
            'date', 'photo_path', "emotion", 'Anger',
            'Contempt', 'Disgust', 'Fear', 'Happiness',
            'Neutral', 'Sadness', 'Surprise'
        ]
        self.df = pd.DataFrame(index=[], columns=cols)

        # 写真と結果をまとめたテーブルの保存場所
        self.photos_path = photos_path
        self.table_path = table_path

    # ボタンイベント(START/STOP)----------------------------------------------------

    def start_stop(self):
        print('-def start_stop()')
        # global self.cap_flg
        if self.cap_flg:
            # 動画を停止
            self.cap_flg = False
        else:
            # 動画を再生(画像の取得を開始・継続する)
            self.cap_flg = True
            self.start_video()

    # ボタンイベント(QUIT)----------------------------------------------------
    def quit_app(self):
        self.df.to_csv(self.table_path / "result.csv", index=None)
        self.root.destroy()

    # 人の顔を検出する関数----------------------------------------------------

    def detect_face(self, frame):
        bounding_boxes, probs = self.mtcnn.detect(frame, landmarks=False)

        # 顔が検出されなかった時
        if probs is None or bounding_boxes is None:
            print("顔が検出されませんでした。")
            return bounding_boxes
        # 顔が検出された時
        else:
            bounding_boxes = bounding_boxes[probs > 0.9]
            # print(len(bounding_boxes), probs)
            return bounding_boxes

    # 表情認識モデル呼び出し
    def face_model(self, frame):
        # デフォルト値の設定
        emotion = "Unknown"
        scores = [0] * 8  # 8要素の0で初期化されたリスト
        face_img = frame
        # 画像の大きさ
        h = 1080  # 画像の高さ
        w = 1920  # 幅

        # 人の顔を検出する
        bounding_boxes = self.detect_face(frame)
        # bounding_boxがNoneなら0を返す。写真はframeをそのまま返す。
        if bounding_boxes is not None:
            # モデルを利用して、表情を分析する
            for bbox in bounding_boxes:
                box = bbox.astype(int)
                x1, y1, x2, y2 = box[0:4]
                # 切り取り領域の判定
                # 座標が画像の範囲内に収まるように調整
                x1 = max(0, min(x1, w))
                y1 = max(0, min(y1, h))
                x2 = max(0, min(x2, w))
                y2 = max(0, min(y2, h))
                # 切り取り範囲が有効かチェック（x1 < x2 かつ y1 < y2）
                if x1 < x2 and y1 < y2:
                    # ここでface_imgを処理
                    face_img = frame[y1:y2, x1:x2, :]
                    emotion, scores = self.fer.predict_emotions(
                        face_img, logits=True)
                else:
                    # 無効な切り取り範囲の場合の処理
                    emotion = "Unknown"
                    scores = [0, 0, 0, 0, 0, 0, 0, 0]
                    face_img = frame
            return emotion, scores, face_img
        else:
            emotion = "Unknown"
            scores = [0, 0, 0, 0, 0, 0, 0, 0]
            face_img = frame
            return emotion, scores, face_img

    # 動画再生(再帰的に自身を呼ぶ)----------------------------------------------------
    def start_video(self):
        # 時間計測開始
        start = time.perf_counter()

        # グローバル変数
        global photo

        # カメラ画像の取得(ret:画像の取得可否のTrue/Flase, frame:RGB画像)
        ret, frame = self.cap.read()
        # 写真をディレクトリに保存
        # 撮影年月日時間秒
        str_date = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
        image_name = self.photos_path / f"{str_date}.jpg"  # 写真の名前を設定
        cv2.imwrite(str(image_name), frame)  # 写真を所定の場所に保存
        # BGRで取得したものをRGBに変換する(写真表示の時のみ)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 表情認識
        emotion, scores, face_img = self.face_model(frame)
        print(emotion, scores)  # デバッグ用
        # 表情認識の結果をself.dfに保存する
        pred_result = [
            str_date, image_name, emotion, scores[0], scores[1], scores[2],
            scores[3], scores[4], scores[5], scores[6], scores[7]
        ]
        self.df.loc[len(self.df)] = pred_result

        # 感情を表す文字を表示するコード ----------------------------------------------
        # new_text = self.char[emotion]
        # self.canvas_cam.itemconfig(self.id, text=new_text)

        # # 感情を表す顔文字を表示するコード ------------------------------------------
        # new_text = self.kaomoji[emotion]
        # self.canvas_cam.itemconfig(self.id, text=new_text)

        # 撮影した画像を表示するコード ------------------------------------------------
        # OpenCV frame を Pillow Photo に変換(canvasに表示するにはPillowの軽視にする必要がある)
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(face_img))
        # canvasに画像を表示
        self.canvas_cam.create_image(
            self.canvas_w/2, self.canvas_h/2, image=photo)
        # 画像サイズをラベルに表示
        self.label_quality['text'] = 'Image shape:'+str(frame.shape)

        # 時間計測終了 処理時間計測 & 1秒より何秒短かったのかを計算-------------------------
        end = time.perf_counter()
        diff_time = (end - start)*1000
        remaining_time = int(1000 - diff_time)
        print(remaining_time)  # デバッグ用

        # 1秒(1000ms)ごとに start_video()を実行(繰り返し)-----------------
        if self.cap_flg:
            if remaining_time < 1000:
                # １秒までの残り時間が１秒未満のとき、残り時間だけ処理を遅らせる
                self.cap_flg = self.after(remaining_time, self.start_video)
            elif remaining_time <= 0:
                # １秒までの残り時間が0秒以下ののとき、100msだけ処理を遅らせる
                self.cap_flg = self.after(100, self.start_video)


if __name__ == '__main__':
    # 写真保存場所のパスを取得 & 作成
    folder_path = get_path()
    photos_path, table_path = mk_dir(folder_path)

    #  アプリ起動
    root = tkinter.Tk()
    app = CameraApplication(photos_path, table_path, master=root)
    app.mainloop()
