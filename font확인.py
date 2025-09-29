import os
from PIL import ImageFont
import matplotlib.font_manager as fm

# Windows 기본 폰트 경로
font_folder = r"C:\Windows\Fonts"

# '가' 글자를 렌더링할 수 있는지 확인
def supports_korean(font_path):
    try:
        font = ImageFont.truetype(font_path, size=12)
        return font.getmask("가").getbbox() is not None
    except Exception:
        return False

# 해당 폴더 내 .ttf 파일만 대상으로 검사
korean_fonts = []
for font_path in fm.findSystemFonts(fontpaths=[font_folder], fontext='ttf'):
    if supports_korean(font_path):
        korean_fonts.append(font_path)

# 결과 출력 (파일명 + 전체 경로)
for path in korean_fonts:
    print(f"{os.path.basename(path)}  ←  {path}")
