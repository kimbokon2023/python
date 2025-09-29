# -*- coding: utf-8 -*- # 파일 상단에 인코딩 명시
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchFrameException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager # Service() 사용 시 필요 없을 수 있음
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
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import font as tkFont, messagebox, IntVar
import json
# import numpy as np # 사용되지 않음
import re
import subprocess
import psutil
import requests
from screeninfo import get_monitors
import google.generativeai as genai


# ==============================================================
# 전역 변수 및 초기 설정
# ==============================================================
# !!! 보안 경고: API 키를 코드에 직접 포함하는 것은 매우 위험합니다 !!!
# !!! 이 키는 이미 노출되었을 수 있으므로 즉시 폐기하고 새로 발급받는 것을 강력히 권장합니다. !!!
GEMINI_API_KEY = "AIzaSyDU4BBPxngNjSlI-xdwrIdN0TzWc10_Hyg" # <<< 사용자님이 제공한 실제 API 키

driver = None
ReserveExecute = False
user_id = ""
user_pw = ""
selected_options = [] # 전역 리스트로 변경

# 실행 번호 변수 초기화 (현재 사용되지 않으나 유지)
current_execution_number = 0

# --- 화면 정보 ---
try:
    monitors = get_monitors()
    for monitor in monitors:
        print(f"Monitor {monitor.name}: Width={monitor.width}, Height={monitor.height}, X={monitor.x}, Y={monitor.y}")
except Exception as e:
    print(f"모니터 정보 로드 중 오류 발생: {e}")
    monitors = []

start_time = time.time()
current_time_str = datetime.now().strftime("%Y%m%d_%H%M%S") # 변수명 충돌 방지

# --- GUI 설정 ---
window = tk.Tk()
window.title("네이버 블로그 공감 댓글 ")
try:
    customFont = tkFont.Font(family="굴림", size=13)
