from yt_dlp import YoutubeDL
import urllib.parse

def get_channel_videos(channel_url):
    # /shorts 주소일 경우 /videos로 변환
    if "/shorts" in channel_url:
        channel_url = channel_url.split("/shorts")[0]

    ydl_opts = {
        'quiet': False,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        entries = info.get('entries', [])
        print(f"✅ 채널명: {urllib.parse.unquote(info.get('title', '제목없음'))}")
        print(f"총 영상 수: {len(entries)}")
        for i, entry in enumerate(entries, 1):
            print(f"{i:>3}. {entry.get('title')} - {entry.get('webpage_url')}")

# 테스트용 주소

url ="http://xhslink.com/a/vpfZPJuptx6ab"
# get_channel_videos("https://www.youtube.com/@%EB%AF%B8%EA%B5%AD%ED%98%95-x4u/shorts")
get_channel_videos(url)
