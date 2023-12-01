# tensolflowを動かすのに環境設定のやり直しが必要
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import torch
from facenet_pytorch import MTCNN
from hsemotion.facial_emotions import HSEmotionRecognizer
import tensorflow as tf

# 使用するプロセッサーの確認
use_cuda = torch.cuda.is_available()
device = 'cuda' if use_cuda else 'cpu'
