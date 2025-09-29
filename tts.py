# -*- coding: utf-8 -*-
import torch
import os
import scipy.io.wavfile # MMS 예제는 scipy 사용 (soundfile도 가능)
from transformers import AutoProcessor, MmsForConditionalGeneration

class MmsKoreanTTS:
    """
    Hugging Face Transformers를 사용하여 facebook/mms-tts-kor 모델 기반의
    한국어 Text-to-Speech(TTS) 시스템을 구현하는 클래스입니다.
    """
    def __init__(self, device=None):
        """
        MMS-TTS 시스템 초기화
        """
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        print(f"선택된 디바이스: {self.device}")
        model_id = "facebook/mms-tts-kor"
        print(f"{model_id} 모델과 프로세서를 로드합니다...")

        try:
            self.processor = AutoProcessor.from_pretrained(model_id)
            self.model = MmsForConditionalGeneration.from_pretrained(model_id).to(self.device)
            self.model.eval()
            # 모델 설정에서 샘플링 레이트 가져오기
            self.sampling_rate = self.model.config.sampling_rate
            print("MMS-TTS 모델 로딩 완료!")
            print(f"오디오 샘플링 레이트: {self.sampling_rate} Hz")

        except Exception as e:
            print(f"모델 로딩 중 오류 발생: {e}")
            print(f"'{model_id}' 모델이 허깅페이스 Hub에 존재하거나 접근 가능한지 확인하세요.")
            raise

    def text_to_speech(self, text, output_path="output_mms_kor.wav"):
        """
        주어진 텍스트를 한국어 음성으로 변환하여 오디오 파일로 저장합니다.

        Args:
            text (str): 음성으로 변환할 한국어 텍스트.
            output_path (str, optional): 생성된 오디오를 저장할 파일 경로.

        Returns:
            str: 성공적으로 생성된 오디오 파일의 경로.
        """
        print(f"텍스트를 음성으로 변환 시작 (MMS-TTS): '{text[:30]}...'")

        try:
            # 텍스트 처리
            inputs = self.processor(text=text, return_tensors="pt").to(self.device)

            # 음성 생성 (Waveform 직접 생성)
            with torch.no_grad():
                outputs = self.model.generate(**inputs)

            # NumPy 배열로 변환 (float32 형태)
            # outputs 텐서 구조 확인 필요 (보통 [1, sequence_length])
            audio_waveform = outputs.cpu().numpy().squeeze().astype(np.float32)

            # 출력 디렉토리 확인 및 생성
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                print(f"출력 디렉토리를 생성합니다: {output_dir}")
                os.makedirs(output_dir)

            # WAV 파일로 저장 (scipy 사용 예시)
            # scipy.io.wavfile.write는 정수형 데이터를 기대할 수 있으므로 스케일링 필요 시 주의
            # soundfile 사용 시: sf.write(output_path, audio_waveform, self.sampling_rate)
            scipy.io.wavfile.write(output_path, rate=self.sampling_rate, data=audio_waveform)
            print(f"음성 파일이 성공적으로 생성되었습니다: {output_path}")

            return output_path

        except Exception as e:
            print(f"MMS-TTS 음성 생성/저장 중 오류 발생: {e}")
            raise

# --- MMS-TTS 실행 예제 ---
if __name__ == "__main__":
    print("--- MMS-TTS 한국어 실행 예제 ---")
    output_dir_mms = "output_audio_mms"
    os.makedirs(output_dir_mms, exist_ok=True)

    try:
        mms_tts = MmsKoreanTTS()
        mms_tts.text_to_speech(
            "안녕하세요, 이것은 Meta의 MMS 한국어 음성 합성 모델 테스트입니다.",
            output_path=os.path.join(output_dir_mms, "mms_korean_test.wav")
        )
        mms_tts.text_to_speech(
            "허깅페이스 트랜스포머 라이브러리를 통해 쉽게 사용할 수 있습니다.",
            output_path=os.path.join(output_dir_mms, "mms_korean_test2.wav")
        )
        print("\nMMS-TTS 작업 완료.")

    except Exception as e:
        print(f"MMS-TTS 예제 실행 중 오류: {e}")

    print("\n=============================================\n")