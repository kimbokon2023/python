import sys
import os
import whisper
import yt_dlp
from pydub import AudioSegment
import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel, Label
import threading
import re

# 📥 오디오 다운로드
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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    expected_file = "temp_audio.mp3"
    if not os.path.exists(expected_file):
        raise FileNotFoundError("오디오 파일이 생성되지 않았습니다.")
    return expected_file

# 🔄 mp3 → wav
def convert_to_wav(input_path, output_path='audio.wav'):
    if not os.path.exists(input_path):
        raise FileNotFoundError("mp3 파일이 존재하지 않습니다.")
    sound = AudioSegment.from_mp3(input_path)
    sound.export(output_path, format="wav")
    return output_path

# 🧠 whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language='ko')
    return result['text']

# 🎬 GUI용 백그라운드 작업 함수
def threaded_transcription(url):
    try:
        show_progress("오디오 다운로드 중...")
        mp3_path = download_audio(url)

        update_progress("WAV 변환 중...")
        wav_path = convert_to_wav(mp3_path)

        update_progress("자막 생성 중...")
        transcript = transcribe_audio(wav_path)

        update_progress("완료되었습니다.")

        result_textbox.insert(tk.END, "=" * 50 + "\n")
        result_textbox.insert(tk.END, transcript + "\n")
        result_textbox.insert(tk.END, "=" * 50 + "\n")

        os.remove(mp3_path)
        os.remove(wav_path)
    except Exception as e:
        messagebox.showerror("오류 발생", str(e))
    finally:
        progress_window.destroy()

# 💬 진행 상태 표시
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

# 🧵 실행 버튼이 눌리면 스레드로 실행
def run_transcription():
    url = url_entry.get().strip()
    result_textbox.delete(1.0, tk.END)

    if not url:
        messagebox.showwarning("입력 필요", "유튜브 URL을 입력해주세요.")
        return

    if "youtube.com/shorts/" in url:
        video_id = url.split("shorts/")[1].split("?")[0]
        url = f"https://www.youtube.com/watch?v={video_id}"

    threading.Thread(target=threaded_transcription, args=(url,), daemon=True).start()

# 📋 추출된 자막 복사
def copy_to_clipboard():
    content = result_textbox.get("1.0", tk.END).strip()
    if not content:
        messagebox.showinfo("알림", "복사할 내용이 없습니다.")
        return
    root.clipboard_clear()
    root.clipboard_append(content)
    messagebox.showinfo("복사 완료", "자막이 클립보드에 복사되었습니다!")

# 📝 GPT 프롬프트 생성 및 복사
def generate_gpt_prompt():
    content = result_textbox.get("1.0", tk.END).strip()
    if not content:
        messagebox.showinfo("알림", "프롬프트로 생성할 내용이 없습니다.")
        return

    # ========== 사이의 텍스트 추출
    pattern = r'={50}\n(.*?)\n={50}'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        messagebox.showerror("오류", "자막 형식이 올바르지 않습니다. 자막을 먼저 추출해주세요.")
        return
    
    transcript = match.group(1).strip()

    # 프롬프트 템플릿
    prompt_template = """다음은 내가 유튜브에서 가져온 콘텐츠 대본입니다:

================================
{transcript}
================================

위의 대본을 바탕으로 네이버 블로그에 최적화된 양질의 포스팅을 작성해줘. 아래의 조건을 정확히 지켜서 작성해야 해:

1. 블로그 제목은 사람들이 클릭하고 싶게 흥미롭고 명확하게 작성해줘. (키워드를 자연스럽게 포함)
2. 네이버 검색 엔진 최적화를 위해 핵심 키워드를 본문과 소제목에 자연스럽게 여러 번 배치해줘.
3. 전체 글의 길이는 네이버 블로그가 좋아하는 글 길이인 3000자 이상으로 구성해줘.
4. 글의 서두에 사람들이 관심을 가질 만한 매력적인 '리드 문장'을 써서 흥미를 끌어줘.
5. 주요 내용은 간결하고 가독성 높은 문장으로 구성해줘. 중요한 부분은 굵은 글씨(강조) 처리해줘.
6. 내용 중간에 관련된 자연스러운 소제목을 5~7개 만들어서 구성을 명확하게 나눠줘.
7. 글의 마지막에는 자연스럽게 글을 요약하고 공감을 유도하는 문장을 추가해줘 '마무리글'이라는 표현은 하지말자.
8. 블로그 특유의 친근하고 자연스러운 말투로 작성해줘. 특히 문장 끝에 '~입니다', '~했어요', '~죠', '~답니다' 등 친근한 어투를 사용해줘.
9. 위의 영상의 저자나 인터뷰대상자는 '이 분야 전문가'이라고 정의하면 좋겠다. 실명은 제외해줘.
10. 마지막 부분에 네이버 블로그에 효과적인 검색 태그를 #으로 시작하고, 쉼표(,)로 구분하여 5~10개 추가해줘.
11. 결과에 나오는 이모지는 생략한다.
"""

    # 프롬프트에 자막 삽입
    final_prompt = prompt_template.format(transcript=transcript)

    # 클립보드에 복사
    root.clipboard_clear()
    root.clipboard_append(final_prompt)
    messagebox.showinfo("복사 완료", "GPT 프롬프트가 클립보드에 복사되었습니다!")

# 📝 GPT 이미지 프롬프트 생성 및 복사
def generate_gpt_prompt_image():   

    # 프롬프트 템플릿
    prompt_template = " 아래의 내용이 간단히 표시되게 한글은 제외하고 간단한 이미지로 생성해줘.  "

    # 프롬프트에 자막 삽입
    final_prompt = prompt_template

    # 클립보드에 복사
    root.clipboard_clear()
    root.clipboard_append(final_prompt)
    messagebox.showinfo("복사 완료", "GPT 이미지 프롬프트가 클립보드에 복사되었습니다!")

# 🖼️ GUI 구성
root = tk.Tk()
root.title("유튜브 자막 추출기")
root.geometry("700x540")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="유튜브 URL 입력:").pack(anchor="w")
url_entry = tk.Entry(frame, width=80)
url_entry.pack(pady=5)

button_frame = tk.Frame(frame)
button_frame.pack(pady=10)

tk.Button(button_frame, text="자막 추출", command=run_transcription, bg="#4CAF50", fg="white", width=10).pack(side="left", padx=2)
tk.Button(button_frame, text="추출 복사", command=copy_to_clipboard, bg="#2196F3", fg="white", width=10).pack(side="left", padx=2)
tk.Button(button_frame, text="GPT", command=generate_gpt_prompt, bg="#FF9800", fg="white", width=10).pack(side="left", padx=2)
tk.Button(button_frame, text="이미지문구", command=generate_gpt_prompt_image, bg="#FF0000", fg="white", width=10).pack(side="left", padx=2)

result_textbox = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
result_textbox.pack(pady=(5, 10))

root.mainloop()