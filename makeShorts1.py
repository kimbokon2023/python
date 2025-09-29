import os
import re
import textwrap
import requests
import random
import pyttsx3
import gc
from moviepy.editor import (
    TextClip, ImageClip, CompositeVideoClip, ColorClip,
    concatenate_videoclips, AudioFileClip, CompositeAudioClip
)
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

# 기본 설정
font_path = "C:/Windows/Fonts/HANSomaB.ttf"
WIDTH, HEIGHT = 1080, 1920
PIXABAY_API_KEY = "30559987-df2ee55eeb0cdbaef8ad520a5"
BGM_FOLDER = "C:/music/bgm"

def ensure_folder(path):
    os.makedirs(path, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def wrap_text(text, width=30):
    return "\n".join(textwrap.wrap(text, width=width))

def split_sentences(text):
    return [s.strip() for s in re.split(r'[.?!]\s+', text) if s.strip()]

def extract_keyword(sentence):
    return sentence.split()[0] if sentence else "배경"

def download_pixabay_image(search_query, api_key, save_path="default.jpg"):
    base_url = "https://pixabay.com/api/"
    params = {
        "key": api_key,
        "q": search_query,
        "image_type": "photo",
        "orientation": "vertical",
        "safesearch": "true",
        "per_page": 5,
        "lang": "ko"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "hits" in data and len(data["hits"]) > 0:
        image_url = data["hits"][0]["largeImageURL"]
        image_data = requests.get(image_url).content
        with open(save_path, "wb") as f:
            f.write(image_data)
        print(f"✅ 이미지 저장 완료: {save_path}")
        return save_path
    else:
        print("❌ 이미지 검색 결과가 없습니다.")
        return None

# 🔄 이미지 배경 효과
def apply_random_effect(image_clip, duration):
    effect_type = random.choice(["zoom_in", "zoom_out", "pan_left", "pan_right", "static"])
    if effect_type == "zoom_in":
        return image_clip.resize(lambda t: 1 + 0.05 * t).set_duration(duration)
    elif effect_type == "zoom_out":
        return image_clip.resize(lambda t: 1.2 - 0.05 * t).set_duration(duration)
    elif effect_type == "pan_left":
        return image_clip.set_position(lambda t: (-50 + 50 * t / duration, 0)).set_duration(duration)
    elif effect_type == "pan_right":
        return image_clip.set_position(lambda t: (50 - 50 * t / duration, 0)).set_duration(duration)
    else:
        return image_clip.set_duration(duration)

# 🗣️ TTS 생성
def generate_tts(text, index, voice_gender="male", lang="ko"):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voice_gender == "male":
        for v in voices:
            if "male" in v.name.lower() or "남성" in v.name:
                engine.setProperty('voice', v.id)
                break
    output_path = f"tts_{index}.wav"
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path

# 🎬 슬라이드 생성
def create_slide(text, image_path, font_path=font_path, duration=5, index=0):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"{image_path} 파일이 없습니다.")

    img_clip_raw = ImageClip(image_path).resize((WIDTH, HEIGHT))
    img_clip = apply_random_effect(img_clip_raw, duration)

    txt = TextClip(
        wrap_text(text),
        fontsize=90,
        font=font_path,
        color='white',
        stroke_color='black',
        stroke_width=3,
        method='caption',
        size=(WIDTH - 200, None),
        align='center'
    ).set_duration(duration)

    bar_height = txt.size[1] + 40
    bar = ColorClip(size=(WIDTH, bar_height), color=(0, 0, 0)).set_opacity(0.0).set_duration(duration)

    txt = txt.set_position(("center", HEIGHT - bar_height - 80))
    bar = bar.set_position(("center", HEIGHT - bar_height - 80))

    # 오디오 추가
    tts_path = generate_tts(text, index)
    audio_clip = AudioFileClip(tts_path)
    video = CompositeVideoClip([img_clip, bar, txt]).set_audio(audio_clip)
    video = video.set_duration(audio_clip.duration)

    return video, tts_path

# 🎞 전환 효과
def apply_transition(prev_clip, next_clip, transition_type):
    if transition_type == "crossfade":
        return prev_clip.crossfadeout(1), next_clip.crossfadein(1)
    elif transition_type == "fadeinout":
        return prev_clip.fadeout(1), next_clip.fadein(1)
    elif transition_type == "slide_right":
        next_slide = next_clip.set_start(prev_clip.duration - 1).set_position(lambda t: ('center', HEIGHT - t * 100))
        return prev_clip, next_slide
    elif transition_type == "slide_bottom":
        next_slide = next_clip.set_start(prev_clip.duration - 1).set_position(lambda t: ('center', HEIGHT + 50 - t * 200))
        return prev_clip, next_slide
    else:
        return prev_clip, next_clip

# 🎵 배경음악 랜덤 선택
def get_random_bgm():
    if not os.path.exists(BGM_FOLDER):
        return None
    files = [f for f in os.listdir(BGM_FOLDER) if f.lower().endswith(('.mp3', '.wav'))]
    if not files:
        return None
    bgm_path = os.path.join(BGM_FOLDER, random.choice(files))
    print(f"🎶 배경음악 삽입: {os.path.basename(bgm_path)}")
    return AudioFileClip(bgm_path)

# 🏁 메인
def main():
    input_text = """
    트럼프 소녀가 사치를 하지 않는이유. 트럼프의 아들인 배런이 황제의 삶을 누려온 반면 트럼프 소녀카이는 투박한 삶을 살고 있다고 합니다. 카이는 보통 일반 항공편을 이용하며 허스트 클래스를 거의 타지 않고 할아버지와 함께 여행할 때만 전용기를 이용한다고 밝혔죠. 이뿐만 아니라 내용 행사에 참석할 때는 59$ 이들에스와 245$ 하이의 신수입니다. 반면 배런이 어릴 적의 목욕을 마친 후 멜라니아는 그의 몸에 최고급 캐비어 크림을 발라주고 했다고 하죠. 또한 트럼프 타워에서는 한층 전체가 배런의 전용 공간으로 꾸며져 있었으며 그 공간은 마치 왕실에 공전처럼 화려하게 장식되어 있었습니다. 멜라니아는 배런을 첫 번째 상속자로 키우기 위해 엄격한 기대치를 설정했으며 그리고 이내 배런이 잡혜증을 가지고 있다고 오해받을 정도였습니다. 배런을 보며 카이는 더 자유롭게 사는 것을 선택한 것처럼 보이죠.
    """
    sentences = split_sentences(input_text)
    slides = []
    tts_files = []

    for i, sentence in enumerate(sentences):
        keyword = extract_keyword(sentence)
        image_path = f"bg_{i}.jpg"
        result = download_pixabay_image(keyword, PIXABAY_API_KEY, save_path=image_path)
        if result:
            clip, tts_path = create_slide(sentence, image_path, index=i)
            slides.append(clip)
            tts_files.append(tts_path)

    if not slides:
        print("⚠️ 영상 생성 실패: 슬라이드가 없습니다.")
        return

    # 전환 효과 적용
    final_clips = []
    for i in range(len(slides) - 1):
        transition = random.choice(["crossfade", "fadeinout", "slide_right", "slide_bottom", "none"])
        clip_a, clip_b = apply_transition(slides[i], slides[i + 1], transition)
        final_clips.append(clip_a)
        if transition != "none":
            clip_b = clip_b.set_start(clip_a.end)
        final_clips.append(clip_b)

    if len(slides) == 1:
        final_clips = slides
    elif len(final_clips) < len(slides):
        final_clips.append(slides[-1])

    final_video = concatenate_videoclips(final_clips, method="compose")

    # 🔈 배경음악 삽입
    bgm_clip = get_random_bgm()
    if bgm_clip:
        bgm = bgm_clip.volumex(0.3).set_duration(final_video.duration)
        final_video = final_video.set_audio(CompositeAudioClip([final_video.audio, bgm]))

    # 저장
    save_folder = "C:\\shortsClip"
    ensure_folder(save_folder)
    raw_title = sentences[0][:20] if sentences else "shorts_clip"
    safe_title = sanitize_filename(raw_title)
    output_path = os.path.join(save_folder, f"{safe_title}.mp4")
    final_video.write_videofile(output_path, fps=24)

    # 정리
    for f in tts_files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"파일 삭제 실패: {f} - {e}")

    del final_video
    gc.collect()

    print(f"🎉 영상 저장 완료: {output_path}")

if __name__ == "__main__":
    main()
