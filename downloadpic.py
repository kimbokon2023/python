import os
import time
import threading
import queue
import tkinter as tk
from tkinter import messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import traceback

DOWNLOAD_DIR = r"C:\downloadpic"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

log_queue = queue.Queue()

def update_log(text_widget):
    try:
        while not log_queue.empty():
            msg = log_queue.get_nowait()
            text_widget.insert(tk.END, msg + "\n")
            text_widget.see(tk.END)
    except queue.Empty:
        pass
    finally:
        text_widget.after(100, lambda: update_log(text_widget))

def log(msg):
    print(msg)
    log_queue.put(msg)

def download_images(keyword):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(service=Service(), options=chrome_options)

        log("Google 이미지 검색 페이지 접속 중...")
        driver.get("https://www.google.com/imghp?hl=ko")

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img.YQ4gaf, img.cC9Rib, img.Q4LuWd"))
        )

        for _ in range(10):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(1.5)

        images = driver.find_elements(By.CSS_SELECTOR, "img.YQ4gaf, img.cC9Rib, img.Q4LuWd")
        downloaded = 0

        for index, img in enumerate(images):
            try:
                img.click()
                time.sleep(2.5)

                # 원본 이미지가 로딩될 때까지 기다림
                big_img = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb"))
                )

                src = big_img.get_attribute("src")
                print(f"[{index}] src: {src}")

                if src and src.startswith("http") and "encrypted-tbn" not in src:
                    filename = os.path.join(DOWNLOAD_DIR, f"{keyword}_{index+1}.jpg")
                    urllib.request.urlretrieve(src, filename)
                    downloaded += 1
                    log(f"[{downloaded}/100] 저장됨: {filename}")

                if downloaded >= 100:
                    break

            except Exception as e:
                log(f"{index+1}번째 이미지 실패: {e}")
                continue



        log(f"총 {downloaded}개의 이미지를 저장했습니다.")
        messagebox.showinfo("완료", f"{downloaded}개의 이미지를 저장했습니다.")

    except Exception as e:
        log("오류 발생:\n" + traceback.format_exc())
        messagebox.showerror("오류", str(e))
    finally:
        driver.quit()

def start_thread(keyword_entry):
    keyword = keyword_entry.get().strip()
    if not keyword:
        messagebox.showwarning("입력 오류", "검색어를 입력하세요.")
        return
    threading.Thread(target=download_images, args=(keyword,), daemon=True).start()

def create_gui():
    window = tk.Tk()
    window.title("이미지 검색 다운로드")
    window.geometry("600x500")

    tk.Label(window, text="검색어를 입력하세요:").pack(pady=5)

    keyword_entry = tk.Entry(window, font=("맑은 고딕", 14))
    keyword_entry.pack(pady=5, fill=tk.X, padx=10)

    tk.Button(window, text="이미지 다운로드 시작", command=lambda: start_thread(keyword_entry)).pack(pady=10)

    log_area = scrolledtext.ScrolledText(window, height=20, font=("Consolas", 11))
    log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    update_log(log_area)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
