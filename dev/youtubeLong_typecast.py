import os
import time
import json
import textwrap
import requests
from moviepy.editor import *
from moviepy.config import change_settings
from pygments import highlight
from pygments.lexers import JavascriptLexer
from pygments.formatters import ImageFormatter
from PIL import Image
import numpy as np # TextClip 높이 계산 위해 추가

# 기본 설정
WIDTH, HEIGHT = 1920, 1080
FONT_PATH = "C:/Windows/Fonts/HANSomaB.ttf"
API_TOKEN = "__plt4tj3EcRdrNaiX6vjui6k6Ycz4DQK8ioC3kCsoS5q" # 제공된 값 유지
ACTOR_ID = "5ecbbc7399979700087711db" # 제공된 값 유지
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_TOKEN}'
}
OUTPUT_DIR = "C:/shortsClip"

change_settings({
    "IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"
})

def ensure_folder(path): os.makedirs(path, exist_ok=True)
def sanitize_filename(name): return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()

# wrap_text: 지정된 너비로 텍스트 줄바꿈 (기존과 유사, 너비 조정 가능)
def wrap_text(text, width=40): # 너비를 줄여서 2줄 제한에 용이하게 함
    if not text: return ""
    return "\n".join(textwrap.wrap(text.strip(), width, drop_whitespace=False, replace_whitespace=False))

# split_text_into_chunks: 줄바꿈된 텍스트를 최대 max_lines 줄씩 자름
def split_text_into_chunks(wrapped_text, max_lines=2):
    lines = wrapped_text.split('\n')
    chunks = []
    for i in range(0, len(lines), max_lines):
        chunk = "\n".join(lines[i:min(i + max_lines, len(lines))])
        if chunk.strip(): # 빈 청크는 추가하지 않음
            chunks.append(chunk)
    # 청크가 없는 경우 (원본 텍스트가 매우 짧거나 공백일 때) 빈 문자열 하나를 포함하는 리스트 반환 방지
    if not chunks and wrapped_text.strip():
         return [wrapped_text.strip()] # 원본 텍스트를 그대로 사용
    return chunks if chunks else [" "] # 완전히 비었으면 공백 청크 하나 반환 (오류 방지)


def split_paragraphs(text):
    # 빈 줄을 포함하여 단락을 나눌 수 있도록 split('\n\n') 사용 유지
    # strip()을 통해 앞뒤 공백 제거
    paras = [p.strip() for p in text.strip().split('\n\n') if p.strip()]
    return paras

def split_code_lines(code):
    # 코드 라인 분할 (기존 유지)
    lines = [line for line in code.strip().split("\n")]
    return lines

def render_code_image(code_str, output_path="code_image.png"):
    # 코드 이미지 렌더링 (기존 유지)
    formatter = ImageFormatter(font_name='Consolas', font_size=36, line_numbers=False, style='monokai', image_pad=20)
    try:
        img_data = highlight(code_str, JavascriptLexer(), formatter)
        with open(output_path, "wb") as f:
            f.write(img_data)
    except Exception as e:
        print(f"⚠️ 코드 하이라이팅 중 오류 발생 (코드를 이미지로 저장): {e}")
        # 오류 발생 시 빈 이미지 생성 또는 다른 대체 처리 가능
        # 여기서는 일단 에러 로그만 남기고 진행
        img = Image.new("RGB", (100, 50), (0, 0, 0)) # 임시 검은 이미지
        img.save(output_path)


    # 이미지 리사이징 (기존 유지)
    try:
        img = Image.open(output_path)
        img_w, img_h = img.size
        target_w = 1600
        if img_w > target_w:
            ratio = target_w / img_w
            img = img.resize((target_w, int(img_h * ratio)), Image.Resampling.LANCZOS)
            img.save(output_path)
    except Exception as e:
        print(f"⚠️ 코드 이미지 리사이징 중 오류 발생: {e}")
        # 리사이징 실패해도 원본 이미지 사용

    return output_path

