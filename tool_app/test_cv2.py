from pathlib import Path
import cv2
import datetime
import schedule
import time
import sys
import matplotlib.pyplot as plt


def get_path():
    """
    このプロジェクトを管理している親フォルダーの絶対リンクを取得する。
    parents[1]は1個前を取得するので、階層を変えるとその数に合わせて変更の必要がある。
    """
    folder_path = Path(__file__).resolve().parents[1]
    return folder_path


def mk_dir(folder_path):
    """
    写真保存用のディレクトリとそのパスを作成する
    """
    str_date = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    photos_path = folder_path / "photos" / str(str_date)
    Path(photos_path).mkdir()
    return photos_path


def job(capture, photos_path):
    ret, frame = capture.read()
    str_date = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    fname = photos_path / f"{str_date}.jpg"
    cv2.imwrite(str(fname), frame)
    print(f"{fname} is created.")
    # BGRのデータの並びからRGBのデータの並びに変換
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    plt.clf()
    plt.imshow(rgb_image)
    plt.draw()  # 描画を更新
    plt.pause(0.001)


if __name__ == '__main__':
    # 写真保存場所のパスを取得 & 作成
    folder_path = get_path()
    photos_path = mk_dir(folder_path)

    # カメラの初期設定
    """
    カメラをパソコンが認識している番号。Webカメラを接続した場合は、Webカメラ = 0, 内蔵カメラ = 1。
    接続しない場合は、内蔵カメラ = 0
    """
    device_id = 0
    capture = cv2.VideoCapture(device_id)  # カメラをプログラムからいじれるように認識させる(クラスを作成)。

    # Schedule the job every 10 seconds
    schedule.every(0.3).seconds.do(job, capture, photos_path)
    flag = True

    try:
        while flag:
            schedule.run_pending()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('interrupted!')
        flag = False

    capture.release()
