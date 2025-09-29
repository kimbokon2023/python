# -*- coding: utf-8 -*-
import sys
import os
import threading
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk
from pathlib import Path
import re
import time

# stdout의 인코딩을 UTF-8로 설정 (터미널 환경에 따라 필요할 수 있음)
# GUI 환경에서는 주로 GUI 위젯을 통해 피드백하므로 중요도는 낮을 수 있습니다.
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
except AttributeError: # sys.stdout/stderr가 None인 경우 (예: pythonw.exe로 실행 시)
    pass

# 전역 변수로 취소 이벤트와 프로세스 추가
cancel_event = None
current_process = None

# --- 핵심 기능 함수 ---

def check_ffmpeg():
    """
    FFmpeg가 시스템에 설치되어 있는지 확인합니다.

    Returns:
        bool: FFmpeg가 사용 가능하면 True, 아니면 False
    """
    try:
        subprocess.run(['ffmpeg', '-version'],
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_video_duration(file_path):
    """FFprobe를 사용하여 비디오 길이를 가져옵니다."""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'compact=print_section=0:nokey=1:escape=csv',
            '-show_entries', 'format=duration', str(file_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())
    except:
        pass
    return 0

def parse_ffmpeg_time(line):
    """FFmpeg 출력에서 현재 시간을 파싱합니다."""
    time_match = re.search(r'time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})', line)
    if time_match:
        hours, minutes, seconds, centiseconds = map(int, time_match.groups())
        return hours * 3600 + minutes * 60 + seconds + centiseconds / 100
    return None

def format_time(seconds):
    """초를 시:분:초 형식으로 변환합니다."""
    if seconds <= 0:
        return "00:00:00"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def estimate_remaining_time(current_time, total_duration):
    """남은 시간을 추정합니다."""
    if current_time <= 0:
        return total_duration
    return total_duration - current_time

def get_video_info(file_path):
    """비디오 정보를 가져옵니다 (해상도, 프레임레이트 등)."""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_streams', '-select_streams', 'v:0', str(file_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            if 'streams' in data and len(data['streams']) > 0:
                stream = data['streams'][0]
                width = stream.get('width', 0)
                height = stream.get('height', 0)
                # 프레임레이트 계산
                fps_str = stream.get('r_frame_rate', '30/1')
                try:
                    fps_parts = fps_str.split('/')
                    fps = float(fps_parts[0]) / float(fps_parts[1])
                except:
                    fps = 30.0
                return {'width': width, 'height': height, 'fps': fps}
    except:
        pass
    return {'width': 1920, 'height': 1080, 'fps': 30.0}  # 기본값

def convert_video_file(input_file, output_path, output_format, progress_callback, cancel_event=None):
    """
    동영상 파일을 지정된 포맷으로 변환합니다.

    Args:
        input_file (str): 변환할 동영상 파일 경로
        output_path (str): 변환된 파일을 저장할 경로
        output_format (str): 출력 포맷 ('mp4' 또는 'avi')
        progress_callback (function): 진행 상황 메시지를 전달할 콜백 함수
        cancel_event: 취소 이벤트
    """
    input_path = Path(input_file)
    if not input_path.exists():
        progress_callback(f"❌ 파일을 찾을 수 없습니다: {input_file}\n")
        return False

    # 지원되는 동영상 포맷 확인
    supported_formats = ['.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v']
    if input_path.suffix.lower() not in supported_formats:
        progress_callback(f"❌ 지원되지 않는 파일 형식입니다: {input_file}\n")
        progress_callback(f"지원 형식: {', '.join(supported_formats)}\n")
        return False

    # FFmpeg 확인
    if not check_ffmpeg():
        progress_callback("❌ FFmpeg를 찾을 수 없습니다. FFmpeg를 설치해주세요.\n")
        return False

    output_file = Path(output_path) / f"{input_path.stem}.{output_format}"

    # 비디오 정보 분석
    video_info = get_video_info(input_path)
    width, height, fps = video_info['width'], video_info['height'], video_info['fps']

    progress_callback(f"변환 시작: {input_path.name}\n")
    progress_callback(f"원본 해상도: {width}x{height} @ {fps:.1f}fps\n")
    progress_callback(f"저장 경로: {output_file}\n")

    try:
        # 환경 변수 설정 (한글 경로 처리)
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        # FFmpeg 명령어: 동영상 파일을 지정된 포맷으로 변환
        if output_format == 'mp4':
            # MP4: 스마트TV 최적 호환성 설정

            # 해상도 제한 (4K는 30fps, FHD는 60fps 제한)
            video_filter = []
            target_fps = fps

            if height > 2160:  # 4K 초과
                video_filter.append('scale=3840:2160')  # 4K로 다운스케일
                target_fps = min(fps, 30)
                progress_callback("📺 4K로 다운스케일 (스마트TV 호환성)\n")
            elif height > 1080 and fps > 30:  # 4K에서 30fps 초과
                target_fps = 30
                progress_callback("🎬 30fps로 제한 (4K 스마트TV 호환성)\n")
            elif height <= 1080 and fps > 60:  # FHD에서 60fps 초과
                target_fps = 60
                progress_callback("🎬 60fps로 제한 (FHD 스마트TV 호환성)\n")

            # 짝수 해상도 강제
            video_filter.append('scale=trunc(iw/2)*2:trunc(ih/2)*2')

            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                # 비디오 설정
                '-c:v', 'libx264',           # H.264 (AVC) 코덱
                '-profile:v', 'high',        # High 프로파일 (호환성 최고)
                '-level', '4.1',             # Level 4.1 (대부분 TV 지원)
                '-preset', 'medium',         # 품질/속도 균형
                '-crf', '20',                # 고품질 (18-23 권장)
                '-maxrate', '15M',           # 최대 비트레이트 15Mbps
                '-bufsize', '30M',           # 버퍼 크기
                '-vf', ','.join(video_filter),  # 비디오 필터 적용
                '-r', str(target_fps),       # 목표 프레임레이트
                # 오디오 설정
                '-c:a', 'aac',               # AAC 코덱 (최고 호환성)
                '-b:a', '192k',              # 오디오 비트레이트 192kbps
                '-ac', '2',                  # 스테레오 강제 (서라운드 제거)
                '-ar', '48000',              # 샘플레이트 48kHz
                # 호환성 설정
                '-movflags', '+faststart',   # 스트리밍 최적화
                '-map', '0:v:0',             # 첫 번째 비디오 트랙만
                '-map', '0:a:0',             # 첫 번째 오디오 트랙만
                '-sn',                       # 자막 제거
                '-progress', 'pipe:1',       # 진행률 출력
                '-y',                        # 덮어쓰기 확인
                str(output_file)
            ]
        elif output_format == 'avi':
            # AVI: 호환성을 위해 XVID + MP3 사용
            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-c:v', 'libxvid',   # XVID 비디오 코덱
                '-c:a', 'libmp3lame', # MP3 오디오 코덱
                '-q:v', '3',         # 비디오 품질 (1-31, 낮을수록 고품질)
                '-q:a', '2',         # 오디오 품질 (0-9, 낮을수록 고품질)
                '-progress', 'pipe:1',  # 진행률 출력
                '-y',  # 덮어쓰기 확인
                str(output_file)
            ]
        else:
            progress_callback(f"❌ 지원되지 않는 출력 포맷: {output_format}\n")
            return False 

        # 프로세스 실행 (실시간 진행률 표시)
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
            encoding='utf-8',
            errors='replace',  # 인코딩 오류 시 대체 문자 사용
            env=env  # 환경 변수 적용
        )

        # 비디오 총 길이 가져오기 (진행률 계산용)
        duration = get_video_duration(input_path)
        progress_callback(f"📹 비디오 길이: {format_time(duration)}\n")

        # 실시간 진행률 모니터링
        try:
            for line in iter(process.stdout.readline, ''):
                if cancel_event and cancel_event.is_set():
                    process.terminate()
                    progress_callback("❌ 사용자에 의해 취소되었습니다.\n")
                    return False

                # 안전한 문자열 처리
                try:
                    if isinstance(line, bytes):
                        line = line.decode('utf-8', errors='replace')

                    # FFmpeg 진행률 파싱
                    if 'time=' in line:
                        current_time = parse_ffmpeg_time(line)
                        if current_time and duration > 0:
                            progress_percent = (current_time / duration) * 100
                            remaining_time = estimate_remaining_time(current_time, duration)
                            progress_callback(f"진행률: {progress_percent:.1f}% | 남은 시간: {format_time(remaining_time)}\r")
                except UnicodeDecodeError:
                    # 인코딩 오류는 무시하고 계속 진행
                    continue
        except Exception as e:
            progress_callback(f"⚠️ 진행률 모니터링 오류 (변환은 계속됩니다): {str(e)}\n")

        process.wait()
        return_code = process.returncode

        if return_code == 0:
            progress_callback(f"✅ 변환 성공: {output_file.name}\n")
            return True
        else:
            progress_callback(f"❌ 변환 실패 (종료 코드: {return_code})\n")
            return False

    except Exception as e:
        progress_callback(f"❌ 변환 중 오류 발생: {str(e)}\n")
        return False

