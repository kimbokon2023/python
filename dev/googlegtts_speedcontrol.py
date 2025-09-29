from gtts import gTTS
import os
from pydub import AudioSegment

# --- 1. gTTS로 오디오 파일 생성 ---

# 출력 폴더 생성
os.makedirs("c:\\output", exist_ok=True)

# 텍스트 정의 (한국어 또는 영어)
# text = "안녕하세요, 이것은 한국어 음성 생성 테스트입니다. 속도를 더 빠르게 조절해 보겠습니다."
text = "Hello, this is an English speech synthesis test. Let's try increasing the speed."
# text = "안녕하세요, 이것은 한국어 음성 생성 테스트입니다. 자연스러운 발음과 억양으로 이야기합니다."
lang_code = 'en' # 한국어는 'ko'
# lang_code = 'ko' 

# TTS 객체 생성 및 기본 속도로 저장
tts = gTTS(text=text, lang=lang_code)
original_path = f"c:\\output/gtts_{lang_code}_original.mp3"
tts.save(original_path)
print(f"원본 파일 생성 완료: {original_path}")

# --- 2. pydub으로 속도 조절 ---

# 속도 조절 배율 (1.0이 기본 속도, 1.2는 20% 빠르게, 1.5는 50% 빠르게)
speed_factor = 1

# 원본 오디오 파일 로드
try:
    sound = AudioSegment.from_mp3(original_path)
except Exception as e:
    print(f"오디오 파일 로딩 중 오류 발생: {e}")
    print("FFmpeg이 시스템에 설치되어 있고 PATH에 등록되어 있는지 확인하세요.")
    exit()


# 속도 변경 (pydub에는 직접적인 speedup 함수가 효과적이지 않을 수 있어, frame_rate 조절 방식을 사용)
# 참고: 이 방식은 피치(음높이)도 함께 변경될 수 있습니다.
# 피치 변경 없이 속도만 조절하려면 더 복잡한 알고리즘(예: Phase Vocoder)이나 외부 도구(ffmpeg 명령어 직접 사용)가 필요할 수 있습니다.
# pydub의 speedup 함수는 때때로 예상대로 작동하지 않거나 ffmpeg 기능에 의존합니다.
# 간단한 속도 증가를 위해 frame_rate를 직접 조절하는 방법을 시도해볼 수 있습니다.

# --- pydub의 speedup 함수 사용 (더 권장되는 방식) ---
# 이 함수는 내부적으로 ffmpeg의 atempo 필터를 사용하려고 시도합니다.
# playback_speed > 1.0 이면 빨라집니다.


# try:
#     fast_sound = sound.speedup(playback_speed=speed_factor)

#     # 속도를 조절한 오디오 파일 저장
#     fast_path = f"c:\\output/gtts_{lang_code}_fast_{speed_factor}x.mp3"
#     fast_sound.export(fast_path, format="mp3")

#     print(f"속도 조절된 파일 생성 완료: {fast_path} ({speed_factor}배속)")

# except Exception as e:
#      print(f"오디오 속도 조절 중 오류: {e}")
#      print("FFmpeg이 설치되어 있고 pydub에서 접근 가능한지 확인해주세요.")

# 사용 후 원본 파일 삭제 (선택 사항)
# os.remove(original_path)

# # gTTS 사용 예제 (Google TTS 기반이지만 설치가 간단함)
# from gtts import gTTS
# import os

# # 출력 폴더 생성
# os.makedirs("c:\\output", exist_ok=True)

# # 텍스트 정의
# text = "안녕하세요, 이것은 한국어 음성 생성 테스트입니다. 자연스러운 발음과 억양으로 이야기합니다."

# # TTS 객체 생성 및 음성 생성
# tts = gTTS(text=text, lang='ko')

# # 파일로 저장
# output_path = "c:\\output/ko_gtts_test.mp3"
# tts.save(output_path)

# print(f"파일이 생성되었습니다: {output_path}")


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