def make_solid_background(path="slide_bg.jpg", color=(28, 28, 28)):
    # 배경 생성 (기존 유지)
    img = Image.new("RGB", (WIDTH, HEIGHT), color)
    img.save(path)
    return path

def generate_tts_typecast(text, index):
    # TTS 생성 (기존 유지, 오류 처리 강화)
    if not text or not text.strip():
        print(f"⏭️ TTS 생략 (빈 텍스트): index {index}")
        return None, 0

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
    print(f"🎙️ TTS 요청 ({index}): {text[:30]}...")
    try:
        # --- 기존 TTS 요청 및 폴링 로직 ---
        response = requests.post("https://typecast.ai/api/speak", headers=HEADERS, data=json.dumps(payload), timeout=30) # 타임아웃 증가
        response.raise_for_status()
        result = response.json().get("result", {})
        speak_url = result.get("speak_v2_url")

        if not speak_url:
             print(f"❌ TTS 실패 (speak_url 없음): {response.text}")
             raise Exception("TTS speak_url not found")

        audio_url = None
        audio_length = 0
        for i in range(150): # 폴링 횟수/시간 증가 (최대 2.5분)
            poll_response = requests.get(speak_url, headers=HEADERS, timeout=15) # 폴링 타임아웃 증가
            # 404 에러는 speak_url이 만료되었거나 잘못된 경우 발생 가능 -> 실패 처리
            if poll_response.status_code == 404:
                 print(f"❌ TTS 실패 (Speak URL Not Found or Expired): {speak_url}")
                 raise Exception("TTS polling failed (404 Not Found)")
            poll_response.raise_for_status() # 다른 HTTP 오류 체크

            poll_result = poll_response.json().get("result", {})
            status = poll_result.get("status")

            if status == "done":
                audio_url = poll_result.get("audio_download_url")
                audio_length = poll_result.get("audio_length_ms", 0) / 1000.0
                if not audio_url:
                     print(f"❌ TTS 완료되었으나 다운로드 URL 없음: {poll_result}")
                     raise Exception("TTS audio_download_url not found though status is done")
                print(f"  [폴링 {i+1}] TTS 상태: {status}, URL 발견.")
                break
            elif status == "failed":
                 print(f"❌ TTS 실패 (상태: failed): {poll_result}")
                 error_msg = poll_result.get('error_message', 'Unknown error')
                 # 제한 초과 관련 에러 메시지 추가 확인
                 if "limit exceeded" in error_msg.lower():
                     print("🚫 TTS API 사용량 제한에 도달했을 수 있습니다.")
                 raise Exception(f"TTS generation failed: {error_msg}")
            # else: status == "progressing" or 다른 상태 -> 계속 폴링
            print(f"  [폴링 {i+1}] TTS 상태: {status}")
            time.sleep(1)
        else:
            print("❌ TTS 타임아웃 (폴링)")
            raise Exception("TTS polling timeout after 150 seconds")

        tts_path = f"tts_{index}.wav"
        print(f"⬇️ TTS 다운로드 시도: {audio_url}")
        audio_response = requests.get(audio_url, timeout=60) # 다운로드 타임아웃 증가
        audio_response.raise_for_status()

        if len(audio_response.content) == 0:
             print("❌ TTS 다운로드 실패 (파일 내용 없음)")
             raise Exception("Downloaded TTS file is empty")

        with open(tts_path, "wb") as f:
            f.write(audio_response.content)
        print(f"✅ TTS 저장 완료: {tts_path} (길이: {audio_length:.2f}s)")
        # 파일 크기 확인 (선택적)
        if os.path.getsize(tts_path) < 100: # 매우 작은 파일이면 문제 가능성
             print(f"⚠️ TTS 파일 크기가 매우 작습니다: {os.path.getsize(tts_path)} bytes")
        return tts_path, audio_length

    except requests.exceptions.Timeout:
         print(f"❌ TTS 요청/폴링/다운로드 시간 초과")
         raise
    except requests.exceptions.RequestException as e:
        print(f"❌ TTS 요청 오류: {e}")
        # 상태 코드에 따른 분기 가능 (e.g., 401 Unauthorized, 429 Too Many Requests)
        if e.response is not None:
             print(f"  - 상태 코드: {e.response.status_code}")
             print(f"  - 응답 내용: {e.response.text}")
        raise

