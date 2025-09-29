from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
import whisper
import yt_dlp
import os

# ---------- 설정 ----------
VIDEO_URL = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
TEMP_VIDEO_FILE = "temp_video.mp4"
TEMP_AUDIO_FILE = "temp_audio.mp3"
TEMP_WAV_FILE = "temp_audio.wav"
FINAL_OUTPUT = "output_short.mp4"
BGM_FILE = "bgm.mp3"  # BGM 삽입할 경우

# ---------- 유튜브 영상 다운로드 ----------
def download_video(url, filename):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': filename,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# ---------- 오디오 추출 ----------
def extract_audio(filename, output_audio):
    os.system(f"ffmpeg -y -i {filename} -vn -acodec libmp3lame -ar 44100 -ac 2 -ab 192k -f mp3 {output_audio}")

# ---------- Whisper 자막 추출 ----------
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language='ko')
    return result['segments']  # segment별로 시간 포함

# ---------- 자막 클립 생성 ----------
def create_captioned_clips(video_path, segments, bgm_path=None):
    clips = []
    video = VideoFileClip(video_path)
    for segment in segments:
        start = segment['start']
        end = segment['end']
        text = segment['text'].strip()
        if end - start < 0.5:
            continue
        sub_video = video.subclip(start, end)
        subtitle = TextClip(text, fontsize=40, color='white', bg_color='black', size=sub_video.size)
        subtitle = subtitle.set_position(("center", "bottom")).set_duration(sub_video.duration)
        clip = CompositeVideoClip([sub_video, subtitle])
        clips.append(clip)
    final = concatenate_videoclips(clips)
    if bgm_path and os.path.exists(bgm_path):
        audio = AudioFileClip(bgm_path).subclip(0, final.duration).volumex(0.3)
        final = final.set_audio(audio)
    return final

# ---------- 실행 ----------
download_video(VIDEO_URL, TEMP_VIDEO_FILE)
extract_audio(TEMP_VIDEO_FILE, TEMP_AUDIO_FILE)
segments = transcribe_audio(TEMP_AUDIO_FILE)
final_clip = create_captioned_clips(TEMP_VIDEO_FILE, segments, bgm_path=BGM_FILE)
final_clip.write_videofile(FINAL_OUTPUT, fps=24)

# ---------- 정리 ----------
os.remove(TEMP_VIDEO_FILE)
os.remove(TEMP_AUDIO_FILE)
