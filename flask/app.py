import os
from flask import Flask, request, render_template, jsonify

# Flask 애플리케이션 생성
app = Flask(__name__)

# 현재 Flask 애플리케이션 파일이 위치한 디렉토리를 기준으로 uploads 폴더 생성
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # uploads 폴더가 없으면 생성

# 파일 업로드 처리
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # 업로드된 파일 확인
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        # 파일 확장자 체크 (xlsm 또는 xlsx만 허용)
        if not file.filename.endswith((".xlsx", ".xlsm")):
            return jsonify({"error": "Invalid file type"}), 400

        # 파일 저장
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # 업로드 성공 메시지 반환
        return jsonify({"message": "File uploaded successfully", "path": file_path}), 200

    # GET 요청 시 index.html 렌더링
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
