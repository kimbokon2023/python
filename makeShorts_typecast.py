import os
import time
import requests
import re
import textwrap
import random
import gc
import json
from moviepy.editor import (
    TextClip, ImageClip, CompositeVideoClip, ColorClip,
    concatenate_videoclips, AudioFileClip, CompositeAudioClip
)
from moviepy.config import change_settings

# 환경 설정
change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
font_path = "C:/Windows/Fonts/HANSomaB.ttf"
WIDTH, HEIGHT = 1080, 1920
PIXABAY_API_KEY = "30559987-df2ee55eeb0cdbaef8ad520a5"
BGM_FOLDER = "C:/music/bgm"

# 유틸
def ensure_folder(path): os.makedirs(path, exist_ok=True)
def sanitize_filename(name): return re.sub(r'[\\/*?:"<>|]', "", name)
def wrap_text(text, width=20): return "\n".join(textwrap.wrap(text, width=width))
def split_sentences(text): return [s.strip() for s in re.split(r'[,.?!]\s+', text) if s.strip()]
def extract_keyword(sentence): return sentence.split()[0] if sentence else "배경"

# Pixabay 이미지 다운로드 (오류 처리 추가)
def download_pixabay_image(search_query, api_key, save_path="default.jpg"):
    base_url = "https://pixabay.com/api/"
    params = {
        "key": api_key,
        "q": search_query,
        "image_type": "photo",
        "orientation": "vertical",
        "safesearch": "true",
        "per_page": 3,
        "lang": "ko"
    }
    response = requests.get(base_url, params=params)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ JSON 디코딩 실패 (응답 내용이 비어있거나 JSON 아님)")
        print(f"상태 코드: {response.status_code}")
        print(f"응답 본문: {response.text}")
        return None

    if "hits" in data and len(data["hits"]) > 0:
        image_url = data["hits"][0]["largeImageURL"]
        image_data = requests.get(image_url).content
        with open(save_path, "wb") as f:
            f.write(image_data)
        print(f"✅ 이미지 저장 완료: {save_path}")
        return save_path
    else:
        print("❌ 이미지 검색 결과 없음.")
        return None

# Typecast TTS
API_TOKEN = "__plt4tj3EcRdrNaiX6vjui6k6Ycz4DQK8ioC3kCsoS5q"
ACTOR_ID = "5ecbbc7399979700087711db"
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_TOKEN}'
}

