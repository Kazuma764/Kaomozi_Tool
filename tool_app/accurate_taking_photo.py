from pathlib import Path
import cv2
import datetime
import time
import sys


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
    photos_path = folder_path / "accurate_test" / str(str_date)
    Path(photos_path).mkdir(parents=True, exist_ok=True)
    return photos_path


def job(capture, photos_path, count):
    ret, frame = capture.read()
    str_date = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    fname = photos_path / f"{str_date}.jpg"
    cv2.imwrite(str(fname), frame)
    print(f"{fname} is created.")
    return count - 1  # GPT4


if __name__ == '__main__':
    # 写真保存場所のパスを取得 & 作成
    folder_path = get_path()
    photos_path = mk_dir(folder_path)

    # カメラの初期設定
    device_id = 0
    capture = cv2.VideoCapture(device_id)

    # GPT4
    count = 5
    while count > 0:
        count = job(capture, photos_path, count)
        time.sleep(1)

    capture.release()
