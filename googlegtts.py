# gTTS 사용 예제 (Google TTS 기반이지만 설치가 간단함)
from gtts import gTTS
import os

# 출력 폴더 생성
os.makedirs("c:\\output", exist_ok=True)

# 텍스트 정의
text = "안녕하세요, 이것은 한국어 음성 생성 테스트입니다. 자연스러운 발음과 억양으로 이야기합니다."

# TTS 객체 생성 및 음성 생성
tts = gTTS(text=text, lang='ko')

# 파일로 저장
output_path = "c:\\output/ko_gtts_test.mp3"
tts.save(output_path)

print(f"파일이 생성되었습니다: {output_path}")


# # 출력 폴더 생성
# os.makedirs("c:\output", exist_ok=True)

# # 영어 텍스트 정의
# text = "Hello, this is a test of English speech synthesis using gTTS. It speaks with a relatively natural pronunciation and intonation."

# # TTS 객체 생성 (언어를 'en'으로 설정)
# tts = gTTS(text=text, lang='en')

# # 파일로 저장
# output_path = "c:\\output/gtts_english_test.mp3"
# tts.save(output_path)

# print(f"English audio file created: {output_path}")