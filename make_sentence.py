from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # TimeoutException 추가
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyautogui
import pyperclip
import os
import sys
from bs4 import BeautifulSoup
import random
import threading
import keyboard
import logging
import tkinter as tk
from tkinter import font as tkFont  # 폰트 모듈 추가
from tkinter import messagebox
import json
import cv2
import numpy as np

# Adjusting the approach to efficiently generate 300 unique sentences with emojis and emoticons.
def generate_blog_style_sentences_v2():
    base_phrases = [
        "블로그 글 잘 봤습니다", "정성가득한 글 잘 보고 갑니다", "답방은 필수인거 맞죠?  먼저 달려와 주세요~ ", "작성해주신 포스팅이 참 괜찮네요 ",
        "감기 조심, 늘 조심이요~", "답방은 센스입니다", "안녕하세요! 자주 소통해야 즐거워용~ ", "따뜻한 세상을 위해~ 우리 소통해요! ",
        "행복은 나누는 것인가 봐요~ ", " 이웃과 소통하며 우리 모두 행복해야 하는거 아시죠? ", "잇님! 가까운 마음으로 더욱 밝아져요 ",
        "정성가득한 포스팅 감사합니다", "오늘도 화이팅하세요~ ",
        "행복한 하루 보내세요", "쉬운게 없는건 알지만, 늘 건강하세요! ", " 상호 존중하는 눈높이를 맞추며, ", "적어주신 좋은 정보 감사합니다",
        "긍정적인 에너지로 이해의 깊이를 ... 더하는 날이 되시길 바래요. ^^ ", "모두 기분이 좋아졌으면 해요! 즐거운 시간 보내세요", "오늘도 좋은 기분으로 시작하고 마무리해야 해요 ", "마음을 열면 우리 삶이 더욱 밝아져요"
    ]

    emojis = ["^^", "ㅎㅎ", "😊", "👍", "😁", "💪", "🌟", "🌞", "🌈", "❄️", "🍀", "🌷", "🍂", "☔"]

    sentences = set()
    while len(sentences) < 1:
        # Randomly select a base phrase and an emoji
        sentence = random.choice(base_phrases) + " " + random.choice(emojis)
        # Ensure uniqueness and character limit
        if len(sentence) <= 60 and sentence not in sentences:
            sentences.add(sentence)

    return list(sentences)

# Generate the sentences again
blog_style_sentences_v2 = generate_blog_style_sentences_v2()

# Save to a file
application_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
file_path_v2 = os.path.join(application_path, 'data', 'prefix_blog.txt')

for sentence in blog_style_sentences_v2:
    print(sentence)

