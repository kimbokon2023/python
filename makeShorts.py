import os
import re
import textwrap
import requests
import random
from moviepy.editor import TextClip, ImageClip, CompositeVideoClip, ColorClip, concatenate_videoclips
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

font_path = "C:/Windows/Fonts/HANSomaB.ttf"
WIDTH, HEIGHT = 1080, 1920
PIXABAY_API_KEY = "30559987-df2ee55eeb0cdbaef8ad520a5"

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

# 🔄 랜덤 효과 함수 정의
def apply_random_effect(image_clip, duration):
    effect_type = random.choice(["zoom_in", "zoom_out", "pan_left", "pan_right", "static"])

    if effect_type == "zoom_in":
        return image_clip.resize(lambda t: 1 + 0.05 * t).set_duration(duration)
    elif effect_type == "zoom_out":
        return image_clip.resize(lambda t: 1.2 - 0.05 * t).set_duration(duration)
    elif effect_type == "pan_left":
        return image_clip.set_position(lambda t: (int(-50 + 50 * t / duration), 0)).set_duration(duration)
    elif effect_type == "pan_right":
        return image_clip.set_position(lambda t: (int(50 - 50 * t / duration), 0)).set_duration(duration)
    else:  # static
        return image_clip.set_duration(duration)

# 🎬 슬라이드 생성 함수
def create_slide(text, image_path, font_path=font_path, duration=4):
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

    return CompositeVideoClip([img_clip, bar, txt])

# 🏁 메인 실행
def main():
    input_text = """
    트럼프의 비행기는 절대 사고나지 않는 일. 트럼프는 대통령이 되기 전 트럼프포스 원이라는 별명이 붙은 전용기를 타고 다녔습니다. 2025년 그가 제선의 성공함으로써 미국 공군 이룩인 에어포스 원을 타게 되었죠. 미국 대통령들만 탈 수 있는 에어포스 원은 사고가 나기 힘듭니다. 발은 어떤 항공기보다 더 높이 비행하며 F16 전투기만큼 빠르고 핵 공격시에는 방어를 해주는 번코도 장착되어 있기 때문이죠. 실제로 911테로 당시 워싱턴으로 에어포스 원을 호의했던 F16 조종사중 한 명은 에어포스 원을 따라잡기 위해 속도를 높여야 했다고 말했습니다. 또한 에어포스 원은 너무나도 안전하기 때문에 평상시에는 전투기 호의를 받지 않는다고 합니다. 전투기와 함께 비행하는 경우는 911테로 같은 위기 상황이거나 행사를 할 때라고 하네요.
    """

    sentences = split_sentences(input_text)
    clips = []

    for i, sentence in enumerate(sentences):
        keyword = extract_keyword(sentence)
        image_path = f"bg_{i}.jpg"
        result = download_pixabay_image(keyword, PIXABAY_API_KEY, save_path=image_path)
        if result:
            clip = create_slide(sentence, image_path)
            clips.append(clip)

    if clips:
        save_folder = "C:\\shortsClip"
        ensure_folder(save_folder)

        raw_title = sentences[0][:20] if sentences else "shorts_clip"
        safe_title = sanitize_filename(raw_title)
        output_path = os.path.join(save_folder, f"{safe_title}.mp4")

        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(output_path, fps=24)

        print(f"🎉 영상 저장 완료: {output_path}")
    else:
        print("⚠️ 영상 생성에 실패했습니다.")

if __name__ == "__main__":
    main()
