# -*- coding: utf-8 -*-
import torch
import os
import soundfile as sf # SpeechT5 예제는 soundfile 사용
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset # 스피커 임베딩 로드용
import numpy as np

class SpeechT5KoreanTTS:
    """
    Hugging Face Transformers를 사용하여 microsoft/speecht5_tts 모델 기반의
    한국어 Text-to-Speech(TTS) 시스템을 구현하는 클래스 (한국어 스피커 임베딩 필요).
    """
    def __init__(self, device=None, speaker_embedding_path=None):
        """
        SpeechT5 TTS 시스템 초기화

        Args:
            device (str, optional): 실행 디바이스.
            speaker_embedding_path (str or tuple, optional):
                한국어 스피커 임베딩 파일(.pt, .npy) 경로 또는
                허깅페이스 datasets 라이브러리로 로드할 (dataset_id, speaker_id) 튜플.
                None이면 기본 (영어) 임베딩 로드를 시도합니다.
        """
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        print(f"선택된 디바이스: {self.device}")
        model_id = "microsoft/speecht5_tts"
        vocoder_id = "microsoft/speecht5_hifigan"
        print(f"{model_id} 모델, 프로세서, 보코더({vocoder_id})를 로드합니다...")

        try:
            self.processor = SpeechT5Processor.from_pretrained(model_id)
            self.model = SpeechT5ForTextToSpeech.from_pretrained(model_id).to(self.device)
            self.vocoder = SpeechT5HifiGan.from_pretrained(vocoder_id).to(self.device)
            self.model.eval()
            self.vocoder.eval()
            # 보코더에서 샘플링 레이트 가져오기 (보통 16000Hz)
            self.sampling_rate = self.vocoder.config.sampling_rate
            print("SpeechT5 모델 로딩 완료!")
            print(f"오디오 샘플링 레이트: {self.sampling_rate} Hz")

            # --- 스피커 임베딩 로드 ---
            self.speaker_embeddings = self._load_speaker_embedding(speaker_embedding_path)

        except Exception as e:
            print(f"SpeechT5 관련 요소 로딩 중 오류 발생: {e}")
            raise

    def _load_speaker_embedding(self, path_or_id):
        """ 스피커 임베딩 로드 (파일 또는 datasets 라이브러리) """
        if path_or_id is None:
            print("경고: 스피커 임베딩 경로가 제공되지 않았습니다. 기본 CMU ARCTIC 영어 임베딩(spk_id=7306)을 로드합니다.")
            print("한국어 음성을 원하시면, 한국어 화자의 스피커 임베딩을 찾아서 'speaker_embedding_path' 인자로 제공해야 합니다.")
            try:
                # 허깅페이스 datasets에서 영어 예시 로드
                embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
                # 예시 스피커 ID (변경 가능)
                speaker_id_idx = 7306
                embedding = torch.tensor(embeddings_dataset[speaker_id_idx]["xvector"]).unsqueeze(0).to(self.device)
                print(f"기본 영어 스피커 임베딩 로드 완료 (Index: {speaker_id_idx}).")
                return embedding
            except Exception as e:
                print(f"기본 영어 임베딩 로드 실패: {e}")
                print("스피커 임베딩 없이 진행할 수 없습니다.")
                raise ValueError("스피커 임베딩 로드 실패")

        elif isinstance(path_or_id, str): # 파일 경로인 경우
            print(f"파일에서 스피커 임베딩 로드 중: {path_or_id}")
            if path_or_id.endswith(".pt"):
                embedding = torch.load(path_or_id).unsqueeze(0).to(self.device)
            elif path_or_id.endswith(".npy"):
                embedding = torch.from_numpy(np.load(path_or_id)).unsqueeze(0).to(self.device)
            else:
                raise ValueError("지원하지 않는 임베딩 파일 형식입니다 (.pt 또는 .npy 사용).")
            print("파일 스피커 임베딩 로드 완료.")
            return embedding

        elif isinstance(path_or_id, tuple) and len(path_or_id) == 2: # (dataset_id, speaker_id) 형태
             dataset_id, speaker_id = path_or_id
             print(f"Hugging Face Dataset '{dataset_id}'에서 스피커 ID '{speaker_id}' 임베딩 로드 중...")
             try:
                 # 실제 데이터셋 구조에 따라 키('xvector', 'embedding' 등)와 ID 형식이 다를 수 있음
                 embeddings_dataset = load_dataset(dataset_id, split="validation") # 또는 다른 split
                 # speaker_id가 인덱스인지, 아니면 특정 필드 값인지 확인 필요
                 # 예시: speaker_id가 인덱스인 경우
                 # embedding = torch.tensor(embeddings_dataset[int(speaker_id)]["xvector"]).unsqueeze(0).to(self.device)
                 # 예시: speaker_id가 'speaker_name' 필드 값인 경우 (데이터셋을 필터링해야 함)
                 # speaker_data = embeddings_dataset.filter(lambda example: example["speaker_name"] == speaker_id)
                 # if len(speaker_data) == 0: raise ValueError(f"Speaker ID '{speaker_id}' not found in dataset.")
                 # embedding = torch.tensor(speaker_data[0]["xvector"]).unsqueeze(0).to(self.device)

                 # **이 부분은 사용할 한국어 임베딩 데이터셋의 정확한 구조에 맞게 수정해야 합니다.**
                 raise NotImplementedError("실제 한국어 임베딩 데이터셋 로직을 구현해야 합니다.")

             except Exception as e:
                 print(f"Dataset '{dataset_id}' 또는 Speaker ID '{speaker_id}' 처리 중 오류: {e}")
                 raise ValueError("지정된 Dataset/Speaker ID로 임베딩 로드 실패")
        else:
             raise ValueError("잘못된 speaker_embedding_path 형식입니다.")


    def text_to_speech(self, text, output_path="output_speecht5_kor.wav"):
        """
        주어진 텍스트를 한국어 음성으로 변환하여 오디오 파일로 저장합니다.
        로드된 스피커 임베딩을 사용합니다.

        Args:
            text (str): 음성으로 변환할 한국어 텍스트.
            output_path (str, optional): 생성된 오디오를 저장할 파일 경로.

        Returns:
            str: 성공적으로 생성된 오디오 파일의 경로.
        """
        print(f"텍스트를 음성으로 변환 시작 (SpeechT5): '{text[:30]}...'")

        if self.speaker_embeddings is None:
             raise RuntimeError("TTS를 생성하기 전에 유효한 스피커 임베딩이 로드되어야 합니다.")

        try:
            # 텍스트 처리
            inputs = self.processor(text=text, return_tensors="pt").to(self.device)

            # 스펙트로그램 생성
            with torch.no_grad():
                spectrogram = self.model.generate_speech(inputs["input_ids"], self.speaker_embeddings)

            # 보코더를 사용하여 스펙트로그램을 음성 파형으로 변환
            with torch.no_grad():
                audio_waveform = self.vocoder(spectrogram).cpu().numpy().squeeze()

            # 출력 디렉토리 확인 및 생성
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                print(f"출력 디렉토리를 생성합니다: {output_dir}")
                os.makedirs(output_dir)

            # WAV 파일로 저장 (soundfile 사용)
            sf.write(output_path, audio_waveform, self.sampling_rate)
            print(f"음성 파일이 성공적으로 생성되었습니다: {output_path}")

            return output_path

        except Exception as e:
            print(f"SpeechT5 음성 생성/저장 중 오류 발생: {e}")
            raise

