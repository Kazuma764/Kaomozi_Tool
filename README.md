# Kaomozi_Tool
論文発表用 レポジトリ

<h2>リポジトリの概要</h2>
このリポジトリはSavchenko A.V., Savchenko L.V., Makarov I(2020)の<a href = "https://paperswithcode.com/paper/classifying-emotions-and-engagement-in-online">「Classifying emotions and engagement in online learning based on a single facial expression recognition neural network」</a>の公開しているモデルを利用して作成した、インタビュー支援ツールについてまとめたものです。

<h2>リポジトリの説明</h2>
<pre>
.
├── accurate_test
├── build
├── dist
├── face-emotion-recognition-main
├── hsemotion-main
├── models
├── photos
├── tool_app
  ├── code
    ├── test_hsemotion_package.ipynb
    ├── test.py
  ├── src
    ├── __init__.py
    ├── facial_emotions.py
  ├── accurate_taking_photo.py
  ├── main_char.py
  ├── main_img.py
  ├── main_kaomoji.py
  ├── main_mobilenet.py
  ├── test_app.py
  ├── test_cv2.py
  ├── test_mobile.by
└── README.md
</pre>

<h3>ファイルの説明</h3>

**test_hsemotion_package.ipynb / test.py**
- hsemotion-mainのdemoディレクトリ内にあるコードをコピーしてきたもの
- コピーしてきたファイルを.pyファイルで動作するように調整したもの

**__init__.py / facial_emotions.py**
- hsemotion-mainのhsemotionディレクトリ内にあるコードをコピーしてきたもの
- 関数の内部確認用

**accurate_taking_photo.py**
- モデルの表情の分類性能確認のため、1秒間隔で5回の写真を撮るファイル
- 撮影された画像は、accurate_test内に撮影した年月日時をファイル名として保存される
  
**main_char.py**
- 1秒に1回写真を撮影し、モデルに入力&表情を取得。取得した表情をアプリケーション上で文字として出力する

**main_img.py**
- 1秒に1回写真を撮影し、モデルに入力&表情を取得。アプリケーション上で検出した顔切り抜いた部分だけ出力する
- 作ったアプリが表情を検出できているのかの動作確認用

**main_kaomoji.py**
- 1秒に1回写真を撮影し、モデルに入力&表情を取得。取得した表情をアプリケーション上で顔文字として出力する

**main_mobilenet.py / test_mobile.py**
- tensorflowのモデルで動くように調整しているコード
- 現在の環境だと実行できないので、未完

**test_app.py**
- tkinterの実行テストファイル
- 参考ページ1をコピーしてきたもの

**test_cv2.py**
- opencvの実行テストファイル
- 参考文献2をコピーしてきたもの

<h2>実行に必要になったライブラリ</h2>

```
hsemotion
torch
torchvision
timm #timm = 0.9.7.でないと動かない場合がある
pillow
opencv-python
```
hsemotion-main内のsetup.pyを実行することで、opencvを除いたライブラリはインストール可能。


<h2>参考文献</h2>
<h3>GPT4のChatのリンク</h3>

- コードの作成や修正等に利用 その1：<a href = "https://chat.openai.com/share/66b9ef5d-d084-4ec6-ba31-45275210074d">リンク</a>
- コードの作成や修正等に利用 その2：<a href = "https://chat.openai.com/share/5b0b4a1e-862e-4fdf-b264-3cfdfd414862">リンク</a>

<h3>利用したモデルについて</h3>

**Githubのリポジトリ**
- メインリポジトリ(スペック表などが置いてある)：<a href = "https://github.com/HSE-asavchenko/face-emotion-recognition/tree/main">リンク</a>
- ライブラリなど実際にコード作成で参考にしたリポジトリ：<a href = "https://github.com/HSE-asavchenko/hsemotion">リンク</a>

論文
```
@article{savchenko2022classifying,
  title={Classifying emotions and engagement in online learning based on a single facial expression recognition neural network},
  author={Savchenko, Andrey V and Savchenko, Lyudmila V and Makarov, Ilya},
  journal={IEEE Transactions on Affective Computing},
  year={2022},
  publisher={IEEE},
  url={https://ieeexplore.ieee.org/document/9815154}
}
```

<h3>参考にしたWebの記事</h3>

1. すぽてくブログ(2022)「【Python】USBカメラの映像をGUIに表示する方法【Tkinter】」, https://shinshin-log.com/python-usbcamera/, 2023年11月30日閲覧。
1. @dgkmtu(dgk)(2019)「【Python】scheduleを使ってモジュールを定期実行させよう」, https://qiita.com/dgkmtu/items/3bd3794b44a0aa03bfe3, 2023年11月30日閲覧。

