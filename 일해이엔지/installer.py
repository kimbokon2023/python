## 새로운 로직개발 헤밍구조에 대한 통합버전 개발 쪽쟘, 멍텅구리 통합
## 실전 사용하면서 수정사항 반영 B1, B2 크기 조정 pyinstaller 실행 후 반영되는 값 적용
## 작지 양식 일부 수정 라이트케이스 크기 강제입력 부분 추가 24/03/05
## LED는 CD값이 1030인 경우는 기본 -100 처리 후 930이면 950으로, 즉 50단위로 생성해야 하는데, 30이면 30을 버리는 것이 아니라 50으로 만든다.

import math
import ezdxf
from ezdxf.enums import TextEntityAlignment
from datetime import datetime
import openpyxl
import os
import glob
import time
import os
import sys
import io
from datetime import datetime
import json
from gooey import Gooey, GooeyParser
import warnings
import re
import logging

from gooey import Gooey, GooeyParser
import os
import zipfile

@Gooey(program_name="Zip File Extractor")
def gui_app():
    parser = GooeyParser(description="Extract Zip File to Specified Folder")
    parser.add_argument('zip_file_path', widget='FileChooser', help="Select the zip file to extract")
    parser.add_argument('target_folder', widget='DirChooser', help="Select the folder to extract the zip file into")

    args = parser.parse_args()

    zip_folder(args.zip_file_path, args.target_folder)

def extract_zip_to_folder(zip_file_path, target_folder):
    # Create target folder if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(target_folder)

def zip_folder(folder_path, output_zip_file):
    with zipfile.ZipFile(output_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), 
                                           os.path.join(folder_path, '..')))


# To run the GUI app
gui_app()

