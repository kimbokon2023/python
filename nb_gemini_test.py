
import time
import os
import sys
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
import json
import numpy as np
import re
import subprocess
import psutil
import requests
from screeninfo import get_monitors
import google.generativeai as genai

# 실행 번호 변수 초기화
current_execution_number = 0

monitors = get_monitors()
# 모든 모니터의 정보를 출력합니다.
for monitor in monitors:
    print(f"Monitor {monitor.name}: Width={monitor.width}, Height={monitor.height}, X={monitor.x}, Y={monitor.y}")

# 프로그램 시작 시간 기록
start_time = time.time()

# 현재 날짜와 시간을 '년월일_시분초' 형식으로 가져옴
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

element_text = """크리스마스도 이제 끝나고.. 본격적인 연말연시네요~
우리 직장인들은 연말정산이란 단어가 이때쯤은 자주 생각날거예요~

연말이 다가오면서 직장인들에게 필수적인 세금 지식에 대해 알아보고자 합니다. 올바른 세금 지식은 여러분의 재정적 부담을 줄이는 데 큰 도움이 될 것입니다. 여기서는 핵심적인 다섯 가지 세금 상식을 정리하여 소개합니다.

사진 설명을 입력하세요.

첫째,

연말정산, 이거 정말 중요하다 냐고요? 그거 아실래요? 한 해 동안 내가 세금으로 내놓은 돈과 실제로 내야 할 세금을 체크하는 거라고요. 그런데 이게 중요한 이유가 있는데, 의료비나 교육비 같은 걸 공제받을 수 있어서 세금 혜택을 최대한 누릴 수 있거든요.
예를 들어요, 내년에 연말정산을 할 때 내가 지난 해에 얼마나 의료비를 썼는지, 교육비를 얼마나 들였는지가 중요해요. 그 비용들을 제대로 기록하고 정리해두면 세금을 덜 내거나 환급받을 수 있는 기회가 높아져요. 그러니까 꼭 철저히 준비해보세요. 이웃집 아저씨가 말하길, 연말정산은 돈을 아끼고 세금 혜택을 누리는 데 큰 도움이 될 거예요!

사진 설명을 입력하세요.

둘째,

건강보험료와 국민연금 공제, 그거 소득에 따라서 내야 하는 거 알고 계시나요? 이거 연말정산 때 정말 중요하답니다. 왜냐하면 이걸 잘 활용하면 세금 부담을 줄일 수 있거든요.
간단히 설명드릴게요. 건강보험료와 국민연금은 내 연봉에 따라서 정해지는데, 이게 바로 소득공제 항목 중 하나에요. 그러니까 내 소득에서 이 부분들을 공제하면 세금을 덜 내야 한답니다. 예를 들어, 내 소득이 높으면 건강보험료와 국민연금을 많이 내야 하지만, 그걸 공제로 활용하면 세금을 줄일 수 있어요.
그래서 연말에 정리할 때 이 부분을 꼭 확인해보세요. 이웃집 아줌마가 말하길, 건강보험료와 국민연금 공제를 잘 활용하면 더 많은 돈을 쥐어짤 수 있답니다. 꼭 기억해두세요!

사진 설명을 입력하세요.

셋째,

주택자금 이자 공제 혜택, 정말 좋아요! 주택 대출 이자를 내면 그걸로 세금에서 혜택을 받을 수 있는데, 특히 첫 주택을 사거나 장기 주택 저당 대출을 이용할 때 더 큰 혜택을 받을 수 있답니다.
예를 들어요, 첫 집을 사면 주택자금 이자 공제를 통해 세금을 덜 내야 해요. 그리고 장기 주택 저당 대출을 이용하면 매년 이자를 공제해서 세금 혜택을 계속 받을 수 있어요.
이거 꼭 알아두세요! 주택자금 이자 공제를 잘 활용하면 세금을 아낄 수 있고, 집을 사는데도 더 도움이 돼요. 이웃집 아줌마들끼리 얘기하면서 정보 공유하듯, 주택 관련 혜택은 놓치지 마세요! """

# 제외할 문구들  # 제외할 문구들
exclude_phrases = ["인쇄", "이 글에 공감한 블로거 열고 닫기","댓글 쓰기","이 글에 댓글 단 블로거 열고 닫기","블로그 보내기","카페 보내기","Keep 보내기","메모 보내기","기타 보내기 펼치기","URL 복사","서로이웃","본문 기타 기능","공감","인쇄","방금","© NAVER Corp.","태그","내용 변경 불가", "영리적 사용 불가","저작자 명시 필수"]

# 각 문구를 제외
for phrase in exclude_phrases:
    element_text = element_text.replace(phrase, "")                                  
# Check if element_text is not None before processing
if element_text:    
    max_length = 1000
    extracted_txt = element_text[:max_length]
    #  print(extracted_txt)
else:
    print("No matching element text found.")

retry_limit = 100  # 재시도 횟수 제한
retry_count = 0  # 현재 재시도 횟수

text_to_paste = "   이 글은 타인이 작성한 블로그 글이다. 이 글에 댓글을 생성하려고 한다. 친절하고 정중한 표현으로 블로그에 내가 직접 만든 댓글을 한글 30자~50자 이내로, 한국어로 자연스러운 말로  주제에 어울리는 댓글로 자연스럽게 만들어줘. 최대한 위의 주제를 잘 읽어서 도움이 되었고, 감사하는 말투로 말이지. 자연스럽게 '..니다'라는 말보다는 '...요'라는 식으로 부탁해. '블로그 댓글'이란 단어는 절대 안들어가게 작성해줘. 정중하면서 자연스러운 글에 대한 감상을 전해주세요.'댓글'이란 단어는 금지한다. 자연스럽고 공손하게 한국어로만 생성해줘.  "                                                    
prompt_parts = [ extracted_txt + text_to_paste ]

retry_limit = 100  # 재시도 횟수 제한

genai.configure(api_key="AIzaSyDwNMPZl7J-Wl-pKYM2N92-TsYTvE_X93k")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# 반복 횟수 설정
num_retries = 100

for retry_count in range(num_retries):
    try:
        text_to_paste = "   이 글은 타인이 작성한 블로그 글이다. 이 글에 댓글을 생성하려고 한다. 친절하고 정중한 표현으로 블로그에 내가 직접 만든 댓글을 한글 30자~50자 이내로, 한국어로 자연스러운 말로  주제에 어울리는 댓글로 자연스럽게 만들어줘. 최대한 위의 주제를 잘 읽어서 도움이 되었고, 감사하는 말투로 말이지. 자연스럽게 '..니다'라는 말보다는 '...요'라는 식으로 부탁해. '블로그 댓글'이란 단어는 절대 안들어가게 작성해줘. 정중하면서 자연스러운 글에 대한 감상을 전해주세요.'댓글'이란 단어는 금지한다. 자연스럽고 공손하게 한국어로만 생성해줘.  "                                                    
        prompt_parts = [ extracted_txt + text_to_paste ]
        genai.configure(api_key="AIzaSyDwNMPZl7J-Wl-pKYM2N92-TsYTvE_X93k")        
        response = model.generate_content(prompt_parts)
        if response.parts:
            # 여기에 응답을 처리하는 코드를 작성하세요.
            print(f"Retry {retry_count + 1} Response:")
            print(response.text)
            time.sleep(1)
    except ValueError as e:
        print(f"Retry {retry_count + 1} 오류 발생: {e}")
    except Exception as e:
        print(f"Retry {retry_count + 1} 예외 발생: {e}")
    finally:
        if retry_count == num_retries - 1:
            print("재시도 완료")                  
