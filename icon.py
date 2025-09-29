from PIL import Image

# WEBP 파일 열기
webp_image = Image.open(r"c:\python\icon.webp")  # 경로에서 '\' 대신 'r'로 처리

# 이미지 크기 조정 (128x128)
resized_image = webp_image.resize((128, 128))

# 크기 조정된 이미지를 PNG로 저장
resized_image.save(r"c:\python\icon.png", "PNG")
