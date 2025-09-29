import torch
from transformers import AutoProcessor, AutoModel
import soundfile as sf
import os

# 출력 폴더 생성
os.makedirs("output", exist_ok=True)

# 메시지 출력
print("모델 로딩 중...")

# 프로세서와 모델 로드
processor = AutoProcessor.from_pretrained("suno/bark")
model = AutoModel.from_pretrained("suno/bark")

# 짧은 텍스트로 테스트
text = "안녕하세요"
print(f"'{text}' 변환 중...")

# 음성 생성
inputs = processor(text, voice_preset="ko_speaker_0")
audio_array = model.generate(**inputs)

# 변환 및 저장
audio_array = audio_array.cpu().numpy().squeeze()
output_path = "output/test.wav"
sf.write(output_path, audio_array, 24000)

print(f"파일이 저장되었습니다: {output_path}")