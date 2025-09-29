import os
import time
import requests
import re
import textwrap
import random
import gc
from moviepy.editor import (
    TextClip, ImageClip, CompositeVideoClip, ColorClip,
    concatenate_videoclips, AudioFileClip, CompositeAudioClip
)
from moviepy.config import change_settings

# 환경 설정
change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
font_path = "C:/Windows/Fonts/HANSomaB.ttf"
WIDTH, HEIGHT = 1080, 1920
BGM_FOLDER = "C:/music/bgm"
LOAD_IMAGE_FOLDER = "C:/shortsLoadPic"

# 유틸
def ensure_folder(path): os.makedirs(path, exist_ok=True)
def sanitize_filename(name): return re.sub(r'[\\/*?:"<>|]', "", name)
def wrap_text(text, width=20): return "\n".join(textwrap.wrap(text, width=width))
def split_sentences(text): return [s.strip() for s in re.split(r'[,.?!]\s+', text) if s.strip()]
def extract_keyword(sentence): return sentence.split()[0] if sentence else "배경"

# Typecast TTS 설정
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
        response = requests.post("https://typecast.ai/api/speak", headers=HEADERS, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Typecast 요청 오류: {e}")
        print(f"응답: {response.text}")
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
def create_slide(text, image_path, font_path=font_path, duration=4, index=0):
    if not os.path.exists(image_path):
        print(f"❌ 이미지 없음: {image_path}")
        return None, None

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
    트럼프 딸들의 후덜덜한 결혼 상대.
    이방카 남편 알고 보면 유대계 재벌이라는 거.
    하버드 출신에 뉴욕 주간지 전 소유주!
    그런데 더 소름 돋는 건 나이 24살에 아버지 기업 상속!
    그리고 순자산이 무려 1조 3천억 원 넘는다네요!
    이방카 아버지 트럼프가 그랬다죠.
    그는 천재다 내 최애 사위다!
    그런데 이방카만 그런 줄 아셨죠?
    트럼프의 두 번째 딸 티파니 트럼프는요,
    레바논계 아프리카 재벌의 아들과 결혼했어요.
    청혼 반지? 무려 18억 원짜리 다이아몬드!
    신랑은 런던대 졸업 아버지는 서아프리카 비즈니스 왕국의 수장!
    모델급 외모에 억만장자 남편까지?
    트럼프 딸들의 결혼 상대는.
    왕자보다 더 왕자네?
    이쯤 되면 사랑도 스펙이다?
    여러분 생각은 어떠세요?
    """

    sentences = split_sentences(input_text)
    slides, tts_paths = [], []

    for i, sentence in enumerate(sentences):
        image_path = os.path.join(LOAD_IMAGE_FOLDER, f"{i + 1}.jpg")
        clip, tts_path = create_slide(sentence, image_path, index=i)
        if clip:
            slides.append(clip)
            tts_paths.append(tts_path)

    if not slides:
        print("⚠️ 슬라이드 생성 실패")
        return

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

    # ✅ 배경음악 + TTS 믹싱
    bgm = get_random_bgm()
    if bgm:
        bgm = bgm.volumex(0.2).set_duration(final_video.duration)
        final_video = final_video.set_audio(CompositeAudioClip([final_video.audio, bgm]))

    save_path = "C:/shortsClip"
    ensure_folder(save_path)
    filename = sanitize_filename(sentences[0][:20]) + ".mp4"
    output = os.path.join(save_path, filename)
    final_video.write_videofile(output, fps=24)

    for f in tts_paths:
        try: os.remove(f)
        except: pass

    print(f"🎉 영상 저장 완료: {output}")

if __name__ == "__main__":
    main()
