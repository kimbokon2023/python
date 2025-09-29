import tkinter as tk
from tkinter import messagebox
import requests
from xml.etree import ElementTree

def get_youtube_transcript(video_id, lang='ko'):
    url = f'https://video.google.com/timedtext?lang={lang}&v={video_id}'
    response = requests.get(url)
    if response.status_code != 200 or not response.text:
        return None
    root = ElementTree.fromstring(response.content)
    transcript = ''
    for child in root:
        if child.text:
            transcript += child.text.strip() + '\n'
    return transcript.strip()

def on_submit():
    url = entry.get().strip()
    if "youtube.com/shorts/" in url:
        video_id = url.split("shorts/")[1].split("?")[0]
    elif "youtube.com/watch?v=" in url:
        video_id = url.split("watch?v=")[1].split("&")[0]
    else:
        messagebox.showerror("오류", "유효한 유튜브 URL이 아닙니다.")
        return

    result = get_youtube_transcript(video_id)
    if result:
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, result)
    else:
        messagebox.showinfo("결과", "자막을 찾을 수 없습니다.")

# GUI 구성
root = tk.Tk()
root.title("유튜브 대본 추출기")
root.geometry("600x400")

label = tk.Label(root, text="유튜브 쇼츠 또는 영상 URL을 입력하세요:")
label.pack(pady=10)

entry = tk.Entry(root, width=60)
entry.pack()

submit_btn = tk.Button(root, text="대본 추출", command=on_submit)
submit_btn.pack(pady=10)

text_box = tk.Text(root, wrap=tk.WORD)
text_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

root.mainloop()