except tk.TclError:
    print("경고: '굴림' 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
    customFont = tkFont.Font(size=13)

exit_program = False
id_pw_dict = {}

# --- 파일 경로 설정 ---
try:
    if getattr(sys, 'frozen', False): # PyInstaller 등으로 패키징된 경우
        application_path = sys._MEIPASS
    else: # 일반 스크립트로 실행된 경우
        application_path = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(application_path, 'data')
    os.makedirs(data_dir, exist_ok=True) # data 디렉토리 생성

    # 필요한 파일 경로 정의
    data_file = os.path.join(data_dir, 'selected_options.json')
    idpw_saved_file = os.path.join(data_dir, 'idpwsaved.json')
    selected_id_file = os.path.join(data_dir, 'selected_id.json')
    repeat_count_file = os.path.join(data_dir, 'repeat_count.json')
    visit_path = os.path.join(data_dir, 'visit.txt')
    log_file = os.path.join(data_dir, 'log.txt')
    reservation_list_path = os.path.join(data_dir, 'reservation_list.json')
    chrome_txt_path = os.path.join(data_dir, 'chrome.txt')
    random_prefix_file = os.path.join(data_dir, 'random_sayhell_prefix.txt')
    sayhello_file = os.path.join(data_dir, 'sayhello.txt')

except Exception as e:
    print(f"파일 경로 설정 중 치명적 오류: {e}")
    messagebox.showerror("오류", f"프로그램 경로 설정 실패:\n{e}") # GUI 사용 가능하면 표시
    sys.exit(1) # 프로그램 종료

# --- 로깅 설정 ---
try:
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # 파일 핸들러 설정 (기존 핸들러 제거 후 추가)
    log_handler = logging.FileHandler(log_file, encoding='utf-8')
    log_handler.setFormatter(log_formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    # 기존 핸들러 제거 (중복 로깅 방지)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    root_logger.addHandler(log_handler)

    logging.info("="*30 + " 프로그램 시작 " + "="*30)
except Exception as e:
    print(f"로깅 설정 중 오류: {e}")

# --- GUI 관련 변수 ---
repeat_count_var = tk.StringVar(window)
id_var = tk.StringVar(window)
pw_var = tk.StringVar(window)
var_dict = {}
run_at = None # 예약 시간 저장용
seconds_var = tk.StringVar(value='0')
reservation_list = [] # 예약 목록 저장용 전역 리스트


# ==============================================================
# 함수 정의
# ==============================================================

# --- 예약 목록 관련 함수 ---
def add_reservation_to_list():
    """ 현재 GUI 설정을 예약 목록에 추가 """
    id_value = id_var.get()
    pw_value = pw_var.get()
    selected_options_values = [option for option, var in var_dict.items() if var.get() == 1]
    repeat_count_value = repeat_count_var.get()

    if not id_value or not pw_value or "(ID" in id_value:
        messagebox.showwarning("입력 오류", "ID와 비밀번호를 모두 입력하거나 선택해주세요.")
        return
    if not repeat_count_value.isdigit() or int(repeat_count_value) <= 0:
        messagebox.showwarning("입력 오류", "반복 횟수는 1 이상의 숫자로 입력해주세요.")
        return

    reservation = {
        "id": id_value, "pw": pw_value, "options": selected_options_values,
        "repeat_count": int(repeat_count_value), "current_count": 0
    }
    reservation_list.append(reservation)
    save_reservation_list(reservation_list)
    update_listbox()
    logging.info(f"예약 추가됨: ID={id_value}, 옵션={selected_options_values}, 반복={repeat_count_value}")

def delete_selected_reservation():
    """ 선택된 예약을 목록에서 삭제 """
    selected_indices = listbox.curselection()
    if selected_indices:
        if messagebox.askyesno("삭제 확인", "선택한 예약을 삭제하시겠습니까?"):
            selected_index = selected_indices[0]
            if 0 <= selected_index < len(reservation_list):
                removed = reservation_list.pop(selected_index)
                save_reservation_list(reservation_list)
                update_listbox()
                logging.info(f"예약 삭제됨 (Index {selected_index}): ID={removed.get('id')}")
            else: messagebox.showerror("오류", "잘못된 선택입니다.")
    else: messagebox.showwarning("선택 오류", "삭제할 예약을 목록에서 선택해주세요.")

def delete_all_reservations():
    """ 모든 예약을 삭제 """
    if messagebox.askyesno("전체 삭제 확인", "정말로 모든 예약을 삭제하시겠습니까?"):
        global reservation_list
        reservation_list = []
        save_reservation_list(reservation_list)
        update_listbox()
        logging.info("모든 예약 삭제됨.")

def update_listbox():
    """ 리스트박스 내용을 현재 예약 목록으로 업데이트 """
    global reservation_list
    listbox.delete(0, tk.END)
    if reservation_list:
        for index, res in enumerate(reservation_list):
            opts = ", ".join(res.get('options', []))
            item_text = f"[{index+1}] {res.get('id','N/A')} (옵션:{opts}, 반복:{res.get('repeat_count','N/A')}, 현재:{res.get('current_count','N/A')})"
            listbox.insert(index, item_text)
    else:
        listbox.insert(0, "  (예약된 작업 없음)")

def load_reservation_list():
    """ JSON 파일에서 예약 목록 로드 (전역 변수 업데이트)"""
    global reservation_list
    try:
        if not os.path.exists(reservation_list_path):
             reservation_list = []
             return
        with open(reservation_list_path, "r", encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                 valid_reservations = []
                 for item in data: # 간단한 유효성 검사
                     if isinstance(item, dict) and all(k in item for k in ['id', 'pw', 'options', 'repeat_count']):
                         item['current_count'] = item.get('current_count', 0) # 없으면 0으로 초기화
                         valid_reservations.append(item)
                     else: logging.warning(f"잘못된 예약 항목 발견, 무시됨: {item}")
                 reservation_list = valid_reservations
                 logging.info(f"{len(reservation_list)}개의 유효한 예약 로드.")
            else:
                logging.warning(f"{reservation_list_path} 파일 형식이 리스트가 아님.")
                reservation_list = []
    except json.JSONDecodeError:
        logging.error(f"{reservation_list_path} 파일 파싱 오류.")
        reservation_list = []
    except Exception as e:
        logging.error(f"예약 목록 로드 중 오류: {e}", exc_info=True)
        reservation_list = []

def save_reservation_list(reservation_list_data):
    """ 예약 목록을 JSON 파일에 저장 """
    try:
        with open(reservation_list_path, "w", encoding='utf-8') as file:
            json.dump(reservation_list_data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.error(f"예약 목록 저장 중 오류: {e}", exc_info=True)

# --- 작업 실행 관련 함수 ---
def perform_actions_sequentially():
    """ 예약 목록을 순차적으로 일괄 실행 (스레드 사용) """
    global ReserveExecute, reservation_list, exit_program

    load_reservation_list() # 항상 최신 목록으로 시작
    if not reservation_list:
        messagebox.showinfo("알림", "실행할 예약 목록이 없습니다.")
        return
    if ReserveExecute:
        messagebox.showwarning("실행 중", "이미 작업이 진행 중입니다.")
        return

    if messagebox.askyesno("일괄 실행 확인", f"총 {len(reservation_list)}개의 예약을 순차적으로 실행하시겠습니까?"):
        ReserveExecute = True
        exit_program = False
        print(f"\n=== 예약 목록 일괄 실행 시작 (총 {len(reservation_list)}개) ===")
        logging.info(f"예약 목록 일괄 실행 시작 (총 {len(reservation_list)}개)")
        disable_gui_elements()
        # 별도 스레드에서 실행
        execution_thread = threading.Thread(target=run_reservations_thread, args=(reservation_list.copy(),), daemon=True)
        execution_thread.start()

def run_reservations_thread(reservations_to_run):
     """ 예약 실행 로직을 처리하는 별도 스레드 """
     global ReserveExecute, exit_program

     total_count = len(reservations_to_run)
     for i, reservation in enumerate(reservations_to_run):
         if exit_program:
             logging.info("사용자 요청으로 예약 실행 중단됨.")
             break
         print(f"\n--- 예약 {i+1}/{total_count} 실행 시작 ({reservation.get('id', 'N/A')}) ---")
         logging.info(f"예약 {i+1}/{total_count} 실행 시작 - ID: {reservation.get('id', 'N/A')}")
         try:
             execute_action(reservation.copy(), i) # 여기서 execute_action 호출
         except Exception as e:
             print(f"!!! 예약 {i+1} ({reservation.get('id', 'N/A')}) 실행 중 최상위 오류: {e}")
             logging.error(f"ID {reservation.get('id', 'N/A')} 예약 실행 중 최상위 오류: {e}", exc_info=True)
             time.sleep(5) # 오류 시 잠시 대기 후 계속
         finally:
              print(f"--- 예약 {i+1}/{total_count} 실행 완료 ({reservation.get('id', 'N/A')}) ---")
              logging.info(f"예약 {i+1}/{total_count} 실행 완료 - ID: {reservation.get('id', 'N/A')}")

         if exit_program: break
         sleep_interval = random.uniform(10, 20)
         print(f"다음 예약까지 {sleep_interval:.1f}초 대기...")
         try: sleep_with_esc(sleep_interval)
         except KeyboardInterrupt: exit_program = True; break

     ReserveExecute = False
     print("\n=== 예약 목록 일괄 실행 완료 ===")
     logging.info("예약 목록 일괄 실행 완료.")
     window.after(0, enable_gui_elements)
     window.after(0, lambda: messagebox.showinfo("완료", "모든 예약 실행을 완료했습니다."))

def close_all_chrome_windows():
    """ 실행 중인 모든 Chrome 및 ChromeDriver 프로세스 종료 """
    print("기존 Chrome/ChromeDriver 프로세스를 종료합니다...")
    closed_count = 0
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            proc_name = proc.info['name'].lower()
            if 'chrome' in proc_name:
                logging.debug(f"Terminating process '{proc_name}' (PID: {proc.info['pid']})...")
                p = psutil.Process(proc.info['pid'])
                p.terminate()
                closed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): pass
        except Exception as e: logging.error(f"프로세스 종료 중 오류 (PID: {proc.info.get('pid', 'N/A')}): {e}")

    if closed_count > 0:
        print(f"{closed_count}개의 Chrome 관련 프로세스 종료 시도.")
        time.sleep(2) # 종료 시간 확보
    else:
        print("실행 중인 Chrome 관련 프로세스 없음.")

# --- 타이머 및 예약 실행 함수 ---
def update_timer_display():
    """ 예약 실행까지 남은 시간을 GUI에 표시 """
    global run_at, timer_after_id
    try:
        if run_at and isinstance(run_at, datetime):
            remaining = run_at - datetime.now()
            if remaining.total_seconds() > 0:
                h, rem = divmod(remaining.total_seconds(), 3600)
                m, s = divmod(rem, 60)
                timer_label.config(text=f"예약 실행까지: {int(h):02d}:{int(m):02d}:{int(s):02d}")
                timer_after_id = window.after(1000, update_timer_display)
            else:
                timer_label.config(text="예약 시간 도달")
                run_at = None
        else:
            timer_label.config(text="")
            if 'timer_after_id' in globals() and timer_after_id:
                window.after_cancel(timer_after_id)
                timer_after_id = None
    except Exception as e: logging.error(f"타이머 업데이트 오류: {e}")

def schedule_single_action():
    """ 현재 GUI 설정을 바탕으로 단일 작업을 예약하거나 즉시 실행 """
    global run_at, ReserveExecute, timer_after_id

    if ReserveExecute: messagebox.showwarning("실행 중", "작업이 이미 진행 중입니다."); return

    try: seconds_to_wait = int(seconds_var.get()); assert seconds_to_wait >= 0
    except: messagebox.showerror("입력 오류", "예약 시간(초)은 0 이상의 숫자로 입력하세요."); return

    # 현재 설정값 가져오기
    cfg = {
        "id": id_var.get(), "pw": pw_var.get(),
        "options": [opt for opt, var in var_dict.items() if var.get() == 1],
        "repeat_count": 1, "current_count": 0 # 단일 실행용 기본값
    }
    try: cfg["repeat_count"] = int(repeat_count_var.get()); assert cfg["repeat_count"] > 0
    except: messagebox.showerror("입력 오류", "반복 횟수는 1 이상의 숫자로 입력하세요."); return
    if not cfg["id"] or not cfg["pw"] or "(ID" in cfg["id"]: messagebox.showerror("입력 오류", "ID/PW를 확인하세요."); return

    # 실행 함수 (스레드에서 호출될)
    def _run_single():
        global ReserveExecute
        ReserveExecute = True
        print("\n=== 현재 설정 실행 시작 ===")
        logging.info(f"현재 설정 실행 시작 - ID: {cfg['id']}")
        disable_gui_elements()
        try:
            execute_action(cfg.copy(), -1) # -1은 단일 실행 식별
        except Exception as e: logging.error(f"현재 설정 실행 중 오류 - ID: {cfg['id']}: {e}", exc_info=True)
        finally:
            ReserveExecute = False
            print("=== 현재 설정 실행 완료 ===")
            logging.info(f"현재 설정 실행 완료 - ID: {cfg['id']}")
            window.after(0, enable_gui_elements)
            window.after(0, lambda: timer_label.config(text="실행 완료"))

    # 예약 또는 즉시 실행
    if seconds_to_wait > 0:
        run_at = datetime.now() + timedelta(seconds=seconds_to_wait)
        print(f"{seconds_to_wait}초 후 작업 실행 예약: {run_at.strftime('%H:%M:%S')}")
        logging.info(f"{seconds_to_wait}초 후 작업 실행 예약 - ID: {cfg['id']}")
        timer = threading.Timer(seconds_to_wait, lambda: threading.Thread(target=_run_single, daemon=True).start())
        timer.start()
        update_timer_display()
    else:
        print("즉시 작업 실행 시작...")
        logging.info(f"즉시 작업 실행 시작 - ID: {cfg['id']}")
        threading.Thread(target=_run_single, daemon=True).start()
        timer_label.config(text="즉시 실행 중...")


# --- 설정 저장/로드 함수 ---
def save_repeat_count(count):
    try:
        with open(repeat_count_file, 'w', encoding='utf-8') as f: json.dump({'repeat_count': int(count)}, f)
    except: pass # 오류 무시

def save_current_run_count(index, count):
    """ 예약 목록의 특정 항목 진행 상황 저장 """
    global reservation_list
    try:
        if 0 <= index < len(reservation_list):
            reservation_list[index]['current_count'] = count
            save_reservation_list(reservation_list)
        # else: logging.warning(f"잘못된 인덱스({index}) 저장 시도.") # 너무 빈번할 수 있음
    except Exception as e: logging.error(f"현재 실행 횟수 저장 오류 (Index: {index}): {e}")

def load_repeat_count():
    try:
        if not os.path.exists(repeat_count_file): return '1'
        with open(repeat_count_file, 'r', encoding='utf-8') as f: data = json.load(f)
        count = data.get('repeat_count', '1'); return str(int(count)) if str(count).isdigit() and int(count) > 0 else '1'
    except: return '1'

def sleep_with_esc(duration):
    """ ESC 감지하며 대기 (KeyboardInterrupt 발생시킴) """
    start = time.time()
    while time.time() - start < duration:
        if exit_program: raise KeyboardInterrupt
        time.sleep(0.1)

def on_closing():
    """ 창 닫기 시 처리 """
    if messagebox.askokcancel("종료 확인", "작업 중인 내용이 있다면 중단될 수 있습니다.\n정말로 종료하시겠습니까?"):
        global exit_program
        exit_program = True
        logging.info("프로그램 종료 요청됨.")
        save_selected_id(id_var.get()); save_repeat_count(repeat_count_var.get())
        if driver:
            try: driver.quit()
            except: pass
        window.destroy()

def save_selected_id(selected_id):
    try:
        with open(selected_id_file, 'w', encoding='utf-8') as f: json.dump({'selected_id': selected_id}, f)
    except Exception as e: logging.error(f"선택 ID 저장 오류: {e}")

def load_selected_id():
    try:
        if not os.path.exists(selected_id_file): return None
        with open(selected_id_file, 'r', encoding='utf-8') as f: data = json.load(f); return data.get('selected_id')
    except: return None

def load_saved_id_pw():
    """ 로컬 ID/PW 파일 로드 """
    try:
        if not os.path.exists(idpw_saved_file): return {}
        with open(idpw_saved_file, 'r', encoding='utf-8') as f: return json.load(f)
    except Exception as e: logging.error(f"로컬 ID/PW 로드 오류: {e}"); return {}

def save_id_pw(id_pw_data):
    """ ID/PW 로컬 파일 저장 """
    try:
        with open(idpw_saved_file, 'w', encoding='utf-8') as f: json.dump(id_pw_data, f, indent=2, ensure_ascii=False)
    except Exception as e: logging.error(f"ID/PW 저장 오류: {e}")

def load_selected_options():
    """ 마지막 선택 옵션 로드 """
    try:
        if not os.path.exists(data_file): return []
        with open(data_file, "r", encoding='utf-8') as f: data = json.load(f); return data if isinstance(data, list) else []
    except: return []

def save_selected_options(options_to_save):
    """ 현재 선택 옵션 저장 """
    try:
        with open(data_file, "w", encoding='utf-8') as f: json.dump(options_to_save, f, ensure_ascii=False)
    except Exception as e: logging.error(f"선택 옵션 저장 오류: {e}")

def on_checkbox_change(*args):
    """ 체크박스 변경 시 전역 변수 및 파일 업데이트 """
    global selected_options
    selected_options = [opt for opt, var in var_dict.items() if var.get() == 1]
    save_selected_options(selected_options)

def check_esc_thread_func():
    """ ESC 키 입력을 감지하는 백그라운드 스레드 """
    global exit_program
    print("ESC 감지 스레드 시작됨. 종료하려면 ESC 키를 누르세요.")
    try:
        keyboard.wait('esc')
        if not exit_program: # 이미 종료 중이 아니라면
            print("\nESC 키 입력 감지! 프로그램 종료 요청...")
            logging.warning("ESC 키 입력 감지! 프로그램 종료 요청...")
            exit_program = True
            window.after(0, on_closing) # GUI 스레드에서 종료 처리
    except Exception as e:
        logging.error(f"ESC 감지 스레드 오류: {e}")

# --- Selenium 관련 함수 ---
def wait_for_element(driver_instance, by, selector, timeout=10):
    """ Selenium 요소를 명시적으로 대기 (존재 확인) """
    try:
        return WebDriverWait(driver_instance, timeout).until(EC.presence_of_element_located((by, selector)))
    except TimeoutException: logging.warning(f"요소 '{selector}' 시간 초과 ({timeout}초)."); raise
    except Exception as e: logging.error(f"요소 '{selector}' 대기 중 오류: {e}"); raise

def open_webpage(driver_instance, url):
    """ 웹페이지 열고 소스 반환 (오류 처리 강화) """
    try:
        current_url = driver_instance.current_url
        # URL 비교 시 마지막 '/' 제거 후 비교 (옵션)
        if current_url.rstrip('/') != url.rstrip('/'):
            logging.info(f"페이지 이동: {url}")
            driver_instance.get(url)
            # 페이지 로딩 완료 대기 (JavaScript readyState 사용)
            WebDriverWait(driver_instance, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            logging.debug(f"페이지 로딩 완료: {url}")
        # else: logging.debug("이미 해당 URL, 이동 생략.")
        # 필요한 경우 추가적인 안정화 시간
        # time.sleep(random.uniform(0.5, 1.5))
        return driver_instance.page_source
    except TimeoutException:
        logging.error(f"페이지 로딩 시간 초과(30초): {url}")
        raise
    except Exception as e:
        logging.error(f"웹페이지({url}) 열기 실패: {e}", exc_info=True)
        raise

# --- 메시지/키워드 관련 함수 ---
def load_messages_from_file(file_path):
    """ 파일에서 메시지 목록 로드 """
    messages = []
    try:
        if not os.path.exists(file_path): logging.warning(f"메시지 파일 없음: {file_path}"); return []
        with open(file_path, 'r', encoding='utf-8') as f: messages = [line.strip() for line in f if line.strip()]
        logging.debug(f"{len(messages)}개 메시지 로드: {file_path}")
    except Exception as e: logging.error(f"메시지 파일 로드 오류 '{file_path}': {e}")
    return messages

def select_random_message(messages, default="안녕하세요! 좋은 글 잘 보고 갑니다."):
    """ 리스트에서 랜덤 메시지 선택 """
    return random.choice(messages) if messages else default

def select_random_location():
    """ 랜덤 지역/일반 키워드 선택 """
    locations = [ "서울", "부산", "인천", "대구", "대전", "광주", "울산", "세종", "수원", "창원", "강남", "홍대", "해운대", "전주", "경주", "제주", "맛집", "여행", "카페", "일상", "리뷰", "후기", "정보", "사진", "풍경" ]
    return random.choice(locations)

def get_post_id_from_href(href):
    """ 블로그 URL에서 포스트 ID 추출 (간단 버전) """
    try: return href.split('/')[-1].split('?')[0]
    except: return None

# --- ID/PW 관련 함수 ---
def load_default_id_pw():
    """ 원격 또는 로컬에서 ID/PW 데이터 로드 """
    global id_pw_dict
    remote_url = "http://8440.co.kr/data/idpw.json"
    loaded_data = {}
    try:
        response = requests.get(remote_url, timeout=5)
        response.raise_for_status()
        loaded_data = response.json()
        if not isinstance(loaded_data, dict): raise ValueError("원격 데이터 형식 오류")
        print("원격 ID/PW 목록 로드 성공."); logging.info("원격 ID/PW 로드 성공.")
        save_id_pw(loaded_data) # 로컬 백업
    except Exception as e:
        print(f"원격 ID/PW 로드 실패: {e}. 로컬 파일 시도..."); logging.warning(f"원격 ID/PW 로드 실패: {e}")
        loaded_data = load_saved_id_pw()
        if loaded_data: print("로컬 ID/PW 목록 로드 성공."); logging.info("로컬 ID/PW 로드 성공.")
        else: print("로컬 ID/PW 목록 로드 실패."); logging.error("ID/PW 목록 로드 최종 실패.")
    id_pw_dict = loaded_data
    return id_pw_dict

def update_pw(*args):
    """ GUI에서 ID 변경 시 PW 업데이트 """
    pw_var.set(id_pw_dict.get(id_var.get(), ''))

def disable_gui_elements():
    """ 작업 실행 중 GUI 요소 비활성화 (종료 버튼 제외) """
    try:
        for widget in window.winfo_children():
            # 모든 프레임 내부의 위젯까지 재귀적으로 처리
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if hasattr(child, 'configure') and child.winfo_class() != 'TScrollbar':
                        widget_type = child.winfo_class()
                        # 종료 버튼은 제외
                        is_exit_button = (widget_type == 'Button' and child.cget('text') == '종료')
                        if widget_type in ('Button', 'Entry', 'OptionMenu', 'Checkbutton', 'Listbox') and not is_exit_button:
                            try: child.configure(state=tk.DISABLED)
                            except tk.TclError: pass # 이미 비활성화된 경우 등 무시

            # 최상위 위젯도 처리
            if hasattr(widget, 'configure') and widget.winfo_class() != 'TScrollbar':
                 widget_type = widget.winfo_class()
                 is_exit_button = (widget_type == 'Button' and widget.cget('text') == '종료')
                 if widget_type in ('Button', 'Entry', 'OptionMenu', 'Checkbutton', 'Listbox') and not is_exit_button:
                     try: widget.configure(state=tk.DISABLED)
                     except tk.TclError: pass
    except Exception as e: logging.error(f"GUI 비활성화 중 오류: {e}")


def enable_gui_elements():
    """ 작업 완료 후 GUI 요소 활성화 """
    try:
        for widget in window.winfo_children():
             # 모든 프레임 내부의 위젯까지 재귀적으로 처리
             if hasattr(widget, 'winfo_children'):
                 for child in widget.winfo_children():
                     if hasattr(child, 'configure') and child.winfo_class() != 'TScrollbar':
                          widget_type = child.winfo_class()
                          if widget_type in ('Button', 'Entry', 'OptionMenu', 'Checkbutton', 'Listbox'):
                              # PW 입력 필드는 readonly 유지
                              is_pw_entry = (widget_type == 'Entry' and str(child.cget('textvariable')) == str(pw_var))
                              try: child.configure(state='readonly' if is_pw_entry else tk.NORMAL)
                              except tk.TclError: pass # 위젯 상태 변경 오류 무시

             # 최상위 위젯도 처리
             if hasattr(widget, 'configure') and widget.winfo_class() != 'TScrollbar':
                  widget_type = widget.winfo_class()
                  if widget_type in ('Button', 'Entry', 'OptionMenu', 'Checkbutton', 'Listbox'):
                      is_pw_entry = (widget_type == 'Entry' and str(widget.cget('textvariable')) == str(pw_var))
                      try: widget.configure(state='readonly' if is_pw_entry else tk.NORMAL)
                      except tk.TclError: pass
    except Exception as e: logging.error(f"GUI 활성화 중 오류: {e}")


# ==============================================================
# 블로그 작업 수행 함수 (핵심 로직)
# ==============================================================
def execute_action(reservation, reservation_index):
    global user_id, user_pw, selected_options, driver, exit_program

    # --- 예약 정보 설정 ---
    try:
        user_id = reservation['id']
        user_pw = reservation['pw']
        current_options = reservation['options'] # 해당 예약의 옵션 사용
        repeat_count = int(reservation['repeat_count'])
        start_count = int(reservation.get('current_count', 0))
        # 작업 시작 시 로그 강화
        logging.info(f"작업 시작 - ID:{user_id}, Opts:{current_options}, Target:{repeat_count}, Start:{start_count+1}, Index:{reservation_index}")
    except (KeyError, ValueError, TypeError) as e:
        logging.error(f"잘못된 예약 정보 (Index: {reservation_index}): {reservation} - {e}")
        return # 잘못된 예약이면 이 함수 종료

    # --- 로그인 ---
    if not naver_login(user_id, user_pw):
        logging.error(f"로그인 실패 (Index: {reservation_index}), 예약 건너<0xEB><0x9B><0x84>.")
        return # 로그인 실패 시 함수 종료

    counter = start_count
    visited_urls_session = set() # 이번 세션 방문 기록
    is_neighbor_visit = "이웃방문" in current_options
    search_page_no = 1 # 이웃/검색 페이지 번호

    # --- 작업 루프 ---
    while not exit_program and counter < repeat_count:
        blog_post_urls = [] # 현재 페이지에서 찾은 블로그 URL 목록
        try:
            # --- 다음 작업 대상 URL 목록 가져오기 ---
            if is_neighbor_visit:
                list_url = f"https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage={search_page_no}&groupId=0"
                logging.debug(f"이웃 목록 로드: {list_url}")
            else: # 키워드 검색
                keyword = select_random_location()
                list_url = f"https://section.blog.naver.com/Search/Post.naver?pageNo={search_page_no}&rangeType=ALL&orderBy=sim&keyword={keyword}"
                logging.debug(f"키워드 검색: {list_url}")

            page_html = open_webpage(driver, list_url)
            if not page_html: raise ConnectionError(f"페이지 로드 실패: {list_url}") # 페이지 로드 실패 시 예외 발생

            soup = BeautifulSoup(page_html, 'html.parser')
            # 네이버 구조 변경에 대비하여 여러 선택자 사용 및 중복 제거
            links = soup.select('div.desc a[href*="blog.naver.com/"], div.list_post_article a[href*="blog.naver.com/"], li.item a.desc_inner[href*="blog.naver.com/"]')
            blog_post_urls = list(set([link['href'] for link in links if link.has_attr('href') and '/RedirectLog.naver' not in link['href']])) # 리다이렉트 제외

            if not blog_post_urls:
                logging.info(f"페이지 {search_page_no}에서 더 이상 URL 찾을 수 없음 ({'이웃' if is_neighbor_visit else '검색'}).")
                if search_page_no > 20: # 너무 많은 페이지 탐색 방지
                    logging.warning("탐색 페이지 제한 초과. 작업 종료.")
                    break
                search_page_no += 1 # 다음 페이지 시도
                continue # URL 목록 없으면 다음 페이지로

            random.shuffle(blog_post_urls) # 작업 순서 랜덤화
            logging.debug(f"페이지 {search_page_no}에서 {len(blog_post_urls)}개 URL 발견.")
            search_page_no += 1 # 다음 작업 위해 페이지 번호 증가

            # --- 개별 URL 작업 수행 ---
            for blog_url in blog_post_urls:
                if exit_program or counter >= repeat_count: break # 루프 종료 조건

                logging.info(f"[{counter + 1}/{repeat_count}] 처리 시도: {blog_url}")
                session_visit_key = f"{user_id}_{blog_url}" # 사용자별 방문 기록 키

                # 전체 방문 기록 로드 (최적화 필요 시 파일 대신 DB 사용 고려)
                visited_urls_total = set()
                try:
                    if os.path.exists(visit_path):
                        with open(visit_path, "r", encoding='utf-8') as f: visited_urls_total = {line.strip() for line in f}
                except Exception as e: logging.error(f"방문 기록({visit_path}) 로드 오류: {e}")

                if session_visit_key in visited_urls_session or session_visit_key in visited_urls_total:
                    logging.debug("이미 방문한 주소, 건너<0xEB><0x9B><0x84>.")
                    continue # 다음 URL로

                try:
                    # --- 블로그 포스트 열기 ---
                    open_webpage(driver, blog_url)
                    visited_urls_session.add(session_visit_key) # 세션 방문 기록 추가
                    try: # 전체 방문 기록 파일에 추가 (append 모드)
                        with open(visit_path, "a", encoding='utf-8') as f: f.write(session_visit_key + "\n")
                    except Exception as e: logging.error(f"방문 기록 파일 쓰기 오류: {e}")

                    # 카운터 증가 및 상태 저장
                    counter += 1
                    print(f"  진행: {counter}/{repeat_count} - {blog_url[-30:]}") # 간략 표시
                    if reservation_index != -1: save_current_run_count(reservation_index, counter)

                    # --- 옵션별 작업 수행 (iframe 내) ---
                    blog_owner_id_match = re.search(r'blog\.naver\.com/([^/]+)/', blog_url)
                    blog_owner_id = blog_owner_id_match.group(1) if blog_owner_id_match else None
                    main_frame_switched = False

                    try:
                        # --- mainFrame 전환 ---
                        logging.debug("  > mainFrame 전환 시도...")
                        iframe = wait_for_element(driver, By.ID, "mainFrame", timeout=20) # 대기 시간 증가
                        driver.switch_to.frame(iframe)
                        main_frame_switched = True
                        logging.debug("  > mainFrame 전환 성공.")
                        time.sleep(random.uniform(0.5, 1.0)) # 전환 후 안정화

                        # --- 공감 ---
                        if "공감" in current_options:
                             logging.debug("  > 공감 작업 시도...")
                             try:
                                 # 공감 버튼 선택자 개선 (텍스트 포함 또는 여러 클래스 조합)
                                 like_button = wait_for_element(driver, By.CSS_SELECTOR, "button._sympathyButton[aria-pressed='false'], em.u_cnt._cnt", timeout=5)
                                 driver.execute_script("arguments[0].click();", like_button) # JS 클릭 시도
                                 print("    - 공감 완료")
                                 logging.info(f"    - 공감 성공 - {blog_url}")
                                 time.sleep(random.uniform(1, 2))
                             except (NoSuchElementException, TimeoutException):
                                 logging.debug("  > 공감 버튼 (클릭 가능 상태) 못찾음 또는 이미 공감함.")
                             except Exception as e:
                                 logging.warning(f"  > 공감 작업 중 오류 - {blog_url}: {e}")

                        # --- 댓글 (Gemini API) ---
                        if "댓글" in current_options:
                            logging.debug("  > 댓글 작업 시도...")
                            try:
                                # 본문 추출 선택자 강화
                                post_body_element = wait_for_element(driver, By.CSS_SELECTOR, "div.se-main-container, div#postViewArea, div.post_ct", timeout=15)
                                element_text = post_body_element.text
                                logging.debug(f"    - 본문 길이 (정제 전): {len(element_text)}")

                                if len(element_text) > 100: # 최소 길이 확인
                                    # 텍스트 정제 강화 (HTML 태그 제거 등)
                                    soup_body = BeautifulSoup(post_body_element.get_attribute('outerHTML'), 'html.parser')
                                    element_text = soup_body.get_text(separator=' ', strip=True)

                                    element_text = element_text[:25000] # 길이 제한
                                    exclude_phrases = ["인쇄", "공감한 블로거", "댓글 쓰기", "댓글 단 블로거", "보내기", "URL 복사", "서로이웃", "본문 기타 기능", "공감", "인쇄", "방금", "© NAVER Corp.", "태그", "내용 변경 불가", "영리적 사용 불가", "저작자 명시", "목록열기", "통계보기", "글 요소", "이웃추가", "통계", "엮인글", "지도", "첨부파일", "이전글", "다음글", "신고", "TOP", "전체보기"]
                                    for phrase in exclude_phrases:
                                        element_text = element_text.replace(phrase, " ")
                                    extracted_txt = ' '.join(element_text.split()).strip()

                                    if len(extracted_txt) > 50: # 정제 후 최소 길이
                                        logging.debug(f"    - API 요청 본문 길이: {len(extracted_txt)}")

                                        # --- Gemini API 호출 ---
                                        try:
                                            # !!! API 키 직접 사용 !!!
                                            if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
                                                raise ValueError("API 키가 설정되지 않았습니다.")
                                            genai.configure(api_key=GEMINI_API_KEY)

                                            # 모델 설정 (Flash 추천, Pro도 가능)
                                            generation_config = {"temperature": 0.8, "max_output_tokens": 120}
                                            safety_settings = [{"category": c, "threshold": "BLOCK_MEDIUM_AND_ABOVE"} for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
                                            model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config=generation_config, safety_settings=safety_settings)

                                            # 프롬프트 개선
                                            prompt = f"다음 네이버 블로그 본문을 요약하고, 블로그 주인에게 도움이 되었거나 공감한다는 내용의 자연스러운 한국어 댓글(40~70자, '...요.'체)을 작성해주세요. ('블로그', '포스팅', '댓글' 단어는 제외하고 친근하게 작성해주세요.)\n\n---본문 시작---\n{extracted_txt}\n---본문 끝---\n\n댓글:"

                                            response_text = None; api_retry_count = 0
                                            while api_retry_count < 3: # 최대 3번 시도
                                                try:
                                                    logging.debug(f"      > Gemini API 호출 ({api_retry_count+1}/3)...")
                                                    response = model.generate_content(prompt, request_options={'timeout': 60})

                                                    if hasattr(response, 'text'): # 응답 객체 확인
                                                        response_text = response.text.strip().replace("\"", "").replace("\'", "") # 불필요 문자 제거
                                                        print(f"      > API 응답: {response_text}")
                                                        if 15 < len(response_text) < 100: # 길이 범위 조정
                                                            logging.debug("      > 유효한 응답 받음.")
                                                            break # 성공
                                                        else: logging.warning(f"      > API 응답 길이 부적절 ({len(response_text)}자)")
                                                    elif response.prompt_feedback: # 차단된 경우
                                                        logging.warning(f"      > API 응답 차단됨 - Feedback: {response.prompt_feedback}")
                                                        break # 재시도 불필요
                                                    else: # 예상치 못한 응답
                                                         logging.warning(f"      > API에서 예상치 못한 응답 받음: {response}")

                                                except Exception as api_err:
                                                    logging.error(f"      > Gemini API 호출 오류: {api_err}")
                                                # 재시도 로직
                                                api_retry_count += 1
                                                if api_retry_count < 3: time.sleep(2 ** api_retry_count)
                                                else: print("      > API 호출 최종 실패.")
                                            # --- API 호출 끝 ---

                                            # --- 댓글 작성 UI 자동화 ---
                                            if response_text:
                                                logging.debug("  > 댓글 작성 UI 자동화 시도...")
                                                pyperclip.copy(response_text)
                                                try:
                                                    # 댓글 영역으로 스크롤
                                                    comment_section = wait_for_element(driver, By.CSS_SELECTOR, "div#comment-area, div.area_comment") # 댓글 영역 선택자
                                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_section)
                                                    time.sleep(0.5)
                                                    # 댓글 버튼 클릭 (필요시)
                                                    try:
                                                        comment_btn = wait_for_element(driver, By.CSS_SELECTOR, "button._commentCountButton, a.btn_comment", timeout=3)
                                                        driver.execute_script("arguments[0].click();", comment_btn)
                                                        time.sleep(random.uniform(1, 2))
                                                    except: pass # 버튼 없어도 진행
                                                    # 입력창 찾기 및 입력
                                                    comment_area = wait_for_element(driver, By.CSS_SELECTOR, "div.u_cbox_write_wrap", timeout=10)
                                                    comment_textarea = wait_for_element(comment_area, By.CSS_SELECTOR, "textarea.u_cbox_text")
                                                    comment_textarea.click()
                                                    time.sleep(random.uniform(0.5, 1))
                                                    comment_textarea.send_keys(response_text) # 직접 입력 방식 권장
                                                    time.sleep(random.uniform(0.5, 1))
                                                    # 등록 버튼 클릭
                                                    upload_button = wait_for_element(comment_area, By.CSS_SELECTOR, "button.u_cbox_btn_upload")
                                                    driver.execute_script("arguments[0].click();", upload_button) # JS 클릭이 더 안정적일 수 있음
                                                    print("    - 댓글 등록 완료")
                                                    logging.info(f"    - 댓글 작성 성공 - {blog_url}")
                                                    time.sleep(random.uniform(2, 4)) # 등록 후 대기
                                                except Exception as ui_err:
                                                    print(f"    - 댓글 작성 UI 오류: {ui_err}")
                                                    logging.error(f"    - 댓글 작성 UI 오류 - {blog_url}: {ui_err}")
                                            else:
                                                logging.warning(f"  > 유효 API 응답 없음, 댓글 작성 건너<0xEB><0x9B><0x84> - {blog_url}")

                                        except ValueError as ve: logging.error(f"  > API 설정 오류: {ve}") # API 키 문제 등
                                        except Exception as api_ex: logging.error(f"  > Gemini API 관련 오류 - {blog_url}: {api_ex}", exc_info=True)

                                    else: logging.info(f"  > 본문 길이 짧음(정제 후 {len(extracted_txt)}자), 댓글 생성 건너<0xEB><0x9B><0x84> - {blog_url}")
                                else: logging.info(f"  > 본문 길이 짧음(정제 전 {len(element_text)}자), 댓글 생성 건너<0xEB><0x9B><0x84> - {blog_url}")

                            except Exception as e:
                                print(f"  > 댓글 작업 중 오류: {e}")
                                logging.error(f"  > 댓글 작업 중 오류 - {blog_url}: {e}", exc_info=True)

                        # --- 서이추 --- (로직 유지하되, 오류 처리 강화)
                        if "서이추" in current_options:
                            logging.debug("  > 서이추 작업 시도...")
                            try:
                                # 서이추 관련 버튼 클릭 로직 (기존 로직 사용, WebDriverWait 강화)
                                # 예시: 이웃추가 버튼 클릭
                                add_neighbor_btn = wait_for_element(driver, By.CSS_SELECTOR, "button._buddyAddButton, a#buddy_add_button", timeout=5) # 예시 선택자
                                driver.execute_script("arguments[0].click();", add_neighbor_btn)
                                time.sleep(random.uniform(1,2))
                                # 팝업 내에서 '서로이웃' 라디오 버튼 선택 및 확인 클릭 (선택자 필요)
                                # ... WebDriverWait 사용 ...
                                print("    - 서이추 신청 시도 (성공 여부 확인 어려움)")
                                logging.info(f"    - 서이추 시도됨 - {blog_url}")
                            except (NoSuchElementException, TimeoutException):
                                logging.debug(f"  > 서이추 버튼/과정 요소 못찾음 - {blog_url}")
                            except Exception as e:
                                logging.warning(f"  > 서이추 작업 중 오류 - {blog_url}: {e}")

                    except (NoSuchFrameException, TimeoutException) as e:
                         logging.error(f"mainFrame 오류 - {blog_url}: {e}")
                         continue # iframe 오류 시 다음 URL
                    except Exception as e:
                         logging.error(f"iframe 내 작업 오류 - {blog_url}: {e}", exc_info=True)
                    finally: # iframe 작업 후 반드시 메인으로 복귀
                        if main_frame_switched:
                             try: driver.switch_to.default_content(); logging.debug("  > 메인 문서 복귀.")
                             except Exception: pass

                    # --- 안부글 --- (별도 페이지 이동)
                    if "안부" in current_options and blog_owner_id:
                        logging.debug("  > 안부글 작성 시도...")
                        guestbook_url = f"https://blog.naver.com/guestbook/GuestBookList.naver?blogId={blog_owner_id}"
                        try:
                            # 현재 탭에서 안부 게시판으로 이동
                            open_webpage(driver, guestbook_url)
                            # 안부글 작성 iframe 전환 및 자동화 (WebDriverWait 필수)
                            # 예시: iframe 전환
                            logging.debug("    - 안부글 mainFrame 전환 시도")
                            g_iframe_main = wait_for_element(driver, By.ID, "mainFrame", timeout=15)
                            driver.switch_to.frame(g_iframe_main)
                            logging.debug("    - 안부글 writeIFrame 전환 시도")
                            g_iframe_write = wait_for_element(driver, By.ID, "writeIFrame", timeout=10)
                            driver.switch_to.frame(g_iframe_write)
                            logging.debug("    - 안부글 POSTEDITOR 전환 시도")
                            g_iframe_post = wait_for_element(driver, By.ID, "POSTEDITOR", timeout=10)
                            driver.switch_to.frame(g_iframe_post)
                            # 입력 필드 클릭 및 메시지 작성
                            guest_input = wait_for_element(driver, By.CSS_SELECTOR, "body.se2_inputarea")
                            guest_input.click()
                            time.sleep(0.5)
                            # 안부 메시지 선택 및 입력
                            prefix_msgs = load_messages_from_file(random_prefix_file)
                            hello_msgs = load_messages_from_file(sayhello_file)
                            final_msg = select_random_message(prefix_msgs, "") + " " + select_random_message(hello_msgs)
                            guest_input.send_keys(final_msg.strip())
                            logging.debug(f"    - 안부글 내용: {final_msg.strip()}")
                            time.sleep(random.uniform(1, 2))
                            # 저장 버튼 클릭 (iframe 빠져나와서)
                            driver.switch_to.default_content() # POSTEDITOR -> writeIFrame
                            driver.switch_to.default_content() # writeIFrame -> mainFrame
                            # driver.switch_to.default_content() # mainFrame -> Top (이 단계는 불필요할 수 있음)
                            save_btn = wait_for_element(driver, By.CSS_SELECTOR, "button#guestbookSubmitBtn, a.btn_register") # 저장 버튼 선택자 확인 필요
                            driver.execute_script("arguments[0].click();", save_btn)
                            print("    - 안부글 등록 완료")
                            logging.info(f"    - 안부글 작성 성공 - BlogID: {blog_owner_id}")
                            time.sleep(random.uniform(2, 4))
                        except Exception as e:
                            print(f"    - 안부글 작업 오류: {e}")
                            logging.error(f"    - 안부글 작업 오류 - BlogID: {blog_owner_id}: {e}", exc_info=True)
                        finally:
                            try: driver.switch_to.default_content() # 모든 iframe에서 확실히 빠져나옴
                            except: pass
                            # 원래 블로그 포스트로 돌아가기 (선택 사항)
                            # open_webpage(driver, blog_url)

                except KeyboardInterrupt: exit_program = True; break # 사용자 중단
                except Exception as e: # 개별 블로그 처리 중 발생하는 모든 예외 처리
                    logging.error(f"블로그 처리 중 예상치 못한 오류 - {blog_url}: {e}", exc_info=True)
                    # 오류 발생 시 스크린샷 저장 (디버깅용)
                    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    # driver.save_screenshot(f"error_{timestamp}_{blog_owner_id}.png")
                    continue # 다음 URL로 넘어감

                # --- 작업 간 딜레이 ---
                if not exit_program:
                    sleep_interval = random.uniform(5, 12) # 딜레이 조정
                    logging.debug(f"  > 다음 작업까지 {sleep_interval:.1f}초 대기...")
                    try: sleep_with_esc(sleep_interval)
                    except KeyboardInterrupt: exit_program = True; break

            # --- 내부 URL 루프 종료 ---
            if exit_program or counter >= repeat_count: break

        except KeyboardInterrupt: exit_program = True; break # 외부 루프 중단
        except ConnectionError as e: # 페이지 로드 실패 시
             logging.error(f"페이지 로드 실패, 10초 후 재시도: {e}")
             time.sleep(10)
        except Exception as loop_err: # 그 외 루프 오류
            logging.error(f"작업 루프 오류: {loop_err}", exc_info=True)
            time.sleep(15) # 오류 발생 시 잠시 대기 후 계속

    # --- 작업 루프 종료 ---
    print(f"\n=== {user_id} 작업 완료/중단 (최종: {counter}/{repeat_count}) ===")
    logging.info(f"{user_id} 작업 완료/중단 (최종: {counter}/{repeat_count})")

# ==============================================================
# GUI 설정 및 메인 루프
# ==============================================================
if __name__ == "__main__":
    try:
        # --- GUI 위젯 생성 및 배치 ---
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = max(700, screen_width // 2) # 창 크기 조정
        window_height = max(750, screen_height // 2 + 150)
        x_pos = max(0, (screen_width - window_width) // 2)
        y_pos = max(0, (screen_height - window_height) // 2)
        window.geometry(f'{window_width}x{window_height}+{x_pos}+{y_pos}')
        window.minsize(650, 700) # 최소 크기

        # --- 상단 프레임 (ID/PW, 옵션) ---
        top_frame = tk.Frame(window)
        top_frame.pack(pady=10, padx=10, fill=tk.X)
        id_pw_frame = tk.Frame(top_frame)
        id_pw_frame.pack(side=tk.LEFT, padx=(0, 20))
        tk.Label(id_pw_frame, text="ID:", font=customFont).grid(row=0, column=0, sticky='w', padx=2, pady=2)
        id_pw_dict = load_default_id_pw()
        id_options = list(id_pw_dict.keys()) or ["(ID 없음)"]
        id_var.set(load_selected_id() or id_options[0])
        id_dropdown = tk.OptionMenu(id_pw_frame, id_var, *id_options, command=update_pw)
        id_dropdown.config(font=customFont, width=15)
        id_dropdown.grid(row=0, column=1, sticky='w', padx=2, pady=2)
        try: menu = window.nametowidget(id_dropdown.menuname); menu.config(font=customFont)
        except: pass
        tk.Label(id_pw_frame, text="PW:", font=customFont).grid(row=1, column=0, sticky='w', padx=2, pady=2)
        pw_entry = tk.Entry(id_pw_frame, textvariable=pw_var, font=customFont, width=18, state='readonly')
        pw_entry.grid(row=1, column=1, sticky='w', padx=2, pady=2)
        update_pw() # 초기 PW 로드

        options_frame = tk.LabelFrame(top_frame, text="작업 선택", font=customFont, padx=10, pady=5)
        options_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        options = ["공감", "댓글", "이웃방문", "서이추", "안부"]
        loaded_selected_options = load_selected_options()
        for i, option in enumerate(options):
            var = tk.IntVar(value=1 if option in loaded_selected_options else 0)
            chk = tk.Checkbutton(options_frame, text=option, variable=var, font=customFont)
            chk.grid(row=i // 3, column=i % 3, padx=5, pady=2, sticky='w')
            var_dict[option] = var
            var.trace_add('write', on_checkbox_change)
        on_checkbox_change() # 초기값 저장

        # --- 예약 목록 프레임 ---
        reservation_frame = tk.LabelFrame(window, text="예약 목록 관리", font=customFont, padx=10, pady=10)
        reservation_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        listbox_frame = tk.Frame(reservation_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        listbox_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, font=customFont, height=10, yscrollcommand=listbox_scrollbar.set)
        listbox_scrollbar.config(command=listbox.yview)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        load_reservation_list(); update_listbox() # 로드 및 업데이트
        reservation_button_frame = tk.Frame(reservation_frame)
        reservation_button_frame.pack(pady=5)
        add_button = tk.Button(reservation_button_frame, text="현재 설정 추가", font=customFont, command=add_reservation_to_list); add_button.grid(row=0, column=0, padx=5)
        delete_button = tk.Button(reservation_button_frame, text="선택 삭제", font=customFont, command=delete_selected_reservation); delete_button.grid(row=0, column=1, padx=5)
        delete_all_button = tk.Button(reservation_button_frame, text="전체 삭제", font=customFont, command=delete_all_reservations); delete_all_button.grid(row=0, column=2, padx=5)

        # --- 실행 제어 프레임 ---
        control_frame = tk.Frame(window)
        control_frame.pack(pady=10, padx=10, fill=tk.X)
        control_frame.columnconfigure(0, weight=1); control_frame.columnconfigure(1, weight=1)

        single_run_frame = tk.LabelFrame(control_frame, text="개별 실행 설정", font=customFont, padx=10, pady=10); single_run_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        tk.Label(single_run_frame, text="반복회수:", font=customFont).grid(row=0, column=0, sticky='w', pady=2)
        repeat_entry = tk.Entry(single_run_frame, textvariable=repeat_count_var, font=customFont, width=8); repeat_entry.grid(row=0, column=1, sticky='w', pady=2)
        repeat_count_var.set(load_repeat_count())
        tk.Label(single_run_frame, text="예약(초):", font=customFont).grid(row=1, column=0, sticky='w', pady=2)
        seconds_entry = tk.Entry(single_run_frame, textvariable=seconds_var, font=customFont, width=8); seconds_entry.grid(row=1, column=1, sticky='w', pady=2)
        timer_label = tk.Label(single_run_frame, text="", font=customFont, fg="blue"); timer_label.grid(row=2, column=0, columnspan=2, sticky='w', pady=5)
        single_run_button = tk.Button(single_run_frame, text="현재 설정 실행", font=customFont, command=schedule_single_action); single_run_button.grid(row=3, column=0, columnspan=2, pady=5)

        batch_run_frame = tk.LabelFrame(control_frame, text="일괄 실행", font=customFont, padx=10, pady=10); batch_run_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        batch_run_button = tk.Button(batch_run_frame, text="예약 목록\n일괄 실행", font=customFont, command=perform_actions_sequentially, height=4, width=15); batch_run_button.pack(pady=20, expand=True)

        # 종료 버튼
        tk.Button(window, text="종료", font=customFont, command=on_closing, width=10).pack(pady=20)

        # --- 이벤트 바인딩 및 스레드 시작 ---
        window.protocol("WM_DELETE_WINDOW", on_closing)
        esc_thread = threading.Thread(target=check_esc_thread_func, daemon=True); esc_thread.start()

        print("GUI 설정 완료. 메인 루프 시작.")
        logging.info("GUI 메인 루프 시작.")
        window.mainloop()

    except Exception as main_e:
        print(f"프로그램 실행 중 치명적인 오류 발생: {main_e}")
        logging.critical(f"프로그램 실행 중 치명적인 오류: {main_e}", exc_info=True)
        try: messagebox.showerror("치명적 오류", f"프로그램 오류:\n{main_e}\n로그 파일을 확인해주세요.")
        except: pass
    finally:
        print("프로그램 종료.")
        logging.info("프로그램 종료됨.")
        if 'driver' in globals() and driver:
            try: driver.quit()
            except: pass