# create_segment_slide 함수 수정
def create_segment_slide(text, code_line, index):
    segment_clips = []
    temp_files = []

    # 1. TTS 생성 시도 및 API 보고 길이 얻기
    tts_path, api_reported_duration = generate_tts_typecast(text, index)

    audio_clip = None
    actual_audio_duration = 0 # 실제 사용할 오디오 길이 (로드 후 결정)

    if tts_path: # TTS 경로가 있다면 (생성 시도 및 다운로드 성공)
        temp_files.append(tts_path) # 임시 파일 목록에 우선 추가
        try:
            # 파일을 AudioFileClip으로 로드 시도
            print(f"  ⏳ AudioFileClip 로드 시도: {tts_path}")
            audio_clip = AudioFileClip(tts_path)

            # 로드 성공 및 실제 길이 확인 (0.1초보다 커야 유효하다고 간주)
            if audio_clip and audio_clip.duration > 0.1:
                 actual_audio_duration = audio_clip.duration
                 print(f"  🔊 오디오 클립 로드 성공. 실제 길이: {actual_audio_duration:.2f}s (API 보고: {api_reported_duration:.2f}s)")
            else:
                 # 로드 실패했거나, 로드했어도 길이가 너무 짧음
                 print(f"⚠️ AudioFileClip 로드 실패 또는 실제 길이가 너무 짧음 (<0.1s). API 보고 길이: {api_reported_duration:.2f}s")
                 # 파일 크기 확인하여 단서 찾기
                 file_size = os.path.getsize(tts_path) if os.path.exists(tts_path) else 0
                 print(f"   - 파일 크기: {file_size} bytes")
                 if api_reported_duration == 0 and file_size < 1000: # API 길이 0이고 파일도 작으면 빈 파일 가능성 높음
                      print(f"   - API 길이 0, 파일 작음. 빈 오디오로 간주.")
                 # 실제 오디오 사용 불가 처리
                 audio_clip = None # audio_clip을 None으로 확실히 설정
                 actual_audio_duration = 0

        except Exception as e:
             print(f"❌ AudioFileClip 로드 중 오류 발생: {tts_path} - {e}")
             # 로드 중 에러 발생 시에도 오디오 사용 불가 처리
             audio_clip = None
             actual_audio_duration = 0

    # 실제 오디오 길이가 유효하지 않으면 기본 지속 시간 계산
    if actual_audio_duration <= 0.1:
        print(f"  🔇 유효한 오디오 없음. 기본 지속 시간 사용.")
        total_slide_duration = max(1.0, len(text.split()) * 0.20) # 단어당 0.2초, 최소 1초
        # audio_clip은 이미 None이거나 위에서 None으로 설정되었으므로 다시 할 필요 없음
    else:
        total_slide_duration = actual_audio_duration # 로드된 실제 오디오 길이 사용

    # 2. 기본 시각 요소 생성 (배경, 코드 이미지)
    # ... (기존 코드와 동일) ...
    bg_path = make_solid_background()
    code_img_path = f"code_{index}.png"
    code_img_clip = None # 초기화
    if code_line.strip():
        render_code_image(code_line, code_img_path)
        temp_files.append(code_img_path)
        # 코드 이미지 클립은 나중에 각 청크에서 생성/사용됨

    # 3. 자막 생성 및 분할
    # ... (기존 코드와 동일) ...
    wrapped_subtitle_text = wrap_text(text, width=35)
    subtitle_chunks = split_text_into_chunks(wrapped_subtitle_text, max_lines=2)
    if not subtitle_chunks: subtitle_chunks = [" "]
    num_chunks = len(subtitle_chunks)
    chunk_duration = total_slide_duration / num_chunks
    chunk_duration = max(0.5, chunk_duration) # 최소 지속 시간 보장

    current_time = 0
    for i, chunk in enumerate(subtitle_chunks):
        start_time = current_time
        # 마지막 청크는 전체 길이에 맞추기 (부동소수점 오차 방지)
        if i == num_chunks - 1:
            end_time = total_slide_duration
        else:
            end_time = start_time + chunk_duration

        actual_chunk_duration = end_time - start_time
        if actual_chunk_duration <= 0.01: continue # 매우 짧은 청크 건너뛰기

        # 각 청크에 대한 시각 요소 생성
        bg_clip_chunk = ImageClip(bg_path, ismask=False).resize((WIDTH, HEIGHT)).set_duration(actual_chunk_duration)

        if code_line.strip() and os.path.exists(code_img_path): # 코드 있고 이미지 파일 존재하면
             code_img_clip_chunk = ImageClip(code_img_path, ismask=False).set_position(("center", 100)).set_duration(actual_chunk_duration)
        else: # 코드가 없거나 이미지 파일이 없으면
             code_img_clip_chunk = ColorClip(size=(1, 1), color=(0,0,0), ismask=False).set_opacity(0).set_duration(actual_chunk_duration)

        # 자막 클립 생성
        subtitle_clip = TextClip(
            chunk.strip(),
            fontsize=60, color="whitesmoke", font=FONT_PATH,
            method="caption", align="center", stroke_color='black', stroke_width=2,
            size=(WIDTH * 0.85, None)
        ).set_position(("center", HEIGHT - 250)).set_duration(actual_chunk_duration)

        # 현재 청크의 최종 클립 합성
        composite_chunk = CompositeVideoClip(
            [bg_clip_chunk, code_img_clip_chunk, subtitle_clip],
            size=(WIDTH, HEIGHT)
        ).set_duration(actual_chunk_duration)

        # 첫 번째 청크이고 유효한 audio_clip이 있을 때만 오디오 연결
        if i == 0 and audio_clip: # audio_clip 객체가 유효할 때만 set_audio 시도
            print(f"  🎵 오디오 연결 (청크 {i+1}/{num_chunks})")
            composite_chunk = composite_chunk.set_audio(audio_clip)
        else:
             # 오디오가 없거나 첫번째 청크가 아니면 오디오를 None으로 설정 (중복 방지)
             composite_chunk = composite_chunk.set_audio(None)

        segment_clips.append(composite_chunk)
        current_time = end_time

    # 사용된 임시 파일 목록에서 tts_path를 최종적으로 정리 (실패 시 포함되지 않도록)
    final_temp_files = [f for f in temp_files if os.path.exists(f)]

    return segment_clips, final_temp_files


