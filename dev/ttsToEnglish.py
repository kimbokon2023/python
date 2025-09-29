import tkinter as tk
from tkinter import scrolledtext, messagebox, Toplevel, Label
from tkinter import ttk  # ttk 모듈 추가 (프로그레스바 위젯 포함)
from gtts import gTTS
import os
import threading

# --- TTS 생성 함수 (이전과 동일) ---
def create_tts_audio(text_to_speak, output_path="c:\\output\\english.mp3"):
    """주어진 텍스트로 gTTS를 사용하여 영어 mp3 파일을 생성합니다."""
    try:
        if not text_to_speak.strip():
            raise ValueError("텍스트 입력창이 비어 있습니다. 영어 텍스트를 입력해주세요.")

        # 출력 폴더 생성
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        # gTTS 객체 생성 (영어)
        # gTTS 호출 자체가 블로킹(blocking) 작업이므로, 이 부분에서 세부 진행률을 알 수 없음
        tts = gTTS(text=text_to_speak, lang='en')

        # 파일로 저장
        tts.save(output_path)
        return True, f"파일 생성 완료: {output_path}"

    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        # 네트워크 오류 등 다양한 gTTS 관련 예외 처리 가능성
        return False, f"TTS 생성 중 오류 발생: {e}\n인터넷 연결 상태를 확인하거나 잠시 후 다시 시도해주세요."

# --- 진행 상태 표시 창 (프로그레스바 추가) ---
progress_window = None
progress_label = None
progress_bar = None # 프로그레스바 변수 추가

def show_progress(msg):
    global progress_window, progress_label, progress_bar
    # 이전 창이 있다면 닫기
    if progress_window and progress_window.winfo_exists():
        progress_window.destroy()

    progress_window = Toplevel(root)
    progress_window.title("처리 중...")
    # 창 크기 조절하여 프로그레스바 공간 확보
    progress_window.geometry("350x130")
    progress_window.resizable(False, False)

    # 메시지 레이블
    progress_label = Label(progress_window, text=msg, font=("맑은 고딕", 11))
    progress_label.pack(pady=(20, 10)) # 상하 패딩 조절

    # 프로그레스바 생성 (indeterminate 모드)
    progress_bar = ttk.Progressbar(progress_window, mode='indeterminate', length=300)
    progress_bar.pack(pady=(0, 20)) # 하단 패딩 추가
    progress_bar.start(10)  # 애니메이션 시작 (10ms 간격으로 업데이트)

    progress_window.grab_set() # 다른 창 상호작용 방지
    root.update_idletasks() # 창 즉시 표시

def update_progress(new_msg):
    # 메시지만 업데이트 (프로그레스바는 계속 움직임)
    if progress_label and progress_window and progress_window.winfo_exists():
        progress_label.config(text=new_msg)
        progress_window.update_idletasks()

def close_progress():
    global progress_window, progress_bar
    if progress_bar:
        progress_bar.stop() # 애니메이션 중지
        progress_bar = None
    if progress_window and progress_window.winfo_exists():
        progress_window.destroy()
        progress_window = None
    progress_label = None


# --- GUI용 백그라운드 작업 함수 (동일) ---
def threaded_tts_creation():
    """TTS 생성을 별도 스레드에서 실행하여 GUI 멈춤 방지"""
    input_text = text_input_area.get("1.0", tk.END).strip()

    if not input_text:
        messagebox.showwarning("입력 필요", "영어 텍스트를 입력해주세요.")
        execute_button.config(state=tk.NORMAL) # 오류 시 버튼 다시 활성화
        return

    try:
        show_progress("영어 TTS 생성 중...\n(텍스트 길이에 따라 시간이 소요될 수 있습니다)")
        # 실제 작업 수행
        success, message = create_tts_audio(input_text)

        # 작업 완료 후 처리
        close_progress() # 작업 완료 후 진행 창 닫기

        if success:
            messagebox.showinfo("성공", message)
        else:
            messagebox.showerror("오류", message)

    except Exception as e:
        close_progress() # 에러 발생 시에도 진행 창 닫기
        messagebox.showerror("심각한 오류", f"예상치 못한 오류 발생: {e}")
    finally:
        # 버튼 다시 활성화
        if root.winfo_exists(): # 메인 윈도우가 닫히지 않았을 경우에만 상태 변경
             execute_button.config(state=tk.NORMAL)


# --- 실행 버튼 클릭 시 호출될 함수 (동일) ---
def on_execute_button_click():
    # 버튼 비활성화 (중복 실행 방지)
    execute_button.config(state=tk.DISABLED)
    # 스레드 시작
    threading.Thread(target=threaded_tts_creation, daemon=True).start()


# --- GUI 구성 (동일) ---
root = tk.Tk()
root.title("텍스트를 영어 음성으로 변환 (gTTS)")
root.geometry("600x450") # 창 크기 조절

frame = tk.Frame(root, padx=15, pady=15)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="아래 입력창에 영어 텍스트를 입력하세요:", font=("맑은 고딕", 10)).pack(anchor="w", pady=(0, 5))

text_input_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=70, height=15, font=("맑은 고딕", 10))
text_input_area.pack(fill="both", expand=True, pady=(0, 10))

execute_button = tk.Button(frame, text="영어 음성 파일 생성 (english.mp3)", command=on_execute_button_click, bg="#4CAF50", fg="white", font=("맑은 고딕", 11, "bold"), width=30, height=2)
execute_button.pack(pady=(5, 0))

root.mainloop()