def generate_tts_typecast(text, index):
    print(f"TTS 요청 중입니다... {text[:25]}")
    payload = {
        "actor_id": ACTOR_ID,
        "text": text,
        "lang": "auto",
        "tempo": 1,
        "volume": 100,
        "pitch": 0,
        "xapi_hd": True,
        "max_seconds": 60,
        "model_version": "latest",
        "xapi_audio_format": "wav"
    }

    try:
        response = requests.post("https://typecast.ai/api/speak", headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Typecast 요청 오류: {e}")
        try:
            print(f"응답: {response.text}")
        except:
            print("응답 본문을 출력할 수 없습니다.")
        raise Exception("TTS 요청 실패")

    result = response.json().get("result", {})
    speak_url = result.get("speak_v2_url")
    if not speak_url:
        raise Exception("TTS 응답 오류: speak_v2_url 없음")

    for _ in range(60):
        poll = requests.get(speak_url, headers=HEADERS)
        poll_data = poll.json().get("result", {})
        status = poll_data.get("status")
        if status == "done":
            audio_url = poll_data.get("audio_download_url")
            break
        elif status == "fail":
            raise Exception("TTS 생성 실패")
        time.sleep(1)
    else:
        raise Exception("TTS 타임아웃")

    if not audio_url:
        raise Exception("TTS 오디오 URL 없음")

    output_path = f"tts_{index}.wav"
    audio_response = requests.get(audio_url)
    with open(output_path, "wb") as f:
        f.write(audio_response.content)

    print(f"✅ TTS 저장 완료: {output_path}")
    return output_path

# 이미지 효과
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

# 슬라이드 생성
def create_slide(text, image_path, font_path=font_path, duration=5, index=0):
    img_clip = apply_random_effect(ImageClip(image_path).resize((WIDTH, HEIGHT)), duration)
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
    bar = ColorClip((WIDTH, bar_height), color=(0, 0, 0)).set_opacity(0.0).set_duration(duration)
    txt = txt.set_position(("center", HEIGHT - bar_height - 80))
    bar = bar.set_position(("center", HEIGHT - bar_height - 80))

    tts_path = generate_tts_typecast(text, index)
    audio_clip = AudioFileClip(tts_path)

    video = CompositeVideoClip([img_clip, bar, txt]).set_audio(audio_clip).set_duration(audio_clip.duration)
    return video, tts_path

# 전환 효과
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

# 배경음악
def get_random_bgm():
    if not os.path.exists(BGM_FOLDER): return None
    files = [f for f in os.listdir(BGM_FOLDER) if f.lower().endswith(('.mp3', '.wav'))]
    if not files: return None
    bgm_path = os.path.join(BGM_FOLDER, random.choice(files))
    print(f"🎶 배경음악 삽입: {os.path.basename(bgm_path)}")
    return AudioFileClip(bgm_path)

# 메인 실행
def main():
    input_text = """
    AI가 일자리를 뺏는다. 이제는 진짜 기술이 필요. 기술 없는 백수는 위험. 그중 가장 먼저 무너진 곳. 바로 코딩 학원이야. 코딩 학원이 왜 망했냐고? 수강생이 다 떨어져 나가. AI가 코딩까지 하거든. 근데 진짜 웃긴 건 뭔지? 그래도 코딩은 필수야. AI도 결국 코딩의 산물. 기초는 알아야 대응돼. 아예 못하면 진짜 끝이야. 코딩은 현대의 글쓰기. 안 하면 무기 없이 전쟁. 코딩 몰라도 됐던 시대. 이제는 다시 안 와. 머뭇대면 늦어. 지금부터라도 시작해. 코딩, 꼭 배워야 해.
    """
    sentences = split_sentences(input_text)
    slides, tts_paths = [], []

    for i, sentence in enumerate(sentences):
        keyword = extract_keyword(sentence)
        img_path = f"bg_{i}.jpg"
        if download_pixabay_image(keyword, PIXABAY_API_KEY, img_path):
            clip, tts_path = create_slide(sentence, img_path, index=i)
            slides.append(clip)
            tts_paths.append(tts_path)

    if not slides:
        print("⚠️ 슬라이드 생성 실패")
        return

    # 전환 적용
    final_clips = []
    for i in range(len(slides) - 1):
        transition = random.choice(["crossfade", "fadeinout", "slide_right", "slide_bottom", "none"])
        a, b = apply_transition(slides[i], slides[i + 1], transition)
        final_clips.append(a)
        if transition != "none": b = b.set_start(a.end)
        final_clips.append(b)

    if len(slides) == 1:
        final_clips = slides
    elif len(final_clips) < len(slides):
        final_clips.append(slides[-1])

    final_video = concatenate_videoclips(final_clips, method="compose")

    # 배경음악 추가
    bgm = get_random_bgm()
    if bgm:
        bgm = bgm.volumex(0.2).set_duration(final_video.duration)
        final_video = final_video.set_audio(CompositeAudioClip([final_video.audio, bgm]))

    # 저장
    save_path = "C:/shortsClip"
    ensure_folder(save_path)
    filename = sanitize_filename(sentences[0][:20]) + ".mp4"
    output = os.path.join(save_path, filename)
    final_video.write_videofile(output, fps=24)

    # 정리 만든파일 지우기
    # for f in tts_paths:
    #     try: os.remove(f)
    #     except: pass

    print(f"🎉 영상 저장 완료: {output}")

if __name__ == "__main__":
    main()