# --- SpeechT5 실행 예제 ---
if __name__ == "__main__":
    # 이 부분은 계속 실행됩니다.
    print("--- SpeechT5 한국어 실행 예제 ---")
    output_dir_s5 = "output_audio_speecht5"
    os.makedirs(output_dir_s5, exist_ok=True)

    try:
        # ** 중요: 한국어 음성을 위해서는 아래 speaker_embedding_path 인자에
        #    찾아낸 한국어 스피커 임베딩 경로('.pt' 또는 '.npy') 또는
        #    (데이터셋 ID, 스피커 ID) 튜플을 제공해야 합니다.
        #    None으로 두면 기본 영어 목소리(경고와 함께)로 생성됩니다. **

        # 예시 1: 기본 영어 목소리 사용 (경고 발생)
        s5_tts_en = SpeechT5KoreanTTS(speaker_embedding_path=None)
        s5_tts_en.text_to_speech(
            "This is a test using the default English speaker embedding.",
            output_path=os.path.join(output_dir_s5, "speecht5_default_english.wav")
        )

        # 예시 2: 한국어 임베딩 파일이 있다고 가정 ('./korean_speaker_embedding.pt' 경로)
        # korean_embedding_file = "korean_speaker_embedding.pt" # 실제 파일 경로로 변경
        # if os.path.exists(korean_embedding_file):
        #     print(f"\n'{korean_embedding_file}' 파일을 사용하여 한국어 목소리 생성 시도...")
        #     s5_tts_ko = SpeechT5KoreanTTS(speaker_embedding_path=korean_embedding_file)
        #     s5_tts_ko.text_to_speech(
        #         "이것은 한국어 스피커 임베딩을 사용한 테스트입니다.",
        #         output_path=os.path.join(output_dir_s5, "speecht5_korean_from_file.wav")
        #     )
        # else:
        #     print(f"\n경고: 한국어 임베딩 파일 '{korean_embedding_file}'을 찾을 수 없습니다. 한국어 테스트를 건너<0xEB><0x9A><0x8D>니다.")

        print("\nSpeechT5 작업 완료 (한국어 임베딩 제공 여부에 따라 결과 다름).")

    except Exception as e:
        print(f"SpeechT5 예제 실행 중 오류: {e}")