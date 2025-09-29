# -*- coding: utf-8 -*-
import sys
import os
import re # 정규 표현식 모듈 추가
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, Toplevel, Label
from yt_dlp import YoutubeDL

# stdout의 인코딩을 UTF-8로 설정 (터미널 환경에 따라 필요할 수 있음)
# GUI 환경에서는 주로 GUI 위젯을 통해 피드백하므로 중요도는 낮을 수 있습니다.
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
except AttributeError: # sys.stdout/stderr가 None인 경우 (예: pythonw.exe로 실행 시)
    pass

# --- 핵심 기능 함수 ---

def extract_url(text):
    """
    입력된 텍스트에서 첫 번째 HTTP 또는 HTTPS URL을 추출합니다.

    Args:
        text (str): URL을 포함할 수 있는 문자열.

    Returns:
        str or None: 추출된 URL 문자열 또는 찾지 못한 경우 None.
    """
    # URL을 찾기 위한 정규 표현식
    # http:// 또는 https:// 로 시작하고 공백이나 특정 문자가 아닌 문자로 구성된 패턴
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None

def download_video_from_url(video_url, output_path, progress_callback):
    """
    주어진 URL에서 동영상을 다운로드하고 진행 상황을 콜백으로 알립니다.

    Args:
        video_url (str): 다운로드할 동영상의 URL.
        output_path (str): 동영상을 저장할 경로.
        progress_callback (function): 진행 상황 메시지를 전달할 콜백 함수.
    """
    progress_callback(f"다운로드 시도: {video_url}\n")
    progress_callback(f"저장 경로: {output_path}\n")

    output_template = os.path.join(output_path, '%(title)s [%(id)s].%(ext)s') # 파일명 중복 방지를 위해 ID 추가

    ydl_opts = {
        'quiet': True, # 상세 로그는 GUI로 출력하므로 True로 설정
        'progress_hooks': [lambda d: hook(d, progress_callback)], # 진행 상황 콜백 연결
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_template,
        'noplaylist': True,
        'encoding': 'utf-8',
        # 'force_generic_extractor': True, # 필요시 활성화
        'postprocessors': [{ # 임베드 썸네일 추가 (선택 사항)
            'key': 'FFmpegMetadata',
            'add_metadata': True,
        }, {
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': False,
        }],
        'writethumbnail': True, # 썸네일 파일 별도 저장 (선택 사항)
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([video_url])
            if error_code == 0:
                progress_callback(f"✅ 다운로드 성공: {video_url}\n")
            else:
                progress_callback(f"⚠️ 다운로드 중 문제 발생 (오류 코드: {error_code}): {video_url}\n")

    except Exception as e:
        progress_callback(f"❌ 다운로드 실패: {video_url}\n")
        progress_callback(f"   오류: {e}\n")

def hook(d, callback):
    """yt-dlp 진행 상황 콜백 함수"""
    video_url = ''
    if d['status'] == 'downloading':
        # 다운로드 진행률 표시 (간결하게)
        percent_str = d.get('_percent_str', '0.0%')
        speed_str = d.get('_speed_str', 'N/A')
        eta_str = d.get('_eta_str', 'N/A')
        # 너무 자주 업데이트되지 않도록 조절이 필요할 수 있음
        # 여기서는 간단히 마지막 줄 업데이트 시도 (Tkinter Text 위젯 성능 고려)
        # callback(f"   진행률: {percent_str}, 속도: {speed_str}, 남은 시간: {eta_str}\r")
        pass # 너무 많은 메시지 방지 위해 일단 비활성화
    elif d['status'] == 'finished':
        filename = d.get('filename') or d.get('info_dict', {}).get('filepath')
        if filename:
            callback(f"   파일 저장 완료: {os.path.basename(filename)}\n")
        else:
             callback("   파일 처리 완료.\n")
    elif d['status'] == 'error':
        callback(f"   오류 발생: {d.get('filename') or video_url}\n")


# --- GUI 관련 함수 ---

def threaded_download():
    """GUI에서 다운로드 버튼 클릭 시 실행될 함수 (스레드 사용)"""
    input_text = url_entry.get().strip()
    download_path = path_entry.get().strip()

    if not input_text:
        messagebox.showwarning("입력 필요", "동영상 URL 또는 포함된 텍스트를 입력해주세요.")
        return

    video_url = extract_url(input_text) # URL 추출 시도

    if not video_url:
        messagebox.showerror("오류", "입력된 텍스트에서 유효한 URL을 찾을 수 없습니다.")
        return

    if not download_path or not os.path.isdir(download_path):
        messagebox.showerror("오류", "유효한 다운로드 폴더를 선택해주세요.")
        return

    # 로그창 비우기
    log_textbox.config(state=tk.NORMAL)
    log_textbox.delete(1.0, tk.END)
    log_textbox.config(state=tk.DISABLED)

    # 진행 상황 표시 함수 (GUI 업데이트용)
    def update_log(msg):
        log_textbox.config(state=tk.NORMAL)
        log_textbox.insert(tk.END, msg)
        log_textbox.see(tk.END) # 스크롤 자동 내림
        log_textbox.config(state=tk.DISABLED)
        root.update_idletasks() # GUI 업데이트 강제

    # 다운로드 버튼 비활성화
    download_button.config(state=tk.DISABLED)

    # 스레드 생성 및 시작
    thread = threading.Thread(target=run_download_task, args=(video_url, download_path, update_log), daemon=True)
    thread.start()

# 📝 GPT 이미지 프롬프트 생성 및 복사
def generate_gpt_prompt():   

    # 프롬프트 템플릿
    prompt_template = "내 쇼츠에 적용할 10가지 재밌고 유머스러운 문구가 필요해. 내 영상을 요약하자면 '개들이 단체로 달려와서 만두를 허겁지겁 먹는 장면' 결과가 궁금해지는 한 줄 문구로 부탁해.  "

    # 클립보드에 복사
    root.clipboard_clear()
    root.clipboard_append(prompt_template)
    messagebox.showinfo("복사 완료", "GPT 이미지 프롬프트가 클립보드에 복사되었습니다!")


def run_download_task(url, path, callback):
    """실제 다운로드를 수행하고 버튼 상태를 복구하는 스레드 작업"""
    try:
        download_video_from_url(url, path, callback)
    finally:
        # 작업 완료 후 다운로드 버튼 다시 활성화
        download_button.config(state=tk.NORMAL)


def browse_directory():
    """다운로드 폴더 선택 대화상자 열기"""
    directory = filedialog.askdirectory(initialdir=path_entry.get() or 'c:\\')
    if directory: # 사용자가 폴더를 선택한 경우
        path_entry.config(state=tk.NORMAL)
        path_entry.delete(0, tk.END)
        path_entry.insert(0, directory)
        path_entry.config(state='readonly') # 다시 읽기 전용으로

# --- GUI 구성 ---
root = tk.Tk()
root.title("동영상 다운로더")
root.geometry("700x500") # 세로 길이 조정

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# URL 입력
tk.Label(frame, text="동영상 URL 또는 포함된 텍스트 입력:").pack(anchor="w")
url_entry = tk.Entry(frame, width=80)
url_entry.pack(fill="x", pady=(0, 5)) # 가로로 채우기

# 다운로드 경로 선택
tk.Label(frame, text="저장 폴더:").pack(anchor="w")
path_frame = tk.Frame(frame)
path_frame.pack(fill="x", pady=(0, 10))

path_entry = tk.Entry(path_frame, width=65, state='readonly') # 읽기 전용으로 시작
path_entry.pack(side="left", fill="x", expand=True)

# 기본 경로 설정 및 폴더 생성 확인
default_download_path = 'c:\\downloads'
if not os.path.exists(default_download_path):
    try:
        os.makedirs(default_download_path)
        print(f"기본 다운로드 폴더 생성: {default_download_path}")
    except Exception as e:
        print(f"기본 다운로드 폴더 생성 실패: {e}")
        default_download_path = os.getcwd() # 실패 시 현재 작업 디렉토리로

path_entry.config(state=tk.NORMAL)
path_entry.insert(0, default_download_path)
path_entry.config(state='readonly')

browse_button = tk.Button(path_frame, text="폴더 선택", command=browse_directory, width=10)
browse_button.pack(side="left", padx=(5, 0))

# 다운로드 버튼
download_button = tk.Button(frame, text="다운로드 시작", command=threaded_download, bg="#4CAF50", fg="white", width=15, height=2)
download_button.pack(pady=10)
gpt_button = tk.Button(frame, text="GPT 프롬프트 복사", command=generate_gpt_prompt, bg="#FF0000", fg="white", width=15, height=2)
gpt_button.pack(pady=10)

# 로그 출력
tk.Label(frame, text="로그:").pack(anchor="w")
log_textbox = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=15, state=tk.DISABLED) # 비활성화 상태로 시작
log_textbox.pack(fill="both", expand=True, pady=(5, 0))


root.mainloop()