def select_video_file():
    """
    동영상 파일을 선택하는 대화상자를 엽니다.

    Returns:
        str: 선택된 파일 경로 또는 None
    """
    file_path = filedialog.askopenfilename(
        title="동영상 파일 선택",
        filetypes=[
            ("Video files", "*.mkv *.avi *.mov *.wmv *.flv *.webm *.m4v *.mp4"),
            ("MKV files", "*.mkv"),
            ("AVI files", "*.avi"),
            ("MOV files", "*.mov"),
            ("All files", "*.*")
        ]
    )
    return file_path if file_path else None

# --- GUI 관련 함수 ---

def select_file():
    """동영상 파일을 선택하는 함수"""
    file_path = select_video_file()
    if file_path:
        file_entry.config(state=tk.NORMAL)
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        file_entry.config(state='readonly')

def get_selected_format():
    """선택된 출력 포맷을 반환합니다."""
    if mp4_var.get() and avi_var.get():
        return 'both'
    elif mp4_var.get():
        return 'mp4'
    elif avi_var.get():
        return 'avi'
    else:
        return None

def cancel_conversion():
    """변환을 취소합니다."""
    global cancel_event
    if cancel_event:
        cancel_event.set()
        progress_bar['value'] = 0
        progress_label.config(text="취소됨")
        cancel_button.config(state=tk.DISABLED)
        convert_button.config(state=tk.NORMAL)

