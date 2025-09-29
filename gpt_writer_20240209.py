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
from datetime import datetime
import tkinter as tk
from tkinter import font as tkFont  # 폰트 모듈 추가
from tkinter import messagebox
import json
import cv2
import numpy as np
import re
import subprocess
import psutil
import glob
from screeninfo import get_monitors

monitors = get_monitors()
# 모든 모니터의 정보를 출력합니다.
for monitor in monitors:
    print(f"Monitor {monitor.name}: Width={monitor.width}, Height={monitor.height}, X={monitor.x}, Y={monitor.y}")


# 프로그램 종료 플래그
exit_program = False
source_item = ""
keyword = ""

# 현재 날짜와 시간을 '년월일_시분초' 형식으로 가져옴
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# 파일 이름 설정: 'YYYYMMDD_HHMMSS.dxf'

application_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
chrome_saved_file = os.path.join(application_path, 'data', 'chromesaved.json')
first_file_name = os.path.join(application_path, 'data', f"source_first_{current_time}.txt")
last_file_name = os.path.join(application_path, 'data', f"source_last_{current_time}.txt")

def close_all_chrome_windows():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if 'chrome' in process.info['name'].lower():
                process.terminate()  # 프로세스 종료
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def save_com_data():
    selected_id = com_id_var.get()
    selected_folder_info = com_folder_var.get()
    if selected_id in com_id_pw:
        selected_data = {
            'com_id_var': selected_id,
            'com_folder_var': selected_folder_info
        }
        with open(chrome_saved_file, 'w') as saved_file:
            json.dump(selected_data, saved_file)
        print(f"{selected_id}의 데이터가 chromesaved.json 파일로 저장되었습니다.")
    else:
        print("선택한 ID에 대한 데이터가 없습니다.")

def load_saved_data():
    if os.path.isfile(chrome_saved_file):
        with open(chrome_saved_file, 'r') as saved_file:
            saved_data = json.load(saved_file)
            if 'com_id_var' in saved_data:
                com_id_var.set(saved_data['com_id_var'])
            if 'com_folder_var' in saved_data:
                com_folder_var.set(saved_data['com_folder_var'])
        print(f"{chrome_saved_file} 파일에서 데이터를 불러왔습니다.")
    else:
        print("이전에 저장한 데이터 파일이 없습니다.")

def kill_notepad():    
    sleep_with_esc(0.5)

    # 메모장 프로세스 종료
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if "notepad.exe" in proc.info['name']:
            try:
                process = psutil.Process(proc.info['pid'])
                process.terminate()  # 프로세스 종료
            except Exception as e:
                print(f"메모장 종료 중 오류 발생: {str(e)}")

    print("메모장을 종료했습니다.")

# 문자열 첫째~다섯째 추가적으로 붙여주는 함수
def replace_text_between(source_txt, change_txt, first_word, second_word):
    # 첫째 단어의 위치 찾기
    start_index = source_txt.find(first_word)

    # 둘째 단어의 위치 찾기
    end_index = source_txt.find(second_word, start_index)

    # 첫째와 둘째 단어 사이의 내용을 바꾸기
    if start_index != -1 and end_index != -1:
        updated_txt = source_txt[:start_index] + first_word + ", \n\n" + str(change_txt) + source_txt[end_index:]
    else:
        updated_txt = source_txt  # 첫째와 둘째 단어가 텍스트에 없을 경우 원본 텍스트 유지

    return updated_txt
    
def extract_text_between(source_txt, first_word, second_word):

    # 첫째 단어의 위치 찾기
    start_index = source_txt.find(first_word)

    # 둘째 단어의 위치 찾기
    end_index = source_txt.find(second_word, start_index)

    # 첫째와 둘째 단어 사이의 내용 추출
    if start_index != -1 and end_index != -1:
        extracted_txt = first_word + " " + source_txt[start_index + len(first_word):end_index]
    else:
        extracted_txt = ""  # 첫째와 둘째 단어가 텍스트에 없을 경우 빈 문자열 반환

    return extracted_txt
    
def sleep_with_esc(duration):
    # 'ESC' 키를 감지하는 백그라운드 스레드 시작
    esc_thread = threading.Thread(target=check_esc)
    esc_thread.daemon = True
    esc_thread.start()

    # 주어진 시간 동안 대기
    time.sleep(duration)

