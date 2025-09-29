import sys
import os
import whisper
import yt_dlp
import requests
from pydub import AudioSegment
import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel, Label
import threading
import json
import re # 정규 표현식 모듈 임포트

API_KEY = "AIzaSyCJQs_-6STB3TgViCm4qQqjDZYr42XT3LI"

# 🎯 videoId 추출
def extract_video_id(url):
    if "shorts/" in url:
        return url.split("shorts/")[1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    else:
        raise ValueError("올바른 유튜브 URL이 아닙니다.")

# 💬 대댓글 가져오기 (최대 10개)
def fetch_replies(parent_id, max_replies=10):
    url = "https://www.googleapis.com/youtube/v3/comments"
    params = {
        "part": "snippet",
        "parentId": parent_id,
        "key": API_KEY,
        "maxResults": min(max_replies, 100),
        "textFormat": "plainText"
    }

    replies = []
    fetched = 0
    while True:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            break

        data = response.json()
        for item in data.get("items", []):
            snippet = item["snippet"]

            # replies 리스트가 이전에 초기화되었다고 가정합니다.
            # snippet 변수가 반복문 등에서 정의되었다고 가정합니다.

            original_text = snippet["textDisplay"]

            # 정규 표현식을 사용하여 '@'로 시작하고 뒤이어 공백이 아닌 문자(들)가 오는 패턴 제거
            # r'@\S+' 패턴:
            # @ : 리터럴 '@' 문자
            # \S: 공백이 아닌 문자 (non-whitespace character)
            # + : 바로 앞의 요소(\S)가 1번 이상 반복됨
            text_cleaned = re.sub(r'@\S+', '', original_text)

            # 제거 후 양 끝에 남을 수 있는 공백 제거 (선택 사항이지만 깔끔한 결과를 위해 권장)
            text_cleaned = text_cleaned.strip()

            replies.append({
                "receiver": snippet["authorDisplayName"],
                "text": text_cleaned # @username 패턴이 제거된 텍스트
            })
            fetched += 1
            if fetched >= max_replies:
                break

        if fetched >= max_replies or "nextPageToken" not in data:
            break
        params["pageToken"] = data["nextPageToken"]

    return replies

# 💬 댓글 + 대댓글 가져오기 (댓글 15개)
def get_comments(video_id, max_results=15):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": API_KEY,
        "maxResults": min(max_results, 100),
        "textFormat": "plainText",
        "order": "relevance"
    }

    comments = []
    fetched = 0
    while fetched < max_results:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"API 요청 실패: {response.text}")

        data = response.json()
        for item in data.get("items", []):
            top_comment = item["snippet"]["topLevelComment"]["snippet"]
            author = top_comment["authorDisplayName"]
            text = top_comment["textDisplay"]
            comments.append({ "sender": author, "text": text })

            reply_count = item["snippet"].get("totalReplyCount", 0)
            if reply_count > 0:
                reply_id = item["id"]
                replies = fetch_replies(reply_id, max_replies=10)
                comments.extend(replies)

            fetched += 1
            if fetched >= max_results:
                break

        if "nextPageToken" not in data:
            break
        params["pageToken"] = data["nextPageToken"]

    return comments

# 🎬 댓글 추출 실행 및 저장
def run_comment_extraction():
    url = url_entry.get().strip()
    result_textbox.delete(1.0, tk.END)

    if not url:
        messagebox.showwarning("입력 필요", "유튜브 URL을 입력해주세요.")
        return

    try:
        video_id = extract_video_id(url)
        show_progress("댓글 가져오는 중...")
        comments = get_comments(video_id)

        update_progress("댓글 저장 중...")
        with open("c:\python\dev\comments.json", "w", encoding="utf-8") as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)

        result_textbox.insert(tk.END, f"{len(comments)}개의 댓글과 대댓글이 comments.json에 저장되었습니다.\n")
        update_progress("댓글 추출 완료!")
        progress_window.destroy()
    except Exception as e:
        messagebox.showerror("댓글 오류", str(e))
        if 'progress_window' in globals():
            progress_window.destroy()

# 💬 진행창

def show_progress(msg):
    global progress_window, progress_label
    progress_window = Toplevel(root)
    progress_window.title("진행 중...")
    progress_window.geometry("300x100")
    progress_window.resizable(False, False)
    progress_label = Label(progress_window, text=msg, font=("맑은 고딕", 12))
    progress_label.pack(expand=True, pady=30)
    progress_window.grab_set()
    root.update()

def update_progress(new_msg):
    progress_label.config(text=new_msg)
    progress_window.update()

# 🎨 GUI 구성
root = tk.Tk()
root.title("유튜브 댓글 JSON 저장기")
root.geometry("720x400")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="유튜브 URL 입력:").pack(anchor="w")
url_entry = tk.Entry(frame, width=85)
url_entry.pack(pady=5)

button_frame = tk.Frame(frame)
button_frame.pack(pady=10)

tk.Button(button_frame, text="댓글 추출 및 저장", command=run_comment_extraction, bg="#9C27B0", fg="white", width=20).pack()

result_textbox = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=85, height=15)
result_textbox.pack(pady=(5, 10))

root.mainloop()