def threaded_conversion():
    """GUI에서 변환 버튼 클릭 시 실행될 함수 (스레드 사용)"""
    input_file = file_entry.get().strip()
    output_path = path_entry.get().strip()
    output_format = get_selected_format()

    if not input_file:
        messagebox.showwarning("파일 선택 필요", "변환할 동영상 파일을 선택해주세요.")
        return

    if not output_path or not os.path.isdir(output_path):
        messagebox.showerror("오류", "유효한 저장 폴더를 선택해주세요.")
        return

    if not output_format:
        messagebox.showwarning("포맷 선택 필요", "출력 포맷(MP4 또는 AVI)을 선택해주세요.")
        return

    # 로그창 비우기
    log_textbox.config(state=tk.NORMAL)
    log_textbox.delete(1.0, tk.END)
    log_textbox.config(state=tk.DISABLED)

    # 진행 상황 표시 함수 (GUI 업데이트용)
    def update_log(msg):
        if msg.endswith('\r'):  # 진행률 업데이트
            # 프로그래스 바 업데이트
            if '진행률:' in msg:
                try:
                    percent_match = re.search(r'진행률: (\d+\.\d+)%', msg)
                    if percent_match:
                        percent = float(percent_match.group(1))
                        progress_bar['value'] = percent
                        progress_label.config(text=msg.strip())
                        root.update_idletasks()
                except:
                    pass
        else:
            log_textbox.config(state=tk.NORMAL)
            log_textbox.insert(tk.END, msg)
            log_textbox.see(tk.END) # 스크롤 자동 내림
            log_textbox.config(state=tk.DISABLED)
            root.update_idletasks() # GUI 업데이트 강제

    # 전역 취소 이벤트 설정
    global cancel_event
    cancel_event = threading.Event()

    # 버튼 상태 변경
    convert_button.config(state=tk.DISABLED)
    cancel_button.config(state=tk.NORMAL)

    # 프로그래스 바 초기화
    progress_bar['value'] = 0
    progress_label.config(text="변환 준비 중...")

    # 스레드 생성 및 시작
    thread = threading.Thread(target=run_conversion_task, args=(input_file, output_path, output_format, update_log), daemon=True)
    thread.start()

def run_conversion_task(input_file, output_path, output_format, callback):
    """실제 변환을 수행하고 버튼 상태를 복구하는 스레드 작업"""
    global cancel_event
    try:
        if output_format == 'both':
            # MP4와 AVI 둘 다 변환
            callback("📋 MP4와 AVI 두 포맷으로 변환을 시작합니다...\n")

            success_mp4 = convert_video_file(input_file, output_path, 'mp4', callback, cancel_event)
            if not cancel_event.is_set():
                success_avi = convert_video_file(input_file, output_path, 'avi', callback, cancel_event)
            else:
                success_avi = False

            if success_mp4 and success_avi:
                callback("🎉 모든 변환이 완료되었습니다!\n")
            elif success_mp4 or success_avi:
                callback("⚠️ 일부 변환이 완료되었습니다.\n")
            else:
                callback("💥 모든 변환에 실패했습니다.\n")
        else:
            # 단일 포맷 변환
            success = convert_video_file(input_file, output_path, output_format, callback, cancel_event)
            if success:
                callback(f"🎉 {output_format.upper()} 변환이 완료되었습니다!\n")
            else:
                callback(f"💥 {output_format.upper()} 변환에 실패했습니다.\n")
    except Exception as e:
        callback(f"❌ 예기치 못한 오류: {str(e)}\n")
    finally:
        # 작업 완료 후 버튼 상태 복구
        convert_button.config(state=tk.NORMAL)
        cancel_button.config(state=tk.DISABLED)
        if not cancel_event.is_set():
            progress_bar['value'] = 100
            progress_label.config(text="완료")
        cancel_event = None