# 수정된 lesson 텍스트 (간결화 및 괄호 제거)
lesson = {
    "title": "자바스크립트 변수 완전정복 심화",
    "text": """
안녕하세요! 자바스크립트 변수의 세계, 함께 깊이 알아볼까요?
변수는 데이터를 저장하고 나중에 쓰기 위한 이름표, 즉 저장 공간입니다.

자바스크립트 변수는 주로 var, let, const 키워드로 선언합니다.
과거엔 var만 있었지만, ES6부터 let과 const가 등장했습니다.

var는 함수 스코프를 가집니다. 함수 안에서 선언하면 함수 전체에서 유효해요.
var는 같은 이름으로 여러 번 선언해도 괜찮습니다. 마지막 값으로 덮어쓰이죠.

var의 또 다른 특징은 호이스팅입니다. 선언문이 맨 위로 끌어올려진 것처럼 동작해요.
이때 값은 undefined로 초기화되어, 선언 전에 써도 에러 대신 undefined가 나옵니다.

var는 유연하지만 때론 버그를 만듭니다. 블록문 안의 var도 함수 전체에서 접근 가능하거든요.

그래서 let과 const가 나왔습니다. 이 둘은 블록 스코프를 가집니다.
중괄호 `{}` 블록 안에서만 유효해서, 변수 범위를 명확히 해줍니다.

let은 값을 다시 할당할 수 있는 변수를 선언할 때 씁니다.
하지만 같은 스코프에서 중복 선언은 안됩니다. 실수를 막아주죠.

let도 호이스팅되지만, 선언 전에는 접근할 수 없습니다.
이 구간을 TDZ라고 부릅니다. TDZ에서 변수를 쓰면 참조 에러가 발생해요.

const는 상수를 선언합니다. 한 번 값을 할당하면 재할당은 불가능해요.
const도 블록 스코프이고 TDZ의 영향을 받습니다. 선언 시 초기화는 필수입니다.

중요한 점! const는 재할당을 막는 것이지, 내부 값 변경까지 막는 건 아닙니다.
const로 선언한 객체나 배열의 내용은 변경할 수 있어요.

const 객체의 속성값 변경 예시입니다. 객체 자체를 바꾸진 못해도 속성은 바꿀 수 있죠.
const 배열에 새 요소를 추가하는 것도 가능합니다. 배열 자체가 바뀌는 게 아니에요.

그럼 뭘 써야 할까요? 요즘엔 var는 잘 쓰지 않습니다.
기본은 const! 불변성은 코드 복잡성을 줄이고 버그를 막는 데 좋습니다.

값이 바뀌어야 할 때만 let을 쓰세요. 반복문 카운터 변수처럼요.
let 사용은 최소화하는 것이 좋습니다. 꼭 필요한지 다시 생각해보세요.

변수 이름은 의미를 명확히 알 수 있게 지으세요. 모호한 이름은 피해주세요.
자바스크립트에서는 보통 카멜 케이스 명명 규칙을 따릅니다.

변수 스코프는 최대한 좁게 유지하세요. 넓게 쓰면 추적하기 어렵습니다.
특히 전역 변수는 충돌 위험이 있어 최소화해야 합니다.

자바스크립트는 동적 타입 언어입니다. 변수 타입을 미리 정하지 않아요.
같은 변수에 다른 타입의 값을 넣을 수 있어 유연하지만, 타입 오류에 주의해야 합니다.

선언 없이 변수에 값을 넣으면 어떻게 될까요? 위험할 수 있습니다.
엄격 모드('use strict')에서는 선언 없는 할당 시 에러를 발생시켜 안전합니다.

스코프 체인도 알아볼까요? 중첩 함수는 외부 함수의 변수에 접근할 수 있습니다.
변수를 찾을 때 현재 스코프부터 바깥으로 거슬러 올라가며 찾습니다.

클로저는 스코프와 관련된 중요 개념입니다. 함수가 선언될 때의 환경을 기억해요.
그래서 함수가 다른 곳에서 호출돼도 원래 환경의 변수에 접근할 수 있습니다.

변수와 메모리 관리도 관련 있습니다. 변수 선언 시 메모리가 할당됩니다.
더 이상 쓰지 않는 변수는 가비지 컬렉터가 자동으로 메모리를 해제합니다.

정리해볼까요? 변수는 var, let, const로 선언합니다. var는 함수 스코프입니다.
let과 const는 블록 스코프와 TDZ를 가집니다. let은 재할당 가능, const는 불가능.

최신 개발에서는 const를 기본으로, 필요할 때 let을 사용하세요. var는 피하고요.
의미있는 이름, 좁은 스코프, 전역 변수 최소화, 엄격 모드를 기억하세요.

자바스크립트 변수 심화 학습을 마칩니다. 기초이자 핵심이니 잘 활용해보세요.
다음 시간에는 데이터 타입에 대해 더 자세히 알아보겠습니다. 수고하셨습니다!
""",
    "code": """
// JavaScript Variable Deep Dive

// Variables are named storage for data.

// Keywords: var, let, const

// --- var (Function Scope) ---
function varScopeTest() {
  if (true) { var x = 10; }
  console.log(x); // 10
}
varScopeTest();
var name = "Alice";
var name = "Bob"; // Allowed
console.log(name); // Bob

// --- var Hoisting ---
console.log(hoistedVar); // undefined
var hoistedVar = 5;
// Behaves like: var hoistedVar; console.log(hoistedVar); hoistedVar = 5;

// --- Issues with var ---
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log("var loop:", i), 10); // Outputs 3, 3, 3
}
// 'i' is function-scoped, shared by all loops.

// --- let & const (Block Scope) ---
if (true) {
  let blockLet = "Inside"; // Only here
  const blockConst = "Also inside";
  console.log(blockLet);
}
// console.log(blockLet); // ReferenceError

// --- let (Reassignable) ---
let counter = 0;
counter = 1; // OK
// let counter = 2; // Error: Redeclaration

// --- Temporal Dead Zone (TDZ) ---
// console.log(tdzLet); // ReferenceError!
let tdzLet = "Initialized"; // TDZ ends here

// --- const (Not Reassignable) ---
const PI = 3.14;
// PI = 3.14159; // TypeError!
// const G; // Error: Needs initializer

// --- const: Mutating Object/Array ---
// The binding is constant, not the value inside.
const person = { name: "Charlie" };
person.name = "David"; // OK
console.log(person);
// person = {}; // TypeError!

const numbers = [1, 2];
numbers.push(3); // OK
console.log(numbers);
// numbers = [4, 5]; // TypeError!

// --- Best Practices ---
// Avoid var.

// Default to const.
const API_KEY = "secret";
const MAX_RETRIES = 3;

// Use let when needed.
let currentLevel = 1;
currentLevel++;
for (let j = 0; j < 2; j++) { // Loop counters
  console.log("let loop:", j); // Outputs 0, 1
}

// --- Naming: camelCase ---
let userScore = 100;
const defaultTimeoutMs = 5000;

// --- Minimize Scope ---
function calculate(value) {
  const factor = 0.5; // Local scope
  return value * factor;
}
// Avoid global variables.

// --- Dynamic Typing ---
let thing = 10; // Number
thing = "hello"; // String (OK)
thing = false; // Boolean (OK)

// --- Strict Mode ---
// Add 'use strict'; at the top.
// It prevents using undeclared variables.
// undeclared = 1; // Throws ReferenceError in strict mode

// --- Scope Chain ---
let outer = "Outer";
function func1() {
  let inner = "Inner";
  function func2() {
    console.log(outer); // Found in outer scope
    console.log(inner); // Found in intermediate scope
  }
  func2();
}
func1();

// --- Closure ---
// Function remembers its creation scope.
function makeAdder(x) {
  return function(y) { // This inner function is a closure
    return x + y; // Accesses 'x' from outer scope
  };
}
const add5 = makeAdder(5);
console.log(add5(3)); // 8

// --- Memory Management ---
// JS engine handles memory allocation/deallocation.
let data = { /* ... */ };
// Garbage Collector frees memory when 'data' is no longer reachable.
data = null;

// --- Summary: var ---
// Function scope, hoisting. Avoid.

// --- Summary: let & const ---
// Block scope, TDZ.
// let: Reassignable.
// const: Not reassignable (binding).

// --- Recommendations ---
// const first, then let if needed.
// Meaningful names, small scope.
// Use 'use strict';

// End of lesson.

// Next: Data Types.
"""
}