def check_esc():
    while True:
        if keyboard.is_pressed('esc'):
            print("ESC pressed. Exiting...")
            sys.exit(0)
        time.sleep(0.1)

if __name__ == "__main__":
    duration = 1  # 대기할 시간 (초)
    sleep_with_esc(duration)

def check_exit():
    global exit_program
    while True:
        # if keyboard.is_pressed('windows') and keyboard.is_pressed('esc'):
        if keyboard.is_pressed('esc'):
            print("프로그램 중단")
            exit_program = True
            sys.exit()
            break        

# 키보드 감시 스레드 시작
exit_thread = threading.Thread(target=check_exit)
exit_thread.start()

def wait_for_element(driver, by, selector, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )

def open_webpage(driver, url):
    driver.implicitly_wait(10)  # Wait up to 10 seconds for the page to load
    driver.maximize_window()    # Maximize the browser window
    driver.get(url)             # Open the webpage
    sleep_with_esc(2)
    return driver.page_source   # Return the HTML content of the page

def delaysecond():
    random_sleep_time = random.randint(4, 10)  # 4초에서 10초 사이의 랜덤한 정수 생성
    sleep_with_esc(random_sleep_time)  # 생성된 랜덤한 시간만큼 대기

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

def load_com_id_pw():
    try:        
        # 'data' 폴더 내의 'json' 파일 경로를 구성합니다        
        jsonfile_path = os.path.join(application_path, 'data', 'chrome.json')
        with open(jsonfile_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def update_pw(selected_id, *args):
    com_folder_var.set(com_id_pw.get(selected_id, ''))

def on_escape(event=None):
    global exit_program    
    save_com_data()
    print("ESC pressed. Exiting...")
    window.withdraw()
    exit_program = True
    sys.exit()

def on_closing():    
    global exit_program    
    save_com_data()
    print("ESC pressed. Exiting...")
    window.withdraw()
    exit_program = True
    sys.exit()

# 다음 입력가능 이미지와 continue 이미지를 찾는다
def waitnext(driver):
    sleep_with_esc(20)

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

def execute_action():
    # 버튼이 클릭되었을 때 실행할 작업
    print("버튼 클릭")    
    save_com_data()


    # 프로그램 시작 시간 기록
    start_time = time.time()
    # 여기에 프로그램 코드를 작성합니다.

    # topic_text에서 값을 가져옴
    # keyword = topic_text.get()
    # topic_text에서 값을 가져옴
    global keyword
    keyword = topic_text.get("1.0", tk.END).strip()  # 줄바꿈 문자 제외

    folder_value = com_folder_var.get()

    keyword_path = os.path.join(application_path, 'data', 'keyword.txt')    
    # keyword.txt 파일에 키워드 저장
    with open(keyword_path, 'w', encoding='utf-8') as file:
        file.write(keyword)

    # GUI 창 숨기기
    window.withdraw()     
    
    # 모든 크롬 창 종료
    close_all_chrome_windows()

    time.sleep(3)
    
    options = Options()

    options.add_argument(f"user-data-dir={folder_value}")

    options.add_experimental_option("detach", True)  # 화면이 꺼지지 않고 유지
    options.add_experimental_option("excludeSwitches", ["enabled-automation"])  # chrome 자동화된 프로그램에 의해 제어되고 ' 문구 삭제

    options.add_argument("--start-maximized")  # 최대 크기로 시작
    options.add_argument("--disable-blink-features=AutomationControlled")  # 옵션 한줄로 로봇이 아닌 사람으로 감지되는 방법

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    
    x_coordinate = monitors[0].width
    # Y 좌표는 0으로 설정하면 됩니다.
    y_coordinate = 0
    # Chrome WebDriver 생성
    driver.set_window_position(x_coordinate, y_coordinate)

    url = "https://chat.openai.com"

    driver.implicitly_wait(10)  #페이지가 로딩될때까지 최대 10초 기다려줌
    driver.maximize_window()
    driver.get(url) # 페이지 열기
    sleep_with_esc(3)
    pyautogui.press('esc')    
    sleep_with_esc(3)
    # 메모장 강제로 닫기
    kill_notepad()
    # 메인 프로그램 루프
    while not exit_program:  # exit_program이 False인 동안 반복

        click_element(driver, "gpt4")        
        # textarea 요소를 찾습니다
        textarea = driver.find_element(By.ID, "prompt-textarea")   
        
        # text_to_paste = "이제부터 너는 최고의 세계에서 제일 잘하는 블로그 글 작성자다. 알았으면 '네'라고 대답해."
        # # text_to_paste = "한국의 장점을 첫째, 둘째, 셋째 글로 정리해서 3000자에 맞춰 작성해줘"  # 테스트용
        # textarea.send_keys(text_to_paste)
        # sleep_with_esc(1)
        # pyautogui.press('enter')
        # # sleep_with_esc(10)
        # waitnext(driver)

        sleep_with_esc(1)
                
        # text_to_paste = topic_text.get()  # StringVar 객체에서 문자열 값을 추출
        # topic_text에서 값을 가져옴
        combined_text = ""
        suffix_text = " 라는 주제로 500자 이내로 블로그글 작성해줘 나는 한국인이다. 한국인이라는 말은 본문에는 넣지 않지만, 한국인이라는 기준으로 모든 글을 작성한다. 문장에 한국인이란 말은 넣지 않는다."

        # 두 문자열을 합치기
        combined_text = keyword + suffix_text
        
        # 포커스 잡기
        textarea.click()
        pyperclip.copy(combined_text)   
        pyautogui.hotkey("ctrl", "v")                
        sleep_with_esc(3)
        pyautogui.press('enter')
        # sleep_with_esc(60)
        waitnext(driver)

        print("2 GPT 텍스트 추출: ")                   

        sleep_with_esc(2)
        text_to_paste = """ 위의 글을 이런조건으로 다시 정리해서 생성해. 블로그 제목은 50자 이내로 생성 글에는 ':' 기호 없애줘.
        논문형식으로 '시작하며', '맺으며' 순으로 생성. 핵심적인 내용 5가지는 반드시 한국어로 첫째, 둘째, 셋째, 넷째, 다섯째 이런식으로 글의 첫머리에 붙여주고,         
        각 5개의 글에 대한 세부글 100자 이내. 전체글 크기는 1500자 이내로 생성. """

        pyperclip.copy(text_to_paste)  
        pyautogui.hotkey("ctrl", "v")        
        sleep_with_esc(3)
        pyautogui.press('enter')
        waitnext(driver)        

        # CSS 선택자를 사용하여 요소 찾기 - GPT가 응답한 결과 찾기
        css_selector = "div[data-message-author-role='assistant']"
        elements = driver.find_elements(By.CSS_SELECTOR, css_selector)

        if elements:
            last_element = elements[-1]  # 마지막 요소 선택
            # 이제 last_element를 사용하여 원하는 작업 수행

        global source_item        
        print("3 GPT 텍스트 추출: ")        

        source_item = last_element.text # 리스트 형태를 문자열 형태로 변환한 것
        text_to_paste = "생성된 각각의 글에 해당되는 이미지를 각각 1개씩 총 5개 이미지를 realistic하게 표현하고, 최대한 글의 내용이 조금이라도 들어가게 해줘, '한글'은 사진에 안나오게 생성. 생성된 5가지 이미지를 각각 파일이름을 1.png, 2.png, 3.png 4.png 5png 이런식으로 다운로드할수 있는 링크 생성해줘. "

        pyperclip.copy(text_to_paste)          
        pyautogui.hotkey("ctrl", "v")        
        sleep_with_esc(3)
        pyautogui.press('enter')
        # sleep_with_esc(120)
        waitnext(driver)

        print("4 GPT 이미지부분 text 추출: ")        

        # source.txt 파일을 쓰기 모드로 열고 텍스트 변수의 내용을 파일에 저장합니다.        
        with open(first_file_name , 'w', encoding='utf-8') as file:
            file.write(source_item)
        print("1차 first_file_name.txt 파일에 저장되었습니다.")
        
        # 3.5로 용량을 아낀다
        # 3.5로 용량을 아낀다
        # 3.5로 용량을 아낀다
        click_element(driver, "gpt35")

        source = source_item

        # 코드를 5회 반복
        for i in range(1, 6):
            first_word = ["첫째", "둘째", "셋째", "넷째", "다섯째"][i-1]
            second_word = ["둘째", "셋째", "넷째", "다섯째", "맺으며"][i-1]

            extracted_txt = extract_text_between(source, first_word, second_word)
            print(f"Extracted Text {i}:")
            print(extracted_txt)

            # textarea 요소를 찾습니다
            textarea = driver.find_element(By.ID, "prompt-textarea")

            text_to_paste = "위의 주제로 세부적인 사항 글자 400자 이내로 생성해줘. 전체적으로 전반적인 말투는 '..니다'라는 글을 최대한 자제해 주고, 친한사람에게 들려주는 친근한 어투로 글을 작성해줘. 예를 들어 '했어요' , '였어요' 와 같은 구어체와 문어체의 중간정도로  블로그 글을 작성해줘."
            textarea.click()
            sleep_with_esc(2)
            pyperclip.copy(extracted_txt + text_to_paste)
            pyautogui.hotkey("ctrl", "v")
            sleep_with_esc(2.5)
            pyautogui.press('enter')
            waitnext(driver)

            # CSS 선택자를 사용하여 요소 찾기 - GPT가 응답한 결과 찾기
            css_selector = "div[data-message-author-role='assistant']"
            elements = driver.find_elements(By.CSS_SELECTOR, css_selector)

            combined_text =""
            if elements:
                last_element = elements[-1]  # 마지막 요소 선택
                # 이제 last_element를 사용하여 원하는 작업 수행            

                # 각 요소의 텍스트를 가져와서 누적
                combined_text += last_element.text + "\n\n\n"

            source = replace_text_between(source, combined_text, first_word, second_word)
            print(f"변환 후 source {i}:")
            print(source)             

        # 추가적인 작업 마무리 멘트 만들고 태그 만들기

        # textarea 요소를 찾습니다
        textarea = driver.find_element(By.ID, "prompt-textarea")

        text_to_paste = "위의 '맺으며' 300자 이내로 글을 마무리 정리글을 생성해줘.  예를들어 '..니다'라는 글이 친한 지인에게 말하는 것 같은 친근한 문장으로 예를 들어 '했어요' , '였어요'라는 식으로 친절한 말투로 생성해줘."
        textarea.click()
        sleep_with_esc(2)
        pyperclip.copy(text_to_paste)
        pyautogui.hotkey("ctrl", "v")
        sleep_with_esc(2)
        pyautogui.press('enter')
        waitnext(driver)

        # CSS 선택자를 사용하여 요소 찾기 - GPT가 응답한 결과 찾기
        css_selector = "div[data-message-author-role='assistant']"
        elements = driver.find_elements(By.CSS_SELECTOR, css_selector)

        combined_text =""
        if elements:
            last_element = elements[-1]  # 마지막 요소 선택
            # 이제 last_element를 사용하여 원하는 작업 수행            

            # 각 요소의 텍스트를 가져와서 누적
            combined_text += last_element.text + "\n\n\n"    

        source = source + combined_text

        # textarea 요소를 찾습니다
        textarea = driver.find_element(By.ID, "prompt-textarea")
        
        text_to_paste = "첫째부터 다섯째 글까지 내용을 상징하는 관련 태그 10개에서 20개 사이로 랜덤하게 추천해줘. 각 태그는 문장안에는 공백없이 붙여주고, '#'부호를 앞에 붙여줘.  태그라는 단어는 들어가지 않고, 자연스럽게 작성해줘."
        textarea.click()
        sleep_with_esc(2)
        pyperclip.copy(text_to_paste)
        pyautogui.hotkey("ctrl", "v")
        sleep_with_esc(3)
        pyautogui.press('enter')
        waitnext(driver)

        # CSS 선택자를 사용하여 요소 찾기 - GPT가 응답한 결과 찾기
        css_selector = "div[data-message-author-role='assistant']"
        elements = driver.find_elements(By.CSS_SELECTOR, css_selector)

        if elements:
            last_element = elements[-1]  # 마지막 요소 선택
            # 이제 last_element를 사용하여 원하는 작업 수행              

        combined_text =""
        if elements:
            last_element = elements[-1]  # 마지막 요소 선택
            # 이제 last_element를 사용하여 원하는 작업 수행            

            # 각 요소의 텍스트를 가져와서 누적
            combined_text += last_element.text + "\n\n\n"     

        source = source + combined_text
        
        with open(last_file_name , 'w', encoding='utf-8') as file:
            file.write(source)
        print("last_file_name.txt 파일에 저장되었습니다.")
        sleep_with_esc(2)
        subprocess.Popen(["notepad.exe", last_file_name])
        # 프로그램 종료 시간 기록
        end_time = time.time()

        # 실행 시간 계산
        execution_time = end_time - start_time

        # 결과 출력
        print(f"프로그램 시작 시간: {start_time}")
        print(f"프로그램 종료 시간: {end_time}")
        print(f"프로그램 실행 시간: {execution_time} 초")
        
        #  WebDriver 종료
        driver.quit()

# 윈도우 생성
window = tk.Tk()
window.title("chatGPT 글 생성기")

# 폰트 스타일 설정
customFont = tkFont.Font(family="굴림", size=13) # 여기에서 size를 조절하여 텍스트 크기 변경

# Load ID and Password data
com_id_pw = load_com_id_pw()

# 화면 해상도 가져오기
screen_width = window.winfo_screenwidth()  # 화면의 전체 너비
screen_height = window.winfo_screenheight()  # 화면의 전체 높이

# 윈도우 크기를 화면의 절반으로 설정
window_width = screen_width // 2
window_height = screen_height // 2

# 윈도우를 화면의 중앙에 위치시킴
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 윈도우 크기와 위치 설정
window.geometry(f'{window_width}x{window_height}+{x}+{y}')
# ID 입력
com_id_var = tk.StringVar(window)
com_folder_var = tk.StringVar(window)

com_id_com_folder_frame = tk.Frame(window)  # 동일한 부모 프레임 생성

# keyword_path로부터 키워드 읽기
keyword_path = os.path.join(application_path, 'data', 'keyword.txt')    
with open(keyword_path, 'r', encoding='utf-8') as file:
    keyword = file.read().strip()  # Use strip() to remove any leading/trailing whitespace


# ID 라벨과 드롭다운 메뉴
com_id_label_text = "글작성 컴퓨터 선택 "
com_id_label = tk.Label(com_id_com_folder_frame, text=com_id_label_text, font=customFont)
com_id_label.grid(row=0, column=0, padx=10, pady=10)

com_id_dropdown = tk.OptionMenu(com_id_com_folder_frame, com_id_var, *com_id_pw.keys(), command=update_pw)
com_id_dropdown.grid(row=0, column=1, padx=10, pady=10)

com_folder_label = tk.Label(com_id_com_folder_frame, text="chrome://version 정보", font=customFont)
com_folder_label.grid(row=1, column=0, padx=10, pady=10)  

com_folder_entry = tk.Entry(com_id_com_folder_frame,  width=70, textvariable=com_folder_var, state='readonly')
com_folder_entry.grid(row=1, column=1, padx=10, pady=10)  

# 기존의 저장된 정보를 가져옴
load_saved_data()

# 블로그 주제 라벨과 Text 위젯
topic_label = tk.Label(com_id_com_folder_frame, text="블로그 주제:", font=customFont)
topic_label.grid(row=2, column=0, padx=10, pady=10)  # 블로그 주제 라벨 위치

topic_text = tk.Text(com_id_com_folder_frame, height=1, width=80, font=customFont)
topic_text.grid(row=2, column=1, padx=10, pady=10)  # 블로그 주제 Text 위젯 위치
# topic_text 위젯의 텍스트 내용 변경
topic_text.delete(1.0, tk.END)  # 현재 텍스트 삭제
topic_text.insert(tk.END, keyword)  # 새로운 키워드 삽입

com_id_com_folder_frame.pack(anchor='center', pady=10)  # 간격 추가

# 실행 버튼 추가
execute_button = tk.Button(window, text="실행", font=customFont, command=execute_action)
execute_button.pack(anchor='center', pady=10)  # 간격 추가

# Update password when ID is selected
com_id_var.trace('w', update_pw)

# ESC 키 이벤트에 대한 핸들러 설정
window.bind("<Escape>", on_escape)

window.protocol("WM_DELETE_WINDOW", on_closing)  # 닫기 버튼 클릭 시 on_closing 함수 실행
# Run the application
window.mainloop()

check_exit()