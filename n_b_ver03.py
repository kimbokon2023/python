from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # TimeoutException 추가
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchFrameException
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
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import font as tkFont  # 폰트 모듈 추가
from tkinter import messagebox
from tkinter import IntVar
import json
import cv2
import numpy as np
import re
import subprocess
import psutil
import requests
from screeninfo import get_monitors

# Declare the global variable 'driver'
driver = None

# 추가된 전역 변수
ReserveExecute = False
user_id = ""
user_pw = ""

monitors = get_monitors()
# 모든 모니터의 정보를 출력합니다.
for monitor in monitors:
    print(f"Monitor {monitor.name}: Width={monitor.width}, Height={monitor.height}, X={monitor.x}, Y={monitor.y}")


# 프로그램 시작 시간 기록
start_time = time.time()

# 현재 날짜와 시간을 '년월일_시분초' 형식으로 가져옴
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

window = tk.Tk()
window.title("네이버 블로그 공감 댓글 ")
# 폰트 스타일 설정
customFont = tkFont.Font(family="굴림", size=13)
exit_program = False

id_pw_dict = {}

application_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
data_file = os.path.join(application_path, 'data', 'selected_options.json')
idpw_saved_file = os.path.join(application_path, 'data', 'idpwsaved.json')
selected_id_file = os.path.join(application_path, 'data', 'selected_id.json')  # 변경된 경로
repeat_count_file = os.path.join(application_path, 'data', 'repeat_count.json')
visit_path = os.path.join(application_path, 'data', 'visit.txt')
log_file = os.path.join(application_path, 'data', 'log.txt')
blog_reply_path = os.path.join(application_path, 'data', 'blog_reply.txt')
reservation_list_path = os.path.join(application_path, 'data', 'reservation_list.json')
last_file_name = os.path.join(application_path, 'data', f"div_{current_time}.txt")
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# 업데이트할 데이터를 만듭니다.
new_data = {
    "username": "새로운 유저네임",
    "password": "새로운 패스워드"
}

# 업데이트할 JSON 파일의 URL을 지정합니다.
json_url = "http://8440.co.kr/data/idpw.json"
# jsonfile_path = os.path.join(application_path, 'data', 'idpw.json')

repeat_count_var = tk.StringVar(window)


# Function to add reservation to the list
def add_reservation_to_list():
    id_value = id_var.get()
    pw_value = pw_var.get()
    selected_options_values = [option for option, var in var_dict.items() if var.get() == 1]
    repeat_count_value = repeat_count_var.get()

    reservation = {
        "id": id_value,
        "pw": pw_value,
        "options": selected_options_values,
        "repeat_count": repeat_count_value
    }

    reservation_list = load_reservation_list()
    reservation_list.append(reservation)
    save_reservation_list(reservation_list)
    update_listbox()

# Function to delete selected reservation from the list
def delete_selected_reservation():
    selected_index = listbox.curselection()
    if selected_index:
        reservation_list = load_reservation_list()
        reservation_list.pop(selected_index[0])
        save_reservation_list(reservation_list)
        update_listbox()

# Function to update the listbox with current reservation list
def update_listbox():
    reservation_list = load_reservation_list()
    listbox.delete(0, tk.END)
    for index, reservation in enumerate(reservation_list):
        listbox.insert(
            index, f"ID: {reservation['id']}, Password: {reservation['pw']}, Options: {reservation['options']}, Repeat Count: {reservation['repeat_count']}"
        )

# Function to load reservation list from JSON file
def load_reservation_list():
    try:
        with open(reservation_list_path, "r") as file:
            reservation_list = json.load(file)
    except FileNotFoundError:
        reservation_list = []
    return reservation_list

# Function to save reservation list to JSON file
def save_reservation_list(reservation_list):
    with open(reservation_list_path, "w") as file:
        json.dump(reservation_list, file, indent=2)

# Function to update reservation list
def update_reservation_list():
    id_value = id_var.get()
    pw_value = pw_var.get()
    selected_options_values = [option for option, var in var_dict.items() if var.get() == 1]
    repeat_count_value = repeat_count_var.get()

    reservation = {
        "id": id_value,
        "pw": pw_value,
        "options": selected_options_values,
        "repeat_count": repeat_count_value
    }

    reservation_list = load_reservation_list()
    reservation_list.append(reservation)
    save_reservation_list(reservation_list)

# Function to perform actions based on the reservation list
def perform_actions(reservation_list):
    global ReserveExecute 
    ReserveExecute = True
    for reservation in reservation_list:
        # Perform actions using reservation["id"], reservation["pw"], etc.
        print(f"Performing actions for ID: {reservation['id']}")
        print(f"Options: {reservation['options']}")
        print(f"Repeat Count: {reservation['repeat_count']}")
        # Add your code to perform the actual actions here
        print("Actions performed\n")
        execute_action(reservation)

def close_all_chrome_windows():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if 'chrome' in process.info['name'].lower():
                process.terminate()  # 프로세스 종료
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def update_timer():
    # 현재 시간과 실행 시간 사이의 차이 계산
    remaining_time = run_at - datetime.now()
    if remaining_time.total_seconds() > 0:
        # 남은 시간을 시, 분, 초로 변환
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        # 남은 시간을 레이블에 표시
        timer_label.config(text=f"{hours}시간 {minutes}분 {seconds}초 남음")
        # 1초 후에 함수 다시 호출
        window.after(1000, update_timer)
    else:
        # 시간이 다 됐을 때의 처리
        timer_label.config(text="시간 만료")        

def schedule_action():
    global run_at
    try:
        seconds = int(seconds_var.get())  # 이제 '분' 대신 '초'를 입력 받습니다.
    except ValueError:
        print("유효한 숫자를 입력해주세요.")
        return

    now = datetime.now()
    run_at = now + timedelta(seconds=seconds)  # 분 대신 초를 사용하여 시간을 설정합니다.

    timer = threading.Timer(seconds, execute_action, args=[repeat_count_var.get()])
    # timer = threading.Timer(seconds, execute_action)  # 타이머 설정도 초 단위로 변경합니다.
            
    timer.start()

    # 타이머 업데이트 시작
    update_timer()

   
def kill_notepad():    
    sleep_with_esc(1)

    # 메모장 프로세스 종료
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if "notepad.exe" in proc.info['name']:
            try:
                process = psutil.Process(proc.info['pid'])
                process.terminate()  # 프로세스 종료
            except Exception as e:
                print(f"메모장 종료 중 오류 발생: {str(e)}")

    print("메모장을 종료했습니다.")

def save_repeat_count(count):
    with open(repeat_count_file, 'w') as file:
        json.dump({'repeat_count': count}, file)

def load_repeat_count():
    try:
        with open(repeat_count_file, 'r') as file:
            data = json.load(file)
            return data.get('repeat_count', '1')  # 기본값으로 '1'을 반환
    except FileNotFoundError:
        return '1'

def sleep_with_esc(duration):
    # 'ESC' 키를 감지하는 백그라운드 스레드 시작
    esc_thread = threading.Thread(target=check_esc)
    esc_thread.daemon = True
    esc_thread.start()

    # 주어진 시간 동안 대기
    time.sleep(duration)

