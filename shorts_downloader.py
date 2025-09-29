import os
import re
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from yt_dlp import YoutubeDL
import whisper
from pydub import AudioSegment
import urllib.parse

stop_event = threading.Event()  # ESC로 중단하기 위한 이벤트 객체

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_video_urls_from_channel(channel_url, mode):
    # 📌 /shorts 주소 입력 시 /videos로 보정
    if "/shorts" in channel_url:
        channel_url = channel_url.split("/shorts")[0]

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        entries = info.get('entries', [])
        result = []

        for entry in entries:
            video_id = entry.get("id")
            webpage_url = entry.get("webpage_url")
            if not webpage_url and video_id:
                webpage_url = f"https://www.youtube.com/watch?v={video_id}"

            if not webpage_url:
                continue  # skip invalid

            if mode == "all":
                result.append(webpage_url)
            elif mode == "shorts" and "/shorts/" in webpage_url:
                result.append(webpage_url)
            elif mode == "videos" and "/shorts/" not in webpage_url:
                result.append(webpage_url)

        return result, info.get("title", "channel_output")

def download_audio(url):
    mp3_filename = "temp_audio.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': mp3_filename,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    expected_file = "temp_audio.mp3"
    if not os.path.exists(expected_file):
        raise FileNotFoundError("오디오 파일이 생성되지 않았습니다.")
    return expected_file

def convert_to_wav(input_path, output_path='audio.wav'):
    sound = AudioSegment.from_mp3(input_path)
    sound.export(output_path, format="wav")
    return output_path

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language='ko')
    return result['text']

def run_crawl():
    stop_event.clear()
    channel_url = url_entry.get().strip()
    mode = video_mode.get()
    if not channel_url:
        messagebox.showwarning("입력 필요", "유튜브 채널 주소를 입력해주세요.")
        return
    result_textbox.delete(1.0, tk.END)
    threading.Thread(target=crawl_and_transcribe, args=(channel_url, mode), daemon=True).start()

def cancel_operation(event=None):
    stop_event.set()
    result_textbox.insert(tk.END, "\n❌ ESC 키 입력 → 작업 중단 요청됨...\n")

def crawl_and_transcribe(channel_url, mode):
    try:
        result_textbox.insert(tk.END, f"채널 분석 중...\n")

        video_urls, raw_title = get_video_urls_from_channel(channel_url, mode)
        decoded_title = urllib.parse.unquote(raw_title)
        result_textbox.insert(tk.END, f"📺 채널명: {decoded_title}\n")
        result_textbox.insert(tk.END, f"🎬 영상 개수: {len(video_urls)}\n\n")

        if not video_urls:
            result_textbox.insert(tk.END, "⚠️ 처리할 영상이 없습니다.\n")
            return

        # 폴더 경로 지정
        folder_path = "C:\\shorts"
        os.makedirs(folder_path, exist_ok=True)

        filename = os.path.join(folder_path, sanitize_filename(decoded_title) + ".txt")

        # 파일 초기화: 첫 실행 시 기존 내용 삭제
        open(filename, "w", encoding="utf-8").close()

        for idx, url in enumerate(video_urls):
            if stop_event.is_set():
                result_textbox.insert(tk.END, "\n🛑 사용자 요청으로 작업이 중단되었습니다.\n")
                break

            result_textbox.insert(tk.END, f"[{idx+1}/{len(video_urls)}] 처리 중: {url}\n")
            try:
                mp3_path = download_audio(url)
                wav_path = convert_to_wav(mp3_path)
                transcript = transcribe_audio(wav_path)

                # 📌 영상마다 결과를 즉시 파일에 append 저장
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(f"[{url}]\n")
                    f.write("=" * 50 + "\n")
                    f.write(transcript.strip() + "\n")
                    f.write("=" * 50 + "\n\n")

                os.remove(mp3_path)
                os.remove(wav_path)

            except Exception as e:
                result_textbox.insert(tk.END, f"⚠️ 오류 발생: {e}\n")
                continue

        if not stop_event.is_set():
            result_textbox.insert(tk.END, f"\n✅ 저장 완료: {filename}\n")
            messagebox.showinfo("완료", f"모든 자막이 '{filename}'에 저장되었습니다.")
        else:
            messagebox.showinfo("중단됨", "사용자 요청으로 작업이 중단되었습니다.")

    except Exception as e:
        messagebox.showerror("오류", str(e))

     
root = tk.Tk()
root.title("유튜브 채널 자막 추출기")
root.geometry("800x600")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="유튜브 채널 주소:").pack(anchor="w")
url_entry = tk.Entry(frame, width=90)
url_entry.pack(pady=5)

video_mode = tk.StringVar(value="all")
mode_frame = tk.Frame(frame)
mode_frame.pack(pady=5, anchor="w")

tk.Label(mode_frame, text="대상 영상 종류:").pack(side="left")
tk.Radiobutton(mode_frame, text="전체 영상", variable=video_mode, value="all").pack(side="left")
tk.Radiobutton(mode_frame, text="쇼츠만", variable=video_mode, value="shorts").pack(side="left")
tk.Radiobutton(mode_frame, text="일반 영상만", variable=video_mode, value="videos").pack(side="left")

tk.Button(frame, text="자막 추출 시작", command=run_crawl, bg="#4CAF50", fg="white", width=20).pack(pady=10)

result_textbox = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=100, height=25)
result_textbox.pack(pady=(5, 10))

root.bind('<Escape>', cancel_operation)
root.mainloop()