def browse_directory():
    """저장 폴더 선택 대화상자 열기"""
    directory = filedialog.askdirectory(initialdir=path_entry.get() or 'c:\\')
    if directory: # 사용자가 폴더를 선택한 경우
        path_entry.config(state=tk.NORMAL)
        path_entry.delete(0, tk.END)
        path_entry.insert(0, directory)
        path_entry.config(state='readonly') # 다시 읽기 전용으로

# --- GUI 구성 ---
root = tk.Tk()
root.title("동영상 포맷 변환기")
root.geometry("700x600") # 세로 길이 조정

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# 동영상 파일 선택
tk.Label(frame, text="변환할 동영상 파일:").pack(anchor="w")
file_frame = tk.Frame(frame)
file_frame.pack(fill="x", pady=(0, 10))

file_entry = tk.Entry(file_frame, width=65, state='readonly') # 읽기 전용으로 시작
file_entry.pack(side="left", fill="x", expand=True)

select_file_button = tk.Button(file_frame, text="파일 선택", command=select_file, width=10)
select_file_button.pack(side="left", padx=(5, 0))

# 저장 경로 선택
tk.Label(frame, text="저장 폴더:").pack(anchor="w")
path_frame = tk.Frame(frame)
path_frame.pack(fill="x", pady=(0, 10))

path_entry = tk.Entry(path_frame, width=65, state='readonly') # 읽기 전용으로 시작
path_entry.pack(side="left", fill="x", expand=True)

# 기본 경로 설정 및 폴더 생성 확인
default_output_path = 'c:\\converted'
if not os.path.exists(default_output_path):
    try:
        os.makedirs(default_output_path)
        print(f"기본 저장 폴더 생성: {default_output_path}")
    except Exception as e:
        print(f"기본 저장 폴더 생성 실패: {e}")
        default_output_path = os.getcwd() # 실패 시 현재 작업 디렉토리로

path_entry.config(state=tk.NORMAL)
path_entry.insert(0, default_output_path)
path_entry.config(state='readonly')

browse_button = tk.Button(path_frame, text="폴더 선택", command=browse_directory, width=10)
browse_button.pack(side="left", padx=(5, 0))

# 출력 포맷 선택
tk.Label(frame, text="출력 포맷 선택:").pack(anchor="w", pady=(10, 0))
format_frame = tk.Frame(frame)
format_frame.pack(fill="x", pady=(0, 10))

# 체크박스 변수
mp4_var = tk.BooleanVar(value=True)  # 기본적으로 MP4 선택
avi_var = tk.BooleanVar()

# 체크박스
mp4_checkbox = tk.Checkbutton(format_frame, text="MP4 (스마트TV 최적화 - H.264/AAC, 15Mbps 제한)", variable=mp4_var, font=('Arial', 10))
mp4_checkbox.pack(anchor="w")

avi_checkbox = tk.Checkbutton(format_frame, text="AVI (구형 기기 호환 - XVID/MP3)", variable=avi_var, font=('Arial', 10))
avi_checkbox.pack(anchor="w")

# 변환 및 취소 버튼
button_frame = tk.Frame(frame)
button_frame.pack(pady=10)

convert_button = tk.Button(button_frame, text="변환 시작", command=threaded_conversion, bg="#4CAF50", fg="white", width=12, height=2)
convert_button.pack(side="left", padx=(0, 5))

cancel_button = tk.Button(button_frame, text="취소", command=cancel_conversion, bg="#f44336", fg="white", width=8, height=2, state=tk.DISABLED)
cancel_button.pack(side="left")

# 프로그래스 바
progress_frame = tk.Frame(frame)
progress_frame.pack(fill="x", pady=(10, 0))

tk.Label(progress_frame, text="진행 상황:").pack(anchor="w")
progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
progress_bar.pack(fill="x", pady=(5, 0))

progress_label = tk.Label(progress_frame, text="대기 중", font=('Arial', 9))
progress_label.pack(anchor="w", pady=(2, 0))

# 로그 출력
tk.Label(frame, text="로그:").pack(anchor="w", pady=(10, 0))
log_textbox = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=12, state=tk.DISABLED) # 비활성화 상태로 시작
log_textbox.pack(fill="both", expand=True, pady=(5, 0))

root.mainloop()