def on_closing():    
    save_selected_id(id_var.get())  # 현재 선택된 아이디 저장

    save_repeat_count(repeat_count_var.get())
    # if tk.messagebox.askokcancel("종료 확인", "프로그램을 종료하시겠습니까?"):
    window.destroy()    
    sys.exit()

def save_selected_id(selected_id):
    try:
        with open(selected_id_file, 'w') as file:  # 변경된 경로
            json.dump(selected_id, file)
    except Exception as e:
        print(f"Error saving selected ID: {e}")

def load_selected_id():
    try:
        with open(selected_id_file, 'r') as file:  # 변경된 경로
            return json.load(file)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error loading selected ID: {e}")
        return None

def load_saved_id_pw():
    try:
        with open(idpw_saved_file, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

def save_id_pw(id_pw_data):    
    with open(idpw_saved_file, 'w') as file:
        json.dump(id_pw_data, file)

def load_id_pw_event():
    global id_pw_dict  # 전역 변수로 선언
    id_pw_dict = load_saved_id_pw()
    for option, var in var_dict.items():
        if option in id_pw_dict:
            pw_var.set(id_pw_dict[option])

def load_selected_options():
    try:
        with open(data_file, "r") as file:
            loaded_data = json.load(file)
            return loaded_data
    except FileNotFoundError:
        return []

def save_selected_options(selected_options):
    with open(data_file, "w") as file:
        json.dump(selected_options, file)

def on_checkbox_change(name, index, mode):
    selected_options.clear()
    for option, var in var_dict.items():
        if var.get() == 1:
            selected_options.append(option)        
    print("선택된 옵션:", selected_options)
    save_selected_options(selected_options)
      
def check_exit():
    global exit_program
    while True:
        # if keyboard.is_pressed('windows') and keyboard.is_pressed('esc'):
        if keyboard.is_pressed('esc'):
            print("프로그램 중단")
            exit_program = True
            sys.exit()
            break        

def wait_for_element(driver, by, selector, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )

def open_webpage(driver, url):
    driver.implicitly_wait(20)  # Wait up to 20 seconds for the page to load
    driver.maximize_window()    # Maximize the browser window
    driver.get(url)             # Open the webpage
    time.sleep(2)    
    # Disable right-click prevention using JavaScript
    driver.execute_script("document.addEventListener('contextmenu', function(e) { e.preventDefault(); });")    
    return driver.page_source   # Return the HTML content of the page

def delaysecond():
    random_sleep_time = random.randint(2, 7)  # 3초에서 7초 사이의 랜덤한 정수 생성
    time.sleep(random_sleep_time)  # 생성된 랜덤한 시간만큼 대기

# Function to load messages from a file into an array
def load_messages_from_file(file_path):
    messages = []
    with open(file_path, 'r', encoding='utf-8') as file:
        messages = [line.strip() for line in file.readlines()]
    return messages

# Function to randomly select a message from the array
def select_random_message(messages):
    if messages:
        random_index = random.randint(0, len(messages) - 1)  # Random index in the range of the array
        return messages[random_index]
    return "No messages found"

# def load_default_id_pw():
#     try:        
#         # jsonfile_path = os.path.join(application_path, 'data', 'idpw.json')
#         with open(json_url , 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return {}

def load_default_id_pw():
    try:
        # 업데이트할 JSON 파일의 URL을 지정합니다.
        json_url = "http://8440.co.kr/data/idpw.json"
        
        # JSON 데이터를 가져옵니다.
        response = requests.get(json_url)
        response.raise_for_status()

        # JSON 데이터를 파이썬 딕셔너리로 변환하여 반환합니다.
        return response.json()
    except Exception as e:
        print("오류 발생:", str(e))
        return {}
    
def check_esc():
    global exit_program
    while True:
        if keyboard.is_pressed('esc'):
            print("ESC pressed. Exiting...")            
            exit_program = True
            sys.exit()
        time.sleep(0.2)

# update_pw 함수도 id_pw_dict를 전역 변수로 사용
def update_pw(selected_id, *args):
    pw_var.set(id_pw_dict.get(selected_id, ''))

def on_escape(event=None):
    global exit_program
    print("ESC pressed. Exiting...")
    window.destroy()  # 현재 창을 닫습니다  
    exit_program = True
    sys.exit()

def generate_blog_style_sentences_v2():        
    with open(blog_reply_path, 'r', encoding='utf-8') as file:
        base_phrases = [line.strip() for line in file.readlines()]

    emojis = ["^^", "ㅎㅎ", "😊", "👍", "😁", "💪", "🌟", "🌞", "🌈", "❄️", "🍀", "🌷", "🍂", "☔"]

    sentences = set()
    while len(sentences) < 1:
        # Randomly select a base phrase and an emoji
        sentence = random.choice(base_phrases) + " " + random.choice(emojis)
        # Ensure uniqueness and character limit
        if len(sentence) <= 60 and sentence not in sentences:
            sentences.add(sentence)
    return list(sentences)


def click_element(driver, gpt_version):
    try:
        # div 요소를 찾습니다. 클래스 이름을 사용하여 요소를 식별합니다.
        div_element = driver.find_element(By.CSS_SELECTOR, "div.group.flex.cursor-pointer.items-center.gap-1.rounded-xl.py-2.px-3.text-lg.font-medium")
        # 요소를 클릭합니다.
        div_element.click()        
        try:
            # CSS 선택자를 버전에 따라 결정합니다.
            if gpt_version == "gpt4":
                # XPath를 사용하여 텍스트를 포함하는 요소를 찾습니다.
                text = "GPT-4"
                xpath = f"//*[contains(text(), '{text}')]"
                element = WebDriverWait(driver, 6).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                # 요소를 클릭합니다.
                element.click()
                sleep_with_esc(2)                
            elif gpt_version == "gpt35":
                # XPath를 사용하여 텍스트를 포함하는 요소를 찾습니다.
                text = "GPT-3.5"
                xpath = f"//*[contains(text(), '{text}')]"
                element = WebDriverWait(driver, 6).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                # 요소를 클릭합니다.
                element.click()
                sleep_with_esc(2)                
            else:
                print("잘못된 GPT 버전이 지정되었습니다.")
                return

        except NoSuchElementException:
            print("지정된 div 요소를 찾을 수 없습니다.")
        except Exception as e:
            print(f"오류 발생: {e}")            

    except NoSuchElementException:
        print("지정된 div 요소를 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    sleep_with_esc(2)


def naver_login():
    global driver
    global user_id
    global user_pw

    global selected_id
    selected_id = id_var.get()  # 선택된 ID 업데이트
    id_pw_dict[selected_id] = pw_var.get()  # 선택된 ID에 대한 패스워드 업데이트
    save_id_pw(id_pw_dict)  # ID와 패스워드 정보 저장    
       
    # 모든 크롬 창 종료
    close_all_chrome_windows()
    print("모든 크롬 창 종료")

    # 각 컴퓨터의 브라우저마다 각자의 chrome.txt 데이터를 수정해줘야 한다.    
    options = Options()    
    chrome_txt_path = os.path.join(application_path, 'data', 'chrome.txt')    
    # 사용자 데이터 폴더를 찾는 로직

    # # C 드라이브 검색
    # c_drive_path = "C:\\"
    # user_data_path = None
    # for root, dirs, files in os.walk(c_drive_path):
    #     if "User Data" in dirs and "Chrome" in dirs and "Local" in dirs and "AppData" in dirs:
    #         user_data_path = os.path.join(root, "AppData", "Local", "Google", "Chrome", "User Data")
    #         break

    # # 사용자 데이터 폴더가 발견되었는지 확인
    # if user_data_path:
    #     # 상위 폴더 (사용자 아이디) 찾기
    #     user_id_path = os.path.join(user_data_path, os.pardir)
    #     user_id_path = os.path.abspath(user_id_path)

    #     # 사용자 아이디 경로 출력
    #     print(f"User ID folder found: {user_id_path}")

    #     # 예시: 폴더 내의 파일 목록 출력
    #     # file_list = os.listdir(user_data_path)
    #     # print("Files in Chrome User Data folder:")
    #     # for file_name in file_list:
    #     #     print(file_name)
    # else:
    #     print("Chrome User Data folder not found on C drive.")    

    # chrome_txt_path = user_id_path    
    # chrome.txt 파일을 열고 user_data 값을 읽습니다
    with open(chrome_txt_path, 'r') as file:
        user_data = file.read().strip()  # Use strip() to remove any leading/trailing whitespace

    options.add_argument(f"user-data-dir={user_data}")
    options.add_experimental_option("detach", True)  # 화면이 꺼지지 않고 유지
    # options.add_experimental_option("excludeSwiches", ["enabled-automation-icon"])  # chrome 자동화된 프로그램에 의해 제어되고 ' 문구 삭제
    options.add_argument("--start-maximized")  # 최대 크기로 시작
    options.add_argument("--disable-blink-features=AutomationControlled")  # 옵션 한줄로 로봇이 아닌 사람으로 감지되는 방법

    window.withdraw()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    time.sleep(3)
    x_coordinate = monitors[0].width
    # Y 좌표는 0으로 설정하면 됩니다.
    y_coordinate = 0
    # Chrome WebDriver 생성
    driver.set_window_position(x_coordinate, y_coordinate)
    time.sleep(2)
    
    url = "https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/"

    driver.implicitly_wait(10)  #페이지가 로딩될때까지 최대 10초 기다려줌
    driver.maximize_window()
    driver.get(url) # 페이지 열기
    time.sleep(3)
    pyautogui.press('esc')
    time.sleep(3)      

    # x, y = pyautogui.position()
    # print(f"현재 마우스 위치: ({x}, {y})")
    
    x, y = 427, 355
    # 마우스를 x, y 좌표로 이동
    pyautogui.moveTo(x, y)
    # 좌표에서 클릭
    pyautogui.click()
    time.sleep(2)
    # 메모장 강제로 닫기
    # kill_notepad()
    id_field = wait_for_element(driver, By.CSS_SELECTOR, "#id")
    id_field.click()
    time.sleep(2)

    for _ in range(20):
        pyautogui.press('backspace')
    time.sleep(1)
    pyperclip.copy(user_id)  # 파일에서 읽은 아이디 사용
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

    pw_field = wait_for_element(driver, By.CSS_SELECTOR, "#pw")
    pw_field.click()
    time.sleep(1)
    for _ in range(20):
        pyautogui.press('backspace')
    time.sleep(1)
    pyperclip.copy(user_pw)  # 파일에서 읽은 비밀번호 사용
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    
    login_btn = wait_for_element(driver, By.CSS_SELECTOR, "#log\\.login")  # 로그인 버튼에 대한 올바른 선택자 사용
    login_btn.click()
    time.sleep(2)

def select_random_location():
    # 한국의 주요 도시, 구, 동 50개를 포함하는 배열
    locations = [
        "서울", "부산", "인천", "대구", "대전", "광주", "울산", "세종", "수원", "창원",
        "강남구", "서초구", "해운대구", "수성구", "유성구", "북구", "동구", "중구", "남구", "서구",
        "송파구", "마포구", "용산구", "강서구", "노원구", "은평구", "성동구", "광진구", "구로구", "금천구",
        "종로구", "동작구", "양천구", "영등포구", "도봉구", "강북구", "성북구", "중랑구", "강동구", "관악구",
        "사하구", "동래구", "연제구", "부산진구", "북구", "해운대구", "금정구", "강서구", "사상구", "기장군"
    ]

    # 배열에서 무작위로 하나의 위치를 선택
    selected_location = random.choice(locations)
    return selected_location

# 다음 입력가능 이미지와 continue 이미지를 찾는다
def waitnext(driver):
    while True:
        global exit_program
        # ESC 키가 눌렸는지 확인
        if keyboard.is_pressed('esc'):
            print("ESC 키가 눌려 프로그램을 종료합니다.")
            exit_program = True
            sys.exit()

        try:
            # 페이지의 HTML 소스를 가져옴
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # continue 요소를 포함하는 태그 찾기
            # 'points' 속성이 특정 값을 가진 'polygon' 태그 찾기
            first_polygon = soup.find('polygon', {'points': '11 19 2 12 11 5 11 19'})
            second_polygon = soup.find('polygon', {'points': '22 19 13 12 22 5 22 19'})

            # 두 태그가 모두 존재하는 경우
            if first_polygon and second_polygon:
                print("계속하기 이미지 찾음")
                sleep_with_esc(3)

                # XPath를 사용하여 텍스트를 포함하는 요소를 찾습니다.
                text = "Continue"
                xpath = f"//*[contains(text(), '{text}')]"
                element = WebDriverWait(driver, 6).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                # 요소를 클릭합니다.
                element.click()
                sleep_with_esc(2)        
                print("계속하기 이미지 클릭")                
            else:
                print("계속하기 이미지를 찾지 못함, 상향화살표 찾는중")
                try:
                    # 특정 path 요소를 포함하는 태그 찾기
                    arrow_up_element = soup.find('path', {'d': 'M7 11L12 6L17 11M12 18V7'})

                    if arrow_up_element:
                        print("상향 화살표 이미지 찾음")
                        sleep_with_esc(1)
                        break
                    else:
                        print("상향 화살표 이미지를 찾지 못함, 재검색 중...")

                except Exception as e:
                    print(f"오류 발생: {e}")
                    break
                sleep_with_esc(1)

        except Exception as e:
            print(f"오류 발생: {e}")
            break

def get_post_id_from_href(href):
    # href에서 '/'를 기준으로 나눈 후 마지막 부분을 반환
    return href.split('/')[-1]

def execute_action(reservation):     
    global user_id   
    global user_pw   
    global ReserveExecute   
    global selected_id
    global driver        

    if(ReserveExecute):
        user_id = reservation['id']
        user_pw = reservation['pw']    
        reservation_option = reservation['options']
        print(reservation_option)
        try:
            repeat_count = int(reservation['repeat_count'])
        except ValueError:
            repeat_count = 1  # 변환 실패 시 기본값으로 1 설정
                
        # Create a dictionary to store Tkinter variables for each option
        option_vars = {}

        # Clear the selected options list
        selected_options.clear()
        # Create Tkinter variables for each option and store them in the dictionary
        for option in reservation_option:
            option_vars[option] = IntVar()
            selected_options.append(option)  

        print("최종 옵션선택 :")    
        print(selected_options)    
        # time.sleep(100)
    else:
        user_id = id_var.get()
        user_pw = pw_var.get()    
        selected_id = id_var.get()  # 선택된 ID 업데이트
        id_pw_dict[selected_id] = pw_var.get()  # 선택된 ID에 대한 패스워드 업데이트   
        save_id_pw(id_pw_dict)  # ID와 패스워드 정보 저장    
        try:
            repeat_count = int(repeat_count_var.get())
        except ValueError:
            repeat_count = 1  # 변환 실패 시 기본값으로 1 설정

        # 메인 프로그램 루프
        # 선택된 체크박스 옵션 업데이트
        selected_options.clear()
        for option, var in var_dict.items():
            if var.get() == 1:
                selected_options.append(option)            

    naver_login()

    
    # print("실행시작 클릭")    

    print("루프 시작전 옵션선택 :")    
    print(selected_options)       
    
    counter = 0  # 카운터 초기화
    inner_counter = 0  # 카운터 초기화
    if "이웃방문" not in selected_options:  # 이웃이 아닌 방문  
        while not exit_program and counter < repeat_count:  
            print("이웃방문이 아닌경우 while 시작 ")
            # 이미 방문한 주소를 저장할 파일
            visited_urls = set()

            # visit.txt 파일이 존재하는지 확인
            if os.path.exists(visit_path):
                # visit.txt 파일에서 이전에 방문한 주소를 읽어옴
                with open(visit_path, "r") as file:
                    for line in file:
                        visited_urls.add(line.strip())
            else:
                # 파일이 없을 경우 빈 세트를 사용
                visited_urls = set()

            # Generate the sentences again
            blog_style_sentences_v2 = generate_blog_style_sentences_v2()
            print("blog_style_sentences_v2 실행")
            for sentence in blog_style_sentences_v2:
                select_text = sentence        
            print("선택된 문구 : " + select_text)    

            # Generating a random number between 0 to 34, excluding 1, 2, 3, and 4
            random_number = random.choice([i for i in range(200)])
            random_sufix = select_random_location()

            # Creating a new URL with the generated random number and suffix
            original_url = "https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword=text"
            new_url = original_url.replace("pageNo=1", f"pageNo={random_number}").replace("keyword=text", f"keyword={random_sufix}")
            print("검색어 " + random_sufix)
            print(new_url)           

            html = open_webpage(driver, new_url)

            # BeautifulSoup을 사용하여 HTML 파싱
            soup = BeautifulSoup(html, 'html.parser')

            # 'desc' 클래스를 가진 div 태그 내의 모든 a 태그 찾기
            links = soup.find_all('div', class_='desc')

            # 각 div 태그 내에서 href 속성 추출하여 배열에 저장
            hrefs = [link.find('a').get('href') for link in links if link.find('a')]     
            for href in hrefs:
                # check_exit()            
                print("방문사이트: " + href)
                tovisit_url = user_id + href
                if tovisit_url in visited_urls:
                    print(f"이미 방문한 주소입니다: {tovisit_url}")
                    # 이미 방문한 경우에는 pass 또는 다른 작업 수행 가능
                else:   
                    # 여기서부터 방문 및 크롤링 작업 수행                                      
                    # visited_urls에 새로운 URL을 추가
                    visited_urls.add(tovisit_url)

                    # 방문한 주소를 visit.txt 파일에 추가
                    with open(visit_path, "w") as file:
                        for url in visited_urls:
                            file.write(url + "\n")    

                    open_webpage(driver, href)
                    counter += 1  # 카운터 증가
                    # 현재 시간과 아이디, 카운터 값을 로그 파일에 기록
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    logging.info(f"Time: {current_time}, ID: {user_id}, Counter: {counter}")

                    print(f"진행회수: {counter}")

                    if counter > repeat_count:
                        print("반복수행완료")
                        break 

                    regex = r'blog\.naver\.com/([^/]+)/'
                    match = re.search(regex, href)
                    blog_ID = match.group(1) if match else None     

                    print("선택옵션: " + ", ".join(selected_options))     

                    # 해당 클래스 이름을 가진 요소 찾기 (서이추)
                    if "서이추" in selected_options:
                        print("서이추 - 공감 확장버튼 클릭")
                        allhtml = open_webpage(driver, href)

                        # iframe을 찾습니다
                        iframe = wait_for_element(driver, By.ID, "mainFrame")
                        # iframe으로 전환합니다
                        driver.switch_to.frame(iframe)

                        # URL에서 마지막 슬래시 이후의 숫자 추출
                        last_part = href.split('/')[-1]            

                        try:
                            like_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_arr._symList"))
                            )
                            like_button.click()
                            delaysecond()
                            # 이웃추가 버튼 클릭
                            # 모든 '.btn_buddy.pcol2' 요소 가져오기
                            # 올바른 메소드 사용
                            buttons = driver.find_elements(By.CSS_SELECTOR, ".btn_buddy.pcol2")
                            for button in buttons:
                                try:                                
                                    like_button_reply = WebDriverWait(driver, 10).until(
                                        EC.element_to_be_clickable(button)
                                    )
                                    like_button_reply.click()    
                                    print('버튼 찾음')                                       
                                    delaysecond()  
                                    try:                                
                                        like_button_reply = WebDriverWait(driver, 10).until(
                                            EC.element_to_be_clickable((By.CSS_SELECTOR, "#each_buddy_add"))
                                        )
                                        like_button_reply.click()    
                                        print('buddy 버튼 찾음')                                       
                                        delaysecond()     

                                        buttons = driver.find_elements(By.CSS_SELECTOR, "._buddyAddNext") 
                                        for button in buttons:
                                            try:                                
                                                like_button_reply = WebDriverWait(driver, 10).until(
                                                    EC.element_to_be_clickable(button)
                                                )
                                                like_button_reply.click()    
                                                print('버튼 찾음')                                       
                                                delaysecond()       
                                                
                                            except NoSuchElementException as e:
                                                logging.error(f"Element not found: {e}")
                                                break             
                                            except TimeoutException as e:
                                                logging.error(f"Timeout while waiting for element: {e}")                                                  
                                        
                                    except NoSuchElementException as e:
                                        logging.error(f"Element not found: {e}")
                                        break             
                                    except TimeoutException as e:
                                        logging.error(f"Timeout while waiting for element: {e}")                                              

                                except NoSuchElementException as e:
                                    logging.error(f"Element not found: {e}")
                                    break             
                                except TimeoutException as e:
                                    logging.error(f"Timeout while waiting for element: {e}")                                    

                        except NoSuchElementException as e:
                            logging.error(f"Element not found: {e}")
                            break             
                        except TimeoutException as e:
                            logging.error(f"Timeout while waiting for element: {e}")
                            # 예외를 다시 발생시킴                         
                        # iframe 작업을 마친 후 메인 문서로 다시 전환
                        driver.switch_to.default_content()                                     

                    # 해당 클래스 이름을 가진 요소 찾기 (댓글버튼)
                    if "댓글" in selected_options:
                        print("댓글 작성")
                        allhtml = open_webpage(driver, href)

                        # iframe을 찾습니다
                        iframe = wait_for_element(driver, By.ID, "mainFrame")
                        # iframe으로 전환합니다
                        driver.switch_to.frame(iframe)     

                        # iframe 내부의 HTML 가져오기
                        iframe_page_source = driver.page_source                                           
                        
                        # BeautifulSoup을 사용하여 HTML 파싱
                        blogsoup = BeautifulSoup(iframe_page_source, 'html.parser')

                        # href의 마지막 숫자(포스트 ID) 가져오기
                        post_id = get_post_id_from_href(href)

                        # XPath 동적 생성
                        xpath = f'//*[@id="printPost1"]/tbody/tr/td[2]'
                        # xpath = f'//*[@id="post-view{post_id}"]/div/div[3]'

                        # XPath로 특정 요소의 리스트 가져오기
                        elements = driver.find_elements(By.XPATH, xpath)

                        # XPath가 존재하는지 확인
                        if elements:
                            # XPath로 특정 요소의 텍스트 가져오기
                            element_text = elements[0].text

                            # 텍스트 출력
                            print(element_text)
                        else:
                            print("XPath not found.")    
                            time.sleep(100)               

                        if len(element_text) <= 200:
                            # 문자가 200개 이하면 통과한다.
                            # 글이 없는 것이 많다.
                            counter -= 1
                            pass                        
                                                
                        extracted_txt = ""                        
                        # Check if element_text is not None before processing
                        if element_text:
                            # 텍스트 가져오기 (최대 1500자)
                            max_length = 1500
                            extracted_txt = element_text[:max_length]
                            print(extracted_txt)
                        else:
                            print("No matching element text found.")
                   
                        # time.sleep(100)                                                
                        # 탭 목록 가져오기
                        tab_handles = driver.window_handles

                        if len(tab_handles) > 1:
                            # 두 번째 탭으로 전환 (첫 번째 탭은 0 인덱스)
                            driver.switch_to.window(tab_handles[1])
                        else:
                            print("There are no other open tabs. Opening a new tab.")
                            # 새로운 탭 열기 (예: Ctrl+T를 사용하여)
                            driver.execute_script("window.open('', '_blank');")
                            # 다시 탭 목록 가져오기
                            tab_handles = driver.window_handles
                            # 두 번째 탭으로 전환
                            driver.switch_to.window(tab_handles[1])
                            time.sleep(3)


                        # 두 번째 탭에 새로운 URL로 이동
                        chatgpt_url = "https://chat.openai.com"
                        driver.get(chatgpt_url)

                        sleep_with_esc(5)
                        click_element(driver, "gpt35") 
                        # textarea 요소를 찾습니다
                        textarea = driver.find_element(By.ID, "prompt-textarea")

                        text_to_paste = " '  \n\n   위의 글은 타인이 작성한 블로그 글이다. 이 글에 댓글을 생성하려고 한다. 친절하고 정중한 표현으로 블로그에 내가 직접 만든 댓글을 한글 10자~30자 이내로, 한국어로 자연스러운 말로  주제에 어울리는 댓글로 자연스럽게 만들어줘. 최대한 위의 주제를 잘 읽어서 도움이 되었고, 감사하는 말투로 말이지. 자연스럽게 '..니다'라는 말보다는 '...요'라는 식으로 부탁해. '블로그 댓글'이란 단어는 절대 안들어가게 작성해줘. 정중하면서 자연스러운 글에 대한 감상을 전해주세요.'댓글'이란 단어는 금지한다.  글자수를 꼭 지켜서 작성해줘. 한글 50자 이내로 생성해줘. "                        
                        textarea.click()
                        sleep_with_esc(5)
                        pyperclip.copy(extracted_txt + text_to_paste)
                        pyautogui.hotkey("ctrl", "v")
                        sleep_with_esc(3)
                        pyautogui.press('enter')
                        waitnext(driver)

                        textarea = driver.find_element(By.ID, "prompt-textarea")

                        text_to_paste = " '  \n\n   방금 작성한 글을 80자 이내로 요약해 주고, '이 블로그를' 이런 글은 제거해주고, 반드시 한국어로 작성해줘. "                        
                        textarea.click()
                        sleep_with_esc(5)
                        pyperclip.copy(text_to_paste)
                        pyautogui.hotkey("ctrl", "v")
                        sleep_with_esc(3)
                        pyautogui.press('enter')
                        waitnext(driver)                        
                         
                        sleep_with_esc(2) 
                        # CSS 선택자를 사용하여 요소 찾기 - GPT가 응답한 결과 찾기
                        css_selector = "div[data-message-author-role='assistant']"
                        elements = driver.find_elements(By.CSS_SELECTOR, css_selector)

                        combined_text = ""
                        created_reply_comments = ""

                        if elements:
                            last_element = elements[-1]  # 마지막 요소 선택                            

                            # 텍스트를 클립보드에 복사
                            created_reply_comments = last_element.text
                            pyperclip.copy(created_reply_comments)
                            print("생성한 댓글 : \n")
                            print(created_reply_comments)
   
                        time.sleep(1) 
                        # 다시 첫 번째 탭으로 전환
                        driver.switch_to.window(tab_handles[0])     
                        time.sleep(2)
                        # iframe을 찾습니다
                        iframe = wait_for_element(driver, By.ID, "mainFrame")
                        # iframe으로 전환합니다
                        driver.switch_to.frame(iframe)                
                        try:
                            like_button_reply = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_comment._cmtList"))
                            )
                            like_button_reply.click()                        
                            delaysecond() 
                            # 댓글넣는 input창               
                            try:
                                like_button_input = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".u_cbox_inbox"))
                                )
                                like_button_input.click()
                                delaysecond() 

                                # 파일에서 메시지 로드
                                # file_path = os.path.join(application_path, 'data', 'samplereply.txt')                
                                # messages = load_messages_from_file(file_path)
                                # print(messages)

                                # 무작위 메시지 선택
                                # random_message = select_random_message(messages)                                
                                # pyperclip.copy(select_text + random_message)
                                # chatgpt로 생성한 댓글
                                pyperclip.copy(created_reply_comments)
                                pyautogui.hotkey("ctrl", "v")      
                                delaysecond()   

                                # (저장 누르기)
                                like_button_save = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".u_cbox_btn_upload"))
                                )
                                like_button_save.click()
                                delaysecond()               
                                # pyautogui.press('enter')
                                pyautogui.press('esc')
                                time.sleep(2)             
                            except NoSuchElementException as e:
                                logging.error(f"Element not found: {e}")
                                # 예외를 다시 발생시킴
                            except TimeoutException as e:
                                logging.error(f"Timeout while waiting for element: {e}")
                                # 예외를 다시 발생시킴                

                        except NoSuchElementException as e:
                            logging.error(f"Element not found: {e}")
                            # 예외를 다시 발생시킴
                        except TimeoutException as e:
                            logging.error(f"Timeout while waiting for element: {e}")
                            # 예외를 다시 발생시킴     
                                                
                        # iframe 작업을 마친 후 메인 문서로 다시 전환
                        driver.switch_to.default_content()                                          

                    # 해당 클래스 이름을 가진 요소 찾기 (공감버튼)
                    if "공감" in selected_options:
                        print("공감 클릭")
                        allhtml = open_webpage(driver, href)                 

                        # iframe을 찾습니다
                        iframe = wait_for_element(driver, By.ID, "mainFrame")
                        # iframe으로 전환합니다
                        driver.switch_to.frame(iframe)

                        # URL에서 마지막 슬래시 이후의 숫자 추출
                        last_part = href.split('/')[-1]            

                        try:
                            like_button = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "._button.pcol2"))
                            )
                            like_button.click()
                            delaysecond()
                        except NoSuchElementException as e:
                            logging.error(f"Element not found: {e}")
                            break             
                        except TimeoutException as e:
                            logging.error(f"Timeout while waiting for element: {e}")
                            # 예외를 다시 발생시킴                         
                        # iframe 작업을 마친 후 메인 문서로 다시 전환
                        driver.switch_to.default_content()

                # 해당 클래스 이름을 가진 요소 찾기 (안부) 
                if "안부" in selected_options:                                
                    print("안부선택")
                    target_url = "https://blog.naver.com/guestbook/GuestBookList.naver?blogId=rbrmf"
                    guest_url = target_url.replace("blogId=rbrmf", f"blogId={blog_ID}")
                    open_webpage(driver, guest_url)     

                    try:
                        WebDriverWait(driver, 6).until(
                            EC.frame_to_be_available_and_switch_to_it((By.ID, 'mainFrame'))
                        )                    
                        print("mainFrame 찾음")
                    except NoSuchFrameException:
                        print("첫 번째 iframe (mainFrame)이 존재하지 않습니다.")
                    except TimeoutException as e:
                        logging.error(f"Timeout while waiting for element: {e}")                    

                    try:
                        WebDriverWait(driver, 6).until(
                            EC.frame_to_be_available_and_switch_to_it((By.ID, 'writeIFrame'))
                        )
                        print("writeIFrame 찾음")
                    except NoSuchFrameException:
                        print("두 번째 iframe (writeIFrame)이 존재하지 않습니다.")
                    except TimeoutException as e:
                        logging.error(f"Timeout while waiting for element: {e}")                    

                    try:
                        WebDriverWait(driver, 6).until(
                            EC.frame_to_be_available_and_switch_to_it((By.ID, 'POSTEDITOR'))
                        )
                        print("POSTEDITOR 찾음")
                    except NoSuchFrameException:
                        print("세 번째 iframe (POSTEDITOR)이 존재하지 않습니다.")
                    except TimeoutException as e:
                        logging.error(f"Timeout while waiting for element: {e}")                    

                    try:
                        # WebDriverWait를 사용하여 요소가 클릭 가능할 때까지 기다림
                        guest_input = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "body.view"))                        
                        )
                        guest_input.click()
                        print("body.view 찾음")

                        # 파일에서 메시지 로드
                        file_path = os.path.join(application_path, 'data', 'random_sayhell_prefix.txt')                
                        random_prefix_messages = load_messages_from_file(file_path)
                        file_path2 = os.path.join(application_path, 'data', 'sayhello.txt')                
                        messages = load_messages_from_file(file_path2)
                        # print(messages)

                        # 무작위 메시지 만들기
                        random_prefix = select_random_message(random_prefix_messages)
                        random_message = select_random_message(messages)
                        union_mesage = random_prefix + random_message
                        pyperclip.copy(union_mesage)
                        print(union_mesage)
                        print("정상적으로 안부전함")
                        pyautogui.hotkey("ctrl", "v")      
                        # (저장 누르기)
                        time.sleep(2)
                        pyautogui.press("tab")
                        time.sleep(1)
                        pyautogui.press("tab")
                        time.sleep(1)
                        pyautogui.press("enter")
                        time.sleep(1) 

                    except NoSuchFrameException:
                        print("body.view 존재하지 않습니다.")
                    except TimeoutException as e:
                        logging.error(f"Timeout while waiting for element: {e}")    

                        # (저장 누르기)
                    # try:                    
                    #     button_save = WebDriverWait(driver, 10).until(
                    #         EC.element_to_be_clickable((By.CSS_SELECTOR, "#guestbookSubmitBtn"))
                    #     )
                    #     button_save.click()
                    #     print("guestbookSubmitBtn 클릭")
                    #     delaysecond()                                   
                    #     pyautogui.press('esc')
                    #     time.sleep(2)        

                    # except NoSuchElementException as e:
                    #     logging.error(f"Element not found: {e}")                    
                    # except TimeoutException as e:
                    #     logging.error(f"Timeout while waiting for element: {e}")
                    #     # 예외를 다시 발생시킴                                   

                    # iframe 작업을 마친 후 메인 문서로 다시 전환
                    driver.switch_to.default_content()

                # if counter >= repeat_count:
                #     subprocess.Popen(["notepad.exe", log_file])
                #     break
                    
    else:
        while not exit_program and counter < repeat_count:  
            print("이웃방문 While 시작 ")            

            # 이미 방문한 주소를 저장할 파일
            visited_urls = set()

            # visit.txt 파일이 존재하는지 확인
            if os.path.exists(visit_path):
                # visit.txt 파일에서 이전에 방문한 주소를 읽어옴
                with open(visit_path, "r") as file:
                    for line in file:
                        visited_urls.add(line.strip())
            else:
                # 파일이 없을 경우 빈 세트를 사용
                visited_urls = set()

            # Generate the sentences again
            blog_style_sentences_v2 = generate_blog_style_sentences_v2()            
            for sentence in blog_style_sentences_v2:
                select_text = sentence                    

            inner_counter += 1

            # Creating a new URL with the generated random number and suffix
            target_url = "https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=0&groupId=0"
            guest_url = target_url.replace("currentPage=0", f"currentPage={inner_counter}")            
            html = open_webpage(driver, guest_url)
            # BeautifulSoup을 사용하여 HTML 파싱
            soup = BeautifulSoup(html, 'html.parser')

            # 'desc' 클래스를 가진 div 태그 내의 모든 a 태그 찾기
            links = soup.find_all('div', class_='desc')

            # 각 div 태그 내에서 href 속성 추출하여 배열에 저장
            hrefs = [link.find('a').get('href') for link in links if link.find('a')]                    
            for href in hrefs:
                # check_exit()            
                print("방문: " + href)
                tovisit_url = user_id + href
                if tovisit_url in visited_urls:
                    print(f"이미 방문한 주소입니다: {tovisit_url}")
                    time.sleep(10)
                    # 이미 방문한 경우에는 pass 또는 다른 작업 수행 가능
                else:   
                    # 여기서부터 방문 및 크롤링 작업 수행                                      
                    # visited_urls에 새로운 URL을 추가
                    visited_urls.add(tovisit_url)

                    # 방문한 주소를 visit.txt 파일에 추가
                    with open(visit_path, "w") as file:
                        for url in visited_urls:
                            file.write(url + "\n")    

                    open_webpage(driver, href)
                    counter += 1  # 카운터 증가
                    # 현재 시간과 아이디, 카운터 값을 로그 파일에 기록
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    logging.info(f"Time: {current_time}, ID: {user_id}, Counter: {counter}")

                    print(f"진행회수: {counter}")

                    if counter > repeat_count:
                        print("반복수행완료")
                        break 

                    regex = r'blog\.naver\.com/([^/]+)/'
                    match = re.search(regex, href)
                    blog_ID = match.group(1) if match else None     

                    print("선택옵션: " + ", ".join(selected_options))     

                    # 해당 클래스 이름을 가진 요소 찾기 (댓글버튼)
                    if "댓글" in selected_options:

                        print("댓글 작성")
                        allhtml = open_webpage(driver, href)

                        # iframe을 찾습니다
                        iframe = wait_for_element(driver, By.ID, "mainFrame")
                        # iframe으로 전환합니다
                        driver.switch_to.frame(iframe)     

                        # iframe 내부의 HTML 가져오기
                        iframe_page_source = driver.page_source                                           
                        
                        # BeautifulSoup을 사용하여 HTML 파싱
                        blogsoup = BeautifulSoup(iframe_page_source, 'html.parser')

                        # href의 마지막 숫자(포스트 ID) 가져오기
                        post_id = get_post_id_from_href(href)

                        # XPath 동적 생성
                        xpath = f'//*[@id="printPost1"]/tbody/tr/td[2]'
                        # xpath = f'//*[@id="post-view{post_id}"]/div/div[3]'

                        # XPath로 특정 요소의 리스트 가져오기
                        elements = driver.find_elements(By.XPATH, xpath)

                        # XPath가 존재하는지 확인
                        if elements:
                            # XPath로 특정 요소의 텍스트 가져오기
                            element_text = elements[0].text

                            # 텍스트 출력
                            print(element_text)
                        else:
                            print("XPath not found.")    
                            time.sleep(100)     

                        if len(element_text) <= 200:
                            # 문자가 200개 이하면 통과한다.
                            # 글이 없는 것이 많다.
                            counter -= 1
                            pass
                                                
                        extracted_txt = ""                        
                        # Check if element_text is not None before processing
                        if element_text:
                            # 텍스트 가져오기 (최대 1500자)
                            max_length = 1500
                            extracted_txt = element_text[:max_length]
                            print(extracted_txt)
                        else:
                            print("No matching element text found.")
                
                        # time.sleep(100)                                                
                        # 탭 목록 가져오기
                        tab_handles = driver.window_handles

                        if len(tab_handles) > 1:
                            # 두 번째 탭으로 전환 (첫 번째 탭은 0 인덱스)
                            driver.switch_to.window(tab_handles[1])
                        else:
                            print("There are no other open tabs. Opening a new tab.")
                            # 새로운 탭 열기 (예: Ctrl+T를 사용하여)
                            driver.execute_script("window.open('', '_blank');")
                            # 다시 탭 목록 가져오기
                            tab_handles = driver.window_handles
                            # 두 번째 탭으로 전환
                            driver.switch_to.window(tab_handles[1])
                            time.sleep(3)

                        # 두 번째 탭에 새로운 URL로 이동
                        chatgpt_url = "https://chat.openai.com"
                        driver.get(chatgpt_url)

                        time.sleep(4)
                        click_element(driver, "gpt35")    # 무료버전 3.5 사용이니 필요없음
                        # textarea 요소를 찾습니다
                        textarea = driver.find_element(By.ID, "prompt-textarea")

                        text_to_paste = " '  \n\n   위의 글은 타인이 작성한 블로그 글이다. 이 글에 댓글을 생성하려고 한다. 친절하고 정중한 표현으로 블로그에 내가 직접 만든 댓글을 한글 10자~30자 이내로, 한국어로 자연스러운 말로  주제에 어울리는 댓글로 자연스럽게 만들어줘. 최대한 위의 주제를 잘 읽어서 도움이 되었고, 감사하는 말투로 말이지. 자연스럽게 '..니다'라는 말보다는 '...요'라는 식으로 부탁해. '블로그 댓글'이란 단어는 절대 안들어가게 작성해줘. 정중하면서 자연스러운 글에 대한 감상을 전해주세요.'댓글'이란 단어는 금지한다.  글자수를 꼭 지켜서 작성해줘. 한글 50자 이내로 생성해줘. "                        
                        textarea.click()
                        sleep_with_esc(5)
                        pyperclip.copy(extracted_txt + text_to_paste)
                        pyautogui.hotkey("ctrl", "v")
                        sleep_with_esc(3)
                        pyautogui.press('enter')
                        waitnext(driver)
                        
                        sleep_with_esc(4)                         
                        textarea = driver.find_element(By.ID, "prompt-textarea")
                        
                        text_to_paste = " '  \n\n   방금 작성한 글을 80자 이내로 요약해 주고, '이 블로그를' 이런 글은 제거해주고, 반드시 한국어로 작성해줘. "
                        textarea.click()
                        sleep_with_esc(5)
                        pyperclip.copy(text_to_paste)
                        pyautogui.hotkey("ctrl", "v")
                        sleep_with_esc(3)
                        pyautogui.press('enter')
                        waitnext(driver)         

                        sleep_with_esc(4)    
                        # CSS 선택자를 사용하여 요소 찾기 - GPT가 응답한 결과 찾기
                        css_selector = "div[data-message-author-role='assistant']"
                        elements = driver.find_elements(By.CSS_SELECTOR, css_selector)

                        combined_text = ""
                        created_reply_comments = ""

                        if elements:
                            last_element = elements[-1]  # 마지막 요소 선택                            

                            # 텍스트를 클립보드에 복사
                            created_reply_comments = last_element.text
                            pyperclip.copy(created_reply_comments)
                            print("생성한 댓글 : \n")
                            print(created_reply_comments)

                        time.sleep(1) 
                        # 다시 첫 번째 탭으로 전환
                        driver.switch_to.window(tab_handles[0])     
                        time.sleep(2)                        

                        # iframe을 찾습니다
                        iframe = wait_for_element(driver, By.ID, "mainFrame")
                        # iframe으로 전환합니다
                        driver.switch_to.frame(iframe)                
                        try:
                            like_button_reply = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_comment._cmtList"))
                            )
                            like_button_reply.click()                        
                            delaysecond() 
                            # 댓글넣는 input창               
                            try:
                                like_button_input = WebDriverWait(driver, 15).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".u_cbox_inbox"))
                                )
                                like_button_input.click()
                                delaysecond() 

                                # iframe을 찾습니다
                                pyautogui.hotkey("ctrl", "v")      
                                delaysecond()   

                                # (저장 누르기)
                                like_button_save = WebDriverWait(driver, 15).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".u_cbox_btn_upload"))
                                )
                                like_button_save.click()
                                delaysecond()               
                                # pyautogui.press('enter')
                                pyautogui.press('esc')
                                time.sleep(2)             
                            except NoSuchElementException as e:
                                logging.error(f"Element not found: {e}")
                                # 예외를 다시 발생시킴
                            except TimeoutException as e:
                                logging.error(f"Timeout while waiting for element: {e}")
                                # 예외를 다시 발생시킴                

                        except NoSuchElementException as e:
                            logging.error(f"Element not found: {e}")
                            # 예외를 다시 발생시킴
                        except TimeoutException as e:
                            logging.error(f"Timeout while waiting for element: {e}")
                            # 예외를 다시 발생시킴     
                                                
                        # iframe 작업을 마친 후 메인 문서로 다시 전환
                        driver.switch_to.default_content()                                          


                    # 해당 클래스 이름을 가진 요소 찾기 (공감버튼)
                    if "공감" in selected_options:
                        print("공감 클릭")
                        open_webpage(driver, href)

                        # iframe을 찾습니다
                        iframe = wait_for_element(driver, By.ID, "mainFrame")
                        # iframe으로 전환합니다
                        driver.switch_to.frame(iframe)      

                        try:
                            like_button = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "._button.pcol2"))
                            )
                            like_button.click()
                            delaysecond()
                        except NoSuchElementException as e:
                            logging.error(f"Element not found: {e}")
                            break             
                        except TimeoutException as e:
                            logging.error(f"Timeout while waiting for element: {e}")
                            # 예외를 다시 발생시킴                         
                        # iframe 작업을 마친 후 메인 문서로 다시 전환
                        driver.switch_to.default_content()


                if counter > repeat_count and ReserveExecute == False:
                    subprocess.Popen(["notepad.exe", log_file])
                    # 프로그램 종료 시간 기록
                    end_time = time.time()

                    # 실행 시간 계산
                    execution_time = end_time - start_time

                    # 시간 형식으로 변환
                    hours, remainder = divmod(execution_time, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    # 결과를 포맷팅하는 부분 수정
                    parts = []
                    if hours:
                        parts.append(f"{int(hours)}h")
                    if minutes:
                        parts.append(f"{int(minutes)}m")
                    parts.append(f"{int(seconds) + 3 }초")  # 초를 '초'로 표시

                    formatted_execution_time = " ".join(parts)

                    print(f"실행 시간: {formatted_execution_time}")
                    
                    #  WebDriver 종료
                    driver.quit()
                    break
 
# 화면 해상도 및 윈도우 크기, 위치 설정 (절반크기)
# screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
# window_width, window_height = screen_width // 2, screen_height // 2
# x, y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
# window.geometry(f'{window_width}x{window_height}+{x}+{y}')
# 화면 해상도 및 윈도우 크기, 위치 설정
screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
window_width = screen_width // 2
window_height = (2 * window_width) // 2  # 2/2 비율로 window_height 계산
x, y = (screen_width - window_width) // 2, (screen_height - window_height) // 2 + 50  # 50을 더해서 아래로 조정
window.geometry(f'{window_width}x{window_height}+{x}+{y}')

id_var = tk.StringVar(window)
pw_var = tk.StringVar(window)

# ID, 패스워드 라벨 및 입력 필드 설정
id_label = tk.Label(window, text="ID", font=customFont).pack(anchor='center')
# ID와 패스워드 정보 불러오기 및 드롭다운 메뉴 생성
id_pw_dict = load_default_id_pw()

id_dropdown = tk.OptionMenu(window, id_var, *id_pw_dict.keys(),  command=update_pw )
id_dropdown.pack(anchor='center')

# 드롭다운 메뉴의 각 항목에 customFont 적용
menu = id_dropdown["menu"]
menu.config(font=customFont)  # 전체 메뉴의 폰트 설정

# 저장된 아이디와 해당 비밀번호 설정
selected_id = load_selected_id()
if selected_id in id_pw_dict:
    id_var.set(selected_id)
    pw_var.set(id_pw_dict[selected_id])  # 해당 ID의 비밀번호를 pw_var에 설정
else:
    id_var.set(list(id_pw_dict.keys())[0])
    pw_var.set(id_pw_dict[list(id_pw_dict.keys())[0]]) if id_pw_dict else pw_var.set('')

tk.Entry(window, textvariable=pw_var, state='readonly', font=customFont).pack(anchor='center',pady=10)    

# 체크박스 관련 설정 및 구성
selected_options = []
options = ["공감", "댓글", "이웃방문", "서이추" ]
loaded_selected_options = load_selected_options()
var_dict = {}
for option in options:
    var = tk.IntVar(value=1 if option in loaded_selected_options else 0)
    tk.Checkbutton(window, text=option, variable=var, font=customFont, ).pack(pady=10)
    var_dict[option] = var
    var.trace_add('write', on_checkbox_change)

# Load reservation list at program start
reservation_list = load_reservation_list()

# Add a button to add reservation to the list
tk.Button(window, text="Add List", font=customFont, command=add_reservation_to_list).pack(anchor='center', pady=10)

# Add a listbox to display reservations with width set to screen width
listbox = tk.Listbox(window, selectmode=tk.SINGLE, font=customFont, width=100)
listbox.pack(pady=10)
update_listbox()

# Add a button to delete selected reservation from the list
tk.Button(window, text="Delete List", font=customFont, command=delete_selected_reservation).pack(anchor='center', pady=10)

# Add a button to perform actions based on the reservation list
tk.Button(window, text="예약List 일괄실행", font=customFont, command=lambda: perform_actions(reservation_list)).pack(anchor='center', pady=10)

# 유저 인터페이스에 반복 횟수 입력창 추가
tk.Label(window, text="반복회수", font=customFont).pack(anchor='center')
tk.Entry(window, textvariable=repeat_count_var, font=customFont).pack(anchor='center', pady=10)

# StringVar 객체 생성 및 초기값 설정
seconds_var = tk.StringVar(value='0')
tk.Label(window, text="예약초 : ").pack()
tk.Entry(window, textvariable=seconds_var).pack()

# 타이머 레이블
timer_label = tk.Label(window, text="시간을 설정해주세요")
timer_label.pack()

# 프로그램 시작 시 반복 횟수 로드
repeat_count_var.set(load_repeat_count())

# 실행, 종료 버튼 및 이벤트 핸들러 설정
tk.Button(window, text="실행", font=customFont, command=schedule_action).pack(anchor='center', pady=10)
tk.Button(window, text="종료", font=customFont, command=on_closing).pack(pady=10)
window.bind("<Escape>", on_escape)
window.protocol("WM_DELETE_WINDOW", on_closing)

esc_thread = threading.Thread(target=check_esc)
esc_thread.start()
# 윈도우 실행
window.mainloop()

check_exit()
# WebDriver 종료
# driver.quit()