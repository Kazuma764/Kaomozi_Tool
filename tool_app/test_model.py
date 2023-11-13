import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import torch
from facenet_pytorch import MTCNN
from hsemotion.facial_emotions import HSEmotionRecognizer

# 使用するプロセッサーの確認
use_cuda = torch.cuda.is_available()
device = 'cuda' if use_cuda else 'cpu'

# 顔の認識用の関数
mtcnn = MTCNN(keep_all=False, post_process=False, min_face_size=40, device=device)


def detect_face(frame):
    bounding_boxes, probs = mtcnn.detect(frame, landmarks=False)
    bounding_boxes = bounding_boxes[probs > 0.9]
    return bounding_boxes


print(use_cuda)

# 使用するモデルを選択。mobile_netはtensorflowじゃないと動かない。
# model_name = 'enet_b0_8_best_afew'
model_name = 'enet_b0_8_best_vgaf'
# model_name='enet_b0_8_va_mtl'
# model_name='enet_b2_8'
fer = HSEmotionRecognizer(model_name=model_name, device='cpu')

# 画像の読み込みと編集
fpath = '20180720_174416.jpg'
frame_bgr = cv2.imread("/Users/ishidakazuma/論文用コード/Kaomozi_Tool/tool_app/code/20180720_174416.jpg")
plt.figure(figsize=(5, 5))
frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
plt.axis('off')
plt.imshow(frame)
plt.show()

bounding_boxes = detect_face(frame)

# モデルの実行
for bbox in bounding_boxes:
    box = bbox.astype(int)
    x1, y1, x2, y2 = box[0:4]    
    face_img = frame[y1:y2, x1:x2, :]
    emotion, scores = fer.predict_emotions(face_img, logits=True)
    print(emotion, scores)
    plt.figure(figsize=(3, 3))
    plt.axis('off')
    plt.imshow(face_img)
    plt.title(emotion)
    plt.show()