# main 함수 수정: create_segment_slide 반환값 처리
def main():
    start_time = time.time()
    ensure_folder(OUTPUT_DIR)
    print(f"🎬 비디오 생성 시작: {lesson['title']}")

    paragraphs = split_paragraphs(lesson["text"])
    code_lines = split_code_lines(lesson["code"])

    if len(paragraphs) != len(code_lines):
        print(f"⚠️ 경고: 텍스트 단락({len(paragraphs)})과 코드 라인({len(code_lines)}) 수가 다릅니다.")
        min_len = min(len(paragraphs), len(code_lines))
        paragraphs = paragraphs[:min_len]
        code_lines = code_lines[:min_len]

    all_slides = [] # 최종 비디오를 구성할 모든 (분할된) 슬라이드
    all_temp_files = []

    for i, (para, code_line) in enumerate(zip(paragraphs, code_lines)):
        print(f"\n⚙️ 원본 세그먼트 {i+1}/{len(paragraphs)} 처리 중...")
        try:
            # create_segment_slide는 이제 클립 리스트를 반환
            segment_clips, temp_files = create_segment_slide(para, code_line, i)
            if segment_clips: # 생성된 클립이 있을 경우에만 추가
                 all_slides.extend(segment_clips)
                 all_temp_files.extend(temp_files)
            else:
                 print(f"   -> 해당 세그먼트에서 생성된 클립 없음 (Index {i})")
        except Exception as e:
            print(f"❌ 세그먼트 {i+1} 처리 중 심각한 오류 발생: {e}")
            import traceback
            traceback.print_exc() # 상세 에러 스택 출력
            # 오류 발생 시 중단 또는 계속 진행 선택 가능
            # continue
            print("🛑 오류로 인해 비디오 생성을 중단합니다.")
            return # 오류 발생 시 중단

    if not all_slides:
        print("❌ 생성된 슬라이드가 없어 비디오를 만들 수 없습니다.")
        return

    print(f"\n🔗 총 {len(all_slides)}개의 슬라이드 클립 연결 중...")
    # 연결 전 각 클립의 유효성 검사 (선택적)
    valid_slides = []
    for idx, clip in enumerate(all_slides):
         if clip is None or clip.duration is None or clip.duration <= 0:
              print(f"   ⚠️ 유효하지 않은 클립 발견 (Index {idx}), 건너<0xEB><0x81>니다.")
         else:
              valid_slides.append(clip)

    if not valid_slides:
        print("❌ 유효한 슬라이드가 없어 비디오를 만들 수 없습니다.")
        return

    try:
        final_video = concatenate_videoclips(valid_slides, method="compose")
        print(f"   ➡️ 최종 비디오 길이: {final_video.duration:.2f} 초")
    except Exception as e:
         print(f"❌ 슬라이드 연결 중 오류 발생: {e}")
         # 연결 실패 시 개별 슬라이드 정보를 출력해보는 것이 도움될 수 있음
         # for idx, clip in enumerate(valid_slides):
         #      print(f"  - Clip {idx}: duration={clip.duration}, size={clip.size}, audio={clip.audio}")
         return


    filename = f"{sanitize_filename(lesson['title'])}.mp4"
    output_path = os.path.join(OUTPUT_DIR, filename)
    print(f"\n💾 최종 비디오 저장 중: {output_path}")
    # try:
    #     final_video.write_videofile(output_path,
    #                                 fps=24,
    #                                 codec='libx264',
    #                                 audio_codec='aac',
    #                                 temp_audiofile='temp-audio.m4a',
    #                                 remove_temp=True,
    #                                 threads=4, # 멀티 스레딩 사용 (CPU 코어 수에 맞게 조절)
    #                                 preset='medium' # 인코딩 속도와 품질 절충 (더 빠름: faster, veryfast)
    #                                )
    #     print(f"\n✅ 비디오 저장 완료: {output_path}")
    # except Exception as e:
    #     print(f"❌ 비디오 저장 실패: {e}")
    #     import traceback
    #     traceback.print_exc()


    print("\n🗑️ 임시 파일 정리 중...")
    cleaned_count = 0
    # 중복 제거 후 삭제 시도
    unique_temp_files = set(f for f in all_temp_files if f) # None 제거 및 중복 제거
    for f_path in unique_temp_files:
        if os.path.exists(f_path):
            try:
                os.remove(f_path)
                cleaned_count += 1
            except OSError as e:
                print(f"  - 임시 파일 삭제 실패: {f_path} ({e})")
        # else: # 파일이 이미 없으면 무시
        #     print(f"  - 임시 파일 이미 없음: {f_path}")

    print(f"  - {cleaned_count}개의 임시 파일 삭제 시도 완료.")


    if os.path.exists("slide_bg.jpg"):
      try:
          os.remove("slide_bg.jpg")
          print("  - 배경 이미지 파일 삭제 완료.")
      except OSError as e:
           print(f"  - 배경 이미지 파일 삭제 실패: {e}")

    end_time = time.time()
    print(f"\n⏱️ 총 소요 시간: {end_time - start_time:.2f} 초")

if __name__ == "__main__":
    main()