# 일해이엔지 판넬 자동프로그램 시작

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
import tkinter as tk
from tkinter import messagebox

# 전역 변수 초기화
drawdate_str = ""
thickness = 0
T5_is =""
OP = 0
OPH = 0
KPH = 0
TRH = 0
br = 0   # bending rate 연신율

saved_DimXpos = 0
saved_DimYpos = 0
saved_Xpos = 0
saved_Ypos = 0
saved_direction = "up"
saved_text_height = 0.28
saved_text_gap = 0.05
dimdistance = 0
dim_horizontalbase = 0
dim_verticalbase = 0
distanceXpos = 0
distanceYpos = 0
start_time = 0
secondord = None
drawdate_str = None
company = None
workplace = None
drawnby = None
issuedate = None
usage = None
openType = None
person = None
SU = None
carOP = None
carOPH = None
KH = None
FH = None
Material = None
Spec = None
thickness_string = None
Vcut = None
doorDevice = None
CW = None
CD = None
CH = None
popnut_height = None
CPH = None
SIDE = None
REAR = None
WF = None
WS = None
WSM = None
WR = None
WRM = None
trimMaterial = None
TR1 = None
TR2 = None
TR3 = None
TR4 = None
TR5 = None
TR6 = None
P1_material, P1_width, P1_widthReal, P1_holegap, P1_hole1, P1_hole2, P1_hole3, P1_hole4, P1_COPType = None,None,None,None,None,None,None,None,None
P2_material, P2_width, P2_widthReal, P2_holegap, P2_hole1, P2_hole2, P2_hole3, P2_hole4, P2_COPType= None,None,None,None,None,None,None,None,None
P3_material, P3_width, P3_widthReal, P3_holegap, P3_hole1, P3_hole2, P3_hole3, P3_hole4, P3_COPType= None,None,None,None,None,None,None,None,None
P4_material, P4_width, P4_widthReal, P4_holegap, P4_hole1, P4_hole2, P4_hole3, P4_hole4, P4_COPType= None,None,None,None,None,None,None,None,None
P5_material, P5_width, P5_widthReal, P5_holegap, P5_hole1, P5_hole2, P5_hole3, P5_hole4, P5_COPType= None,None,None,None,None,None,None,None,None
P6_material, P6_width, P6_widthReal, P6_holegap, P6_hole1, P6_hole2, P6_hole3, P6_hole4, P6_COPType= None,None,None,None,None,None,None,None,None
P7_material, P7_width, P7_widthReal, P7_holegap, P7_hole1, P7_hole2, P7_hole3, P7_hole4, P7_COPType= None,None,None,None,None,None,None,None,None
P8_material, P8_width, P8_widthReal, P8_holegap, P8_hole1, P8_hole2, P8_hole3, P8_hole4, P8_COPType= None,None,None,None,None,None,None,None,None
P9_material, P9_width, P9_widthReal, P9_holegap, P9_hole1, P9_hole2, P9_hole3, P9_hole4, P9_COPType= None,None,None,None,None,None,None,None,None
P10_material, P10_width, P10_widthReal, P10_holegap, P10_hole1, P10_hole2, P10_hole3, P10_hole4, P10_COPType= None,None,None,None,None,None,None,None,None
P11_material, P11_width, P11_widthReal, P11_holegap, P11_hole1, P11_hole2, P11_hole3, P11_hole4, P11_COPType= None,None,None,None,None,None,None,None,None
COP_bottomHeight=None
COP_centerdistance=None
COP_width=None
COP_height=None
COP_holegap=None
COP_RibType=None
HOP_bottomHeight=None
HOP_width=None
HOP_height=None
HOP_holegap=None
HOP_RibType=None
HRType=None
handrail_height=None
handrailSidegap1=None
handrailSidegap2=None
handrailSidegap3=None
handrailSidegap4=None
handrailSidegap5=None
HRFrontHolesize=None
handrailReargap1=None
handrailReargap2=None
handrailReargap3=None
handrailReargap4=None
handrailReargap5=None
HRRearHolesize=None
KP_material=None
TR_OP=None
TR_TRH=None
TR_upperhole1=None
TR_upperhole2=None
TR_upperhole3=None
TR_upperhole4=None
TR_material=None
CPIType=None
CPIHoleWidth=None
CPIHoleHeight=None
CPIholegap=None
CPIHeight=None
updateCPIHoleWidth=None
updateCPIHoleHeight=None
updateCPIholegap=None
updateCPIHeight=None
COL_Height=None
column_thickness=None
column_width=None
COL_FH=None
COL_Material=None
column_BottomHoleHorizontal=None
column_BottomHoleVertical=None
ELB_BottomHeight=None
ELB_BoxHorizontal=None
ELB_BoxVertical=None
ELB_RibType=None
CartP_Type=None       
CartP_Height=None
CartP_holegap1=None
CartP_holegap2=None
CartP_holegap3=None
CartP_holegap4=None
CartP_holegap5=None
CartP_HoleSize=None
panel_width=None

P1_width,  P1_height  = 0,0
P2_width,  P2_height  = 0,0
P3_width,  P3_height  = 0,0
P4_width,  P4_height  = 0,0
P5_width,  P5_height  = 0,0
P6_width,  P6_height  = 0,0
P7_width,  P7_height  = 0,0
P8_width,  P8_height  = 0,0
P9_width,  P9_height  = 0,0
P10_width, P10_height = 0,0
P11_width, P11_height = 0,0

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')    

# 경고 메시지 필터링
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.worksheet._reader")

# 폴더 내의 모든 .xlsm 파일을 검색
application_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
# excel_saved_file = os.path.join(application_path, 'panel_excel')
# xlsm_files = glob.glob(os.path.join(excel_saved_file, '*.xlsm'))
# 절대 경로를 지정
excel_saved_file = 'c:/panel/excel파일'
xlsm_files = glob.glob(os.path.join(excel_saved_file, '*.xlsm'))
license_file_path = os.path.join(application_path, 'data', 'hdsettings.json') # 하드디스크 고유번호 인식




# DXF 파일 로드
# doc = ezdxf.readfile(os.path.join(application_path, 'dimstyle', 'style1.dxf'))
doc = ezdxf.readfile(os.path.join(application_path, 'dimstyle', 'miraestyle.dxf'))
msp = doc.modelspace()

# TEXTSTYLE 정의
text_style_name = 'JKW'  # 원하는 텍스트 스타일 이름
if text_style_name not in doc.styles:
    text_style = doc.styles.new(
        name=text_style_name,
        dxfattribs={
            'font': 'Arial.ttf',  # TrueType 글꼴 파일명            
        }
    )
else:
    text_style = doc.styles.get(text_style_name)    


def save_file(company, workplace, CW, CD):
    # 현재 시간 가져오기
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    # 파일 이름에 사용할 수 없는 문자 정의
    invalid_chars = '<>:"/\\|?*'
    # 정규식을 사용하여 유효하지 않은 문자 제거
    cleaned_file_name = re.sub(f'[{re.escape(invalid_chars)}]', '', f"{company}_{workplace}_CW{CW}xCD{CD}_{current_time}")

    # 결과 파일이 저장될 디렉토리
    output_directory = "c:/panel/작업완료"

    # 디렉토리가 존재하지 않으면 생성
    os.makedirs(output_directory, exist_ok=True)

    # 결과 파일 이름
    file_name = f"{cleaned_file_name}.dxf"
    # 전체 파일 경로 생성
    full_file_path = os.path.join(output_directory, file_name)

    # 파일 경로 반환
    return full_file_path    

def page_comment(mx, my) :
    line(doc, mx,my, mx+250, my ,layer='1')                
    line(doc, mx,my-16, mx+250, my-16 ,layer='0')                
    line(doc, mx,my-16-107 , mx+1100, my-16-107 ,layer='1')                
    line(doc, mx,my-16-107-107, mx+1100, my-16-107*2 ,layer='1')                
    line(doc, mx,my-16-107-107-107 , mx+1100, my-16-107*3 ,layer='1')                
    line(doc, mx,my-16-107-107-107-107, mx+1100, my-16-107*4 ,layer='1')                
    text = f"작업 주기"
    draw_Text(doc, mx, my+30, 35, text, layer='0')    
    text = f"1. 본 도면은 WH={CPH} 으로 도시됨."
    draw_Text(doc, mx, my+30-107, 35, text, layer='0')    
    text = f"2. 날카로운 부위는 BURR 제거 할 것."
    draw_Text(doc, mx, my+30-107*2, 35, text, layer='0')    
    text = f"3. 연신율 S :STS 1.2T=2, 1.5T=3."
    draw_Text(doc, mx, my+30-107*3, 35, text, layer='0')    
    text = f"   SPC,EGI 1.2T=2, 1.6T=3, 2t=3.5, 3t=4.5."
    draw_Text(doc, mx, my+30-107*4, 35, text, layer='0')    
    return
def page_comment_small(mx, my) :
    gap = 60
    line(doc, mx,my, mx+150, my ,layer='1')                
    line(doc, mx,my-16, mx+150, my-16 ,layer='0')                
    line(doc, mx,my-16-gap , mx+1100/2, my-16-gap ,layer='1')                
    line(doc, mx,my-16-gap*2, mx+1100/2, my-16-gap*2 ,layer='1')                
    line(doc, mx,my-16-gap*3, mx+1100/2, my-16-gap*3 ,layer='1')                
    line(doc, mx,my-16-gap*4, mx+1100/2, my-16-gap*4 ,layer='1')                
    text = f"작업 주기"
    draw_Text(doc, mx, my+30, 20, text, layer='0')    
    text = f"1. 본 도면은 WH={CPH} 으로 도시됨."
    draw_Text(doc, mx, my-gap*1, 20, text, layer='0')    
    text = f"2. 날카로운 부위는 BURR 제거 할 것."
    draw_Text(doc, mx, my-gap*2, 20, text, layer='0')    
    text = f"3. 연신율 S :STS 1.2T=2, 1.5T=3."
    draw_Text(doc, mx, my-gap*3, 20, text, layer='0')    
    text = f"   SPC,EGI 1.2T=2, 1.6T=3, 2t=3.5, 3t=4.5."
    draw_Text(doc, mx, my-gap*4, 20, text, layer='0')    
    return    
def put_commentLine(mx, my) :    
    line(doc, mx,my, mx+150, my ,layer='1')                
    line(doc, mx,my-16, mx+150, my-16 ,layer='0')     
    text = f"절 곡 도"
    draw_Text(doc, mx, my+30, 20, text, layer='0')       
    return
def put_commentLine_string(mx, my, text) :    
    line(doc, mx,my, mx+150, my ,layer='1')                
    line(doc, mx,my-16, mx+150, my-16 ,layer='0')         
    draw_Text(doc, mx, my+30, 20, text, layer='0')       
    return
def read_excel_value(sheet, cell):
    return sheet[cell].value
def get_excel_value(sheet, cell):
    return sheet[cell].value
def write_log(message):
    logging.info(message)    
def parse_arguments_settings():
    parser = GooeyParser()
    settings = parser.add_argument_group('설정')
    settings.add_argument('--config', action='store_true', default=True,  help='라이센스')
    settings.add_argument('--password', widget='PasswordField', gooey_options={'visible': True, 'show_label': True}, help='비밀번호')

    return parser.parse_args()
def parse_arguments():
    parser = GooeyParser()

    group1 = parser.add_argument_group('라이트케이스')
    # group1.add_argument('--opt1', action='store_true',  help='기본')
    # group1.add_argument('--opt2', action='store_true',  help='도장홀')
    # group1.add_argument('--opt3', action='store_true',  help='쪽쟘 상판끝 라운드(추영덕소장)')    
    group1.add_argument('--opt1', action='store_true', default=True, help='기본')

    settings = parser.add_argument_group('설정')
    settings.add_argument('--config', action='store_true', help='라이센스')
    settings.add_argument('--password', widget='PasswordField', gooey_options={'visible': True, 'show_label': True}, help='비밀번호')

    return parser.parse_args()
def display_message():
    message = program_message.format('\n'.join(sys.argv[1:])).split('\n')
    delay = 1.5 / len(message)

    for line in message:
        print(line)
        time.sleep(delay)
def load_env_settings():
# 환경설정 가져오기(하드공유 번호)    
    try:
        with open(license_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get("DiskID")
    except FileNotFoundError:
        return None
def get_current_disk_id():
    return os.popen('wmic diskdrive get serialnumber').read().strip()
def validate_or_default(value):
# None이면 0을 리턴하는 함수    
    if value is None:
        return 0
    return value
def find_intersection(start1, end1, start2, end2):
    # 교차점 계산 (두 직선이 수직 및 수평으로 만나는 경우에 대해서만)
    if start1[0] == end1[0]:
        return (start1[0], start2[1])
    else:
        return (start2[0], start1[1])
def calculate_fillet_point(center, point, radius):
    # 필렛 접점 계산
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    if abs(dx) > abs(dy):
        return (center[0] + radius * (1 if dx > 0 else -1), center[1])
    else:
        return (center[0], center[1] + radius * (1 if dy > 0 else -1))
def calculate_angle(center, point):
    # 각도 계산
    return math.degrees(math.atan2(point[1] - center[1], point[0] - center[0]))
def add_90_degree_fillet(doc, start1, end1, start2, end2, radius):
    msp = doc.modelspace()

    # 교차점 찾기
    intersection_point = find_intersection(start1, end1, start2, end2)

    # 필렛 접점 계산
    point1 = calculate_fillet_point(intersection_point, end1, radius)
    point2 = calculate_fillet_point(intersection_point, end2, radius)

    # 각도 계산
    start_angle = calculate_angle(intersection_point, point1)
    end_angle = calculate_angle(intersection_point, point2)

    # 필렛 원호 그리기
    msp.add_arc(
        center=intersection_point,
        radius=radius,
        start_angle=start_angle,
        end_angle=end_angle,
        dxfattribs={'layer': '레이져'},
    )    
    return msp
def calculate_midpoint(point1, point2):
    return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
def calculate_circle_center(midpoint, radius, point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    dist = math.sqrt(dx**2 + dy**2)
    factor = math.sqrt(radius**2 - (dist / 2)**2) / dist
    return (midpoint[0] - factor * dy, midpoint[1] + factor * dx)
def add_arc_between_points(doc, point1, point2, radius):
    msp = doc.modelspace()

    # 중점 계산
    midpoint = calculate_midpoint(point1, point2)

    # 원의 중심 계산
    center = calculate_circle_center(midpoint, radius, point1, point2)

    # 각도 계산
    start_angle = calculate_angle(center, point1)
    end_angle = calculate_angle(center, point2)

    # 아크 그리기
    msp.add_arc(
        center=center,
        radius=radius,
        start_angle=start_angle,
        end_angle=end_angle,
        dxfattribs={'layer': '레이져'},
    )    
    return msp
import math

def draw_arc(doc, x1, y1, x2, y2, radius, direction, layer='레이져'): # radius는 반지름을 넣는다. 지름이 아님
    msp = doc.modelspace()
    
    # 점들과 반지름을 이용하여 중점과 원의 중심 계산
    midpoint = calculate_midpoint((x1, y1), (x2, y2))
    center = calculate_circle_center(midpoint, radius, (x1, y1), (x2, y2))

    # 시작 각도와 끝 각도 계산
    start_angle = calculate_angle(center, (x1, y1))
    end_angle = calculate_angle(center, (x2, y2))

    # 방향에 따라 각도 조정
    if direction == 'up' or direction == 'down':
        if start_angle > end_angle:
            start_angle, end_angle = end_angle, start_angle
        if direction == 'down':
            start_angle += 180
            end_angle += 180
    elif direction == 'left' or direction == 'right':
        if start_angle > end_angle:
            start_angle, end_angle = end_angle, start_angle
        if direction == 'right':
            start_angle += 180
            end_angle += 180

    # 아크 그리기
    msp.add_arc(
        center=center,
        radius=radius,
        start_angle=start_angle,
        end_angle=end_angle,
        dxfattribs={'layer': layer},
    )
    return msp
def dim_leader(doc, start_x, start_y, end_x, end_y, text,text_height=30, direction=None):
    global saved_DimXpos, saved_DimYpos, saved_text_height, saved_text_gap, saved_direction, dimdistance, dim_horizontalbase, dim_verticalbase, distanceXpos, distanceYpos 
   
    direction='up'
    msp = doc.modelspace()
    layer = 'COPY OF ISO-25'        
    text_style_name = 'COPY OF ISO-25'        
    style = 'COPY OF ISO-25'        
    # override 설정
    override_settings = {
        'dimasz': 15
    }

    # 지서선 추가
    leader = msp.add_leader(
        vertices=[(start_x, start_y), (end_x, end_y)],  # 시작점과 끝점
        dxfattribs={
            'dimstyle': layer,
            'layer': layer
        },
        override=override_settings
    )

    # 텍스트 위치 조정
    text_offset_x = 50
    text_offset_y = 20
    if direction == 'left':
        text_position = (end_x - text_offset_x, end_y)
    elif direction == 'right':
        text_position = (end_x + text_offset_x, end_y)
    elif direction == 'up':
        text_position = (end_x, end_y + text_offset_y)
    elif direction == 'down':
        text_position = (end_x, end_y - text_offset_y)
    else:
        text_position = (end_x + text_offset_x, end_y + text_offset_y)  # 기본 위치

    # 텍스트 추가 (선택적)
    if text:
        msp.add_mtext(text, dxfattribs={
            'insert': text_position,
            'layer': style,
            'char_height': text_height,
            'style': text_style_name,
            'attachment_point': 1  # 텍스트 정렬 방식 설정
        })

    return leader
def line(doc, x1, y1, x2, y2, layer=None):
    global saved_Xpos, saved_Ypos  # 전역 변수로 사용할 것임을 명시
    
    # 선 추가
    start_point = (x1, y1)
    end_point = (x2, y2)
    if layer:
        # 절곡선 22 layer는 ltscale을 조정한다
        if(layer=="22"):
            msp.add_line(start=start_point, end=end_point, dxfattribs={'layer': layer, 'ltscale' : 30})
        else:
            msp.add_line(start=start_point, end=end_point, dxfattribs={'layer': layer })
    else:
        msp.add_line(start=start_point, end=end_point)

    # 다음 선분의 시작점을 업데이트
    saved_Xpos = x2
    saved_Ypos = y2        
def lt(doc, x, y, layer=None):
    # 상대좌표로 그리는 것
    global saved_Xpos, saved_Ypos  # 전역 변수로 사용할 것임을 명시
    
    # 현재 위치를 시작점으로 설정
    start_x = saved_Xpos
    start_y = saved_Ypos

    # 끝점 좌표 계산
    end_x = start_x + x
    end_y = start_y + y

    # 모델 공간 (2D)을 가져옴
    msp = doc.modelspace()

    # 선 추가
    start_point = (start_x, start_y)
    end_point = (end_x, end_y)
    if layer:
        msp.add_line(start=start_point, end=end_point, dxfattribs={'layer': layer})
    else:
        msp.add_line(start=start_point, end=end_point)

    # 다음 선분의 시작점을 업데이트
    saved_Xpos = end_x
    saved_Ypos = end_y
def lineto(doc, x, y, layer=None):
    global saved_Xpos, saved_Ypos  # 전역 변수로 사용할 것임을 명시
    
    # 현재 위치를 시작점으로 설정
    start_x = saved_Xpos
    start_y = saved_Ypos

    # 끝점 좌표 계산
    end_x = x
    end_y = y

    # 모델 공간 (2D)을 가져옴
    msp = doc.modelspace()

    # 선 추가
    start_point = (start_x, start_y)
    end_point = (end_x, end_y)
    if layer:
        msp.add_line(start=start_point, end=end_point, dxfattribs={'layer': layer})
    else:
        msp.add_line(start=start_point, end=end_point)

    # 다음 선분의 시작점을 업데이트
    saved_Xpos = end_x
    saved_Ypos = end_y
def lineclose(doc, start_index, end_index, layer='레이져'):    

    firstX, firstY = globals()[f'X{start_index}'], globals()[f'Y{start_index}']
    prev_x, prev_y = globals()[f'X{start_index}'], globals()[f'Y{start_index}']

    # start_index+1부터 end_index까지 반복합니다.
    for i in range(start_index + 1, end_index + 1):
        # 현재 인덱스의 좌표를 가져옵니다.
        curr_x, curr_y = globals()[f'X{i}'], globals()[f'Y{i}']

        # 이전 좌표에서 현재 좌표까지 선을 그립니다.
        line(doc, prev_x, prev_y, curr_x, curr_y, layer)

        # 이전 좌표 업데이트
        prev_x, prev_y = curr_x, curr_y

        # print(f"prev_x {prev_x}" )
        # print(f"prev_y {prev_y}" )
    
    # 마지막으로 첫번째 점과 연결
    line(doc, prev_x, prev_y, firstX , firstY, layer)        
def rectangle(doc, x1, y1, dx, dy, layer=None, offset=None):
    if offset is not None:
        # 네 개의 선분으로 직사각형 그리기 offset 추가
        line(doc, x1+offset, y1+offset, dx-offset, y1+offset, layer=layer)   
        lineto(doc, dx - offset, dy - offset, layer=layer)  
        lineto(doc, x1 + offset, dy - offset, layer=layer)  
        lineto(doc, x1 + offset, y1 + offset, layer=layer)  
    else:        
        # 네 개의 선분으로 직사각형 그리기
        line(doc, x1, y1, dx, y1, layer=layer)   
        line(doc, dx, y1, dx, dy, layer=layer)   
        line(doc, dx, dy, x1, dy, layer=layer)   
        line(doc, x1, dy, x1, y1, layer=layer)   
def xrectangle(doc, x1, y1, dx, dy, layer=None):
    # 중간에 x마크로 적색선을 넣는 사각형 만들기
    line(doc, x1, y1, dx, y1, layer=layer)   
    line(doc, dx, y1, dx, dy, layer=layer)   
    line(doc, dx, dy, x1, dy, layer=layer)   
    line(doc, x1, dy, x1, y1, layer=layer)   
    line(doc, x1, y1, dx, dy, layer='3')    # 적색 센터라인
    line(doc, x1, dy, dx, y1, layer='3')  # 적색 센터라인     
def numprint(doc, x1, y1, text=None, layer=None):
    insert_block(x1,y1, "slot_frame")            
    draw_Text(doc, x1-35, y1-panel_width/2, 25, text, layer=layer)
def add_angular_dim_2l(drawing, base, line1, line2, location=None, text=None, text_rotation=None, dimstyle='0', override=None, dxfattribs=None):
    # Create a new dimension line
    dim = drawing.dimstyle.add(
        'EZ_ANGULAR_2L',
        dxfattribs={
            'dimstyle': dimstyle,
            'dimtad': 1,  # Place text above dimension line
            'dimtih': False,  # Align text horizontally to dimension line
            'dimtoh': False,  # Align text outside horizontal
            'dimdec': 1
        }
    )
    
    # If override is provided, update the dimension style
    if override:
        dim.update(override)
    
    # Create angular dimension
    angular_dim = drawing.add_angular_dim_2l(
        base=base,
        line1=line1,
        line2=line2,
        location=location,
        text=text,
        text_rotation=text_rotation,
        dimstyle=dim.name,
        override=override,
        dxfattribs=dxfattribs,
    )
    
    # Render the dimension
    angular_dim.render()
    return angular_dim
def dim_angular(doc, x1, y1, x2, y2, x3, y3, x4, y4, distance=80, direction="left", dimstyle="COPY OF ISO-25"):
    msp = doc.modelspace()

    # 두 선분의 좌표
    p1 = (x1, y1)
    p2 = (x2, y2)
    p3 = (x3, y3)
    p4 = (x4, y4)

    # 치수선의 위치 계산
    base_x = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
    base_y = (p1[1] + p2[1] + p3[1] + p4[1]) / 4

    if direction=="left":
        base = (base_x - distance , base_y)
        # 각도 치수선 추가
        dimension = msp.add_angular_dim_2l(
            base=base,  # 치수선 위치
            line1=(p1, p2),  # 첫 번째 선의 시작점과 끝점
            line2=(p3, p4),  # 두 번째 선의 시작점과 끝점
            dimstyle=dimstyle,  # 치수 스타일        
            override={'dimtxt': 0.27, 'dimgap': 0.02, 'dimscl' : 1, 'dimlfac' : 1, 'dimclrt': 7, 'dimdsep': 46, 'dimdec': 0 } # 선색 백색 소수점 . 표기
        )

    elif direction=="up":
        base = (base_x , base_y + distance )          
        # "dimtad": 1, # 0=center; 1=above; 4=below;  
        # 각도 치수선 추가
        dimension = msp.add_angular_dim_2l(
            base=base,  # 치수선 위치
            line1=(p1, p2),  # 첫 번째 선의 시작점과 끝점
            line2=(p3, p4),  # 두 번째 선의 시작점과 끝점
            dimstyle=dimstyle,  # 치수 스타일        
            override={'dimtxt': 0.27, 'dimgap': 0.02, 'dimscl' : 1, 'dimlfac' : 1, 'dimclrt': 7, 'dimdsep': 46, 'dimdec': 0 } # 선색 백색 소수점 . 표기
        )        
    elif direction=="down":
        base = (base_x , base_y - distance )                    
    else:
        base = (base_x + distance , base_y)    
        # 각도 치수선 추가
        dimension = msp.add_angular_dim_2l(
            base=base,  # 치수선 위치
            line1=(p1, p2),  # 첫 번째 선의 시작점과 끝점
            line2=(p3, p4),  # 두 번째 선의 시작점과 끝점
            dimstyle=dimstyle,  # 치수 스타일        
            override={'dimtxt': 0.27, 'dimgap': 0.02, 'dimscl' : 1, 'dimlfac' : 1, 'dimclrt': 7, 'dimdsep': 46, 'dimdec': 0 } # 선색 백색 소수점 . 표기
        )        

    # 치수선의 기하학적 형태 생성
    dimension.render()
    return dimension
def dim_diameter(doc, center, diameter, angle, dimstyle="COPY OF ISO-25", override=None):
    msp = doc.modelspace()
    
    # 기본 지름 치수선 추가
    dimension = msp.add_diameter_dim(
        center=center,  # 원의 중심점
        radius=diameter/2,  # 반지름
        angle=angle,    # 치수선 각도
        dimstyle=dimstyle,  # 치수 스타일
        override={"dimtoh": 1}    # 추가 스타일 설정 (옵션) 지시선이 한번 꺾여서 글자각도가 표준형으로 나오는 옵션
    )
    
    # 치수선의 기하학적 형태 생성
    dimension.render()
def dim_string(doc, x1, y1, x2, y2, dis,  textstr,  text_height=0.28, text_gap=0.05, direction="up"):
    global saved_DimXpos, saved_DimYpos, saved_text_height, saved_text_gap, saved_direction, dimdistance, dim_horizontalbase, dim_verticalbase

    msp = doc.modelspace()
    dim_style = 'COPY OF ISO-25'
    layer = "COPY OF ISO-25"

    # 치수값 계산
    dimension_value = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # 소수점이 있는지 확인
    if dimension_value % 1 != 0:
        dimdec = 1  # 소수점이 있는 경우 소수점 첫째 자리까지 표시
    else:
        dimdec = 0  # 소수점이 없는 경우 소수점 표시 없음

    # override 설정
    override_settings = {
        'dimtxt': text_height,
        'dimgap': text_gap,
        'dimscl': 1,
        'dimlfac': 1,
        'dimclrt': 7,
        'dimdsep': 46,
        'dimdec': dimdec,
        'dimtix': 1,  # 치수선 내부에 텍스트를 표시 (필요에 따라)
        'dimtad': 1 # 치수선 상단에 텍스트를 표시 (필요에 따라)               
    }

    # 방향에 따른 치수선 추가
    if direction == "up":
        dimension = msp.add_linear_dim(
            base=(x1, y1 + dis),
            dimstyle=dim_style,
            p1=(x1, y1),
            p2=(x2, y2),
            dxfattribs={'layer': layer},
            text = textstr,
            override=override_settings
        )
    elif direction == "down":
        dimension = msp.add_linear_dim(
            dimstyle=dim_style,
            base=(x1, y1 - dis),
            p1=(x1, y1),
            p2=(x2, y2),
            dxfattribs={'layer': layer},
            text = textstr,            
            override=override_settings
        )
    elif direction == "left":        
        dimension =  msp.add_linear_dim(
            dimstyle=dim_style,
            base=(x1 - dis, y1),
            angle=90,
            p1=(x1, y1),
            p2=(x2, y2),
            dxfattribs={'layer': layer},
            text = textstr,  
            override=override_settings
        )     
    elif direction == "right":        
        dimension =  msp.add_linear_dim(
            dimstyle=dim_style,
            base=(x1 + dis, y1),
            p1=(x1, y1),
            p2=(x2, y2),
            dxfattribs={'layer': layer},
            text = textstr,  
            angle=270,            
            override=override_settings
        )
    else:
        raise ValueError("Invalid direction. Use 'up', 'down', or 'aligned'.")

    dimension.render()
    return dimension
def d(doc, x1, y1, x2, y2, dis, text_height=0.28, text_gap=0.05, direction="up", option=None, starbottomtion=None, text=None) :
    global saved_DimXpos, saved_DimYpos, saved_text_height, saved_text_gap, saved_direction, dimdistance, dim_horizontalbase, dim_verticalbase, distanceXpos, distanceYpos

    # Option 처리
    if option == 'reverse':   
        x1, x2 = x2, x1
        y1, y2 = y2, y1    
        saved_DimXpos, saved_DimYpos = x1, y1
    else:
        saved_DimXpos, saved_DimYpos = x2, y2

    dimdistance = dis
    saved_text_height = text_height
    saved_text_gap = text_gap
    saved_direction = direction

    # 연속선 구현을 위한 구문
    if starbottomtion is None:        
        if direction == "left":             
            distance = min(x1, x2) - dis            
            dim_horizontalbase = distance
        elif direction == "right":   
            distance = max(x1, x2) + dis                       
            dim_horizontalbase = distance 
        elif direction == "up":   
            distance = max(y1, y2) + dis            
            dim_verticalbase = distance
        elif direction == "down":     
            distance = min(y1, y2) - dis                                  
            dim_horizontalbase = distance
    else:
        if direction == "left":             
            distance = distanceXpos
        elif direction == "right":                        
            distance = distanceXpos
        elif direction == "up":            
            distance = distanceYpos
        elif direction == "down":     
            distance = distanceYpos
     
    # flip을 선언하면 치수선의 시작과 끝을 바꾼다. 저장된 좌표는 지장없다.
    # 치수선의 시작점 끝점에 따라 치수선이 나오는 것을 만들기 위함이다. 
    # 연속치수선때는 좌표가 바뀌면 안되기때문에 고려한 부분이다.

    msp = doc.modelspace()
    dim_style = 'COPY OF ISO-25'
    layer = "COPY OF ISO-25"

    # 치수값 계산
    dimension_value = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # 소수점 확인
    dimdec = 1 if dimension_value % 1 != 0 else 0

    # override 설정
    override_settings = {      
        'dimtxt': text_height,  
        'dimgap': text_gap if text_gap is not None else 0.05,  # 여기에서 dimgap에 기본값 설정
        'dimscl': 1,
        'dimlfac': 1,
        'dimclrt': 7,
        'dimdsep': 46,
        'dimdec': dimdec,
        'dimtix': 1, 
        'dimtad': 1  
    }

    # 방향에 따른 치수선 추가
    if direction == "up":
        add_dim_args = {
            'base': ((x1+x2)/2, distance),
            'dimstyle': dim_style,
            'p1': (x1, y1),
            'p2': (x2, y2),
            'override': override_settings
        }
        # 절대값으로 거리를 저장
        if starbottomtion is None:
            distanceYpos = max(y1, y2) + dis           
        if text is not None :
            add_dim_args['text'] = text
            msp.add_linear_dim(**add_dim_args).render()
            return
        else:
            return msp.add_linear_dim(**add_dim_args)

    elif direction == "down":
        add_dim_args = {
            'dimstyle': dim_style,
            'base': ((x1+x2)/2, distance),
            'p1': (x1, y1),
            'p2': (x2, y2),
            'override': override_settings
        }
        # 절대값으로 거리를 저장
        if starbottomtion is None:
            distanceYpos = min(y1, y2) - dis         
        if text is not None :
            add_dim_args['text'] = text
            msp.add_linear_dim(**add_dim_args).render()
            return
        else:
            return msp.add_linear_dim(**add_dim_args)

    elif direction == "left":
        if option == 'reverse':   
            add_dim_args = {
                'dimstyle': dim_style,
                'base': (distance, (y1+y2)/2),
                'angle': 90,
                'p1': (x1, y1),
                'p2': (x2, y2),
                'override': override_settings
            }
            # 절대값으로 거리를 저장
            if starbottomtion is None:
                distanceXpos = min(x1, x2) - dis 
        else:
            add_dim_args = {
                'dimstyle': dim_style,
                'base': (distance, (y1+y2)/2),
                'angle': 90,
                'p1': (x2, y2),
                'p2': (x1, y1),
                'override': override_settings
            }       
            # 절대값으로 거리를 저장
            if starbottomtion is None:
                distanceXpos = min(x1, x2) - dis 
        if text is not None :
            add_dim_args['text'] = text
            msp.add_linear_dim(**add_dim_args).render()
            return
        else:
            return msp.add_linear_dim(**add_dim_args)

    elif direction == "right":
        add_dim_args = {
            'dimstyle': dim_style,
            'base': (distance, (y1+y2)/2),
            'angle': 90,
            'p1': (x1, y1),
            'p2': (x2, y2),
            'override': override_settings
        }
        # 절대값으로 거리를 저장
        if starbottomtion is None:
            distanceXpos = max(x1, x2) + dis         
        if text is not None :
            add_dim_args['text'] = text
            msp.add_linear_dim(**add_dim_args).render()
            return
        else:
            return msp.add_linear_dim(**add_dim_args)

    elif direction == "aligned":
        add_dim_args = {
            'dimstyle': dim_style,
            'points': [(x1, y1), (x2, y2)],
            'distance': dis,
            'dxfattribs': {'layer': layer},
            'override': override_settings
        }
        if text is not None :
            add_dim_args['text'] = text
        return msp.add_multi_point_linear_dim(**add_dim_args)

    else:
        raise ValueError("Invalid direction. Use 'up', 'down', 'left', 'right', or 'aligned'.")
def dc(doc, x, y, distance=None, option=None, text=None) :    
    global saved_DimXpos, saved_DimYpos, saved_text_height, saved_text_gap, saved_direction, dimdistance, dim_horizontalbase, dim_verticalbase, distanceXpos, distanceYpos
    x1 = saved_DimXpos
    y1 = saved_DimYpos
    x2 = x
    y2 = y        
    if distance is not None :
        dimdistance = distance    
    # reverse 옵션 처리
    if option == 'reverse':
        x1, x2 = x2, x1
        y1, y2 = y2, y1                
    d(doc, x1, y1, x2, y2, dimdistance, text_height=saved_text_height, text_gap=saved_text_gap, direction=saved_direction, starbottomtion='continue', text=text)
def dim(doc, x1, y1, x2, y2, dis, text_height=0.28, text_gap=0.05, direction="up", option=None, starbottomtion=None, text=None):
    global saved_DimXpos, saved_DimYpos, saved_text_height, saved_text_gap, saved_direction, dimdistance, dim_horizontalbase, dim_verticalbase

    # Option 처리
    if option == 'reverse':
        saved_DimXpos, saved_DimYpos = x1, y1
    else:
        saved_DimXpos, saved_DimYpos = x2, y2

    dimdistance = dis
    saved_text_height = text_height
    saved_text_gap = text_gap
    saved_direction = direction

    # 연속선 구현을 위한 구문
    if starbottomtion is None:
        if direction == "left":             
            dim_horizontalbase = dis - (x1 - x2)
        elif direction == "right":                        
            dim_horizontalbase = dis 
        elif direction == "up":            
            dim_verticalbase = dis
        elif direction == "down":                        
            dim_verticalbase = dis   

    # flip을 선언하면 치수선의 시작과 끝을 바꾼다. 저장된 좌표는 지장없다.
    # 치수선의 시작점 끝점에 따라 치수선이 나오는 것을 만들기 위함이다. 
    # 연속치수선때는 좌표가 바뀌면 안되기때문에 고려한 부분이다.

    msp = doc.modelspace()
    dim_style = 'COPY OF ISO-25'
    layer = "COPY OF ISO-25"

    # 치수값 계산
    dimension_value = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # 소수점 확인
    dimdec = 1 if dimension_value % 1 != 0 else 0

    # override 설정
    override_settings = {      
        'dimtxt': text_height,  
        'dimgap': text_gap if text_gap is not None else 0.05,  # 여기에서 dimgap에 기본값 설정
        'dimscl': 1,
        'dimlfac': 1,
        'dimclrt': 7,
        'dimdsep': 46,
        'dimdec': dimdec,
        'dimtix': 1, 
        'dimtad': 1  
    }

    # 방향에 따른 치수선 추가
    if direction == "up":
        add_dim_args = {
            'base': (x1, y1 + dis),
            'dimstyle': dim_style,
            'p1': (x1, y1),
            'p2': (x2, y2),
            'override': override_settings
        }
        if text is not None :
            add_dim_args['text'] = text
            msp.add_linear_dim(**add_dim_args).render()
            return
        else:
            return msp.add_linear_dim(**add_dim_args)

    elif direction == "down":
        add_dim_args = {
            'dimstyle': dim_style,
            'base': (x1, y1 - dis),
            'p1': (x1, y1),
            'p2': (x2, y2),
            'override': override_settings
        }
        if text is not None :
            add_dim_args['text'] = text
            msp.add_linear_dim(**add_dim_args).render()
            return
        else:
            return msp.add_linear_dim(**add_dim_args)

    elif direction == "left":
        if option == 'reverse':   
            add_dim_args = {
                'dimstyle': dim_style,
                'base': (x2 - dis, y2),
                'angle': 90,
                'p1': (x1, y1),
                'p2': (x2, y2),
                'override': override_settings
            }
        else:
            add_dim_args = {
                'dimstyle': dim_style,
                'base': (x1 - dis, y1),
                'angle': 90,
                'p1': (x2, y2),
                'p2': (x1, y1),
                'override': override_settings
            }        
        if text is not None :
            add_dim_args['text'] = text
            msp.add_linear_dim(**add_dim_args).render()
            return
        else:
            return msp.add_linear_dim(**add_dim_args)

    elif direction == "right":
        add_dim_args = {
            'dimstyle': dim_style,
            'base': (x1 + dis, y1),
            'angle': 90,
            'p1': (x1, y1),
            'p2': (x2, y2),
            'override': override_settings
        }
        if text is not None :
            add_dim_args['text'] = text
            msp.add_linear_dim(**add_dim_args).render()
            return
        else:
            return msp.add_linear_dim(**add_dim_args)

    elif direction == "aligned":
        add_dim_args = {
            'dimstyle': dim_style,
            'points': [(x1, y1), (x2, y2)],
            'distance': dis,
            'dxfattribs': {'layer': layer},
            'override': override_settings
        }
        if text is not None :
            add_dim_args['text'] = text
        return msp.add_multi_point_linear_dim(**add_dim_args)

    else:
        raise ValueError("Invalid direction. Use 'up', 'down', 'left', 'right', or 'aligned'.")
def dimcontinue(doc, x, y, distance=None, option=None) :    
    global saved_DimXpos
    global saved_DimYpos
    global saved_text_height
    global saved_text_gap
    global saved_direction
    global dimdistance
    global dim_horizontalbase
    global dim_verticalbase

    x1 = saved_DimXpos
    y1 = saved_DimYpos
    x2 = x
    y2 = y        



# 방향에 대한 정의를 하고 연속적으로 차이를 감지해서 처리하는 것이다.
    if saved_direction=="left" :
        dimdistance = dim_horizontalbase
        # 재계산해야 함.        
        dim_horizontalbase = dimdistance - (x1 - x2)        
    if saved_direction=="right" :
        dimdistance = dim_horizontalbase 
        # 재계산해야 함.
        dim_horizontalbase = dimdistance - (x2 - x1)
    if saved_direction=="up" :
        dimdistance = dim_verticalbase
        # 재계산해야 함.
        dim_verticalbase = dimdistance - (y2 - y1)
    if saved_direction=="down" :
        dimdistance = dim_verticalbase 
        # 재계산해야 함.
        dim_verticalbase = dimdistance - (y1 - y2)

    if distance is not None :
        dimdistance = distance    

    # reverse 옵션 처리
    if option == 'reverse':
        x1, x2 = x2, x1
        y1, y2 = y2, y1                

    dim(doc, x1, y1, x2, y2, dimdistance, text_height=saved_text_height, text_gap=saved_text_gap, direction=saved_direction, starbottomtion='continue')
def dimto(doc, x2, y2, dis, text_height=0.20, text_gap=None, option=None) :    
    global saved_DimXpos
    global saved_DimYpos
    global saved_text_height
    global saved_text_gap
    global saved_direction

    if text_gap is not None :
        text_gap = saved_text_gap
        saved_text_gap = text_gap

    if text_height is not None :
        text_height = saved_text_height
        saved_text_height = text_height

    dim(doc, saved_DimXpos, saved_DimYpos, x2, y2, dis, text_height=text_height, text_gap=text_gap, direction=saved_direction, option=option)
def create_vertical_dim(doc, x1, y1, x2, y2, dis, angle, layer=None, text_height=0.28, text_gap=0.05):
    msp = doc.modelspace()
    dim_style = layer  # 치수 스타일 이름
    points = [(x1, y1), (x2, y2)]

    if angle==None :
        angle = 270

    # 치수값 계산
    dimension_value = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # 소수점이 있는지 확인
    if dimension_value % 1 != 0:
        dimdec = 1  # 소수점이 있는 경우 소수점 첫째 자리까지 표시
    else:
        dimdec = 1  # 소수점이 없는 경우 소수점 표시 없음    

    return msp.add_multi_point_linear_dim(
        base=(x1 + dis if angle == 270 else x1 - dis , y1),  #40은 보정
        points = points,
        angle = angle,
        dimstyle = dim_style,
        discard = True,
        dxfattribs = {'layer': layer},
        # 치수 문자 위치 조정 (0: 치수선 위, 1: 치수선 옆) 'dimtmove': 1 
        # override={'dimtxt': text_height, 'dimscl': 1, 'dimlfac': 1, 'dimclrt': 7, 'dimdec': dimdec, 'dimdsep': 46, 'dimtmove': 3  }
        override = {'dimtxt': text_height, 'dimgap': text_gap, 'dimscl': 1, 'dimlfac': 1, 'dimclrt': 7, 'dimdec': dimdec, 'dimdsep': 46, 'dimtmove': 3  }
    )
def dim_vertical_right(doc, x1, y1, x2, y2, dis, layer="COPY OF ISO-25", text_height=0.28,  text_gap=0.07, angle=None):
    return create_vertical_dim(doc, x1, y1, x2, y2, dis, angle, layer, text_height, text_gap)
def dim_vertical_left(doc, x1, y1, x2, y2, dis, layer=None, text_height=0.28,  text_gap=0.07):
    return create_vertical_dim(doc, x1, y1, x2, y2, dis, 90, layer, text_height, text_gap)
def create_vertical_dim_string(doc, x1, y1, x2, y2, dis, angle, textstr, text_height=0.28, text_gap=0.07):    
    msp = doc.modelspace()
    dim_style = 'COPY OF ISO-25'
    layer = "COPY OF ISO-25"
    points = [(x1, y1), (x2, y2)]

    # 치수값 계산
    dimension_value = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # 소수점이 있는지 확인
    if dimension_value % 1 != 0:
        dimdec = 1  # 소수점이 있는 경우 소수점 첫째 자리까지 표시
    else:
        dimdec = 1  # 소수점이 없는 경우 소수점 표시 없음    

    return msp.add_multi_point_linear_dim(
        base=(x1 + dis if angle == 270 else x1 - dis , y1),  #40은 보정
        points=points,
        angle=angle,
        dimstyle=dim_style,
        discard=True,
        dxfattribs={'layer': layer},           
        # 치수 문자 위치 조정 (0: 치수선 위, 1: 치수선 옆) 'dimtmove': 1 
        override={'dimtxt': text_height, 'dimgap': text_gap, 'dimscl': 1, 'dimlfac': 1, 'dimclrt': 7, 'dimdec': dimdec, 'dimdsep': 46, 'dimtmove': 3 , 'text' : textstr      }
    )
def dim_vertical_right_string(doc, x1, y1, x2, y2, dis, textstr, text_height=0.28,  text_gap=0.07):
    return create_vertical_dim_string(doc, x1, y1, x2, y2, dis, 270, textstr, text_height, text_gap)
def dim_vertical_left_string(doc, x1, y1, x2, y2, dis, textstr, text_height=0.28,  text_gap=0.07):
    return create_vertical_dim_string(doc, x1, y1, x2, y2, dis, 90, textstr, text_height, text_gap)
def draw_Text_direction(doc, x, y, size, text, layer=None, rotation = 90):
    # 모델 공간 (2D)을 가져옴
    msp = doc.modelspace()

    # MText 객체 생성
    mtext = msp.add_mtext(
        text,  # 텍스트 내용
        dxfattribs={
            'layer': layer,  # 레이어 지정
            'style': text_style_name,  # 텍스트 스타일 지정
            'char_height': size,  # 문자 높이 (크기) 지정
        }
    )

    # MText 위치와 회전 설정
    mtext.set_location(insert=(x, y), attachment_point=1, rotation=rotation)

    return mtext
def draw_Text(doc, x, y, size, text, layer=None):
    # 모델 공간 (2D)을 가져옴
    msp = doc.modelspace()

    # 텍스트 추가 및 생성된 Text 객체 가져오기
    text_entity = msp.add_text(
        text,  # 텍스트 내용
        dxfattribs={
            'layer': layer,  # 레이어 지정
            'style': text_style_name,  # 텍스트 스타일 지정
            'height': size,  # 텍스트 높이 (크기) 지정
        }
    )

    # Text 객체의 위치 설정
    # text_entity.set_placement((x, y), align=TextEntityAlignment.CENTER)  # 텍스트 위치 및 정렬 설정
    # Text 객체의 위치 설정 (가로 및 세로 중앙 정렬)
    text_entity.set_placement((x, y), align=TextEntityAlignment.MIDDLE_LEFT)
def draw_circle(doc, center_x, center_y, radius, layer='0', color='7'):
    """
    원을 그리는 함수 radius는 지름으로 넣도록 수정
    :param doc: ezdxf 문서 객체
    :param center_x: 원의 중심 x 좌표
    :param center_y: 원의 중심 y 좌표
    :param radius: 원의 반지름이 아닌 지름입력
    : radius=radius/2 적용
    :param layer: 원을 추가할 레이어 이름 (기본값은 '0')
    지름으로 수정 
    """
    msp = doc.modelspace()
    circle = msp.add_circle(center=(center_x, center_y), radius=radius/2, dxfattribs={'layer': layer, 'color' : color})
    return circle
def circle_cross(doc, center_x, center_y, radius, layer='0', color='7'):
    """
    DXF 문서에 원을 그리는 함수
    :param doc: ezdxf 문서 객체
    :param center_x: 원의 중심 x 좌표
    :param center_y: 원의 중심 y 좌표
    :param radius: 원의 반지름
    :param layer: 원을 추가할 레이어 이름 (기본값은 '0')
    지름으로 수정 /2 적용
    """
    draw_circle(doc, center_x, center_y, radius, layer=layer, color=color)
    # 적색 십자선 그려주기    
    line(doc, center_x - radius/2 - 5, center_y, center_x +  radius/2 + 5, center_y, layer="CEN" )
    line(doc, center_x , center_y - radius/2 - 5, center_x , center_y +  radius/2 + 5, layer="CEN" )
    return circle_cross        
def cross10(doc, center_x, center_y):
# 10미리 십자선 레이져 만들기   
    line(doc, center_x - 5, center_y, center_x +  5, center_y, layer="레이져" )
    line(doc, center_x, center_y - 5, center_x , center_y + 5, layer="레이져" )
    return cross10
def cross(doc, center_x, center_y, length, layer='레이져'):
    line(doc, center_x - length, center_y, center_x +  length, center_y, layer=layer )
    line(doc, center_x, center_y - length, center_x , center_y + length, layer=layer )
    return cross
def crossslot(doc, center_x, center_y, direction=None):
# 10미리 십자선 레이져 만들기   
    line(doc, center_x - 10, center_y, center_x +  10, center_y, layer="CL" )
    line(doc, center_x, center_y - 10, center_x , center_y + 10, layer="CL" )
    if direction== 'vertical':
        insert_block(center_x, center_y , "8x16_vertical_draw")
    else:
        insert_block(center_x, center_y , "8x16_horizontal_draw")
    return cross10
def m14(doc, center_x, center_y,layer='0', color='4'):
    radius = 14
    draw_circle(doc, center_x, center_y, 14 , layer=layer, color=color)
    draw_circle(doc, center_x, center_y, 8 , layer=layer, color=color)
    draw_circle(doc, center_x, center_y, 4.9 , layer=layer, color=color)
    # 적색 십자선 그려주기    
    line(doc, center_x - radius/2 - 5, center_y, center_x +  radius/2 + 5, center_y, layer="CEN" )
    line(doc, center_x , center_y - radius/2 - 5, center_x , center_y +  radius/2 + 5, layer="CEN" )
    return 
def extract_abs(a, b):
    return abs(a - b)    
def insert_block( x, y, block_name):    
# 도면틀 삽입    
    scale = 1
    insert_point = (x, y, scale)

    # 블록 삽입하는 방법           
    msp.add_blockref(block_name , insert_point, dxfattribs={
        'xscale': scale,
        'yscale': scale,
        'rotation': 0
    })       
def insert_frame( x, y, scale , sep , title, description , dwg_number):    
# 도면틀 삽입    
    if(sep =="drawings_frame"):
        block_name = "drawings_frame_NOtable"
        insert_point = (x, y, scale)

        # 블록 삽입하는 방법           
        msp.add_blockref(block_name , insert_point, dxfattribs={
            'xscale': scale,
            'yscale': scale,
            'rotation': 0
        })

        draw_Text(doc, x + (3545+900) * scale, y + 600*scale  , 50*scale , str(title), '0')
        draw_Text(doc, x + (3545+900) * scale, y + 450*scale  , 50*scale , str(description), '0')
        draw_Text(doc, x + (5000+700) * scale, y + 600*scale  , 50*scale , str(dwg_number) , '0')
def envsettings():
    # 하드디스크 고유번호를 가져오는 코드 (시스템에 따라 다를 수 있음)
    disk_id = os.popen('wmic diskdrive get serialnumber').read().strip()
    data = {"DiskID": disk_id}
    with open(license_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file)
def CalculateLEDbar(car_length):
# LED바 길이 계산 (1030, 등도 계산되도록 로직개발)    
    # Subtract 100 from the input value
    result = car_length - 100

    # Adjust to the next lower or equal multiple of 50
    if result % 100 >= 50:
        result = (result // 100) * 100 + 100
    else:
        if 0 < result % 100 <= 30:
            # For values just over a multiple of 100, bump up to the next 50
            result = (result // 100) * 100 + 50
        else:
            # Otherwise, round down to the nearest 100
            result = (result // 100) * 100 

    return result
def calculate_light_positions_adjusted_031(dataCD):
    # Base coordinates
    y_coord1 = 125
    y_coord_last = dataCD - 125

    # Check if CD is over 2000 for additional coordinates calculation
    if dataCD > 2000:
        # Middle two coordinates with a gap
        midpoint = dataCD / 2
        y_coord4 = midpoint - 185
        y_coord5 = midpoint + 185

        # Calculating other coordinates with equidistant spacing
        interval = (y_coord4 - y_coord1) / 3
        y_coord2, y_coord3 = y_coord1 + interval, y_coord1 + 2 * interval
        y_coord6, y_coord7 = y_coord5 + interval, y_coord5 + 2 * interval

        # Adjusting coordinates to round off and add truncated decimals
        y_coord2, y_coord3, y_coord6 = adjust_coordinates(y_coord2, y_coord3, y_coord6)
        y_coord7 = round(y_coord7)

        all_y_coords = sorted([y_coord1, y_coord2, y_coord3, y_coord4, y_coord5, y_coord6, y_coord7, y_coord_last])
    else:
        # For CD 2000 or less, calculate additional coordinates
        midpoint = dataCD / 2
        y_coord2 = midpoint - 185
        y_coord3 = midpoint + 185

        # Calculating the additional coordinates
        y_coord4 = (y_coord1 + y_coord2) / 2
        y_coord5 = (y_coord3 + y_coord_last) / 2

        all_y_coords = sorted([y_coord1, y_coord4, y_coord2, y_coord3, y_coord5, y_coord_last])

    return all_y_coords
def adjust_coordinates(coord1, coord2, coord3):
# Function to adjust coordinates with rounding and adding truncated decimals    
    adjusted_coord1 = round(coord1)
    decimal_part = coord1 - adjusted_coord1
    adjusted_coord2 = round(coord2 + decimal_part)
    adjusted_coord3 = round(coord3 + (coord2 - adjusted_coord2))

    return adjusted_coord1, adjusted_coord2, adjusted_coord3
def calculate_lc_position_031(inputCW, inputCD):
    # Calculate Y-coordinates for bottom and bottom holes
    bottomholey = inputCD - 40
    Bottomy = 40

    # Initialize the list of x-coordinates for bottom and bottom holes
    bottomholex = []
    Bottomx = []

    # CW에서 양쪽의 여유분 230을 제외한 값을 3등분
    divided_space = (inputCW - 230) // 3
    end_digit = divided_space % 10    

    # Determine the number of holes and calculate their positions
    if inputCW >= 1400:
        # For CW >= 1400, there are 4 holes
        # Calculate space between holes with special distribution
        x1 = 115
        space_available = inputCW - 115 * 2
        
        if end_digit in [3, 4]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 3) // 10 * 10) + 4
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 2 // 10 * 10) + 3                    
        if end_digit in [6, 7]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 3) // 10 * 10) + 6
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 2 // 10 * 10) + 7

        # Calculating all x-coordinates
        x2 = x1 + side_space
        x3 = x2 + middle_space
        x4 = inputCW - 115

        bottomholex = [x1, x2, x3, x4]
        Bottomx = [x1, x2, x3, x4]
    else:
        # For CW < 1400, there are 3 holes
        x1 = 115
        x2 = (inputCW - 115 * 2) / 2 + 115
        x3 = inputCW - 115
        bottomholex = [x1, x2, x3]
        Bottomx = [x1, x2, x3]

    # Create a dictionary to hold the coordinates
    lc_positions = {
        'bottomholex': bottomholex,
        'bottomholey': bottomholey,
        'Bottomx': Bottomx,
        'Bottomy': Bottomy,
        'end_digit' : end_digit
    }

    return lc_positions
def calculate_lc_vertical_hole_positions_031(inputCW, inputCD):
    # 고정된 x 좌표들 설정
    leftholex = [115, 115, 115]
    rightholex = [inputCW - 115, inputCW - 115, inputCW - 115]

    # y 좌표를 계산하기 위한 로직
    if inputCD <= 1250:
        # CD가 1250 이하일 경우, y1만 존재
        y1 = (inputCD - 80) / 2  # 40*2를 제외하고 중간값을 계산
        vertical_holey = [y1]
    elif inputCD > 1250 and inputCD <2100:
        # CD가 1250을 초과할 경우, y 좌표 3개를 계산
        divided_space = (inputCD - 80) // 3  # 40*2를 제외하고 3등분
        end_digit = divided_space % 10

        # For CW >= 1400, there are 4 holes
        # Calculate space between holes with special distribution        
        space_available = inputCD - 40 * 2
        
        if end_digit in [3, 4]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 3) // 10 * 10) + 4
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 2 // 10 * 10) + 3   
            # print (f" 3, 4 선택됨 end_digit : {end_digit}  , side_space : {side_space} , middle_space : {middle_space}")                 
        elif end_digit in [6, 7]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 3) // 10 * 10) + 6
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 2 // 10 * 10) + 7
        else:            
            middle_space = ((space_available // 3) // 10 * 10)             
            side_space = ((space_available - middle_space) // 2 // 10 * 10) 

        # Calculating all x-coordinates
        y1 = side_space + 40    # 40위에서 시작
        y2 = y1 + middle_space

        vertical_holey = [y1, y2]
        # print(f" end_digit : {end_digit}  , side_space : {side_space} , middle_space : {middle_space}")
    # 2100 보다 크면 중간 홀 3개    
    else:         
        divided_space = (inputCD - 80) // 4  # 40*2를 제외하고 4등분
        end_digit = divided_space % 10

        # For CW >= 1400, there are 4 holes
        # Calculate space between holes with special distribution        
        space_available = inputCD - 40 * 2
        
        if end_digit in [3, 4]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 4) // 10 * 10) + 4
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 3 // 10 * 10) + 3                    
        elif end_digit in [6, 7]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 4) // 10 * 10) + 6
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 3 // 10 * 10) + 7
        else:            
            middle_space = space_available // 4
            side_space = (space_available - middle_space) // 3

        # Calculating all x-coordinates
        y1 = side_space + 40
        y2 = y1 + middle_space
        y3 = y2 + side_space

        vertical_holey = [y1, y2, y3]

    # 좌표 딕셔너리 반환
    hole_positions = {
        'leftholex': leftholex,
        'rightholex': rightholex,
        'vertical_holey': vertical_holey
    }

    return hole_positions
def draw_patterned_lines(doc, start_x, end_x, y1, y2, layer):
# 패턴그리는 함수    
    x = start_x
    gap_count = 0  # 1mm 간격으로 그린 선의 개수를 추적

    while x < end_x:
        line(doc, x, y1, x, y2, layer)

        # 1mm 간격으로 3개의 선을 그린 후 5mm 간격 적용
        gap_count += 1
        if gap_count == 3:
            x += 6
            gap_count = 0  # 간격 카운트 리셋
        else:
            x += 1.5
def ALprofile_draw(doc, x, y, length, direction="side"):   
    width = 42
    if direction=='side':
        # 마구리
        rectangle(doc, x, y, x+width, y - 2, layer="CL")        
        rectangle(doc, x, y - length - 2, x+width, y - length, layer="CL")        

        rectangle(doc, x, y - length - 2, x+width, y-2, layer="CL")        
        rectangle(doc, x + 1, y - 2, x+width-1, y-length, layer="CL")
        rectangle(doc, x+15, y - 50, x+width-15, y-length+50-2, layer="6")
        line(doc, x+15+1.2, y - 50, x+15+1.2, y-length+50-2, layer="hidden")
        line(doc, x+width-15-1.2, y - 50, x+width-15-1.2, y-length+50-2, layer="hidden")
        rectangle(doc, x+15+3, y - 50-2, x+width-15-3, y-length+50-2+2, layer="4")
    if direction=='tCOPottom':
        # 마구리
        rectangle(doc, x, y, x+2, y - width, layer="CL")        
        rectangle(doc, x + length - 2, y ,  x + length , y - width, layer="CL")        

        rectangle(doc, x , y , x+length, y-width, layer="CL")        
        rectangle(doc, x + 2 , y - 1, x+length-2, y - width + 1, layer="CL")

        rectangle(doc, x + 50, y - 15, x + length - 50, y-width + 15, layer="6")
        line(doc, x + 50, y - 15 - 1.2, x + length - 50,  y - 15 - 1.2, layer="hidden")
        line(doc, x + 50,  y - width + 15 + 1.2 , x + length - 50, y - width + 15 + 1.2 , layer="hidden")        
        rectangle(doc, x+52, y - 18, x+length -52, y-width + 18, layer="4")
def calculate_hole_positions_separated_lc031(LCD):    
    #031 홀간격계산
    center = LCD // 2  # 중심 지점
    central_start = center - 185  # 중심 구간 시작
    central_end = center + 185  # 중심 구간 끝

    left_positions = []
    right_positions = []

    # 중심으로부터 왼쪽 계산
    left_current = central_start
    while left_current > 0:
        left_positions.insert(0, left_current)
        left_current -= 220

    # 중심으로부터 오른쪽 계산
    right_current = central_end
    while right_current < LCD:
        right_positions.append(right_current)
        right_current += 220

    # 결과 리스트 합치기
    positions = left_positions + right_positions

    return positions
def calculate_ledbar_bottomhole_lc031(ledbar_length):
#031 led bar bracket 홀간격계산    
    center = ledbar_length // 2  # 중심 지점
    central_gap = 350
    interval = 300  # 간격

    left_positions = []
    right_positions = []

    # 중앙 구간 시작 및 종료
    central_start = center - central_gap // 2
    central_end = center + central_gap // 2

    # 중심으로부터 왼쪽 계산
    left_current = central_start
    while left_current > 0:
        left_positions.insert(0, left_current)
        left_current -= interval

    # 중심으로부터 오른쪽 계산
    right_current = central_end
    while right_current < ledbar_length:
        right_positions.append(right_current)
        right_current += interval

    # 결과 리스트 합치기
    positions = left_positions + right_positions

    return positions
def calculate_ledbar_upperhole_lc031(ledbar_length):
    center = ledbar_length // 2  # 중심 지점
    initial_offset = 50  # 최초 간격
    interval = 100  # 이후 간격

    left_positions = []
    right_positions = []

    # 중심으로부터 왼쪽 계산 (초기 간격으로 시작)
    left_current = center - initial_offset
    while left_current > 0:
        left_positions.insert(0, left_current)
        left_current -= interval

    # 중심으로부터 오른쪽 계산 (초기 간격으로 시작)
    right_current = center + initial_offset
    while right_current < ledbar_length:
        right_positions.append(right_current)
        right_current += interval

    # 결과 리스트 합치기
    positions = left_positions + right_positions

    return positions
def calculate_lc_position_035(inputCW, inputCD):
#035 홀간격계산    
    # Calculate Y-coordinates for bottom and bottom holes
    bottomholey = inputCD - 40
    Bottomy = 40

    # Initialize the list of x-coordinates for bottom and bottom holes
    bottomholex = []
    Bottomx = []

    firstXgap = 110
    side_space = 0
    space_available = 0
    middle_space = 0

    # CW에서 양쪽의 여유분 230을 제외한 값을 3등분
    divided_space = (inputCW - firstXgap*2) // 3
    end_digit = divided_space % 10    

    # Determine the number of holes and calculate their positions
    if inputCW >= 1600:
        # For CW >= 1400, there are 4 holes
        # Calculate space between holes with special distribution
        x1 = firstXgap # 라이트케이스 첫홀 위치 25 띄운 치수 제외한 치수
        space_available = inputCW - firstXgap * 2
        
        if end_digit in [3, 4]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 3) // 10 * 10) + 4
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 2 // 10 * 10) + 3                    
        elif end_digit in [6, 7]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 3) // 10 * 10) + 6
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 2 // 10 * 10) + 7
        else:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 3) // 10 * 10) 
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 2 // 10 * 10) 

        # Calculating all x-coordinates
        x2 = x1 + side_space
        x3 = x2 + middle_space
        x4 = inputCW - firstXgap

        bottomholex = [x1, x2, x3, x4]
        Bottomx = [x1, x2, x3, x4]
    else:
        # For CW < 1400, there are 3 holes
        x1 = firstXgap
        x2 = (inputCW - firstXgap * 2) / 2 + firstXgap
        x3 = inputCW - firstXgap
        bottomholex = [x1, x2, x3]
        Bottomx = [x1, x2, x3]

    # Create a dictionary to hold the coordinates
    lc_positions = {
        'bottomholex': bottomholex,
        'bottomholey': bottomholey,
        'Bottomx': Bottomx,
        'Bottomy': Bottomy,
        'end_digit' : end_digit
    }

    # print (f" calculate_lc_position_035 함수 end_digit : {end_digit}  , side_space : {side_space} , middle_space : {middle_space}")
    # print (f" {lc_positions}")

    return lc_positions
def calculate_hole_vertical_lc035(LCD):
    # 중심 지점 계산
    center = LCD // 2

    # 남은 거리를 분할하는 내부 함수
    def divide_remaining_distance(remaining_distance):        
        for div in range(3, 5):
            intervals = [remaining_distance // div] * (div - 1)
            intervals.append(remaining_distance - sum(intervals))
            if all(150 <= x <= 500 for x in intervals):
                return intervals
        return []

    # 중심으로부터의 고정 홀 위치
    fixed_holes = [54, center - 15, center + 15, LCD - 54]

    # LCD 값에 따른 추가 홀 위치 계산
    if LCD < 1950:
        # LCD가 1950 미만일 경우 중간 값 추가
        additional_holes = [(54 + (center - 15)) // 2]
    else:
        # LCD가 1950 이상일 경우 3등분한 값 추가
        first_third = 54 + (center - 15 - 54) // 3
        second_third = first_third + (center - 15 - 54) // 3
        additional_holes = [first_third, second_third]

    # 중심 왼쪽 홀 위치 결합 및 정렬
    left_holes = sorted(fixed_holes[:2] + additional_holes)

    # 중심을 기준으로 오른쪽 홀 위치 계산
    right_holes = [LCD - hole for hole in reversed(left_holes)]

    # 전체 홀 위치 결합 및 정렬
    return sorted(set(left_holes + right_holes))
def calculate_lc_vertical_hole_positions_035(inputCW, inputCD):
    # 고정된 x 좌표들 설정
    firstXgap = 110
    leftholex = [firstXgap, firstXgap, firstXgap]
    rightholex = [inputCW - firstXgap, inputCW - firstXgap, inputCW - firstXgap]

    side_space = 0
    space_available = 0

    # y 좌표를 계산하기 위한 로직
    if inputCD <= 1350:
        # CD가 1250 이하일 경우, y1만 존재
        y1 = (inputCD - 80) / 2  # 40*2를 제외하고 중간값을 계산
        vertical_holey = [y1]
    elif inputCD > 1350 and inputCD <2100:
        # CD가 1250을 초과할 경우, y 좌표 3개를 계산
        divided_space = (inputCD - 80) // 3  # 40*2를 제외하고 3등분
        end_digit = divided_space % 10

        # For CW >= 1400, there are 4 holes
        # Calculate space between holes with special distribution        
        space_available = inputCD - 40 * 2
        
        if end_digit in [3, 4]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 3) // 10 * 10) + 4
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 2 // 10 * 10) + 3   
            # print (f" 3, 4 선택됨 end_digit : {end_digit}  , side_space : {side_space} , middle_space : {middle_space}")                 
        elif end_digit in [6, 7]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 3) // 10 * 10) + 6
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 2 // 10 * 10) + 7
        else:            
            middle_space = ((space_available // 3) // 10 * 10)             
            side_space = ((space_available - middle_space) // 2 // 10 * 10) 

        # Calculating all x-coordinates
        y1 = side_space + 40    # 40위에서 시작
        y2 = y1 + middle_space

        vertical_holey = [y1, y2]
        # print (f" end_digit : {end_digit}  , side_space : {side_space} , middle_space : {middle_space}")
    # 2100 보다 크면 중간 홀 3개    
    else:         
        divided_space = (inputCD - 80) // 4  # 40*2를 제외하고 4등분
        end_digit = divided_space % 10

        # For CW >= 1400, there are 4 holes
        # Calculate space between holes with special distribution        
        space_available = inputCD - 40 * 2
        
        if end_digit in [3, 4]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 4) // 10 * 10) + 4
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 3 // 10 * 10) + 3                    
        elif end_digit in [6, 7]:
            # The middle space needs to end with 4, therefore it should be the nearest multiple of 10 plus 4
            middle_space = ((space_available // 4) // 10 * 10) + 6
            # The side spaces will take the remaining space divided by 2 and adjusted to end with 3
            side_space = ((space_available - middle_space) // 3 // 10 * 10) + 7
        else:            
            middle_space = space_available // 4
            side_space = (space_available - middle_space) // 3

        # Calculating all x-coordinates
        y1 = side_space + 40
        y2 = y1 + middle_space
        y3 = y2 + side_space

        vertical_holey = [y1, y2, y3]

    # 좌표 딕셔너리 반환
    hole_positions = {
        'leftholex': leftholex,
        'rightholex': rightholex,
        'vertical_holey': vertical_holey
    }

    return hole_positions
def calculate_cliphole_lc035(distance , length):
    # 중심 지점 계산
    center = length // 2

    # LCD 길이에 따른 홀의 수와 위치 결정
    if length < 1950:
        # LCD가 1950 미만일 때는 3개의 홀
        hole_positions = [distance, center, length - distance]
    else:
        # LCD가 1950 이상일 때는 4개의 홀
        remaining_center = length - 2 * distance  # 양쪽 끝 홀 사이의 거리
        center_hole1 = distance + remaining_center // 4  # 중앙 왼쪽 홀
        center_hole2 = distance + (remaining_center // 4) * 3  # 중앙 오른쪽 홀
        hole_positions = [distance, center_hole1, center_hole2, length - distance]

    return sorted(hole_positions)
def calculate_midplatehole_lc035(length):
    # 전체 길이를 5등분하는 간격 계산
    interval = length / 5

    # 4개의 위치 좌표 계산
    hole_positions = [round(interval * i, 1) for i in range(1, 5)]

    return hole_positions
def calculate_midplate_connecthole_lc035(length):
    # 양 끝 홀 위치를 고정
    first_and_last_hole = 82.6

    # 중간 홀들 간의 거리 계산
    middle_length = length - 2 * first_and_last_hole  # 양쪽 끝 홀을 제외한 길이
    interval = round(middle_length / 7, 1)  # 6등분한 간격, 소수점 첫째 자리까지

    # 홀 위치 계산
    hole_positions = [first_and_last_hole]  # 첫 홀 위치 추가
    current_position = first_and_last_hole

    # 중간 홀 위치 계산 및 추가
    for _ in range(7):
        current_position += interval
        hole_positions.append(round(current_position, 1))

    # 마지막 홀 위치 추가
    hole_positions.append(length - first_and_last_hole)

    return hole_positions
def calculate_ledbar_bottomhole_lc035(ledbar_length):
#035 led bar bracket 홀간격계산    
    center = ledbar_length // 2  # 중심 지점
    central_gap = 350
    interval = 300  # 간격

    left_positions = []
    right_positions = []

    # 중앙 구간 시작 및 종료
    central_start = center - central_gap // 2
    central_end = center + central_gap // 2

    # 중심으로부터 왼쪽 계산
    left_current = central_start
    while left_current > 0:
        left_positions.insert(0, left_current)
        left_current -= interval

    # 중심으로부터 오른쪽 계산
    right_current = central_end
    while right_current < ledbar_length:
        right_positions.append(right_current)
        right_current += interval

    # 결과 리스트 합치기
    positions = left_positions + right_positions

    return positions
def calculate_ledbar_upperhole_lc035(ledbar_length):
    center = ledbar_length // 2  # 중심 지점
    initial_offset = 50  # 최초 간격
    interval = 100  # 이후 간격

    left_positions = []
    right_positions = []

    # 중심으로부터 왼쪽 계산 (초기 간격으로 시작)
    left_current = center - initial_offset
    while left_current > 0:
        left_positions.insert(0, left_current)
        left_current -= interval

    # 중심으로부터 오른쪽 계산 (초기 간격으로 시작)
    right_current = center + initial_offset
    while right_current < ledbar_length:
        right_positions.append(right_current)
        right_current += interval

    # 결과 리스트 합치기
    positions = left_positions + right_positions

    return positions
def calculate_holeArray(startnum, interval, limit, length):
    # 결과를 저장할 리스트 초기화
    hole_array = []

    # 현재 숫자를 startnum으로 설정
    current_num = startnum

    # current_num이 limit과 length를 넘지 않을 때까지 반복
    while current_num <= limit and current_num <= length:
        # 리스트에 현재 숫자 추가
        hole_array.append(current_num)
        # 다음 숫자를 interval만큼 증가
        current_num += interval
    hole_array.append(length-85)
    return hole_array
def calculate_splitholeArray(startnum, interval, limit, length):
    # P2부터 P10 판넬
    hole_array = []

    # 현재 숫자를 startnum으로 설정
    current_num = startnum

    # current_num이 limit과 length를 넘지 않을 때까지 반복
    while current_num <= limit and current_num <= length:
        # 리스트에 현재 숫자 추가
        hole_array.append(current_num)
        # 다음 숫자를 interval만큼 증가
        current_num += interval
    hole_array.append(length)
    return hole_array
def calculate_handrail_hole_coordinates(panel_name, panel_widths, HRsidegap):
    """
    주어진 패널 이름에 따라 핸드레일 홀의 x좌표들을 계산하여 반환합니다.

    :param panel_name: 핸드레일 홀의 좌표를 찾을 패널 이름 (예: "P2")
    :param panel_widths: 각 패널의 너비를 담고 있는 사전
    :param HRsidegap: 핸드레일 사이의 간격을 나타내는 리스트 (정방향 혹은 역방향)
    :return: 계산된 핸드레일 홀의 x좌표들
    """
    # 이전 패널들의 총 너비 계산
    total_previous_width = sum(panel_widths[key] for key in sorted(panel_widths) if int(key[1:]) < int(panel_name[1:]))

    # 핸드레일 홀의 x좌표 계산
    coordinates = []
    accumulated_gap = 0
    for gap in HRsidegap:
        accumulated_gap += gap
        if total_previous_width < accumulated_gap <= total_previous_width + panel_widths[panel_name]:
            coordinates.append(accumulated_gap - total_previous_width)
            # 마지막 핸드레일 홀만 고려
            if panel_name in ['P4', 'P10', 'P7'] and accumulated_gap + HRsidegap[HRsidegap.index(gap) + 1] > total_previous_width + panel_widths[panel_name]:
                break

    return coordinates

def panel_rib(width, handrail):
    """
    주어진 패널 너비와 핸드레일 위치에 따라 종보강 위치를 계산하여 반환합니다.
    결과는 10단위로 반올림된 정수 형태로 반환됩니다.

    :param width: 패널의 너비
    :param handrail: 핸드레일의 위치를 담은 리스트
    :return: 종보강 위치를 담은 리스트
    """
    # 종보강 개수 결정
    if width < 200:
        rib_count = 0
    elif 200 <= width < 550:
        rib_count = 1
    elif 550 <= width < 900:
        rib_count = 2
    else:  # width >= 900
        rib_count = 3

    # 종보강 위치 계산
    rib_positions = [round((i + 1) * width / (rib_count + 1) / 10) * 10 for i in range(rib_count)]

    # 핸드레일 위치를 정수형으로 변환
    handrail = [int(pos) for pos in handrail]

    # 핸드레일 위치와 충돌 체크 및 조정
    if handrail != [0]:
        for i, rib_pos in enumerate(rib_positions):
            for hr_pos in handrail:
                distance = abs(rib_pos - hr_pos)
                if distance < 60:
                    # 차이가 60이 되도록 조정
                    adjustment = 60 - distance
                    # 종보강 위치 조정
                    if rib_pos < hr_pos:
                        new_rib_pos = rib_pos - adjustment
                    else:
                        new_rib_pos = rib_pos + adjustment
                    # 패널 경계를 넘지 않도록 조정
                    rib_positions[i] = max(0, min(round(new_rib_pos / 10) * 10, width))

    # 종보강 위치가 중복되지 않도록 조정
    rib_positions = sorted(set(rib_positions))

    return rib_positions


def panel_rib_HOP(width, handrail, HOP_width, option=None):
    """
    패널 너비, 핸드레일 위치 및 HOP의 가로 너비를 고려하여 종보강 위치를 계산합니다.

    :param width: 패널의 너비
    :param handrail: 핸드레일의 위치를 담은 리스트
    :param HOP_width: HOP의 가로 너비
    :return: 종보강 위치를 담은 리스트
    """
    # HOP의 중심 위치 계산
    HOP_center = width / 2

    # HOP 타공 자리 좌우 종보강 위치 계산
    HOP_start = HOP_center - HOP_width / 2
    HOP_end = HOP_center + HOP_width / 2
    rib_positions = [round(HOP_start - 11), round(HOP_end + 11)]

    # HOP 타공 자리 중심에 추가 종보강 위치 계산
    # 핸드레일 홀과 최소 60 이상 떨어지는 위치 찾기
    additional_rib_position = HOP_center
    for hr_pos in handrail:
        if option == None :
            if abs(HOP_center - hr_pos) < 60:
                # 핸드레일이 왼쪽에 있으면 오른쪽으로, 오른쪽에 있으면 왼쪽으로 조정
                direction = -1 if HOP_center < hr_pos else 1
                additional_rib_position = hr_pos + (60 * direction)
        else:
            if abs(HOP_center + hr_pos) > 60:
                # 핸드레일이 왼쪽에 있으면 오른쪽으로, 오른쪽에 있으면 왼쪽으로 조정
                direction = -1 if HOP_center < hr_pos else 1
                additional_rib_position = hr_pos - (60 * direction)


    # 중심에서 가장 가까운 쪽으로 조정
    if additional_rib_position not in rib_positions:
        rib_positions.append(additional_rib_position)

    # 종보강 위치가 중복되지 않도록 조정하고 패널 경계를 넘지 않도록 조정
    rib_positions = sorted(set(rib_positions))
    rib_positions = [max(0, min(pos, width)) for pos in rib_positions]

    return rib_positions

def panel_rib_COP(width, center_line, COP_width, option=None):
    """
    패널 너비, 중심선 및 COP의 가로 너비를 고려하여 종보강 위치를 계산합니다.

    :param width: 패널의 너비
    :param center_line: 중심선 위치를 담은 리스트 (예: [중심 위치])
    :param COP_width: COP의 가로 너비
    :param option: 옵션 (예: 'reverse' 일 경우 종보강 위치를 뒤집음)
    :return: 종보강 위치를 담은 리스트
    """

    # 중심선 위치
    hr_pos = int(center_line[0])

    # 중심 위치를 설정
    center_position = hr_pos if option != 'reverse' else width - hr_pos

    # 좌측 종보강 위치
    left_rib_position = center_position - COP_width / 2 - 11 

    # 중앙 종보강 위치
    center_rib_position = center_position

    # 우측 종보강 위치
    right_rib_position = center_position + COP_width / 2 + 11 

    # 위치 리스트 반환
    rib_positions = [
        round(left_rib_position), 
        round(center_rib_position), 
        round(right_rib_position)
    ]

    # 종보강 위치가 패널 경계를 넘지 않도록 조정
    rib_positions = [max(0, min(pos, width)) for pos in rib_positions]

    return rib_positions
    
def calculate_rib_positions(width):
    """
    주어진 패널 너비에 따라 종보강 위치를 계산하여 반환합니다.
    결과는 10단위로 반올림된 정수 형태로 반환됩니다.

    :param width: 패널의 너비
    :return: 종보강 위치를 담은 리스트
    """
    if width < 200:
        rib_count = 0
    elif 200 <= width < 550:
        rib_count = 1
    elif 550 <= width < 900:
        rib_count = 2
    else:  # width >= 900
        rib_count = 3

    if rib_count == 0:
        return []

    rib_positions = [width * i // (rib_count + 1) for i in range(1, rib_count + 1)]
    return [round(pos, -1) for pos in rib_positions]

def calculate_ribs(width, height):
    """
    주어진 패널 너비와 핸드레일 높이에 따라 보강의 개수를 계산합니다.

    :param width: 패널의 너비
    :param height: 핸드레일 높이
    :return: 80mm 보강 개수, 25mm 보강 개수
    """
    rib_positions = calculate_rib_positions(width)
    rib_width80 = 0
    rib_width25 = 0

    if height > 0:
        rib_width25 = len(rib_positions)
    else:
        rib_width80 = len(rib_positions)

    return rib_width80, rib_width25

def total_ribs():
    rib_width80_total = 0
    rib_width25_total = 0

    for i in range(1, 12):
        panel_width = eval(f"P{i}_width")
        height = eval(f"P{i}_height")
        # print (f"panel_width : {panel_width}, height : {height}")
        rib_width80, rib_width25 = calculate_ribs(panel_width, height)
        rib_width80_total += rib_width80
        rib_width25_total += rib_width25

    return rib_width80_total, rib_width25_total


####################################################################################################################################################################################
# 일체형 1page Assy
####################################################################################################################################################################################
def draw_page1():     
    global args  #수정할때는 global 선언이 필요하다. 단순히 읽기만 할때는 필요없다.    
    global start_time
    global drawdate, deadlinedate, text_style, exit_program, program_message, formatted_date, text_style_name
    global CW_raw, CD_raw, panel_thickness, su, LCframeMaterial, LCplateMaterial
    global input_CD, input_CW,CD,CW,drawdate_str , deadlinedate_str, drawdate_str_short, deadlinedate_str_short    
    global doc, msp , T5_is, text_style, distanceXpos, distanceYpos, thickness
    global P1_material, P1_width, P1_widthReal, P1_holegap, P1_hole1, P1_hole2, P1_hole3, P1_hole4, P1_COPType
    global P2_material, P2_width, P2_widthReal, P2_holegap, P2_hole1, P2_hole2, P2_hole3, P2_hole4, P2_COPType
    global P3_material, P3_width, P3_widthReal, P3_holegap, P3_hole1, P3_hole2, P3_hole3, P3_hole4, P3_COPType
    global P4_material, P4_width, P4_widthReal, P4_holegap, P4_hole1, P4_hole2, P4_hole3, P4_hole4, P4_COPType
    global P5_material, P5_width, P5_widthReal, P5_holegap, P5_hole1, P5_hole2, P5_hole3, P5_hole4, P5_COPType
    global P6_material, P6_width, P6_widthReal, P6_holegap, P6_hole1, P6_hole2, P6_hole3, P6_hole4, P6_COPType
    global P7_material, P7_width, P7_widthReal, P7_holegap, P7_hole1, P7_hole2, P7_hole3, P7_hole4, P7_COPType
    global P8_material, P8_width, P8_widthReal, P8_holegap, P8_hole1, P8_hole2, P8_hole3, P8_hole4, P8_COPType
    global P9_material, P9_width, P9_widthReal, P9_holegap, P9_hole1, P9_hole2, P9_hole3, P9_hole4, P9_COPType
    global P10_material, P10_width, P10_widthReal, P10_holegap, P10_hole1, P10_hole2, P10_hole3, P10_hole4, P10_COPType
    global P11_material, P11_width, P11_widthReal, P11_holegap, P11_hole1, P11_hole2, P11_hole3, P11_hole4, P11_COPType

    abs_x = 2000
    abs_y = 0

    ##################################################################################################
    # ASSY 판넬배열도 1page
    ##################################################################################################
    # 0,0은 좌측 하단 기준 판넬 기준점을 기억하자 

    # 각 P변수들에 대한 그룹화
    p_variables = [
        [P1_hole1, P1_hole2, P1_hole4, P1_width],
        [P2_hole1, P2_hole2, P2_hole4, P2_width],
        [P3_hole1, P3_hole2, P3_hole4, P3_width],
        [P4_hole1, P4_hole2, P4_hole4, P4_width],
        [P5_hole1, P5_hole2, P5_hole4, P5_width],
        [P6_hole1, P6_hole2, P6_hole4, P6_width],
        [P7_hole1, P7_hole2, P7_hole4, P7_width],
        [P8_hole1, P8_hole2, P8_hole4, P8_width],
        [P9_hole1, P9_hole2, P9_hole4, P9_width],
        [P10_hole1, P10_hole2, P10_hole4, P10_width],
        [P11_hole1, P11_hole2, P11_hole4, P11_width]
    ]

    # 각 그룹에 대한 계산 실행
    for holes in p_variables:
        if holes[1] is None or holes[1] == 0:
            # 계산 수행 후 새로운 값을 할당
            holes[1] = holes[3] - (holes[0] + holes[2])

    # 필요한 경우, 결과를 다시 튜플로 변환
    P1_hole2, P2_hole2, P3_hole2, P4_hole2, P5_hole2, P6_hole2, P7_hole2, P8_hole2, P9_hole2, P10_hole2, P11_hole2 = [holes[1] for holes in p_variables]

    # 변수 목록 초기화
    hole_variables = [P2_hole1, P2_hole2, P2_hole3, P2_hole4, 
                    P3_hole1, P3_hole2, P3_hole3, P3_hole4, 
                    P4_hole1, P4_hole2, P4_hole3, P4_hole4]
    
    # print (f"p_variables : {p_variables}")
    # print (f"side holes : {hole_variables}")

    limit_point = [P2_width, P2_width + P3_width, P2_width + P3_width + P4_width]
    # leftholes 리스트 초기화
    leftholes = []
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 leftholes에 추가
    for hole in hole_variables:
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                leftholes.append(hole)
                draw_circle(doc, abs_x - P1_holegap, abs_y + sum, 8, layer='0')
                # print(f"side sum: {sum}")

    # 오른쪽 벽 판넬 변수 목록 초기화
    hole_variables = [P8_hole1, P8_hole2, P8_hole3, P8_hole4, 
                    P9_hole1, P9_hole2, P9_hole3, P9_hole4, 
                    P10_hole1, P10_hole2, P10_hole3, P10_hole4]    

    limit_point = [P10_width, P10_width + P9_width, P10_width + P9_width + P8_width]
    rx = abs_x + P5_width + P6_width + P7_width - panel_width * 2 + P9_holegap
    # rightholes 리스트 초기화
    rightholes = []
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(hole_variables): 
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                rightholes.append(hole)
                draw_circle(doc, rx , abs_y + sum, 8, layer='0')        
                if index == 0 :
                    d(doc, rx + panel_width - P9_holegap , abs_y , rx  , abs_y + sum , 151, direction="right" ,option='reverse' )    
                else:
                    dc(doc,rx  , abs_y + sum)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, rx + panel_width - P9_holegap, abs_y + sum)      

    #############################################################
    # 우측 치수선
    #############################################################
    # 우측 2단 치수선
    ry = abs_y
    rx = abs_x + P5_width + P6_width + P7_width - panel_width    
    d(doc, rx, ry , rx , ry + P10_width, 264, direction="right")
    dc(doc, rx , ry + P10_width  + P9_width )    
    dc(doc, rx , ry + P10_width  + P9_width + P8_width )    

    # 우측 3단 치수선
    tstr = f"{P8_width+P9_width+P10_width}[INSIDE]"
    d(doc, rx, ry , rx , ry + P10_width + P9_width + P8_width, 374, direction="right", text=tstr)

    #############################################################
    # 후면 벽 판넬 변수 목록 초기화
    # 후면 벽 치수선표기
    #############################################################

    hole_variables = [P5_hole1, P5_hole2, P5_hole3, P5_hole4, 
                    P6_hole1, P6_hole2, P6_hole3, P6_hole4, 
                    P7_hole1, P7_hole2, P7_hole3, P7_hole4]
    
    limit_point = [P7_width, P7_width + P6_width, P5_width + P6_width + P7_width]
    rx = abs_x - panel_width
    ry = abs_y + P2_width + P3_width + P4_width

    rearholes = []
    sum = 0

    # 뒷벽 
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(hole_variables):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                rearholes.append(hole)
                draw_circle(doc, rx + sum , ry + P6_holegap , 8, layer='0')
                # print(f"sum : {sum}")
                # print(f"side sum: {sum}")
                if index == 0 :
                    d(doc, rx, ry + panel_width, rx + sum, ry + P6_holegap, 76, direction="up" , option='reverse')    
                else:
                    dc(doc, rx + sum, ry + P6_holegap)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, rx + sum, ry + panel_width)                  

    # print(f"rearholes : {rearholes}")

    # 상부 2단 치수선
    d(doc, rx, ry + panel_width, rx + P5_width, ry + panel_width, 160, direction="up")                      
    dc(doc,  rx + P5_width + P6_width, ry + panel_width )                   
    dc(doc,  rx + P5_width + P6_width + P7_width, ry + panel_width )                   
    # 상부 3단 치수선
    d(doc, rx, ry + panel_width, rx + P5_width + P6_width + P7_width, ry + panel_width, 246, direction="up")

    # 전면 벽 판넬 변수 목록 초기화
    hole_variables = [P1_hole1, P1_hole2, P1_hole3, P1_hole4, OP , P11_hole1, P11_hole2, P11_hole3, P11_hole4]
    frontholes = []    
    
    limit_point = [P1_width, P1_width + OP , P1_width + OP + P11_width]
    rx = abs_x - panel_width
    ry = abs_y 
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(hole_variables):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                draw_circle(doc, rx + sum , ry - P1_holegap , 8, layer='0')
                
    # P1 치수선                
    hole_variables = [P1_hole1, P1_hole2, P1_hole3, P1_hole4]       
    rx = abs_x - panel_width
    ry = abs_y 
    sum = 0    
    for index, hole in enumerate(hole_variables):  
        if hole is not None and hole > 0:
            sum += hole
            if index == 0 :
                d(doc,  rx , ry - panel_width, rx + sum, ry - P1_holegap, 164, direction="down" , option='reverse')    
            else:
                dc(doc, rx + sum, ry - P1_holegap)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, rx + sum, ry - P1_holegap)              
   
    # P11 치수선
    hole_variables = [P11_hole1, P11_hole2, P11_hole3, P11_hole4] 
    rx = abs_x - panel_width + P1_width + OP
    ry = abs_y 
    sum = 0    
    for index, hole in enumerate(hole_variables):  
        if hole is not None and hole > 0:
            sum += hole
            if index == 0 :
                d(doc,  rx , ry - panel_width, rx + sum, ry - P11_holegap, 164, direction="down" , option='reverse')    
            else:
                dc(doc, rx + sum, ry - P11_holegap)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, rx + sum, ry - P11_holegap)        

    rx = abs_x - panel_width                      
    # 하단 2단 치수선
    d(doc, rx, ry - panel_width , rx + P1_width, ry - column_width, 215, direction="down")                      
    dc(doc,  rx + P1_width+OP, ry - column_width, text=f"{OP}[OP]") 
    dc(doc,  rx + P1_width+OP + P11_width, ry - column_width)
    # 하단 3단 치수선 25 panel_width 표현
    d(doc, rx, ry - panel_width , rx + panel_width, ry , 350, direction="down", option='reverse')                      
    dc(doc,  rx + P1_width+OP+P11_width - panel_width, ry , text=f"{P1_width+OP+P11_width - panel_width*2}[INSIDE]") 
    dc(doc,  rx + P1_width+OP+P11_width, ry - panel_width)
                
    # 컬럼하부에 브라켓 위치지정         
    transom_upperwing = 30   
    rx = abs_x + P1_width - panel_width - column_BottomHoleHorizontal
    ry = abs_y - column_BottomHoleVertical
    d(doc, abs_x + P1_width-panel_width, abs_y, rx, ry, 150, direction="up")
    d(doc, abs_x + P1_width-panel_width, abs_y, rx, ry, 200, direction="right")    
    insert_block(rx , ry , "assy_bottombase_left")             
    rx = abs_x + P1_width + OP - column_thickness + column_BottomHoleHorizontal                       
    insert_block(rx , ry , "assy_bottombase_right")      

    # 출입구 OP 형상 그리기
    rx = abs_x + P1_width - panel_width 
    ry = abs_y - column_width
    rectangle(doc, rx,ry,rx + OP, ry + column_width, layer='2')
    # 좌우 보강 표현  (좌)  
    rectangle(doc, rx,ry,rx+40.5, ry+ 36.5, layer='2')    
    # 좌우 보강 표현  (우)  
    rectangle(doc, rx+OP-40.5,ry,rx+OP, ry+ 36.5, layer='2')    
    # 상부 날개 표현
    ry = abs_y - transom_upperwing
    rectangle(doc, rx,ry,rx+OP, ry, layer='2')
    # M볼트 표현하기     
    # Ensure that hole variables are initialized to 0 if they are None
    hole_variables = [TR_upperhole1, TR_upperhole2, TR_upperhole3, TR_upperhole4]
    hole_variables = [0 if hole is None else hole for hole in hole_variables]

    # Now you can safely calculate the limit_point
    limit_point = [TR_upperhole1 + TR_upperhole2 + TR_upperhole3 + TR_upperhole4]
    ry = abs_y - transom_upperwing / 2
    transom_upperholes = []    
    total_holes_sum = 0  
    lastpos = 0  
    # print(f"hole_variables : {hole_variables}")

    for index, hole in enumerate(hole_variables):  
        if hole > 0:
            total_holes_sum += hole
            if total_holes_sum not in limit_point:
                transom_upperholes.append(hole)
                m14(doc, rx + total_holes_sum, ry)
                if index > 0 :
                    if index == 1 :
                        d(doc,  rx + lastpos, ry , rx + total_holes_sum, ry , 78, direction="up" )
                    else:
                        dc(doc, rx + total_holes_sum, ry - P11_holegap)                               
                lastpos = total_holes_sum

    # P1번 COP 적용시 그려주기
    rx = abs_x - panel_width                    
    if P1_COPType == 'COP 적용':
        COP_assy_height = 47.5
        xrectangle(doc, rx + P1_width/2 - COP_width/2, abs_y - COP_assy_height, rx + P1_width/2 - COP_width/2 + COP_width,abs_y , layer='0' )
                
    # P1 
    panel_wing = 11
    line(doc, abs_x - panel_width + panel_wing , abs_y - panel_width , abs_x - panel_width  , abs_y - panel_width , layer='0')
    lt(doc,  0  , panel_width , layer='0')
    lt(doc,  P1_width , 0  , layer='0')
    lt(doc,  0 , - column_width , layer='0')
    lt(doc,   - column_thickness  , 0 , layer='0')
    lt(doc,   0 , panel_wing , layer='0')
    # P2
    line(doc, abs_x - panel_width , abs_y  + panel_wing  , abs_x - panel_width  , abs_y  , layer='0')
    lt(doc,  panel_width ,  0 , layer='0')
    lt(doc,  0 , P2_width , layer='0')
    lt(doc,  - panel_width ,  0  , layer='0')
    lt(doc,  0 ,  - panel_wing , layer='0')
    # P3
    rx = abs_x
    ry = abs_y + P2_width
    line(doc, rx - panel_width , ry  + panel_wing  , rx - panel_width  , ry  , layer='0')
    lt(doc,  panel_width ,  0 , layer='0')
    lt(doc,  0 , P3_width , layer='0')
    lt(doc,  - panel_width ,  0  , layer='0')
    lt(doc,  0 ,  - panel_wing , layer='0')
    # P4
    rx = abs_x
    ry = abs_y + P2_width  + P3_width 
    line(doc, rx - panel_width , ry  + panel_wing  , rx - panel_width  , ry  , layer='0')
    lt(doc,  panel_width ,  0 , layer='0')
    lt(doc,  0 , P4_width , layer='0')
    lt(doc,  - panel_width ,  0  , layer='0')
    lt(doc,  0 ,  - panel_wing , layer='0')
    # P5
    rx = abs_x 
    ry = abs_y + P2_width + P3_width + P4_width 
    line(doc, rx - panel_width + panel_wing , ry  + panel_width  , rx - panel_width , ry  + panel_width  , layer='0')
    lt(doc,  0 , - panel_width  , layer='0')
    lt(doc,  P5_width , 0  , layer='0')
    lt(doc,  0 ,  panel_width , layer='0')
    lt(doc,   - panel_wing , 0 , layer='0')    
    # P6
    rx = abs_x + P5_width 
    ry = abs_y + P2_width + P3_width + P4_width
    line(doc, rx - panel_width + panel_wing , ry  + panel_width, rx - panel_width , ry  + panel_width  , layer='0')
    lt(doc,  0 , - panel_width , layer='0')
    lt(doc,  P6_width , 0 , layer='0')
    lt(doc,  0 , panel_width , layer='0')
    lt(doc,  - panel_wing , 0, layer='0')          
    # P7
    rx = abs_x + P5_width + P6_width 
    ry = abs_y + P2_width + P3_width + P4_width
    line(doc, rx - panel_width + panel_wing , ry + panel_width, rx - panel_width , ry  + panel_width  , layer='0')
    lt(doc,  0 , - panel_width , layer='0')
    lt(doc,  P7_width , 0 , layer='0')
    lt(doc,  0 , panel_width , layer='0')
    lt(doc,  - panel_wing , 0, layer='0')                  
    # P8 우측벽시작
    rx = abs_x + P5_width + P6_width + P7_width - panel_width
    ry = abs_y + P10_width + P9_width + P8_width
    line(doc, rx   , ry  - panel_wing  , rx   , ry  , layer='0')
    lt(doc,  - panel_width , 0, layer='0')
    lt(doc,  0, - P8_width  , layer='0')
    lt(doc,  panel_width, 0 , layer='0')
    lt(doc,  0,  panel_wing , layer='0')          
    # P9 우측벽
    rx = abs_x + P5_width + P6_width + P7_width - panel_width
    ry = abs_y + P10_width + P9_width 
    line(doc, rx   , ry  - panel_wing  , rx   , ry  , layer='0')
    lt(doc,  - panel_width , 0, layer='0')
    lt(doc,  0, - P9_width  , layer='0')
    lt(doc,  panel_width, 0 , layer='0')
    lt(doc,  0,  panel_wing , layer='0')      
    # P10 우측벽
    rx = abs_x + P5_width + P6_width + P7_width - panel_width
    ry = abs_y + P10_width 
    line(doc, rx   , ry  - panel_wing  , rx   , ry  , layer='0')
    lt(doc,  - panel_width , 0, layer='0')
    lt(doc,  0, - P10_width  , layer='0')
    lt(doc,  panel_width, 0 , layer='0')
    lt(doc,  0,  panel_wing , layer='0')          
    # P11 전면
    rx = abs_x + P5_width + P6_width + P7_width - panel_width
    ry = abs_y 
    line(doc, rx - panel_wing  , ry  - panel_width , rx  , ry - panel_width , layer='0')
    lt(doc,  0 ,  panel_width , layer='0')
    lt(doc,  - P11_width , 0 , layer='0')
    lt(doc,  0 , - column_width , layer='0')
    lt(doc,  column_thickness , 0 , layer='0')
    lt(doc,  0 , panel_wing , layer='0')

    # 핸드레일 적색선 표현
    # HRsidegap 리스트 초기화
    HRsidegap = []
    if handrailSidegap1 is not None:
        HRsidegap.append(handrailSidegap1)
    if handrailSidegap2 is not None:
        HRsidegap.append(handrailSidegap2)
    if handrailSidegap3 is not None:
        HRsidegap.append(handrailSidegap3)
    if handrailSidegap4 is not None:
        HRsidegap.append(handrailSidegap4)
    if handrailSidegap5 is not None:
        HRsidegap.append(handrailSidegap5)    

    rx = abs_x 
    rxnext = abs_x + P5_width + P6_width + P7_width  - panel_width*2
    ry = abs_y
    gap = 0
    # 리스트의 총 길이를 구함
    total_length = len(HRsidegap)    
    for index, g in enumerate(HRsidegap):
        gap += g
        if g is not None and index < total_length - 1:  # 마지막 요소를 제외하고 실행
            line(doc, rx - 20, ry + gap, rx + 20, ry + gap, layer='3')
            line(doc, rxnext - 20, ry + gap, rxnext + 20, ry + gap, layer='3')
            if index == 0 :
                d(doc, rx-panel_width, ry, rx, ry+gap, 90, direction="left" )                            
            else:
                dc(doc, rx, ry+gap)        
    dc(doc, rx-panel_width, ry+gap)                      

    # Rear Handrail        
    # HRsidegap 리스트 초기화
    HRreargap = []
    if handrailReargap1 is not None:
        HRreargap.append(handrailReargap1)
    if handrailReargap2 is not None:
        HRreargap.append(handrailReargap2)
    if handrailReargap3 is not None:
        HRreargap.append(handrailReargap3)
    if handrailReargap4 is not None:
        HRreargap.append(handrailReargap4)
    if handrailReargap5 is not None:
        HRreargap.append(handrailReargap5)    

    rx = abs_x - panel_width    
    ry = abs_y + P2_width + P3_width + P4_width 
    gap = 0    
    # 리스트의 총 길이를 구함
    total_length = len(HRreargap)

    for index, g in enumerate(HRreargap):
        gap += g
        if g is not None and index < total_length - 1:  # 마지막 요소를 제외하고 실행
            line(doc, rx + gap, ry - 20, rx + gap, ry + 20, layer='3')
        if index == 0 :
            d(doc, rx, ry, rx + gap, ry-20, 110, direction="down" )    
        else:
            dc(doc, rx + gap, ry-20)    

    # P1~P11 화면에 부호 출력하기
    numprint(doc,abs_x+P1_width/2 ,abs_y + 60 , 'P01', layer='문자')
    numprint(doc,abs_x+P1_width+OP+P11_width/2 ,abs_y + 60 , 'P11', layer='문자')
    numprint(doc,abs_x+100 ,abs_y + P2_width/2 , 'P02', layer='문자')
    numprint(doc,abs_x+100 ,abs_y + P2_width + P3_width/2 , 'P03', layer='문자')
    numprint(doc,abs_x+100 ,abs_y + P2_width + P3_width + P4_width/2 , 'P04', layer='문자')
    numprint(doc,abs_x + P5_width /2 + 50 ,abs_y + P2_width + P3_width + P4_width - 50 , 'P05', layer='문자')
    numprint(doc,abs_x + P5_width  + P6_width/2+ 50 ,abs_y + P2_width + P3_width + P4_width - 50 , 'P06', layer='문자')
    numprint(doc,abs_x + P5_width  + P6_width + P7_width/2 + 50 ,abs_y + P2_width + P3_width + P4_width - 50 , 'P07', layer='문자')
    numprint(doc,abs_x + P5_width  + P6_width + P7_width - 130 ,abs_y + P2_width + P3_width + P4_width/2 , 'P08', layer='문자')
    numprint(doc,abs_x + P5_width  + P6_width + P7_width - 130 ,abs_y + P2_width + P3_width/2 , 'P09', layer='문자')
    numprint(doc,abs_x + P5_width  + P6_width + P7_width - 130 ,abs_y + P2_width/2, 'P10', layer='문자')

    #############################################################
    # Assy 단면도 그리기 1page
    #############################################################
    rx = abs_x - 930
    ry = abs_y - 170
    insert_block(rx,ry,"panel_section")
    # FH 바닥마감
    d(doc, rx+231.3 , ry- 236.2 , rx + 231.3 , ry - 277.5, 70, direction="right", text=f"바닥두께:{FH}" )
    # KH, KPH
    d(doc, rx+231.3 , ry- 277.5 , rx + 102.8 , ry - 30.9, 200, direction="right" , text=f"{KPH}" )
    d(doc, rx + 102.8 , ry - 30.9, rx + 127.7 , ry , 200, direction="right" , text=f"5" )
    dc(doc,rx + 127.7 , ry + 1920 , text=f"WH={CPH}" )
    dc(doc,rx + 238.8 , ry + 1957.8 , text=f"5" )
    d(doc, rx+231.3 , ry- 236.2 , rx + 238.8 , ry + 1957.8 , 250, direction="right", text=f"{CH}[CH]" )
    d(doc, rx + 238.8 - 60.9 - 111.1 , ry+1787.8 + 132.2 + 30.9 , rx + 238.8  - 111.1, ry+1787.8 + 132.2, 150, direction="up" , text=f"{P1_holegap}" )

    # ASY 코멘트 달기
    text = f"발주처 : {company}"
    rx = abs_x + (P1_width+OP) / 3
    ry = abs_y + (P2_width+P3_width)
    draw_Text(doc, rx, ry, 40, text, layer='0')
    text = f"인승 : {person} , {usage}"    
    ry -= 80
    draw_Text(doc, rx, ry, 40, text, layer='0')
    text = f"CW : {CW} , CD : {CD}"    
    ry -= 80
    draw_Text(doc, rx, ry, 40, text, layer='0')
    text = f"Handrail 높이 : {handrail_height}"    
    ry -= 80
    draw_Text(doc, rx, ry, 40, text, layer='0')
    text = f"COP 가로:{COP_width}x가로:{COP_height}x높이:{COP_bottomHeight}"    
    ry -= 80
    draw_Text(doc, rx, ry, 40, text, layer='0')
    text = f"HOP 가로:{HOP_width}x가로:{HOP_height}x높이:{HOP_bottomHeight}"    
    ry -= 80
    draw_Text(doc, rx, ry, 40, text, layer='0')

    # 도면틀 넣기
    BasicXscale = 6851
    BasicYscale = 4115
    TargetXscale = CW + 3390
    TargetYscale = CD + 1700
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
    # print("1page 스케일 비율 : " + str(frame_scale))   
    frameYpos = abs_y - 1700 * frame_scale     
    insert_frame(abs_x-2000  , frameYpos  , frame_scale, "drawings_frame", "CAGE ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   
    
    TargetYscale = TargetYscale*frame_scale

    frameXpos = abs_x + TargetXscale * frame_scale + 700


    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################

    ###################################################
    # 2page P1 일체형 전개도
    ###################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 6851 
    TargetYscale = 4870 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    current_page = 2
    # print("{current_page} page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "FRONT PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale
    # insert_block(rx1 , ry , "lc035_frame_section_side")    

    x1 = math.floor(pagex)
    y1 = math.floor(pagey) - 100
    x2 = x1 + panel_wing + column_thickness + column_width + P1_width - panel_width/2 - br*6
    y2 = y1    
    x3 = x2 + panel_width/2 + panel_width + panel_wing - br*4  # panel_width/2는 끝기준 장공 위치
    y3 = y2 
    x4 = x3
    y4 = y3 + FH
    x5 = x4 
    y5 = y4 + OPH 
    x6 = x5 
    y6 = y5 + CH - OPH - FH 
    x7 = x6 + (panel_width/2 + panel_width + panel_wing - br*4 ) * - 1
    y7 = y6 
    x8 = x7 - ( panel_wing + column_thickness + column_width + P1_width + panel_width + panel_wing - br*10 ) + (panel_wing+column_thickness+46) - (panel_width/2 + panel_width + panel_wing - br*4 )* -1
    y8 = y7 
    x9 = x8 
    y9 = y8  - CH + OPH + FH  + 40
    x10 = x1 
    y10 = y9 
    x11 = x10 
    y11 = y10 - 40
    x12 = x11 
    y12 = y11 - OPH

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
      
    #절곡라인  (히든선 : 세로 CLphantom)      
    line(doc, x2, y2, x7, y7,  layer='CLphantom')
    #절곡라인  (히든선 : 가로 magentaphantom)      
    line(doc, x11-30, y11, x5, y5,  layer='magentaphantom')
    line(doc, x12-30, y12, x4, y4,  layer='magentaphantom')

    # 하부 치수선
    d(doc, x1,y1,x3,y3,200,direction="down")
    d(doc, x2,y2,x3,y3,125,direction="down")

    # 장공표시 #P01, P11은 일체형일 경우 만들어본다.
    gap = 0
    hole = calculate_holeArray(KPH+popnut_height+135, 400, KPH+popnut_height+OPH+200 , CH)
    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(x2, y2 + g, "8x16_vertical")
        if index == 0 :
            d(doc, x2, y3, x2, y2 + g, 180, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  x2, y2 + g, x2-100, y2 + g + 100,   text, direction="left")
        else:
            dc(doc, x2, y2 + g)    
    dc(doc, x6, y6)    

    # 8x16 수평모양 slot 장공 3개 위치 지정
    tx = x11 + panel_wing + column_thickness + column_width - 18 - br * 4
    ty = y11 + 50
    tx1 = tx - 25
    ty1 = y11 + TRH - 50 
    insert_block(tx, ty, "8x16_horizontal")    
    insert_block(tx, ty1, "8x16_horizontal")   
    ty2 = y11 + 20
    insert_block(tx1, ty2, "8x16_horizontal")    
    d(doc, tx ,ty2 ,tx, ty, 171, direction="right", option='reverse' )
    dc(doc, tx , ty1)
    dc(doc, tx, y8)
    d(doc, tx1, ty2, tx1, y11, 80, direction="right")

    # 장공 치수선
    d(doc, x10, y10, tx1, ty2, 60, direction="up")
    d(doc, x10, y10, x8, y8, 100, direction="up")
    d(doc, x10, y10, tx, ty1, 240, direction="up")
    d(doc, tx, ty,  tx1, ty2, 85, direction="down")

    # 왼쪽 치수선
    d(doc, x8, y8, x10, y10, 180, direction="left")
    dc(doc, x11, y11,option='reverse')
    d(doc, x8, y8, x11, y11, 260, direction="left")
    dc(doc, x12, y12)
    dc(doc, x1, y1,option='reverse')

    #################################
    # COP타공
    ##################################    
    tx1 = x1 + panel_wing + column_thickness + column_width - br*6 + COP_centerdistance - COP_width/2
    ty1 = y1 + KPH + COP_bottomHeight 
    tx2 = tx1 + COP_width
    ty2 = ty1
    tx3 = tx2
    ty3 = ty2 + COP_height
    tx4 = tx3 - COP_width
    ty4 = ty3
    rectangle(doc, tx1 , ty1, tx3, ty3, layer="레이져" )
    tx5=(tx1+tx2)/2
    ty5=ty1
    tx6=(tx3+tx4)/2
    ty6=ty3
    line(doc, tx5, ty5-20,  tx6, ty6+20,  layer='CLphantom')    
    d(doc, x1, ty1, tx5, ty5, 80, direction='up')
    dc(doc, x3, ty5)    

    d(doc, tx1, ty1, tx2, ty2, 145, direction='down')
    d(doc, tx4, ty4, tx1, ty1, 153, direction='left')
    dc(doc, tx4, y1)

    #################################
    # 세화정공 헤더표시
    ##################################
    # 장공표시 #P01, P11은 일체형일 경우 만들어본다.
    hole = [90, 50, 90 , 50]
    limit = TRH
    xp = x3-panel_wing -11
    gap = 0    
    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            cross10(doc, xp, y5 + gap)
        if index == 1 :
            d(doc, xp, y5+ pre_gap, xp, y5 + gap, 250, direction="right", option='reverse' )    
        elif index != 0 :
            dc(doc, xp, y5 + gap)   
        pre_gap = gap 
            
    # 지시선 추가 4-M8육각
    text = "4-M8육각"
    dim_leader(doc,  xp, y5 + gap , x6+200, y6 + 150,   text, direction="right")    

    #######################################
    # 1page P1 단면도
    #######################################
    x1 = x1 + column_thickness*2 + column_width + panel_wing - br*7
    y1 = pagey + CH + 500 + column_width - panel_wing
    x2 = x1 
    y2 = y1 + panel_wing   
    x3 = x2 - column_thickness
    y3 = y2 
    x4 = x3
    y4 = y3 - column_width
    x5 = x4 + P1_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_width
    x7 = x6 - panel_wing
    y7 = y6 
    x8 = x7 
    y8 = y7 - thickness 
    x9 = x8 + panel_wing - thickness
    y9 = y8 
    x10 = x9 
    y10 = y9 - panel_width + thickness*2 
    x11 = x10 - P1_width + thickness*2 
    y11 = y10
    x12 = x11 
    y12 = y11 + column_width - thickness*2 
    x13 = x12 + column_thickness - thickness*2 
    y13 = y12
    x14 = x13 
    y14 = y13 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 14
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x15 = x4
    y15 = y4 + 18
    x16 = x15
    y16 = y15 + 25
    x17 = x5 - panel_width/2
    y17 = y5
    x18 = x4 + COP_centerdistance
    y18 = y4
    line(doc, x15-10, y15, x15+10, y15, layer="CL")     
    line(doc, x16-10, y16, x16+10, y16, layer="CL")     
    line(doc, x17, y17-10, x17, y17+10, layer="CL")     
    line(doc, x18, y18-20, x18, y18+20, layer="0")     
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 108, direction='right')   
    d(doc, x2, y2, x3, y3, 85, direction='up')   
    # 좌측
    d(doc, x2, y2, x3, y3, 85, direction='up')  
    d(doc, x3, y3, x4, y4, 184, direction='left')  
    d(doc, x16, y16, x15-10, y15, 95, direction='left')  
    d(doc,  x4, y4, x15-10, y15, 95, direction='left')  
    # 하부
    d(doc, x4, y4, x18, y18-20, 95, direction='down')  
    d(doc, x17, y17-10, x5, y5, 95, direction='down')  
    d(doc, x4, y4, x5, y5, 200, direction='down')  
    # 우측 상부
    d(doc, x5, y5, x6, y6, 100, direction='right')  
    d(doc, x6, y6, x7, y7, 85, direction='up')  

    # description    
    desx = x1 + P1_width/2 - 200
    desy = y1 + 450
    textstr = f"Part Name : #1"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Spec}"    
    draw_Text(doc, desx , desy -60 , 35, str(textstr), layer='0')    
    textstr = f"Quantity : {SU} EA"    
    draw_Text(doc, desx , desy - 120 , 35, str(textstr), layer='0')        

    ###################################################
    # P11 일체형 전개도
    ###################################################

    rx = math.floor(pagex + P1_width+ column_width + column_thickness + panel_width + panel_wing *2 + 770 )  # 770은 두 객체의 간격   
    ry = math.floor(pagey) - 100

    x1 = rx 
    y1 = ry
    x2 = x1 + panel_width/2 + panel_width + panel_wing - br*4  # panel_width/2는 끝기준 장공 위치
    y2 = y1    
    x3 = x2 + panel_wing + column_thickness + column_width + P11_width - panel_width/2 - br*6
    y3 = y2 
    x4 = x3
    y4 = y3 + FH
    x5 = x4 
    y5 = y4 + OPH 
    x6 = x5 
    y6 = y5 + 40
    x7 = x6  - (column_thickness + panel_wing + column_width - br*4 - 30) 
    y7 = y6 
    x8 = x7 
    y8 = y7 + CH - OPH - FH  - 40 
    x9 = x1 + (panel_width/2 + panel_width + panel_wing - br*4 ) 
    y9 = y8  
    x10 = x1 
    y10 = y9 
    x11 = x10 
    y11 = y10 + (CH - OPH - FH ) * -1
    x12 = x11 
    y12 = y11 - OPH

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
      
    #절곡라인  (히든선 : 세로 CLphantom)      
    line(doc, x2, y2, x9, y9,  layer='CLphantom')
    #절곡라인  (히든선 : 가로 magentaphantom)      
    line(doc, x11-30, y11, x5, y5,  layer='magentaphantom')
    line(doc, x12-30, y12, x4, y4,  layer='magentaphantom')

    # 하부 치수선
    d(doc, x1,y1,x3,y3, 200,direction="down")
    d(doc, x2,y2,x1,y1, 125,direction="down")

    # 장공표시 #P01, P11은 일체형일 경우 만들어본다.
    gap = 0
    hole = calculate_holeArray(KPH+popnut_height+135, 400, KPH+popnut_height+OPH+200 , CH)
    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(x2, y2 + g, "8x16_vertical")
        if index == 0 :
            d(doc, x1, y1, x2, y2 + g, 180, direction="left" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  x2, y2 + g, x2+100, y2 + g + 100,   text, direction="right")
        else:
            dc(doc, x2, y2 + g)

    dc(doc, x10, y10)

    # 8x16 slot 장공 3개 위치 지정
    tx = x5 + (panel_wing + column_thickness + column_width - 18 - br * 4 ) * -1
    ty = y5 + 50
    tx1 = tx + 25
    ty1 = y5 + TRH - 50 
    insert_block(tx, ty, "8x16_horizontal")    
    insert_block(tx, ty1, "8x16_horizontal")   
    tx2 = tx1
    ty2 = y5 + 20
    insert_block(tx1, ty2, "8x16_horizontal")    
    # 왼쪽 장공 치수선
    d(doc, tx, ty2, tx1 ,ty , 171, direction="left")
    dc(doc, tx , ty1)
    dc(doc, tx,  y8 ,option='reverse' )

    d(doc, tx1, ty2, tx1, y5, 80, direction="left" )

    # 장공 치수선
    d(doc, x6, y6, tx2, ty2, 60, direction="up")
    d(doc, x6, y6, x8, y8, 100, direction="up")
    d(doc, x6, y6, tx, ty1, 240, direction="up")
    d(doc, tx, ty,  tx1, ty2, 85, direction="down")

    # 우측 치수선
    d(doc, x8, y8, x6, y6, 180, direction="right")
    dc(doc, x5, y5)
    d(doc, x8, y8, x5, y5, 260, direction="right")
    dc(doc, x12, y12)
    dc(doc, x1, y1)
    d(doc, x3, y3, x8, y8, 360, direction="right")    

    #################################
    # 세화정공 헤더표시 (십자표시)
    #################################
    # 장공표시 #P01, P111은 일체형일 경우 만들어본다.
    hole = [90, 50, 90 , 50]
    limit = TRH
    xp = x10 + panel_wing + 11
    gap = 0    
    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            cross10(doc, xp, y5 + gap)
            if index == 1 :
                d(doc, xp, y5+ pre_gap, xp, y5 + gap, 300, direction="left", option='reverse' )    
            elif index != 0 and index != len(hole)-1 :
                dc(doc, xp, y5 + gap)               
            else:
                dc(doc, xp, y5 + gap, option='reverse')                            
        pre_gap = gap 
            
    # 지시선 추가 4-M8육각
    text = "4-M8육각"
    dim_leader(doc,  xp, y5 + gap , x10-100, y10 + 150,   text, direction="left")    

    #######################################
    # 1page P11 단면도
    #######################################
    rx = x12 + panel_width  + panel_wing*2 - br*5
    ry = pagey + CH + 500 + panel_width

    x1 = rx 
    y1 = ry
    x2 = x1 - panel_wing   
    y2 = y1 
    x3 = x2 
    y3 = y2 - panel_width
    x4 = x3 + P11_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + column_width
    x6 = x5 - column_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 - panel_wing
    x8 = x7 + thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 + panel_wing - thickness
    x10 = x9 + column_thickness - thickness*2 
    y10 = y9 
    x11 = x10 
    y11 = y10 - column_width + thickness*2 
    x12 = x11 - P11_width +  thickness*2 
    y12 = y11 
    x13 = x12 
    y13 = y12 + panel_width - thickness*2 
    x14 = x13 + panel_wing - thickness
    y14 = y13 
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 14
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x15 = x4
    y15 = y4 + 18
    x16 = x15
    y16 = y15 + 25
    x17 = x3 + panel_width/2
    y17 = y3
    if P11_COPType =='COP 적용':
        x18 = x4 - COP_centerdistance
        y18 = y4
        line(doc, x18, y18-20, x18, y18+20, layer="0")     
    line(doc, x15-10, y15, x15+10, y15, layer="CL")     
    line(doc, x16-10, y16, x16+10, y16, layer="CL")     
    line(doc, x17, y17-10, x17, y17+10, layer="CL")     

    # 상부 치수선
    d(doc, x2, y2, x1, y1,  85, direction='up')       
    # 좌측
    d(doc, x2, y2, x3, y3, 85, direction='left') 
    # 하부
    d(doc, x3, y3, x17, y17-10, 100, direction='down')  
    d(doc, x3, y3, x4, y4, 184, direction='down')  
    d(doc, x16+10, y16, x15+10, y15, 95, direction='right',option='reverse')  
    d(doc, x4, y4, x15+10, y15, 95, direction='right',option='reverse')  
    d(doc, x4, y4, x5, y5, 200, direction='right')  
    # 우측 상부
    d(doc, x6, y6, x5, y5, 85, direction='up')  
    d(doc, x6, y6, x7, y7, 100, direction='left')  

    # description    
    desx = x1 + P11_width/2 - 200
    desy = y1 + 450
    textstr = f"Part Name : #11"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Spec}"    
    draw_Text(doc, desx , desy -60 , 35, str(textstr), layer='0')    
    textstr = f"Quantity : {SU} EA"    
    draw_Text(doc, desx , desy - 120 , 35, str(textstr), layer='0')        

    ###################################################
    # P1 일체형 조립도 (상부에 위치한 단면도)
    ###################################################
    rx = math.floor(rx + P11_width+ column_width + column_thickness + panel_width + panel_wing *2 + 1240 + 115.8)
    ry = pagey + CH + 500 + column_width - panel_wing

    x1 = rx 
    y1 = ry 
    x2 = x1 - panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 + P1_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - column_width
    x6 = x5 - column_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 + panel_wing
    x8 = x7 + thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  - panel_wing + thickness
    x10 = x9 + column_thickness - thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + column_width - thickness*2
    x12 = x11 - P1_width + thickness*2
    y12 = y11 
    x13 = x12 
    y13 = y12 - panel_width + thickness*2
    x14 = x13 + panel_wing - thickness
    y14 = y13    

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 14
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   

    # 보강표현 475이면 5미리 작은 470 원리 23 높이는 panel_width-2 적용
    rectangle(doc, x12, y12, x11, y11 - panel_width + 3 , layer='구성선')
    rectangle(doc, x11, y11 - panel_width + 3, x11-column_thickness+4, y11 - column_width+5, layer='구성선')

    # 전면 벽 판넬 변수 목록 초기화
    hole_variables = [P1_hole1, P1_hole2, P1_hole3, P1_hole4]
    frontholes = []    

    # print (f"hole val : {hole_variables}")
    limit_point = [P1_width]
    tx = x3 
    ty = y3 - P1_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(hole_variables):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                crossslot(doc, tx + sum, ty)
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 150, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)                   
       
    d(doc,  x3 , y3, x4, y4, 250, direction="up")
    d(doc,  tx , ty, x3, y3, 140, direction="left", option='reverse')
    d(doc,  x2 , y2, x3, y3, 190, direction="left")

    # 컬럼 하부 보강 
    tx, ty = x4 - column_BottomHoleHorizontal, y4 - column_BottomHoleVertical    
    crossslot(doc, tx , ty, direction="vertical")

    d(doc,  x4 , y4, tx, ty, 150, direction="right")
    d(doc,  x4 , y4, x5, y5, 250, direction="right")    
    d(doc,  x5 , y5, tx, ty, 100, direction="down")    
    d(doc,  x1 , y1, x2, y2, 100, direction="down")    

    # 중앙선 보강위치 단면도에 표기하기
    line(doc, x4 - COP_centerdistance, y4 - 10 , x4 - COP_centerdistance, y4 + 10 , layer='CLphantom')
    # 좌측선 
    bp_left = x4-COP_centerdistance-COP_width/2-1 - 10  
    # 우측선
    bp_right = x4-COP_centerdistance+COP_width/2+1 + 10
    line(doc, bp_left, y4 - 10 , bp_left, y4 + 10 , layer='CLphantom')
    line(doc, bp_right, y4 - 10 , bp_right, y4 + 10 , layer='CLphantom')
    d(doc,  x2, y2 , bp_left, y4 - 10 , 250, direction="down")    
    dc(doc, x4 - COP_centerdistance,  y4 - 10)
    dc(doc, bp_right,  y4 - 10)
    dc(doc, x5,  y5)
    # 상부에 중심거리 떨어지 치수
    d(doc,  x4, y4 , x4 - COP_centerdistance, y4+10  , 80, direction="up")    
    

    ###################################################
    # P1 일체형 조립도 본체 만들기
    ###################################################
    
    rx = math.floor(pagex + 780 + 1376 + (P11_width+ column_width + column_thickness + panel_width + panel_wing *2)*2)
    ry = pagey - 100
    rectangle(doc, rx, ry , rx+ P1_width, ry+CH, layer='0')
    rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CH, layer='0')
    rectangle(doc, rx + P1_width - panel_wing , ry , rx+P1_width-column_thickness , ry+CH , layer='0')
    line(doc, rx, ry + FH, rx+ P1_width, ry + FH, layer='magentaphantom')
    line(doc, rx+panel_wing, ry + 40 ,rx+P1_width-column_thickness , ry + 40, layer='0')
    line(doc, rx+panel_wing, ry + 41 ,rx+P1_width-column_thickness , ry + 41, layer='1')
    # 상부 3선 가로
    line(doc, rx+panel_wing, ry + CH -4,rx+P1_width-column_thickness , ry + CH -4, layer='0')
    line(doc, rx+panel_wing, ry + CH -41,rx+P1_width-column_thickness , ry + CH -41, layer='1')
    line(doc, rx+panel_wing, ry + CH -40,rx+P1_width-column_thickness , ry + CH -40, layer='0')

    # 세로선
    line(doc, rx+P1_width-COP_centerdistance, ry + CH + 25 ,rx+P1_width-COP_centerdistance , ry + 40 , layer='CLphantom')

    # COP 보강 세로방향 그리기 5개 선그리기
    bp = rx+P1_width-COP_centerdistance-COP_width/2-1  # basic point
    yp_bottom = ry + 41
    yp_upper = ry + CH -41
    xlist = [bp , bp-2 ,bp-10 ,bp-20 ,bp-25 ]   
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightxposs에 추가
    for index, xpos in enumerate(xlist):  
        if xpos is not None and xpos > 0:
            sum += xpos  
            if index == 0 or index==3 or index ==4:                      
                line(doc, xpos , yp_bottom, xpos, yp_upper, layer='0')                                
            elif index == 1 :                      
                line(doc, xpos , yp_bottom, xpos, yp_upper, layer='22')                                
            elif index == 2 :                      
                line(doc, xpos , yp_bottom, xpos, yp_upper, layer='CLphantom')                                                           
    # 우측선 그리기    
    bp = rx+P1_width-COP_centerdistance+COP_width/2+1  # basic point                
    xlist = [bp , bp+2 ,bp+10 ,bp+20 ,bp+25 ]   
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightxposs에 추가
    for index, xpos in enumerate(xlist):  
        if xpos is not None and xpos > 0:
            sum += xpos  
            if index == 0 or index==3 or index ==4:                      
                line(doc, xpos , yp_bottom, xpos, yp_upper, layer='0')                                
            elif index == 1 :                      
                line(doc, xpos , yp_bottom, xpos, yp_upper, layer='22')                                
            elif index == 2 :                      
                line(doc, xpos , yp_bottom, xpos, yp_upper, layer='CLphantom')        

    # COP 상하 고정 Bracket
    # 하부
    bp1 = rx+P1_width-COP_centerdistance-COP_width/2-1  # basic point
    bp2 = rx+P1_width-COP_centerdistance+COP_width/2+1  # basic point  
    yp_bottom_bottom = ry + KPH + COP_bottomHeight - 30 -1
    yp_bottom_upper = ry + KPH + COP_bottomHeight - 1
    rectangle(doc, bp1, yp_bottom_bottom,bp2, yp_bottom_upper, layer='0')
    rectangle(doc, bp1, yp_bottom_upper,bp2, yp_bottom_upper-1.6, layer='0')
    # COP 상하 고정 Bracket
    # 상부
    yp_top_bottom = ry + KPH + COP_bottomHeight + COP_height + 1
    yp_top_upper = ry + KPH + COP_bottomHeight + COP_height + 30 + 1
    rectangle(doc, bp1, yp_top_bottom,bp2, yp_top_upper, layer='0')
    rectangle(doc, bp1, yp_top_bottom,bp2, yp_top_bottom+1.6, layer='0') 

    # 실제타공 치수 사격형 그려주기 
    copleftbtx = bp1+1
    copleftbty = yp_bottom_upper + 1
    coprighttopx = bp2-1
    coprighttopy = yp_top_bottom - 1
    rectangle(doc, copleftbtx, copleftbty,coprighttopx, coprighttopy, layer='0') 

    # 치수선
    d(doc,  bp2, ry, bp2 ,yp_bottom_upper + 1 ,  280 , direction="right")
    dc(doc,  bp2 , yp_top_bottom - 1)
    # 우측전체선
    d(doc,  rx+P1_width, ry, rx+P1_width ,ry + CH ,  220 , direction="right")
    # 상부 2개
    d(doc,  rx, ry+CH, rx+P1_width-COP_centerdistance ,ry + CH,  150 , direction="up")
    dc(doc, rx+P1_width ,ry + CH)
    # 본체 COP 타공 상단 중간에 들어가는 치수선
    d(doc,  rx+P1_width-COP_centerdistance-COP_width/2 ,  ry + KPH + COP_bottomHeight + COP_height, rx+P1_width-COP_centerdistance+COP_width/2  , ry + KPH + COP_bottomHeight + COP_height ,  120 , direction="up")
    d(doc,  copleftbtx, coprighttopy, bp1 ,coprighttopy,  200 , direction="up")
    d(doc,  coprighttopx, coprighttopy, bp2 ,coprighttopy,  200 , direction="up")
    # 본체 COP 타공 하단 들어가는 치수선 100
    line(doc, rx+P1_width-COP_centerdistance-COP_holegap/2,ry + KPH + COP_bottomHeight-50 , rx+P1_width-COP_centerdistance-COP_holegap/2,ry + KPH + COP_bottomHeight + 50 , layer="CL")
    line(doc, rx+P1_width-COP_centerdistance+COP_holegap/2,ry + KPH + COP_bottomHeight-50 , rx+P1_width-COP_centerdistance+COP_holegap/2,ry + KPH + COP_bottomHeight + 50 , layer="CL")
    d(doc, rx+P1_width-COP_centerdistance-COP_holegap/2,ry + KPH + COP_bottomHeight-50 , rx+P1_width-COP_centerdistance+COP_holegap/2,ry + KPH + COP_bottomHeight-50  , 100 , direction="down")
    d(doc,  bp1, yp_bottom_upper,copleftbtx ,copleftbty , 60 , direction="left")

    ###################################################
    # P11 일체형 조립도 (상부에 위치한 단면도)
    ###################################################
    rx = math.floor(pagex + 780 + 1376 + (P11_width + column_width + column_thickness + panel_width + panel_wing *2)*2 + P1_width + 800)
    ry = pagey + CH + 500 + column_width - panel_wing
    
    x1 = rx + P11_width - panel_wing
    y1 = ry 
    x2 = x1 + panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 - P11_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - column_width
    x6 = x5 + column_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 + panel_wing
    x8 = x7 - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  - panel_wing + thickness
    x10 = x9 + (column_thickness - thickness*2)*-1
    y10 = y9 
    x11 = x10 
    y11 = y10 + column_width - thickness*2
    x12 = x11 - (P11_width - thickness*2) * -1
    y12 = y11 
    x13 = x12 
    y13 = y12 - panel_width + thickness*2
    x14 = x13 + (panel_wing - thickness) * -1
    y14 = y13    

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 14
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   

    # 보강표현 475이면 5미리 작은 470 원리 23 높이는 panel_width-2 적용
    rectangle(doc, x12, y12, x11, y11 - panel_width + 3 , layer='구성선')
    rectangle(doc, x11, y11 - panel_width + 3, x11+column_thickness-4, y11 - column_width+5, layer='구성선')

    # 전면 벽 판넬 변수 목록 초기화
    hole_variables = [P1_hole1, P1_hole2, P1_hole3, P1_hole4]
    frontholes = []    

    # print (f"hole val : {hole_variables}")
    limit_point = [P1_width]
    tx = x3 
    ty = y3 - P1_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(hole_variables):  
        if hole is not None and hole > 0:
            sum += hole
            frontholes.append(hole)            
            if sum not in limit_point:
                crossslot(doc, tx - sum, ty)
            if index == 0 :
                d(doc,  x3 , y3, tx - sum, ty, 150, direction="up" , option='reverse')                    
            else:
                dc(doc, tx - sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx - sum, ty)                   
       
    d(doc,  x3 , y3, x4, y4, 250, direction="up")
    d(doc,  tx , ty, x3, y3, 140, direction="right", option='reverse')
    d(doc,  x2 , y2, x3, y3, 190, direction="right")

    # 컬럼 하부 보강 
    tx, ty = x4 + column_BottomHoleHorizontal, y4 - column_BottomHoleVertical    
    crossslot(doc, tx , ty, direction="vertical")

    d(doc,  x4 , y4, tx, ty, 150, direction="left")
    d(doc,  x4 , y4, x5, y5, 250, direction="left")    
    d(doc,  x5 , y5, tx, ty, 100, direction="down")    
    d(doc,  x1 , y1, x2, y2, 100, direction="down")    

    # 중앙선 보강위치 단면도에 표기하기
    bp = rx+COP_centerdistance
    line(doc, bp, y4 - 10 , bp, y4 + 10 , layer='CLphantom')
    # 상부에 중심거리 떨어지 치수
    d(doc,  x4, y4 , bp, y4+10  , 70, direction="up")   


    ###################################################
    # P11 일체형 조립도 # P11 조립도 본체 만들기
    ###################################################
    
    ry = pagey - 100
    rectangle(doc, rx, ry , rx+ P11_width, ry+CH, layer='0')
    rectangle(doc, rx+column_thickness , ry , rx+column_thickness , ry+CH, layer='0')
    rectangle(doc, rx + P11_width - panel_wing , ry , rx+P11_width-panel_wing , ry+CH , layer='0')
    line(doc, rx, ry + FH, rx+ P11_width, ry + FH, layer='magentaphantom')
    line(doc, rx+column_thickness, ry + 40 ,rx+P11_width-panel_wing , ry + 40, layer='0')
    line(doc, rx+column_thickness, ry + 41 ,rx+P11_width-panel_wing , ry + 41, layer='1') # 1은 녹색선
    # 상부 3선 가로
    line(doc, rx+column_thickness, ry + CH -4,rx+P11_width-panel_wing , ry + CH -4, layer='0')
    line(doc, rx+column_thickness, ry + CH -41,rx+P11_width-panel_wing , ry + CH -41, layer='1')
    line(doc, rx+column_thickness, ry + CH -40,rx+P11_width-panel_wing , ry + CH -40, layer='0')

    # 세로선
    line(doc, rx+COP_centerdistance, ry + CH + 25 ,rx+COP_centerdistance , ry + 40 , layer='CLphantom')

    yp_bottom = ry + 41
    yp_upper = ry + CH -41    
                                                         
    # 종보강 우측선 그리기    
    bp = rx+COP_centerdistance-10
    # line(doc, bp , ry+CH -30, bp, ry+CH +30, layer='CLphantom')     # 보강 중심선
    xlist = [bp , bp+2 ,bp+10 ,bp+20 ,bp+25 ]   
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightxposs에 추가
    for index, xpos in enumerate(xlist):  
        if xpos is not None and xpos > 0:
            sum += xpos  
            if index == 0 or index==3 or index ==4:                      
                line(doc, xpos , yp_bottom, xpos, yp_upper, layer='0')                                
            elif index == 1 :                      
                line(doc, xpos , yp_bottom, xpos, yp_upper, layer='22')                                
            elif index == 2 :                      
                line(doc, xpos , yp_bottom, xpos, yp_upper, layer='CLphantom')        
       
    # 좌측 전체선
    d(doc,  rx, ry, rx ,ry + FH ,    150 , direction="left")
    d(doc,  rx, ry, rx ,ry + CH ,  250 , direction="left")
    # 상부 2개
    d(doc,  rx, ry+CH, rx+COP_centerdistance ,ry + CH,  150 , direction="up")
    dc(doc, rx+P11_width ,ry + CH)    
    d(doc,  copleftbtx, coprighttopy, bp1 ,coprighttopy,  200 , direction="up")
    d(doc,  coprighttopx, coprighttopy, bp2 ,coprighttopy,  200 , direction="up")        
    
    # 장공표시 #P01, P11은 일체형일 경우 만들어본다.
    gap = 0
    hole = calculate_holeArray(KPH+popnut_height+135, 400, KPH+popnut_height+OPH+200 , CH)
    tx = rx + P11_width - panel_width/2
    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(tx, ry + g, "8x16_vertical_draw")
        if index == 0 :
            d(doc, rx + P11_width, ry, tx, ry + g, 180, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  tx, ry + g, tx-100, ry + g + 100,   text, direction="left")
        else:
            dc(doc, tx, ry + g)    
    dc(doc, rx+ P11_width, ry + CH)    

    frameXpos = frameXpos + TargetXscale + 400

    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################


    ###################################################
    # 3page 보강 bracket
    ###################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 1200 + CPH 
    TargetYscale = 1500 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    # print("3page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "BRACKET DETAIL", f"WH:{CPH}", "drawing number")   

    ###################################################
    # 3page 부착면 80mm 모자보강 등 bracket P4형태에서 정보를 가져옴
    ###################################################
    
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale    
    rib_length = CPH - 2

    x1 = pagex 
    y1 = pagey + 1400
    x2 = x1 + rib_length - 12*2 
    y2 = y1    
    x3 = x2
    y3 = y2 + 39.1
    x4 = x3 + 12
    y4 = y3 
    x5 = x4 
    y5 = y4 + 38
    x6 = x5 - 12
    y6 = y5 
    x7 = x6 
    y7 = y6 + 39.1
    x8 = x7 - rib_length + 12*2 
    y8 = y7 
    x9 = x8 
    y9 = y8 - 39.1
    x10 = x9 - 12
    y10 = y9 
    x11 = x10 
    y11 = y10 - 38
    x12 = x11 + 12
    y12 = y11

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x10 가로방향 장공 레이져 layer
    x13 , y13 =  x11+6,(y10+y11)/2
    x14 , y14 =  x4-6,(y10+y11)/2
    insert_block(x13 , y13 ,"5x10_horizontal_laser") 
    insert_block(x14 , y14 ,"5x10_horizontal_laser") 
    dim_leader(doc, x13 , y13, x13+100 , y13+100,direction="right", text="2-5x10" )
      
    # 상부 치수선
    d(doc, x10,y10,x13,y13,200,direction="up")
    d(doc, x5,y5,x14,y14,200,direction="up")
    # 하부 치수선
    d(doc, x11,y11,x1,y1,100,direction="down")
    d(doc, x4,y4,x2,y2,100 ,direction="down")
    d(doc, x11,y11,x4,y4,200,direction="down")
    # 좌측 치수
    d(doc, x8,y8,x13,y13,100,direction="left")
    dc(doc, x1,y1 , option='reverse')
    d(doc, x8,y8,x1,y1,170,direction="left")
    # 우측 치수
    d(doc, x7,y7,x5,y5,120,direction="right", option='reverse')
    d(doc, x7,y7,x5,y5,120,direction="right", option='reverse')
    d(doc, x5,y5,x4,y4, 60,direction="right", option='reverse')    
    d(doc, x7,y7,x2, y2, 210,direction="right")

    # 보강산출
    global P1_height, P2_height, P3_height, P4_height, P5_height
    global P6_height, P7_height, P8_height, P9_height, P10_height, P11_height

    P1_height  = 100
    P2_height  = 0
    P3_height  = 0
    P4_height  = 0
    P5_height  = 0
    P6_height  = 0
    P7_height  = 0
    P8_height  = 100 if handrail_height > 0 else 0
    P9_height  = 0
    P10_height = 0
    P11_height = 0

    rib_width80_total, rib_width25_total = total_ribs()
    rib_width25_total = 4
    # print(f"80mm 보강 개수: {rib_width80_total}, 25mm 보강 개수: {rib_width25_total}")    

    # description    
    desx = x1 + rib_length/2 - 300
    desy = y1 - 300
    textstr = f"Part Name : 모자 보강"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 116.2 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {rib_width80_total * SU} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')           

    ################
    # 단면도 그리기
    ################    
    rib_wing = 20
    rib_height = 23.5
    rib_top_width = 40
    rib_thickness = 1.6

    x1 = x1 - 420
    y1 = y1 + 35
    x2 = x1
    y2 = y1 + rib_wing - rib_thickness
    x3 = x2 + rib_height - rib_thickness
    y3 = y2 
    x4 = x3
    y4 = y3 + rib_top_width
    x5 = x4 - rib_height + rib_thickness
    y5 = y4 
    x6 = x5 
    y6 = y5 + rib_wing - rib_thickness
    x7 = x6 - rib_thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - rib_wing
    x9 = x8 + rib_height - rib_thickness
    y9 = y8 
    x10 = x9 
    y10 = y9 - rib_top_width + rib_thickness*2
    x11 = x10 - rib_height + rib_thickness
    y11 = y10
    x12 = x11 
    y12 = y11 - rib_wing

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     
      
    # 하부 치수선
    d(doc, x12,y12,x3,y3,150,direction="down")
    # 좌측 치수
    d(doc, x8,y8,x7,y7,80,direction="left")
    d(doc, x11,y11,x12,y12,80,direction="left")
    # 우측 치수    
    d(doc, x4, y4, x3, y3, 80, direction="right", option='reverse')


############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################



    ###################################################
    # 3page HOP 보강 'ㄷ'자 보강 좌측 하단 bracket
    ###################################################    
    rx = x1
    ry = y1

    rib_length = HOP_bottomHeight  - 4
    x1 = rx + 300
    y1 = ry - 900
    x2 = x1 + rib_length - 12 - 35 
    y2 = y1    
    x3 = x2
    y3 = y2 + 26
    x4 = x3 + 35
    y4 = y3 
    x5 = x4 
    y5 = y4 + 38
    x6 = x5 - rib_length
    y6 = y5 
    x7 = x6 
    y7 = y6 - 19
    x8 = x7 + 12
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x10 가로방향 장공 레이져 layer
    x9 , y9 =  x6+5,(y6+y7)/2
    x10 , y10 =  x5-5,(y6+y7)/2
    draw_circle(doc, x9,y9, 5,layer="레이져")
    draw_circle(doc, x10,y10, 5,layer="레이져")
      
    # 상부 치수선
    d(doc, x9,y9,x6,y6,80,direction="up")
    d(doc, x6,y6,x5,y5,150,direction="up")
    # 하부 치수선
    d(doc, x1,y1,x7,y7,80,direction="down")
    d(doc, x4,y4,x2,y2,106 ,direction="down")
    # 좌측 치수    
    d(doc, x9,y9,x6,y6,106 ,direction="left")
    d(doc, x7,y7,x6,y6,170,direction="left")
    # 우측 치수
    d(doc, x2,y2,x5,y5,200,direction="right")
    d(doc, x4,y4,x2,y2,120,direction="right")

    # description    
    desx = x1 + rib_length/2 - 200
    desy = y1 - 300
    textstr = f"Part Name : HOP 하부 보강"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 64 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ################
    # 단면도 그리기 'ㄷ'자 형태 25 부착면 보강
    ################
    rib_topwing = 20
    rib_bottomwing = 25    
    rib_top_width = 23.5
    rib_thickness = 1.6

    x1 = x1 - 350
    y1 = y1 + 35
    x2 = x1 - rib_topwing 
    y2 = y1
    x3 = x2 
    y3 = y2 - rib_top_width
    x4 = x3 + rib_bottomwing
    y4 = y3 
    x5 = x4
    y5 = y4 + rib_thickness
    x6 = x5 - rib_bottomwing + rib_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 + rib_top_width - rib_thickness*2
    x8 = x7 + rib_topwing - rib_thickness
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x8 = x2 + 10
    y8 = y2

    line(doc, x8,y8-10, x8,y8+10, layer='0')
      
    # 상부 치수선
    d(doc, x8,y8,x2,y2,100,direction="up")
    d(doc, x1,y1,x2,y2,180,direction="up")
    # 하부
    d(doc, x3,y3,x4,y4,150,direction="down")
    # 좌측 치수
    d(doc, x3,y3,x2,y2,100,direction="left")
    

    ###################################################
    # 3page HOP 상단 보강 'ㄷ'자 보강 우측 하단 bracket
    ###################################################

    HOP_upper_rib_length = CPH - HOP_bottomHeight - HOP_height - 7

    x1 = rx + 400 * 2 + HOP_bottomHeight
    y1 = ry - 900
    x2 = x1 + HOP_upper_rib_length - 12 - 35
    y2 = y1    
    x3 = x2
    y3 = y2 + 26
    x4 = x3 + 35
    y4 = y3 
    x5 = x4 
    y5 = y4 + 38
    x6 = x5 - HOP_upper_rib_length
    y6 = y5 
    x7 = x6 
    y7 = y6 - 19
    x8 = x7 + 12
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x10 가로방향 장공 레이져 layer
    x9 , y9 =  x6+5,(y6+y7)/2
    x10 , y10 =  x5-5,(y6+y7)/2
    draw_circle(doc, x9,y9,5,layer="레이져")
    draw_circle(doc, x10,y10,5,layer="레이져")
      
    # 상부 치수선
    d(doc, x9,y9,x6,y6,80,direction="up")
    d(doc, x6,y6,x5,y5,150,direction="up")
    # 하부 치수선
    d(doc, x1,y1,x7,y7,80,direction="down")
    d(doc, x4,y4,x2,y2,106 ,direction="down")
    # 좌측 치수    
    d(doc, x9,y9,x6,y6,106 ,direction="left")
    d(doc, x7,y7,x6,y6,170,direction="left")
    # 우측 치수
    d(doc, x2,y2,x5,y5,200,direction="right")
    d(doc, x4,y4,x2,y2,120,direction="right")

    # description    
    desx = x1 + HOP_upper_rib_length/2 - 250
    desy = y1 - 300
    textstr = f"Part Name : HOP 상부 보강"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 64 x {str(HOP_upper_rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')    

    frameXpos = frameXpos + TargetXscale + 400

    ###################################################
    # 4page 보강 COP bracket 등 7가지 부속
    ###################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 1800 + CPH 
    TargetYscale = 1500 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    # print("3page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "BRACKET DETAIL", f"WH:{CPH}", "drawing number")   

    ###################################################
    # 4page Front판넬 보강 'ㄷ'자 보강 좌측 하단 bracket 25미리 보강
    ###################################################
    
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale    
    rib_length = CPH - 2

    rx = math.floor(pagex - 100)
    ry = math.floor(pagey + 1800)

    rib_length = P1_width  - 5
    x1 = rx
    y1 = ry
    x2 = x1 + rib_length 
    y2 = y1    
    x3 = x2
    y3 = y2 + 76.6
    x4 = x3 - rib_length
    y4 = y3 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 8x20 가로방향 장공 
    x5 , y5 =  x4+(frontholes[-1]-2.5), y4 - 10
    x6 , y6 =  x3-(frontholes[0]-2.5), y3 - 10

    # print (f"frontholes : {frontholes}")
    # draw_circle(doc, x9,y9,2.5,layer="레이져")
    insert_block(x5,y5,"8x20_horizontal_laser")
    insert_block(x6,y6,"8x20_horizontal_laser")
      
    # 상부 치수선
    d(doc, x4,y4,x5,y5,80,direction="up",option='reverse')
    dc(doc, x6,y6)
    dc(doc, x3,y3)
    # 하부 치수선
    d(doc, x1,y1,x2,y2,80,direction="down")    
    # 우측 치수
    d(doc, x6,y6,x3,y3,180,direction="right")
    d(doc, x2,y2,x3,y3,260,direction="right")

    # description    
    desx = x1 + rib_length/2 - 300
    desy = y1 - 300
    textstr = f"Part Name : P1,P11 상하 보강"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 76.6 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU*4} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ##################################
    # 단면도 그리기 'ㄷ'자 형태
    ##################################    
    rib_topwing = 21
    rib_bottomwing = 21
    rib_top_width = 40
    rib_thickness = 1.6

    x1 = x1 - 250
    y1 = y1 + 35
    x2 = x1 - rib_topwing 
    y2 = y1
    x3 = x2 
    y3 = y2 - rib_top_width
    x4 = x3 + rib_bottomwing
    y4 = y3 
    x5 = x4
    y5 = y4 + rib_thickness
    x6 = x5 - rib_bottomwing + rib_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 + rib_top_width - rib_thickness*2
    x8 = x7 + rib_topwing - rib_thickness
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x8 = x2+10
    y8 = y2

    line(doc, x8,y8-10, x8,y8+10, layer='0')
      
    # 상부 치수선
    d(doc, x8,y8,x2,y2,100,direction="up")
    d(doc, x1,y1,x2,y2,180,direction="up")
    # 하부
    d(doc, x3,y3,x4,y4,150,direction="down")
    # 좌측 치수
    d(doc, x3,y3,x2,y2,80,direction="left")

    ###################################################
    # 4page '역 ㄴ'자 1번 11번 하부 컬럼이나 일체형 기둥 고정용 바닥 bracket
    ###################################################

    rx = math.floor(pagex + P1_width + 900)
    ry = pagey + 1800

    rib_length = 40
    x1 = rx
    y1 = ry
    x2 = x1 + rib_length 
    y2 = y1    
    x3 = x2
    y3 = y2 + 82.3
    x4 = x3 - rib_length
    y4 = y3 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 8x16 세로방향 장공 
    x5 , y5 =  x1+20, y1 + 25 - (column_BottomHoleHorizontal-2)

    # print (f"frontholes : {frontholes}")
    # draw_circle(doc, x9,y9,2.5,layer="레이져")
    insert_block(x5,y5,"8x16_vertical")
      
    # 하부 치수선
    d(doc, x5,y5,x2,y2,80,direction="down")
    d(doc, x1,y1,x2,y2,140,direction="down")
    
    # 우측 치수    
    d(doc, x2,y2,x3,y3,260,direction="right")
    # 좌측 치수
    d(doc, x5,y5,x1,y1,60,direction="left")

    # description    
    desx = x1 + rib_length/2 - 300
    desy = y1 - 300
    textstr = f"Part Name : P1,P11 bracket"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 82.3 x 40 mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU*2} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ################
    # 단면도 그리기 '역 ㄴ'자 형태
    ################    

    rib_bottomwing = 25
    rib_height = 60
    rib_thickness = 1.6

    x1 = rx -  350
    y1 = y1 + 35
    x2 = x1 + rib_bottomwing 
    y2 = y1
    x3 = x2 
    y3 = y2 + rib_height
    x4 = x3 - rib_thickness
    y4 = y3 
    x5 = x4  
    y5 = y4 - rib_height + rib_thickness
    x6 = x5 - rib_bottomwing + rib_thickness
    y6 = y5

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x7 = x2 - (column_BottomHoleHorizontal-2)
    y7 = y2

    line(doc, x7,y7-10, x7,y7+10, layer='0')
        
    # 하부
    d(doc, x7,y7-10,x2,y2,100,direction="down")
    d(doc, x1,y1,x2,y2,160,direction="down")
    # 우측 치수
    d(doc, x2,y2,x3,y3,80,direction="right")

    ###################################################
    # 4page H/R bracket 
    ###################################################

    rx = math.floor(pagex + P1_width + 900 + 1000 )
    ry = pagey + 1800

    rib_length = 30
    x1 = rx
    y1 = ry
    x2 = x1 + rib_length 
    y2 = y1    
    x3 = x2
    y3 = y2 + 50
    x4 = x3 - rib_length
    y4 = y3 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 12파이 단공 
    x5 , y5 =  x1+15, y1 + 25 
    draw_circle(doc, x5,y5, 12,layer='레이져')
    dim_leader(doc, x5,y5, x5+150, y5+250, direction='right', text='%%c12 Hole')
      
    # 하부 치수선
    d(doc, x5,y5,x1,y1,80,direction="down")
    d(doc, x1,y1,x2,y2,140,direction="down")
    
    # 우측 치수    
    d(doc, x5,y5,x2,y2,150,direction="right")
    d(doc, x2,y2,x3,y3,250,direction="right")
    

    # description    
    # 핸드레일 개소를 계산해야 함.
    handrailhole_total = (len(HRsidegap)-1)*2 + len(HRreargap)-1
    # print (f"len(HRsidegap) {len(HRsidegap)} list {HRsidegap},  len(HRreargap) { len(HRreargap)} list {HRreargap}")
    desx = x1 + rib_length/2 - 200
    desy = y1 - 300
    textstr = f"Part Name : handrail bracket"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 2.0T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 50 x 30 mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU*handrailhole_total} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               


    ###################################################
    # 4page 종보강 'ㄷ'자  1.6T 따임 형태 25mm 부착면
    ###################################################
    
    rx = math.floor(pagex - 150)
    ry = pagey + 1000

    rib_length = CPH  - 2
    x1 = rx 
    y1 = ry 
    x2 = x1 + rib_length - 12 - 12 
    y2 = y1    
    x3 = x2
    y3 = y2 + 44.1
    x4 = x3 + 12
    y4 = y3 
    x5 = x4 
    y5 = y4 + 19
    x6 = x5 - rib_length
    y6 = y5 
    x7 = x6 
    y7 = y6 - 19
    x8 = x7 + 12
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x8 가로방향 장공 레이져 layer
    x9 , y9 =  x6+6,(y6+y7)/2
    x10 , y10 =  x5-6,(y6+y7)/2
    insert_block(x9,y9,"5x8_horizontal_laser")
    insert_block(x10,y10,"5x8_horizontal_laser")
      
    # 상부 치수선
    d(doc, x9,y9,x6,y6,50,direction="up")
    d(doc, x6,y6,x5,y5,100,direction="up")
    # 하부 치수선
    d(doc, x1,y1,x7,y7,80,direction="down")
    d(doc, x4,y4,x2,y2,106 ,direction="down")
    # 좌측 치수    
    d(doc, x9,y9,x6,y6,106 ,direction="left")
    d(doc, x7,y7,x6,y6,170,direction="left")
    # 우측 치수
    d(doc, x2,y2,x5,y5,200,direction="right")
    d(doc, x4,y4,x2,y2,120,direction="right")

    # description    
    desx = x5 + 400
    desy = y1 + 100
    textstr = f"Part Name : 종보강"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 63.1 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {(rib_width25_total) * SU} EA"     
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ##########################
    # 단면도 그리기 'ㄷ'자 형태
    ##########################    
    rib_topwing = 20
    rib_bottomwing = 25    
    rib_top_width = 23.5
    rib_thickness = 1.6

    x1 = x1 - 350
    y1 = y1 + 35
    x2 = x1 - rib_topwing 
    y2 = y1
    x3 = x2 
    y3 = y2 - rib_top_width
    x4 = x3 + rib_bottomwing
    y4 = y3 
    x5 = x4
    y5 = y4 + rib_thickness
    x6 = x5 - rib_bottomwing + rib_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 + rib_top_width - rib_thickness*2
    x8 = x7 + rib_topwing - rib_thickness
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x8 = x2+10
    y8 = y2

    line(doc, x8,y8-10, x8,y8+10, layer='0')
      
    # 상부 치수선
    d(doc, x8,y8,x2,y2,100,direction="up")
    d(doc, x1,y1,x2,y2,180,direction="up")
    # 하부
    d(doc, x3,y3,x4,y4,150,direction="down")
    # 좌측 치수
    d(doc, x3,y3,x2,y2,100,direction="left")
    

    ###################################################
    # 4page 종보강 'ㄷ'자  1.6T 따임없음 형태
    # 일체형일때  종보강 길이는  판넬 전체길이에서 상,하보강 붙이는면40 으로 작업해서 전체길이에서 82mm 뺀값으로 종보강값구합니다.
    ###################################################
    
    rx = math.floor(pagex - 150)
    ry = pagey + 550

    rib_length = CH  - 82
    x1 = rx 
    y1 = ry 
    x2 = x1 + rib_length 
    y2 = y1    
    x3 = x2 
    y3 = y2 + 63.1
    x4 = x3 - rib_length
    y4 = y3 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     
    
    # 하부 치수선
    d(doc, x1,y1,x2,y2,80,direction="down")    
    # 우측 치수
    d(doc, x2,y2,x3,y3,100,direction="right",option='reverse')

    # description    
    desx = x2 + 400
    desy = y1 + 100
    textstr = f"Part Name : 종보강"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy - 70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 63.1 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : 수량산출 필요 {SU} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ##########################
    # 단면도 그리기 'ㄷ'자 형태
    ##########################    
    rib_topwing = 20
    rib_bottomwing = 25    
    rib_top_width = 23.5
    rib_thickness = 1.6

    x1 = x1 - 350
    y1 = y1 + 35
    x2 = x1 - rib_topwing 
    y2 = y1
    x3 = x2 
    y3 = y2 - rib_top_width
    x4 = x3 + rib_bottomwing
    y4 = y3 
    x5 = x4
    y5 = y4 + rib_thickness
    x6 = x5 - rib_bottomwing + rib_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 + rib_top_width - rib_thickness*2
    x8 = x7 + rib_topwing - rib_thickness
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x8 = x2+10
    y8 = y2
      
    # 상부 치수선    
    d(doc, x1,y1,x2,y2,60,direction="up")
    # 하부
    d(doc, x3,y3,x4,y4,100,direction="down")
    # 좌측 치수
    d(doc, x3,y3,x2,y2,100,direction="left")


    ###################################################
    # 4page COP 고정 bracket '역 ㄱ'자 형태
    ###################################################
    
    rx = math.floor(pagex - 150)
    ry = pagey + 100

    rib_length = COP_width + 2
    mid_cut_length = COP_holegap/2  # 타공간격
    remain_length = (rib_length - mid_cut_length)/2
    x1 = rx 
    y1 = ry 
    x2 = x1 + rib_length
    y2 = y1    
    x3 = x2
    y3 = y2 + 50.3
    x4 = x3 - remain_length
    y4 = y3 
    x5 = x4 
    y5 = y4 - 23
    x6 = x5 - mid_cut_length
    y6 = y5 
    x7 = x6 
    y7 = y6 + 23
    x8 = x7 - remain_length
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x8 가로방향 장공 레이져 layer
    x9 , y9 =  x7 -  COP_holegap/4  , y7 - 10
    x10 , y10 =  x4 + COP_holegap/4  , y4 - 10
    insert_block(x9,y9,"cross_mark") # + 선
    insert_block(x10,y10,"cross_mark") 
    dim_leader(doc, x10,y10, x10+150, y10+200, direction='right', text='2-M6육각')
      
    # 상부 치수선
    d(doc, x7,y7,x4,y4,50,direction="up")
    d(doc, x9,y9,x10,y10,120,direction="up")
    # 하부 치수선
    d(doc, x1,y1,x2,y2,80,direction="down")
    # 좌측 치수    
    d(doc, x9,y9,x8,y8,80 ,direction="left")
    # 우측 치수
    d(doc, x5,y5,x3,y3,60 + extract_abs(x3,x5) , direction="right")
    d(doc, x3,y3,x2,y2,120,direction="right")

    # description    
    desx = x2 + 300
    desy = y1 + 100
    textstr = f"Part Name : COP 고정 bracket"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 50.3 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ##########################
    # 단면도 '역 ㄱ'자 형태
    ##########################    
    rib_topwing = 23    
    rib_top_width = 30
    rib_thickness = 1.6

    x1 = x1 - 350
    y1 = y1 - 50
    x2 = x1 - rib_topwing 
    y2 = y1
    x3 = x2 
    y3 = y2 - rib_top_width
    x4 = x3 + rib_thickness
    y4 = y3 
    x5 = x4
    y5 = y4 + rib_top_width - rib_thickness
    x6 = x5 + rib_topwing - rib_thickness
    y6 = y5 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x8 = x2+13
    y8 = y2

    line(doc, x8,y8-10, x8,y8+10, layer='0')
      
    # 상부 치수선
    d(doc, x8,y8,x2,y2,100,direction="up")
    d(doc, x1,y1,x2,y2,180,direction="up")    
    # 좌측 치수
    d(doc, x3,y3,x2,y2,100,direction="left")

    ###################################################
    # 4page HOP 고정 bracket '역 ㄱ'자 형태 (두번째 전개도)
    ###################################################
    
    rx = math.floor(pagex + 1400)

    rib_length = HOP_width + 2
    mid_cut_length = HOP_holegap/3
    remain_length = (rib_length - mid_cut_length)/2
    x1 = rx 
    y1 = ry 
    x2 = x1 + rib_length
    y2 = y1    
    x3 = x2
    y3 = y2 + 50.3
    x4 = x3 - remain_length
    y4 = y3 
    x5 = x4 
    y5 = y4 - 23
    x6 = x5 - mid_cut_length
    y6 = y5 
    x7 = x6 
    y7 = y6 + 23
    x8 = x7 - remain_length
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x8 가로방향 장공 레이져 layer
    x9 , y9 =  x7 - HOP_holegap/3 , y7 - 10
    x10 , y10 =  x4 + HOP_holegap/3 , y4 - 10
    insert_block(x9,y9,"cross_mark") # + 선
    insert_block(x10,y10,"cross_mark") 
    dim_leader(doc, x10,y10, x10+150, y10+200, direction='right', text='2-M6육각')
      
    # 상부 치수선
    d(doc, x7,y7, x4,y4,50,direction="up")
    d(doc, x9,y9,x10,y10,120,direction="up")
    
    # 하부 치수선
    d(doc, x1,y1,x2,y2,80,direction="down")
    # 좌측 치수    
    d(doc, x9,y9,x8,y8,80 ,direction="left")
    # 우측 치수
    d(doc, x5,y5,x3,y3,60 + extract_abs(x3,x5) , direction="right")
    d(doc, x3,y3,x2,y2,120,direction="right")

    # description
    desx = x2 + 400
    desy = y1 + 100
    textstr = f"Part Name : HOP 고정 bracket"
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 50.3 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')        

    frameXpos = frameXpos + TargetXscale + 400










    #########################################################################################
    # 5page P2, P8 같으면 하나만 표시
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 6851 
    TargetYscale = 4870 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    # print("page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "SIDE PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # P2 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
    ###################################################
    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx + panel_wing
    y1 = ry + CH + 500
    x2 = x1 - panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 + P2_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 + thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  + panel_width - thickness*2
    x10 = x9 - P2_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 - panel_width + thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   
    
    x13, y13 =  x1-10, y3-P2_holegap
    line(doc, x3-10, y3-P2_holegap, x3 + 10, y3-P2_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y4-P2_holegap, x4 + 10, y4-P2_holegap , layer='CLphantom') # '구성선' 회색선
    rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')

    if handrail_height > 0 :
        panel_widths = {'P2': P2_width, 'P3': P3_width, 'P4': P4_width}    
        # 함수 호출 및 결과 확인 (필요한 경우 테스트 코드 작성)
        panel_name_to_search = 'P2'
        P2_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P2_handrailxpos}")

        panel_name_to_search = 'P3'
        P3_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P3_handrailxpos}")

        panel_name_to_search = 'P4'
        P4_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P4_handrailxpos}")

        # 오른쪽 벽면은 기존의 리스트를 역순으로 리스트 정리한다. 비 대칭일경우를 대비해서 코드를 이렇게 짠다.
        HRsidegap_reversed = list(reversed(HRsidegap))

        panel_widths = {'P8': P8_width, 'P9': P9_width, 'P10': P10_width}    
        
        panel_name_to_search = 'P8'
        P8_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap_reversed)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P8_handrailxpos}")

        panel_name_to_search = 'P9'
        P9_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap_reversed)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P9_handrailxpos}")

        panel_name_to_search = 'P10'
        P10_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap_reversed)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P10_handrailxpos}")

        # rear  핸드레일 홀    
        panel_widths = {'P5': P5_width, 'P6': P6_width, 'P7': P7_width}    
        
        panel_name_to_search = 'P5'
        P5_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRreargap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P5_handrailxpos}")

        panel_name_to_search = 'P6'
        P6_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRreargap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P6_handrailxpos}")

        panel_name_to_search = 'P7'
        P7_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRreargap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P7_handrailxpos}")

    # A작업 표기
    if P2_width == P8_width :
        insert_block(x4 + 230 , y4 + 320,"a_work")
    
    # 전면 벽 판넬 변수 목록 초기화
    P2_hole = [P2_hole1, P2_hole2, P2_hole3, P2_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P2_width]
    tx = x3 
    ty = y3 - P2_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P2_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)               

    d(doc,  x3 , y3, x4, y4, 173, direction="up")
    d(doc,  x13 , y13, x3, y3, 140, direction="left")
    d(doc,  x5 , y5, x4, y4, 190, direction="right")
    d(doc,  x6, y6, x5 , y5,  80, direction="down")    
    d(doc,  x1 , y1, x2, y2, 80, direction="down")     

    # 모자보강 Y위치 저장 y3
    rib_posy = y3

    #############################################################
    # P2 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
    # P2 조립도 본체구성 표현
    #############################################################
            
    ry = pagey 

    rectangle(doc, rx, ry , rx+ P2_width, ry+CPH, layer='0')
    rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
    rectangle(doc, rx + P2_width , ry , rx+P2_width-panel_wing , ry+CPH , layer='0')

    # 세로 날개 표시 panel_wing
    line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
    line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
    line(doc, rx + P2_width - panel_wing, ry  ,rx + P2_width - panel_wing , ry + CPH, layer='0')
    line(doc, rx + P2_width - thickness, ry  ,rx + P2_width - thickness , ry + CPH, layer='22')

    # 상부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P2_width -  panel_wing - 4 ,ry+CPH , layer='0')
    line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P2_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
    # 하부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P2_width -  panel_wing - 4 ,ry,  layer='0')
    line(doc, rx + panel_wing + 4, ry+thickness , rx + P2_width -  panel_wing - 4 ,ry+thickness,  layer='22')

    x1 = rx 
    y1 = ry 
    x2 = x1 + P2_width
    y2 = y1    
    x3 = x2 
    y3 = y2 + CPH
    x4 = x3 - P2_width
    y4 = y3 

    # 팝너트 표시하기    
    P2_hole = [P2_hole1, P2_hole2, P2_hole3, P2_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P2_width]
    tx = rx
    ty = ry+CPH    
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P2_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6_popnut")
                insert_block(tx + sum, ry,"M6_popnut_upset")
            if index == 0 :
                d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)         

    # 상부 전체치수
    d(doc,  rx , ry+CPH, rx + P2_width , ry+CPH, 120, direction="up")

    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P2_handrailxpos):            
            if g is not None : 
                tx = x2 - g
                insert_block(tx , y2 + handrail_height , "handrail_bracket")                
                d(doc, tx, y2 + handrail_height , x2 , y2 + handrail_height , 100 + index*100, direction="down")                    
                line(doc, tx , rib_posy + 10 , tx , rib_posy - 10 , layer='CLphantom')  

    d(doc, x1, y1, tx , y2 + handrail_height , 150, direction="left")    

    yp_bottom = ry  + 1
    yp_upper = ry + CPH - 1

    rb_list = panel_rib(P2_width, P2_handrailxpos)    
    # print(f"P2 패널의 종보강 위치: {rb_list}")
    # print(f"P2 핸드레일 위치: {P2_handrailxpos}")
    for index, g in enumerate(rb_list):
        bp = rx + P2_width - g
        xlist = [bp , bp-40 ,bp-20 ,bp + 20 ,bp + 40 ]       
        # 모자보강
        rectangle(doc, xlist[2] , yp_bottom, xlist[3] , yp_upper, layer='0')
        rectangle(doc, xlist[1] , yp_bottom+panel_wing+1, xlist[4] , yp_upper-panel_wing-1, layer='구성선') # 구성선은 회색선    
        line(doc, xlist[0] , yp_bottom, xlist[0] , yp_upper, layer='CLphantom')  
        # 치수선
        # print (f"index = {index}, x : {bp}")        
        # print (f" len(rb_list) = { len(rb_list)}" )        
        if index == 0:
            d(doc, x3, y3,  bp , y4, 150, direction="down")     
        else:
            dc(doc, bp,y3)

        # 단면도에 모자보강 위치 표시하기
        line(doc, bp , rib_posy + 10 , bp , rib_posy - 10 , layer='0')  
            
        # 5x10 장공 용접홀          
        insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
        insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")                     

    if len(rb_list)-1 > 0 :  # 마지막인 경우
        dc(doc, x4,y4)            

    # 장공홀 표현하기 M6_nut
    gap = 0    
    length = CPH - 85 + popnut_height 
    hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
    leftx = x1 + 1.5
    rightx = x2 - 1.5
    ty = y2

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "M6_nut")
            insert_block(rightx, ty + g, "M6_nut")
        if index == 0 :
            d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x3, y3)    

    # 우측 전체 치수선
    d(doc, x2, y2, x3, y3, 220, direction="right" )  

    ###########################################################################
    # P2 전개도 그리기
    ###########################################################################

    rx = pagex + P2_width + 1200                         
    x1 = rx
    y1 = pagey
    x2 = x1 + P2_width - (panel_width+5)*2
    y2 = y1    
    x3 = x2
    y3 = y2 + panel_wing + 4 
    x4 = x3 + panel_wing + 4 
    y4 = y3 
    x5 = x4 
    y5 = y4 + 14.5 if br == 1.5 else y4 + 16
    x6 = x5 + 45 if br == 1.5 else x5 + 47
    y6 = y5 
    x7 = x6 
    y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
    x8 = x7 - 45 if br == 1.5 else x7 - 47 
    y8 = y7 
    x9 = x8 
    y9 = y8 + 14.5 if br == 1.5 else y8 + 16
    x10 = x9 - (panel_wing + 4)
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_wing + 4 
    x12 = x11 - P2_width + (panel_width+5)*2
    y12 = y11
    x13 = x12 
    y13 = y12 - (panel_wing + 4)
    x14 = x13 - (panel_wing + 4)
    y14 = y13
    x15 = x14 
    y15 = y14 - 14.5 if br == 1.5 else y14 - 16
    x16 = x15 - 45 if br == 1.5 else x15 - 47
    y16 = y15 
    x17 = x16 
    y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
    x18 = x17 + 45 if br == 1.5 else x17 + 47
    y18 = y17 
    x19 = x18
    y19 = y18 - (panel_wing + 4)
    x20 = x19 + (panel_wing + 4)
    y20 = y19 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 20
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                     
    gap = 0
    gap = - 1.5 if br == 1.5 else - 1
    length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
    hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
    leftx = x17 + (panel_width+panel_wing - P2_holegap - br * 2 )
    rightx = x6 - (panel_width+panel_wing - P2_holegap - br * 2 )
    ty = y6

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "8x16_vertical")
            insert_block(rightx, ty + g, "8x16_vertical")
        if index == 0 :
            d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x11, y11)    

    # 장공치수선 그리기    좌,우 떨어짐
    for index, g in enumerate(hole):
        if index == 4 :
            d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
            d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )        

    yp_bottom = y1
    yp_upper = y11

    rb_list = panel_rib(P2_width, P2_handrailxpos)    
    # print(f"P2 패널의 종보강 위치: {rb_list}")
    # print(f"P2 핸드레일 위치: {P2_handrailxpos}")
    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            text = "%%C3"
            dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="left")                    
            # 5mm 치수선표시
            d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
            d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

        circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
        circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
        if index == 0 :
            d(doc, x16, y16, bp, y11, 200, direction="down")
        else:
            dc(doc, bp,y11)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x7,y7)     

    if handrail_height > 0 :
        # 핸드레일 그리기       
        for index, g in enumerate(P2_handrailxpos):            
            if g is not None : 
                tx = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
                ty = y6 + handrail_height - 1  if br == 1 else y6 + handrail_height - 1.5 
                if len(P2_handrailxpos) == 1 :
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    d(doc, tx, ty , x6 , ty , 100  , direction="up")                    
                    d(doc, tx, ty , x17 , ty , 100  , direction="up")                    
                    d(doc, x2, y2, tx , ty , 280, direction="right")  
                    # 보강자리에서 간격 X 축 치수선
                    d(doc, bp, ty, tx , ty , 180, direction="down")  
                else:
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    if index == 0 :
                        d(doc, x16 , ty , tx, ty , 100  , direction="up") 
                    else:                         
                        dc(doc, tx , ty )
                        dc(doc, x6 , ty )
                        # 보강자리에서 간격 X 축 치수선
                        d(doc, x2, y2, tx , ty , 280, direction="right") 
                        d(doc, bp, ty, tx , ty , 180, direction="down")  
                  
     
    # 9파이 팝너트 연결홀 상부/하부
    P2_hole = [P2_hole1, P2_hole2, P2_hole3, P2_hole4]   

    limit_point = [P2_width]
    tx = x16 + 30 if br == 1.5 else x16 + 32
    upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
    lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point
    # 상부의 연결홀
    for index, hole in enumerate(P2_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
            if index == 0 :
                holeupperx = tx + sum                               
                holeuppery = upper_ty                       
                text = "%%C9 M6 POPNUT(머리5mm)"
                dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="left")                
                d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

            elif index == len(hole_variables) - 1 :
                dc(doc, x7, y7)                   
            else:
                dc(doc, tx + sum, upper_ty)                                   
    # 하부에 연결홀 타공
    sum = 0
    for index, hole in enumerate(P2_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
            if index == 0 :
                holelowerx = tx + sum                               
                holelowery = lower_ty                          
                d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

            elif index == len(hole_variables) - 1 :
                dc(doc, x6, y6)                   
            else:
                dc(doc, tx + sum, lower_ty)      
                              
                
    # 상부치수선    
    d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
    dc(doc, x9 , y9)    
    dc(doc, x7, y7)
    # 상부 전체치수선
    d(doc, x16, y16, x7 ,y7, 250, direction="up")

    # 하부치수선    
    d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
    d(doc, x2, y2, x6 ,y6, 110, direction="down")        
    # 하부 2단 절곡 만나는 곳 치수선
    d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
    dc(doc, x4 , y4)    
    dc(doc, x6 , y6)
    # 하부 전체치수선
    d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
    
    # 오른쪽 15mm 표기
    d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
    # 오른쪽 최종 치수선
    d(doc, x11, y11 , x7, y7, 300, direction="right")
    dc(doc, x6, y6)
    dc(doc, x2, y2)    

    # 왼쪽 치수선 20mm 
    d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
    d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
    # 왼쪽 치수선 전체
    d(doc, x12, y12, x1, y1, 280, direction="left")
   

    #######################################  
    # P2,P8 단면도 (상부에 위치한)
    #######################################  

    x1 = x1 - panel_width + 6
    y1 = pagey + CH + 800
    x2 = x1 - panel_wing
    y2 = y1 
    x3 = x2
    y3 = y2 - panel_width
    x4 = x3 + P2_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - panel_width + thickness*2
    x10 = x9 - P2_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_width - thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    # B작업 표기
    if P2_width == P8_width and P4_width == P10_width :
        insert_block(x5 + 700 , y5,"b_work")

    x13 = x3
    y13 = y3 + P2_holegap
    x14 = x4
    y14 = y4 +P2_holegap
    
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 150, direction='up')   
    d(doc, x6, y6, x5, y5, 150, direction='up')   

    # 전체하부
    d(doc, x3, y3, x4, y4, 350, direction='down')              
    d(doc, x14+10, y14, x4, y4, 130, direction='right')    

    x13, y13 =  x1-10, y3 + P2_holegap
    line(doc, x3-10, y3+P2_holegap, x3+ 10, y3+P2_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y3+P2_holegap, x4+ 10, y3+P2_holegap , layer='CLphantom') # '구성선' 회색선
    # 좌측    
    d(doc, x13-10, y13, x3, y3, 100, direction='left')      
    d(doc, x2, y2, x3, y3, 180, direction='left')  

    d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
    rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
    # 하단 날개 23 표기 width 25 -2
    d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')   

    P2_hole = [P2_hole4, P2_hole3, P2_hole2, P2_hole1]     
    limit_point = [P2_width]
    tx = x3 
    ty = y3 + P2_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P2_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 280, direction="down" , option='reverse')                                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)        

    # 보강위치 단면도 표기
    rb_list = panel_rib(P2_width, P2_handrailxpos)        
    for index, g in enumerate(rb_list):      
        bp = x3 + g
        line(doc, bp, y3-10 , bp , y3+10, layer='0')                  
        if index == 0 :
            d(doc, bp, y3-10, x3, y3, 80, direction="down",option='reverse')
        else:
            dc(doc, bp,y3-10)
          
    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P2_handrailxpos):            
            if g is not None : 
                tx = x3 + g                
                d(doc, tx, y3, x3 , y3 - 10 , 130 + index*40, direction="down")                    
                line(doc, tx , y3 + 10 , tx , y3 - 10 , layer='CLphantom')            

    #######################################  
    # P2,P8 단면도 (우측)
    #######################################  
    top_panel_width = panel_width - 2
    x1 = pagex + P2_width*2 + 1000*2
    y1 = pagey + CH
    x2 = x1 
    y2 = y1 + panel_wing
    x3 = x2 - top_panel_width
    y3 = y2 
    x4 = x3 
    y4 = y3 - CPH
    x5 = x4 + top_panel_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_wing
    x7 = x6 - thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - panel_wing + thickness
    x9 = x8 - top_panel_width + thickness*2
    y9 = y8 
    x10 = x9 
    y10 = y9 + CPH - thickness*2
    x11 = x10 + top_panel_width - thickness*2
    y11 = y10 
    x12 = x11 
    y12 = y11 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3 + P2_holegap
    y13 = y3
    x14 = x4 + P2_holegap
    y14 = y4
    
    line(doc, x13, y13+10, x13, y13-10, layer="CL")
    line(doc, x14, y14+10, x14, y14-10, layer="CL")
    d(doc, x1, y1, x2, y2, 150, direction='right')
    d(doc, x3, y3, x13, y13+10, 80, direction='up')
    d(doc, x3, y3, x2, y2, 180, direction='up')
    d(doc, x14, y14-10, x4, y4, 100, direction='down')
    d(doc, x4, y4, x5, y5, 180, direction='down')

    d(doc, x3, y3, x4, y4, 100, direction='left')
    d(doc, x6, y6, x5, y5, 150, direction='right')

    ##################### 코멘트 ##########################
    mx = frameXpos + P2_width*2 + 3000
    my = frameYpos +2000     
    page_comment(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + P2_width*2 + 3500
    my = frameYpos +2000             
    desx = mx - 1300
    desy = my + 1000
    unitsu = 0
    if P2_width == P8_width :
        text = 'SIDE PANEL(#2,#8)'
        unitsu= 2
    else:
        text = 'SIDE PANEL(#2)'        
    if P4_width == P10_width :
        text += ', SIDE PANEL(#4,#10)'
        unitsu += 2

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material}{Spec}"
    draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')  
    frameXpos = frameXpos + TargetXscale + 400


############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

    # for i in range(2, 11):
    #     rib_list = panel_rib(i*100, P2_handrailxpos)
    #     print(f"P2 width : {i*100} , 패널의 종보강 위치: {rib_list}")         

    #########################################################################################
    # 6page P3, P9 같으면 하나만 표시
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 6851 
    TargetYscale = 4870 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    # print("page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "SIDE PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # P3 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
    ###################################################
    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx + panel_wing
    y1 = ry + CH + 500
    x2 = x1 - panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 + P3_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 + thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  + panel_width - thickness*2
    x10 = x9 - P3_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 - panel_width + thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   
    
    x13, y13 =  x1-10, y3-P3_holegap
    line(doc, x3-10, y3-P3_holegap, x3+ 10, y3-P3_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y4-P3_holegap, x4+ 10, y4-P3_holegap , layer='CLphantom') # '구성선' 회색선
    rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')

    # A작업 표기
    if P3_width == P9_width and P3_COPType != 'HOP 적용' and P9_COPType != 'HOP 적용' :
        insert_block(x4 + 230 , y4 + 320,"a_work")
    
    # 전면 벽 판넬 변수 목록 초기화
    P3_hole = [P3_hole1, P3_hole2, P3_hole3, P3_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P3_width]
    tx = x3 
    ty = y3 - P3_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P3_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)                   
       
    d(doc,  x3 , y3, x4, y4, 173, direction="up")
    d(doc,  x13 , y13, x3, y3, 140, direction="left")
    d(doc,  x5 , y5, x4, y4, 190, direction="right")

    d(doc,  x6, y6, x5 , y5,  80, direction="down")    
    d(doc,  x1 , y1, x2, y2, 80, direction="down")     

    # 모자보강 Y위치 저장 y3
    rib_posy = y3

    #############################################################
    # P3 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
    # P3 조립도 본체구성 표현
    #############################################################
        
    ry = pagey 

    rectangle(doc, rx, ry , rx+ P3_width, ry+CPH, layer='0')
    rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
    rectangle(doc, rx + P3_width , ry , rx+P3_width-panel_wing , ry+CPH , layer='0')

    # 세로 날개 표시 panel_wing
    line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
    line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
    line(doc, rx + P3_width - panel_wing, ry  ,rx + P3_width - panel_wing , ry + CPH, layer='0')
    line(doc, rx + P3_width - thickness, ry  ,rx + P3_width - thickness , ry + CPH, layer='22')

    # 상부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P3_width -  panel_wing - 4 ,ry+CPH , layer='0')
    line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P3_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
    # 하부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P3_width -  panel_wing - 4 ,ry,  layer='0')
    line(doc, rx + panel_wing + 4, ry+thickness , rx + P3_width -  panel_wing - 4 ,ry+thickness,  layer='22')


    # 중심선은 핸드레일 홀과 간섭이 없는지를 살펴야 한다. 그리고 새로 설정해야 한다.
    # line(doc, rx, ry + FH, rx+ P3_width, ry + FH, layer='magentaphantom')
    x1 = rx 
    y1 = ry 
    x2 = x1 + P3_width
    y2 = y1    
    x3 = x2 
    y3 = y2 + CPH
    x4 = x3 - P3_width
    y4 = y3 

    # 팝너트 표시하기    
    P3_hole = [P3_hole1, P3_hole2, P3_hole3, P3_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P3_width]
    tx = rx
    ty = ry+CPH    
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P3_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6_popnut")
                insert_block(tx + sum, ry,"M6_popnut_upset")
            if index == 0 :
                d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)         

    # 상부 전체치수
    d(doc,  rx , ry+CPH, rx + P3_width , ry+CPH, 120, direction="up")

    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P3_handrailxpos):            
            if g is not None : 
                tx = x2 - g
                insert_block(tx , y2 + handrail_height , "handrail_bracket")                
                d(doc, tx, y2 + handrail_height , x2 , y2 + handrail_height , 100 + index*100, direction="down")                    
                line(doc, tx , rib_posy + 10 , tx , rib_posy - panel_width - 10 , layer='CLphantom')  

    d(doc, x1, y1, tx , y2 + handrail_height , 150, direction="left")    

    yp_bottom = ry  + 1
    yp_upper = ry + CPH - 1

    rb_list = panel_rib(P3_width, P3_handrailxpos)    
    # print(f"P3 패널의 종보강 위치: {rb_list}")
    # print(f"P3 핸드레일 위치: {P3_handrailxpos}")
    for index, g in enumerate(rb_list):
        bp = rx + P3_width - g
        xlist = [bp , bp-40 ,bp-20 ,bp + 20 ,bp + 40 ]       
        # 모자보강
        rectangle(doc, xlist[2] , yp_bottom, xlist[3] , yp_upper, layer='0')
        rectangle(doc, xlist[1] , yp_bottom+panel_wing+1, xlist[4] , yp_upper-panel_wing-1, layer='구성선') # 구성선은 회색선    
        line(doc, xlist[0] , yp_bottom, xlist[0] , yp_upper, layer='CLphantom')  
        # 치수선
        # print (f"index = {index}, x : {bp}")        
        # print (f" len(rb_list) = { len(rb_list)}" )        
        if index == 0:
            d(doc, x3, y3,  bp , y4, 150, direction="down")     
        else:
            dc(doc, bp,y3)

        # 단면도에 모자보강 위치 표시하기
        line(doc, bp , rib_posy + 10 , bp , rib_posy - panel_width - 10 , layer='0')  
            
        # 5x10 장공 용접홀          
        insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
        insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")     
                

    if len(rb_list)-1 > 0 :  # 마지막인 경우
        dc(doc, x4,y4)            

    # 장공홀 표현하기 M6_nut
    gap = 0    
    length = CPH - 85 + popnut_height 
    hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
    leftx = x1 + 1.5
    rightx = x2 - 1.5
    ty = y2

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "M6_nut")
            insert_block(rightx, ty + g, "M6_nut")
        if index == 0 :
            d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x3, y3)    

    # 우측 전체 치수선
    d(doc, x2, y2, x3, y3, 220, direction="right" )  

    ###########################################################################
    # P3 전개도 그리기
    ###########################################################################

    rx = pagex + P3_width + 1200                         
    x1 = rx
    y1 = pagey
    x2 = x1 + P3_width - (panel_width+5)*2
    y2 = y1    
    x3 = x2
    y3 = y2 + panel_wing + 4 
    x4 = x3 + panel_wing + 4 
    y4 = y3 
    x5 = x4 
    y5 = y4 + 14.5 if br == 1.5 else y4 + 16
    x6 = x5 + 45 if br == 1.5 else x5 + 47
    y6 = y5 
    x7 = x6 
    y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
    x8 = x7 - 45 if br == 1.5 else x7 - 47 
    y8 = y7 
    x9 = x8 
    y9 = y8 + 14.5 if br == 1.5 else y8 + 16
    x10 = x9 - (panel_wing + 4)
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_wing + 4 
    x12 = x11 - P3_width + (panel_width+5)*2
    y12 = y11
    x13 = x12 
    y13 = y12 - (panel_wing + 4)
    x14 = x13 - (panel_wing + 4)
    y14 = y13
    x15 = x14 
    y15 = y14 - 14.5 if br == 1.5 else y14 - 16
    x16 = x15 - 45 if br == 1.5 else x15 - 47
    y16 = y15 
    x17 = x16 
    y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
    x18 = x17 + 45 if br == 1.5 else x17 + 47
    y18 = y17 
    x19 = x18
    y19 = y18 - (panel_wing + 4)
    x20 = x19 + (panel_wing + 4)
    y20 = y19 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 20
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                     
    gap = 0
    gap = - 1.5 if br == 1.5 else - 1
    length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
    hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
    leftx = x17 + (panel_width+panel_wing - P3_holegap - br * 2 )
    rightx = x6 - (panel_width+panel_wing - P3_holegap - br * 2 )
    ty = y6

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "8x16_vertical")
            insert_block(rightx, ty + g, "8x16_vertical")
        if index == 0 :
            d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x11, y11)    
    # 장공치수선 그리기    좌,우 떨어짐
    for index, g in enumerate(hole):
        if index == 4 :
            d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
            d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )        

    yp_bottom = y1
    yp_upper = y11

    rb_list = panel_rib(P3_width, P3_handrailxpos)    
    # print(f"P3 패널의 종보강 위치: {rb_list}")
    # print(f"P3 핸드레일 위치: {P3_handrailxpos}")
    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            text = "%%C3"
            dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="left")                    
            # 5mm 치수선표시
            d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
            d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

        circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
        circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
        if index == 0 :
            d(doc, x16, y16, bp, y11, 200, direction="down")
        else:
            dc(doc, bp,y11)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x7,y7)     

    if handrail_height > 0 :
        # 핸드레일 그리기       
        for index, g in enumerate(P3_handrailxpos):            
            if g is not None : 
                tx = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
                ty = y6 + handrail_height - 1  if br == 1 else y6 + handrail_height - 1.5 
                if len(P3_handrailxpos) == 1 :
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    d(doc, tx, ty , x6 , ty , 100  , direction="up")                    
                    d(doc, tx, ty , x17 , ty , 100  , direction="up")                    
                    d(doc, x2, y2, tx , ty , 280, direction="right")  
                    # 보강자리에서 간격 X 축 치수선
                    d(doc, bp, ty, tx , ty , 180, direction="down")  
                else:
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    if index == 0 :
                        d(doc, x16 , ty , tx, ty , 100  , direction="up") 
                    else:                         
                        dc(doc, tx , ty )
                        dc(doc, x6 , ty )
                        # 보강자리에서 간격 X 축 치수선
                        d(doc, x2, y2, tx , ty , 280, direction="right") 
                        d(doc, bp, ty, tx , ty , 180, direction="down")  
                  
     
    # 9파이 팝너트 연결홀 상부/하부
    P3_hole = [P3_hole1, P3_hole2, P3_hole3, P3_hole4]   

    limit_point = [P3_width]
    tx = x16 + 30 if br == 1.5 else x16 + 32
    upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
    lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point
    # 상부의 연결홀
    for index, hole in enumerate(P3_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
            if index == 0 :
                holeupperx = tx + sum                               
                holeuppery = upper_ty                       
                text = "%%C9 M6 POPNUT(머리5mm)"
                dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="left")                
                d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

            elif index == len(hole_variables) - 1 :
                dc(doc, x7, y7)                   
            else:
                dc(doc, tx + sum, upper_ty)                                   
    # 하부에 연결홀 타공
    sum = 0
    for index, hole in enumerate(P3_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
            if index == 0 :
                holelowerx = tx + sum                               
                holelowery = lower_ty                          
                d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

            elif index == len(hole_variables) - 1 :
                dc(doc, x6, y6)                   
            else:
                dc(doc, tx + sum, lower_ty)                                   
                
    # 상부치수선    
    d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
    dc(doc, x9 , y9)    
    dc(doc, x7, y7)
    # 상부 전체치수선
    d(doc, x16, y16, x7 ,y7, 250, direction="up")

    # 하부치수선    
    d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
    d(doc, x2, y2, x6 ,y6, 110, direction="down")        
    # 하부 2단 절곡 만나는 곳 치수선
    d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
    dc(doc, x4 , y4)    
    dc(doc, x6 , y6)
    # 하부 전체치수선
    d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
    
    # 오른쪽 15mm 표기
    d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
    # 오른쪽 최종 치수선
    d(doc, x11, y11 , x7, y7, 300, direction="right")
    dc(doc, x6, y6)
    dc(doc, x2, y2)    

    # 왼쪽 치수선 20mm 
    d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
    d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
    # 왼쪽 치수선 전체
    d(doc, x12, y12, x1, y1, 280, direction="left")
   

    #######################################  
    # P3 단면도 (상부에 위치한)
    #######################################  

    x1 = x1 - panel_width + 6
    y1 = pagey + CH + 800
    x2 = x1 - panel_wing
    y2 = y1 
    x3 = x2
    y3 = y2 - panel_width
    x4 = x3 + P3_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - panel_width + thickness*2
    x10 = x9 - P3_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_width - thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    # B작업 표기
    if P3_width == P8_width and P4_width == P10_width :
        insert_block(x5 + 700 , y5,"b_work")

    x13 = x3
    y13 = y3 + P3_holegap
    x14 = x4
    y14 = y4 + P3_holegap
    
    line(doc, x13-10, y13, x13+10, y13, layer="CL") 
    line(doc, x14-10, y14, x14+10, y14, layer="CL") 
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 150, direction='up')   
    d(doc, x6, y6, x5, y5, 150, direction='up')   
    # 좌측    
    d(doc, x13-10, y13, x3, y3, 100, direction='left')      
    d(doc, x2, y2, x3, y3, 180, direction='left')  

    # 전체하부
    d(doc, x3, y3, x4, y4, 350, direction='down')              
    d(doc, x14+10, y14, x4, y4, 130, direction='right')    

    x13, y13 =  x1-10, y3 + P3_holegap        
    rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
    # 하단 날개 23 표기 width 25 -2
    d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
    d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')  

    P3_hole = [P3_hole4, P3_hole3, P3_hole2, P3_hole1]     
    limit_point = [P3_width]
    tx = x3 
    ty = y3 + P3_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P3_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 280, direction="down" , option='reverse')                                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)        

    # 보강위치 단면도 표기
    rb_list = panel_rib(P3_width, P3_handrailxpos)        
    preX = x3
    for index, g in enumerate(rb_list):      
        bp = x3 + g
        line(doc, bp, y3-10 , bp , y3+10, layer='0')                  
        d(doc, preX, y3-10, bp, y3, 170, direction="down")
        preX = bp            
    dc(doc, x4,y4)   
          
    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P3_handrailxpos):            
            if g is not None : 
                tx = x3 + g                
                d(doc, tx, y3, x3 , y3 - 10 , 90 + index*40, direction="down")                    
                line(doc, tx , y3 + 10 , tx , y3 - 10 , layer='CLphantom')                    

    #######################################  
    # P3 단면도 (우측)
    #######################################  
    top_panel_width = panel_width - 2
    x1 = pagex + P3_width*2 + 1000*2
    y1 = pagey + CH
    x2 = x1 
    y2 = y1 + panel_wing
    x3 = x2 - top_panel_width
    y3 = y2 
    x4 = x3 
    y4 = y3 - CPH
    x5 = x4 + top_panel_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_wing
    x7 = x6 - thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - panel_wing + thickness
    x9 = x8 - top_panel_width + thickness*2
    y9 = y8 
    x10 = x9 
    y10 = y9 + CPH - thickness*2
    x11 = x10 + top_panel_width - thickness*2
    y11 = y10 
    x12 = x11 
    y12 = y11 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3 + P3_holegap
    y13 = y3
    x14 = x4 + P3_holegap
    y14 = y4
    
    line(doc, x13, y13+10, x13, y13-10, layer="CL")
    line(doc, x14, y14+10, x14, y14-10, layer="CL")
    d(doc, x1, y1, x2, y2, 150, direction='right')
    d(doc, x3, y3, x13, y13+10, 80, direction='up')
    d(doc, x3, y3, x2, y2, 180, direction='up')
    d(doc, x14, y14-10, x4, y4, 100, direction='down')
    d(doc, x4, y4, x5, y5, 180, direction='down')

    d(doc, x3, y3, x4, y4, 100, direction='left')
    d(doc, x6, y6, x5, y5, 150, direction='right')

    ##################### 코멘트 ##########################
    mx = frameXpos + P3_width*2 + 3000
    my = frameYpos +2000     
    page_comment(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + P3_width*2 + 4000
    my = frameYpos +2000             
    desx = mx - 1300
    desy = my + 1000
    unitsu = 0
    if P3_width == P9_width and P3_COPType != 'HOP 적용' and P9_COPType != 'HOP 적용' :
        text = 'SIDE PANEL(#3,#9)'
        unitsu= 2
    else:
        text = 'SIDE PANEL(#3)' 
        unitsu = 1

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')   
    
    frameXpos = frameXpos + TargetXscale + 400



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
       
    if P9_COPType == 'HOP 적용' or P3_COPType == 'HOP 적용' :
        #########################################################################################
        # 7page P9, P3 HOP 적용        
        #########################################################################################
        # 도면틀 넣기    
        BasicXscale = 6851
        BasicYscale = 4870
        TargetXscale = 6851 
        TargetYscale = 4870 + (CH-2500) 
        if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
            frame_scale = TargetXscale/BasicXscale
        else:
            frame_scale = TargetYscale/BasicYscale    

        # print("7page 스케일 비율 : " + str(frame_scale))           
        insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "SIDE PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

        pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

        ###################################################
        # P9 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
        ###################################################
        rx = math.floor(pagex)
        ry = math.floor(pagey)

        x1 = rx + panel_wing
        y1 = ry + CH + 500
        x2 = x1 - panel_wing 
        y2 = y1    
        x3 = x2 
        y3 = y2 + panel_width
        x4 = x3 + P9_width
        y4 = y3 
        x5 = x4 
        y5 = y4 - panel_width
        x6 = x5 - panel_wing
        y6 = y5 
        x7 = x6 
        y7 = y6 + thickness
        x8 = x7 + panel_wing - thickness
        y8 = y7 
        x9 = x8 
        y9 = y8  + panel_width - thickness*2
        x10 = x9 - P9_width + thickness*2
        y10 = y9 
        x11 = x10 
        y11 = y10 - panel_width + thickness*2
        x12 = x11 + panel_wing - thickness
        y12 = y11 

        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 12
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="0")   
        
        x13, y13 =  x1-10, y3-P9_holegap
        line(doc, x3-10, y3-P2_holegap, x3+ 10, y3-P2_holegap , layer='CLphantom') # '구성선' 회색선
        line(doc, x4-10, y4-P2_holegap, x4+ 10, y4-P2_holegap , layer='CLphantom') # '구성선' 회색선        
        rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')

        # A작업 표기
        if P3_width == P9_width and P3_COPType != 'HOP 적용' and P9_COPType != 'HOP 적용' :
            insert_block(x4 + 230 , y4 + 320,"a_work")
        
        P9_hole = [P9_hole1, P9_hole2, P9_hole3, P9_hole4]   
        
        limit_point = [P9_width]
        tx = x3 
        ty = y3 - P9_holegap
        sum = 0        
        for index, hole in enumerate(P9_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                    
                    insert_block(tx + sum, ty,"M6")
                if index == 0 :
                    d(doc,  x3 , y3, tx + sum, ty, 63, direction="up" , option='reverse')                    
                else:
                    dc(doc, tx + sum, ty)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, tx + sum, ty)                   
        
        d(doc,  x3 , y3, x4, y4, 173, direction="up")
        d(doc,  x13 , y13, x3, y3, 140, direction="left")
        d(doc,  x5 , y5, x4, y4, 190, direction="right")

        d(doc,  x6, y6, x5 , y5,  80, direction="down")    
        d(doc,  x1 , y1, x2, y2, 80, direction="down")     

        # 모자보강 Y위치 저장 y3
        rib_posy = y3

        #############################################################
        # P9 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
        # P9 조립도 본체구성 표현
        #############################################################            
        ry = pagey 

        rectangle(doc, rx, ry , rx+ P9_width, ry+CPH, layer='0')
        rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
        rectangle(doc, rx + P9_width , ry , rx+P9_width-panel_wing , ry+CPH , layer='0')

        # 세로 날개 표시 panel_wing
        line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
        line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
        line(doc, rx + P9_width - panel_wing, ry  ,rx + P9_width - panel_wing , ry + CPH, layer='0')
        line(doc, rx + P9_width - thickness, ry  ,rx + P9_width - thickness , ry + CPH, layer='22')

        # 상부 날개 표시
        rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P9_width -  panel_wing - 4 ,ry+CPH , layer='0')
        line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P9_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
        # 하부 날개 표시
        rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P9_width -  panel_wing - 4 ,ry,  layer='0')
        line(doc, rx + panel_wing + 4, ry+thickness , rx + P9_width -  panel_wing - 4 ,ry+thickness,  layer='22')

        x1 = rx 
        y1 = ry 
        x2 = x1 + P9_width
        y2 = y1    
        x3 = x2 
        y3 = y2 + CPH
        x4 = x3 - P9_width
        y4 = y3 

        # 팝너트 표시하기    
        P9_hole = [P9_hole1, P9_hole2, P9_hole3, P9_hole4]   

        # print (f"hole val : {hole_variables}")
        limit_point = [P9_width]
        tx = rx
        ty = ry+CPH    
        sum = 0
        # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
        for index, hole in enumerate(P9_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:
                    frontholes.append(hole)
                    insert_block(tx + sum, ty,"M6_popnut")
                    insert_block(tx + sum, ry,"M6_popnut_upset")
                if index == 0 :
                    d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
                else:
                    dc(doc, tx + sum, ty)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, tx + sum, ty)         

        # 상부 전체치수
        d(doc,  rx , ry+CPH, rx + P9_width , ry+CPH, 120, direction="up")

        if handrail_height > 0 :       
            # 핸드레일 그리기        
            for index, g in enumerate(P9_handrailxpos):            
                if g is not None : 
                    tx = x2 - g
                    insert_block(tx , y2 + handrail_height , "handrail_bracket")                
                    d(doc, tx, y2 + handrail_height , x2 , y2 + handrail_height , 100 + index*100, direction="down")                    
                    line(doc, tx , rib_posy + 10 , tx , rib_posy - panel_width - 10 , layer='CLphantom')  

        d(doc, x1, y1, tx , y2 + handrail_height , 150, direction="left")    

        yp_bottom = ry  + 1
        yp_upper = ry + CPH - 1

        rb_list = panel_rib_HOP(P9_width, P9_handrailxpos, HOP_width)
        # print(f"P9 새로운 함수 적용 HOP 종보강 위치: {rb_list}")                
        # 리스트를 역순으로 조립도는 역순이다. 
        rb_list_reversed = rb_list[::-1]
        # print(f"P9 rb_list_reversed 새로운 함수 적용 HOP 종보강 위치: {rb_list_reversed}")        
        for index, g in enumerate(rb_list_reversed):        
            bp = rx +  g
            if index == 0 :
                xlist = [bp , bp-10 ,bp+10 ,bp - 8 ,bp - 10, bp+15, bp+10 ]       
                # 25 HOP보강 5,10,8,2 = 25 좌우 개념이 있음
                rectangle(doc, xlist[1] , yp_bottom, xlist[2] , yp_upper, layer='0')
                rectangle(doc, xlist[5] , yp_bottom+panel_wing+1, xlist[6] , yp_upper-panel_wing-1, layer='0')
                line(doc, xlist[3] , yp_bottom, xlist[3] , yp_upper, layer='2')                
                line(doc, bp , yp_bottom, bp , yp_upper, layer='CLphantom')                  
                d(doc, x3, y3,  bp , y4, 150, direction="down")     
            elif index == 1 :
                xlist = [bp , bp+10 ,bp-10 ,bp - 8 ,bp - 10, bp+15, bp+10 ]       
                # 25 HOP보강 5,10,8,2 = 25 좌우 개념이 있음
                # HOP 상단
                HOP_box_upperY = ry + HOP_bottomHeight + HOP_height + 1
                HOP_box_lowerY = ry + HOP_bottomHeight - 1

                # box 보강 (상부, 하부 30x23 'ㄱ'자 보강)
                rectangle(doc, rx + P9_width/2 - HOP_width/2, HOP_box_upperY, rx + P9_width/2 + HOP_width/2, HOP_box_upperY + 30, layer='0')
                line(doc, rx + P9_width/2 - HOP_width/2, HOP_box_upperY + 1.6 , rx + P9_width/2 + HOP_width/2, HOP_box_upperY + 1.6, layer='구성선')
                rectangle(doc, rx + P9_width/2 - HOP_width/2, HOP_box_lowerY, rx + P9_width/2 + HOP_width/2, HOP_box_lowerY - 30, layer='0')
                line(doc, rx + P9_width/2 - HOP_width/2, HOP_box_lowerY - 1.6 , rx + P9_width/2 + HOP_width/2, HOP_box_lowerY - 1.6, layer='구성선')                
                
                rectangle(doc, xlist[1] , HOP_box_upperY, xlist[2] , yp_upper, layer='0')
                rectangle(doc, xlist[5] , HOP_box_upperY + 30, xlist[6] , yp_upper-panel_wing-1, layer='0')
                line(doc, xlist[3] , HOP_box_upperY, xlist[3] , yp_upper, layer='2')                
                line(doc, bp , yp_upper, bp , HOP_box_upperY, layer='CLphantom')                  
                # HOP 밑단
                rectangle(doc, xlist[1] , yp_bottom, xlist[2] , HOP_box_lowerY, layer='0')
                rectangle(doc, xlist[5] , yp_bottom+panel_wing+1, xlist[6] , HOP_box_lowerY-30, layer='0')
                line(doc, xlist[3] , yp_bottom, xlist[3] , HOP_box_lowerY, layer='2')                
                line(doc, bp , yp_bottom, bp , HOP_box_lowerY, layer='CLphantom')      
                dc(doc, bp,y3)                            
            else:
                xlist = [bp , bp+10 ,bp-10 ,bp+8 ,bp+10, bp-15, bp-10 ]       
                # 25 HOP보강 5,10,8,2 = 25 좌우 개념이 있음
                rectangle(doc, xlist[1] , yp_bottom, xlist[2] , yp_upper, layer='0')
                rectangle(doc, xlist[5] , yp_bottom+panel_wing+1, xlist[6] , yp_upper-panel_wing-1, layer='0')
                line(doc, xlist[3] , yp_bottom, xlist[3] , yp_upper, layer='2')                
                line(doc, bp , yp_bottom, bp , yp_upper, layer='CLphantom')                  
                dc(doc, bp,y3)

            # 단면도에 모자보강 위치 표시하기
            line(doc, bp , rib_posy + 10 , bp , rib_posy - panel_width - 10 , layer='0')  
                
            # 5x10 장공 용접홀          
            insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
            insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")                         

        if len(rb_list)-1 > 0 :  # 마지막인 경우
            dc(doc, x4,y4)          
    
        #################################
        # HOP 타공
        ##################################    
        tx1 = x1 + P9_width/2 - HOP_width/2
        ty1 = y1 + HOP_bottomHeight 
        tx2 = tx1 + HOP_width
        ty2 = ty1
        tx3 = tx2
        ty3 = ty2 + HOP_height
        tx4 = tx3 - HOP_width
        ty4 = ty3
        rectangle(doc, tx1 , ty1, tx3, ty3, layer="0" )
        tx5=(tx1+tx2)/2
        ty5=ty1
        tx6=(tx3+tx4)/2
        ty6=ty3
        line(doc, tx5-HOP_holegap/2, ty5-10,  tx5-HOP_holegap/2 , ty5+10,  layer='CLphantom')    
        line(doc, tx5+HOP_holegap/2, ty5-10,  tx5+HOP_holegap/2 , ty5+10,  layer='CLphantom')    
        line(doc, tx5-HOP_holegap/2, ty6-10,  tx5-HOP_holegap/2 , ty6+10,  layer='CLphantom')    
        line(doc, tx5+HOP_holegap/2, ty6-10,  tx5+HOP_holegap/2 , ty6+10,  layer='CLphantom')    

        d(doc, tx5-HOP_holegap/2, ty5-10, tx5+HOP_holegap/2 , ty5+10, 70, direction='up')
        d(doc, tx4, ty4, tx3, ty3, 100, direction='up')
        d(doc, tx4, ty4, tx1, ty1, 60, direction='left')
        dc(doc, tx4, y1)       

        # 장공홀 표현하기 M6_nut
        gap = 0    
        length = CPH - 85 + popnut_height 
        hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
        leftx = x1 + 1.5
        rightx = x2 - 1.5
        ty = y2

        for index, g in enumerate(hole):
            gap += g
            if g is not None : 
                insert_block(leftx, ty + g, "M6_nut")
                insert_block(rightx, ty + g, "M6_nut")
            if index == 0 :
                d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    
                # 슬롯등 지시선 추가
                text = "8x16"
                dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
            else:
                dc(doc, rightx, ty + g)    
        dc(doc, x3, y3)    

        # 우측 전체 치수선
        d(doc, x2, y2, x3, y3, 220, direction="right" )  

        ###########################################################################
        # P9 전개도 그리기
        ###########################################################################

        rx = pagex + P9_width + 1200                         
        x1 = rx
        y1 = pagey
        x2 = x1 + P9_width - (panel_width+5)*2
        y2 = y1    
        x3 = x2
        y3 = y2 + panel_wing + 4 
        x4 = x3 + panel_wing + 4 
        y4 = y3 
        x5 = x4 
        y5 = y4 + 14.5 if br == 1.5 else y4 + 16
        x6 = x5 + 45 if br == 1.5 else x5 + 47
        y6 = y5 
        x7 = x6 
        y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
        x8 = x7 - 45 if br == 1.5 else x7 - 47 
        y8 = y7 
        x9 = x8 
        y9 = y8 + 14.5 if br == 1.5 else y8 + 16
        x10 = x9 - (panel_wing + 4)
        y10 = y9 
        x11 = x10 
        y11 = y10 + panel_wing + 4 
        x12 = x11 - P9_width + (panel_width+5)*2
        y12 = y11
        x13 = x12 
        y13 = y12 - (panel_wing + 4)
        x14 = x13 - (panel_wing + 4)
        y14 = y13
        x15 = x14 
        y15 = y14 - 14.5 if br == 1.5 else y14 - 16
        x16 = x15 - 45 if br == 1.5 else x15 - 47
        y16 = y15 
        x17 = x16 
        y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
        x18 = x17 + 45 if br == 1.5 else x17 + 47
        y18 = y17 
        x19 = x18
        y19 = y18 - (panel_wing + 4)
        x20 = x19 + (panel_wing + 4)
        y20 = y19 

        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 20
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                        
        gap = 0
        gap = - 1.5 if br == 1.5 else - 1
        length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
        hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
        leftx = x17 + (panel_width+panel_wing - P9_holegap - br * 2 )
        rightx = x6 - (panel_width+panel_wing - P9_holegap - br * 2 )
        ty = y6

        for index, g in enumerate(hole):
            gap += g
            if g is not None : 
                insert_block(leftx, ty + g, "8x16_vertical")
                insert_block(rightx, ty + g, "8x16_vertical")
            if index == 0 :
                d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
                # 슬롯등 지시선 추가
                text = "8x16"
                dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
            else:
                dc(doc, rightx, ty + g)    
        dc(doc, x11, y11)    
        # 장공치수선 그리기    좌,우 떨어짐
        for index, g in enumerate(hole):
            if index == 4 :
                d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
                d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )            

        yp_bottom = y1
        yp_upper = y11

        rb_list = panel_rib_HOP(P9_width, P9_handrailxpos, HOP_width, option='reverse')
        # print(f"전개도  적용 HOP 종보강 위치: {rb_list}")             
        for index, g in enumerate(rb_list):         
            bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
            line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
            if index == 0 :
                text = "%%C3"
                dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="left")                    
                # 5mm 치수선표시
                d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
                d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

            circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
            circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

        for index, g in enumerate(rb_list):        
            bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
            if index == 0 :
                d(doc, x16, y16, bp, y11, 200, direction="down")
            else:
                dc(doc, bp,y11)

        if len(rb_list) > 0 :  # 마지막인 경우
            dc(doc, x7,y7)     

        if handrail_height > 0 :
            # 핸드레일 그리기       
            for index, g in enumerate(P9_handrailxpos):            
                if g is not None : 
                    tx = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
                    ty = y6 + handrail_height - 1  if br == 1 else y6 + handrail_height - 1.5 
                    if len(P9_handrailxpos) == 1 :
                        circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                        d(doc, tx, ty , x6 , ty , 150  , direction="down")                    
                        d(doc, tx, ty , x17 , ty , 150  , direction="down")                    
                        d(doc, x2, y2, tx , ty , 280, direction="right")                          
                    else:
                        circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                        if index == 0 :
                            d(doc, x16 , ty , tx, ty , 150  , direction="down") 
                        else:                         
                            dc(doc, tx , ty )
                            dc(doc, x6 , ty )
                            # 보강자리에서 간격 X 축 치수선
                            d(doc, x2, y2, tx , ty , 280, direction="right") 
                            d(doc, bp, ty, tx , ty , 350, direction="down")  
                            
        # 9파이 팝너트 연결홀 상부/하부
        P9_hole = [P9_hole1, P9_hole2, P9_hole3, P9_hole4]   

        limit_point = [P9_width]
        tx = x16 + 30 if br == 1.5 else x16 + 32
        upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
        lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
        sum = 0
        # 각 변수에 대해 값이 0보다 크고 limit_point
        # 상부의 연결홀
        for index, hole in enumerate(P9_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                
                    circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                    circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                if index == 0 :
                    holeupperx = tx + sum                               
                    holeuppery = upper_ty                       
                    text = "%%C9 M6 POPNUT(머리5mm)"
                    dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="left")                
                    d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

                elif index == len(hole_variables) - 1 :
                    dc(doc, x7, y7)                   
                else:
                    dc(doc, tx + sum, upper_ty)                                   
        # 하부에 연결홀 타공
        sum = 0
        for index, hole in enumerate(P9_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                
                    circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                    circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
                if index == 0 :
                    holelowerx = tx + sum                               
                    holelowery = lower_ty                          
                    d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

                elif index == len(hole_variables) - 1 :
                    dc(doc, x6, y6)                   
                else:
                    dc(doc, tx + sum, lower_ty)        

        #################################
        # HOP 타공 (전개도 laser layer)
        ##################################    
        tx1 = x16  
        tx1 = x17 + panel_wing + panel_width + P9_width/2 - HOP_width/2  - 4 if br == 1 else x17 + panel_wing + panel_width + P9_width/2 - HOP_width/2  - 6
        ty1 = y6 + HOP_bottomHeight if br == 1 else y6 + HOP_bottomHeight - 1.5
        tx2 = tx1 + HOP_width
        ty2 = ty1
        tx3 = tx2
        ty3 = ty2 + HOP_height
        tx4 = tx3 - HOP_width
        ty4 = ty3
        rectangle(doc, tx1 , ty1, tx3, ty3, layer="레이져" )
        tx5=(tx1+tx2)/2
        ty5=ty1
        tx6=(tx3+tx4)/2
        ty6=ty3        
        
        d(doc, tx4, ty4, tx3, ty3, 100, direction='up')
        d(doc, tx4, ty4, tx1, ty1, extract_abs(x16, tx1) + 120, direction='left')
        dc(doc, tx4, y1)       
                    
        # 상부치수선    
        d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
        dc(doc, x9 , y9)    
        dc(doc, x7, y7)
        # 상부 전체치수선
        d(doc, x16, y16, x7 ,y7, 250, direction="up")

        # 하부치수선    
        d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
        d(doc, x2, y2, x6 ,y6, 110, direction="down")        
        # 하부 2단 절곡 만나는 곳 치수선
        d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
        dc(doc, x4 , y4)    
        dc(doc, x6 , y6)
        # 하부 전체치수선
        d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
        
        # 오른쪽 15mm 표기
        d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
        # 오른쪽 최종 치수선
        d(doc, x11, y11 , x7, y7, 300, direction="right")
        dc(doc, x6, y6)
        dc(doc, x2, y2)    

        # 왼쪽 치수선 20mm 
        d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
        d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
        # 왼쪽 치수선 전체
        d(doc, x12, y12, x1, y1, 280, direction="left")
    

        #######################################  
        # P9 단면도 (상부에 위치한)
        #######################################  

        x1 = x1 - panel_width + 6
        y1 = pagey + CH + 800
        x2 = x1 - panel_wing
        y2 = y1 
        x3 = x2
        y3 = y2 - panel_width
        x4 = x3 + P9_width
        y4 = y3 
        x5 = x4 
        y5 = y4 + panel_width
        x6 = x5 - panel_wing
        y6 = y5 
        x7 = x6 
        y7 = y6 - thickness
        x8 = x7 + panel_wing - thickness
        y8 = y7 
        x9 = x8 
        y9 = y8 - panel_width + thickness*2
        x10 = x9 - P9_width + thickness*2
        y10 = y9 
        x11 = x10 
        y11 = y10 + panel_width - thickness*2
        x12 = x11 + panel_wing - thickness
        y12 = y11
        
        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 12
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="0")     

        # B작업 표기
        if P3_width == P9_width and P3_COPType != 'HOP 적용' and P9_COPType != 'HOP 적용' :
            insert_block(x5 + 700 , y5,"b_work")

        x13 = x3
        y13 = y3 + P9_holegap
        x14 = x4
        y14 = y4 + P9_holegap
        
        line(doc, x13-10, y13, x13+10, y13, layer="CL") 
        line(doc, x14-10, y14, x14+10, y14, layer="CL") 
        # 상부 치수선
        d(doc, x1, y1, x2, y2, 150, direction='up')   
        d(doc, x6, y6, x5, y5, 150, direction='up')   
        # 좌측    
        d(doc, x13-10, y13, x3, y3, 100, direction='left')      
        d(doc, x2, y2, x3, y3, 180, direction='left')  

        # 전체하부
        d(doc, x3, y3, x4, y4, 350, direction='down')              
        d(doc, x14+10, y14, x4, y4, 130, direction='right')    

        x13, y13 =  x1-10, y3 + P9_holegap        
        rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
        # 하단 날개 23 표기 width 25 -2
        d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
        d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')           

        P9_hole = [P9_hole4, P9_hole3, P9_hole2, P9_hole1]     
        limit_point = [P9_width]
        tx = x3
        ty = y3 + P9_holegap
        sum = 0
        # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
        for index, hole in enumerate(P9_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                
                    insert_block(tx + sum, ty,"M6")
                if index == 0 :
                    d(doc,  x3 , y3, tx + sum, ty, 250, direction="down" , option='reverse')                                    
                else:
                    dc(doc, tx + sum, ty)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, tx + sum, ty)        
   
    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P9_handrailxpos):            
            if g is not None : 
                tx = x3 + g                
                d(doc, tx, y3, x3 , y3 - 10 , 90 + index*40, direction="down")                    
                line(doc, tx , y3 + 10 , tx , y3 - 10 , layer='CLphantom')                 

    # 보강 3개 위치 표시
    yp_bottom = y3 - 10
    yp_upper = y3 + 10

    rb_list = panel_rib_HOP(P9_width, P9_handrailxpos, HOP_width, option='reverse')        
    for index, g in enumerate(rb_list):         
        bp = x3 + g
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            d(doc, x3,  y3 , bp , yp_bottom , 150, direction="down")               
        else:
            dc(doc, bp , yp_bottom)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x4,y4)                          

        #######################################  
        # P9 단면도 (우측)
        #######################################  
        top_panel_width = panel_width - 2
        x1 = pagex + P9_width*2 + 1000*2
        y1 = pagey + CH
        x2 = x1 
        y2 = y1 + panel_wing
        x3 = x2 - top_panel_width
        y3 = y2 
        x4 = x3 
        y4 = y3 - CPH
        x5 = x4 + top_panel_width
        y5 = y4 
        x6 = x5 
        y6 = y5 + panel_wing
        x7 = x6 - thickness
        y7 = y6 
        x8 = x7 
        y8 = y7 - panel_wing + thickness
        x9 = x8 - top_panel_width + thickness*2
        y9 = y8 
        x10 = x9 
        y10 = y9 + CPH - thickness*2
        x11 = x10 + top_panel_width - thickness*2
        y11 = y10 
        x12 = x11 
        y12 = y11 - panel_wing + thickness
        
        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 12
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="0")     

        x13 = x3 + P9_holegap
        y13 = y3
        x14 = x4 + P9_holegap
        y14 = y4
        
        line(doc, x13, y13+10, x13, y13-10, layer="CL")
        line(doc, x14, y14+10, x14, y14-10, layer="CL")
        d(doc, x1, y1, x2, y2, 150, direction='right')
        d(doc, x3, y3, x13, y13+10, 80, direction='up')
        d(doc, x3, y3, x2, y2, 180, direction='up')
        d(doc, x14, y14-10, x4, y4, 100, direction='down')
        d(doc, x4, y4, x5, y5, 180, direction='down')

        d(doc, x3, y3, x4, y4, 100, direction='left')
        d(doc, x6, y6, x5, y5, 150, direction='right')

        ##################### 코멘트 ##########################
        mx = frameXpos + P9_width*2 + 3000
        my = frameYpos +2000     
        page_comment(mx, my)
        
        ##################### part 설명  ##########################
        mx = frameXpos + P9_width*2 + 4000
        my = frameYpos +2000             
        desx = mx - 1300
        desy = my + 1000
        unitsu = 0
        if P9_width == P9_width and P9_COPType == '' and P9_COPType == '':
            text = 'SIDE PANEL(#3,#9)'
            unitsu= 2
        else:
            text = 'SIDE PANEL(#9)' 
            unitsu = 1

        textstr = f"Part Name : {text}"    
        draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
        textstr = f"Mat.Spec : {Material} {Spec}"
        draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
        textstr = f"Quantity : {unitsu} SET"    
        draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')   
        
        frameXpos = frameXpos + TargetXscale + 400



###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################








    #########################################################################################
    # 8page P5, P7 같으면 하나만 표시
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 6851 
    TargetYscale = 4870 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    # print("2page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "REAR PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # P5 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
    ###################################################
    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx + panel_wing
    y1 = ry + CH + 500
    x2 = x1 - panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 + P5_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 + thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  + panel_width - thickness*2
    x10 = x9 - P5_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 - panel_width + thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   
    
    x13, y13 =  x1-10, y3-P5_holegap    
    rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')
    line(doc, x3-10, y3-P5_holegap, x3+ 10, y3-P5_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y4-P5_holegap, x4+ 10, y4-P5_holegap , layer='CLphantom') # '구성선' 회색선    

    # A작업 표기
    if P5_width == P7_width :
        insert_block(x4 + 230 , y4 + 320,"a_work")
    
    # 전면 벽 판넬 변수 목록 초기화
    P5_hole = [P5_hole1, P5_hole2, P5_hole3, P5_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P5_width]
    tx = x3 
    ty = y3 - P5_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P5_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 170, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)               

    d(doc,  x3 , y3, x4, y4, 250, direction="up")
    d(doc,  x13 , y13, x3, y3, 140, direction="left")
    d(doc,  x5 , y5, x4, y4, 190, direction="right")
    d(doc,  x6, y6, x5 , y5,  80, direction="down")    
    d(doc,  x1 , y1, x2, y2, 80, direction="down")     

    # P5, P7은 side panel과 결합하니, 홀의 결합위치가 다르다. 주의)
    line(doc, x4 - (panel_width-P5_holegap) , y4 + 10 , x4 - (panel_width-P5_holegap) , y4 - 10 , layer='CLphantom')  
    d(doc, x4 , y4 , x4 - (panel_width-P5_holegap) , y4 + 10 , 50, direction="up")

    if handrail_height > 0 :       
        # 핸드레일 위치 표시 및 치수선
        for index, g in enumerate(P5_handrailxpos):            
            if g is not None : 
                tx = x4 - g                
                d(doc, x4, y4 , tx , y4 + 10 , 100 , direction="up")                                    

    # 모자보강 Y위치 저장 y3
    rib_posy = y3

    #############################################################
    # P5 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
    # P5 조립도 본체구성 표현
    #############################################################
            
    ry = pagey 

    rectangle(doc, rx, ry , rx+ P5_width, ry+CPH, layer='0')
    rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
    rectangle(doc, rx + P5_width , ry , rx+P5_width-panel_wing , ry+CPH , layer='0')

    # 세로 날개 표시 panel_wing
    line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
    line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
    line(doc, rx + P5_width - panel_wing, ry  ,rx + P5_width - panel_wing , ry + CPH, layer='0')
    line(doc, rx + P5_width - thickness, ry  ,rx + P5_width - thickness , ry + CPH, layer='22')

    # 상부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P5_width -  panel_wing - 4 ,ry+CPH , layer='0')
    line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P5_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
    # 하부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P5_width -  panel_wing - 4 ,ry,  layer='0')
    line(doc, rx + panel_wing + 4, ry+thickness , rx + P5_width -  panel_wing - 4 ,ry+thickness,  layer='22')

    x1 = rx 
    y1 = ry 
    x2 = x1 + P5_width
    y2 = y1    
    x3 = x2 
    y3 = y2 + CPH
    x4 = x3 - P5_width
    y4 = y3 

    # 팝너트 표시하기    
    P5_hole = [P5_hole1, P5_hole2, P5_hole3, P5_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P5_width]
    tx = rx
    ty = ry+CPH    
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P5_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6_popnut")
                insert_block(tx + sum, ry,"M6_popnut_upset")
            if index == 0 :
                d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)         

    # 상부 전체치수
    d(doc,  rx , ry+CPH, rx + P5_width , ry+CPH, 120, direction="up")

    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P5_handrailxpos):            
            if g is not None : 
                tx = x2 - g
                insert_block(tx , y2 + handrail_height , "handrail_bracket")                
                d(doc, tx, y2 + handrail_height , x2 , y2 + handrail_height , 100 + index*100, direction="down")                    
                line(doc, tx , rib_posy + 10 , tx , rib_posy - panel_width - 10 , layer='CLphantom')  

    d(doc, x1, y1, tx , y2 + handrail_height , 150, direction="left")    

    yp_bottom = ry  + 1
    yp_upper = ry + CPH - 1

    rb_list = panel_rib(P5_width, P5_handrailxpos)    
    # print(f"P5 패널의 종보강 위치: {rb_list}")
    # print(f"P5 핸드레일 위치: {P5_handrailxpos}")
    for index, g in enumerate(rb_list):
        bp = rx + P5_width - g
        xlist = [bp , bp-40 ,bp-20 ,bp + 20 ,bp + 40 ]       
        # 모자보강
        rectangle(doc, xlist[2] , yp_bottom, xlist[3] , yp_upper, layer='0')
        rectangle(doc, xlist[1] , yp_bottom+panel_wing+1, xlist[4] , yp_upper-panel_wing-1, layer='구성선') # 구성선은 회색선    
        line(doc, xlist[0] , yp_bottom, xlist[0] , yp_upper, layer='CLphantom')  
        # 치수선
        # print (f"index = {index}, x : {bp}")        
        # print (f" len(rb_list) = { len(rb_list)}" )        
        if index == 0:
            d(doc, x3, y3,  bp , y4, 150, direction="down")     
        else:
            dc(doc, bp,y3)

        # 단면도에 모자보강 위치 표시하기
        line(doc, bp , rib_posy + 10 , bp , rib_posy - panel_width - 10 , layer='0')  
            
        # 5x10 장공 용접홀          
        insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
        insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")                     

    if len(rb_list)-1 > 0 :  # 마지막인 경우
        dc(doc, x4,y4)            

    # 장공홀 표현하기 M6_nut
    gap = 0    
    length = CPH - 85 + popnut_height 
    hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
    leftx = x1 + 1.5
    rightx = x2 - (panel_width - P5_holegap)
    ty = y2

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "M6_nut")
            # insert_block(rightx, ty + g, "M6_nut")
            circle_cross(doc, rightx, ty + g , 9, layer='0')    # P4와 연결되는 홀 기둥

        if index == 0 :
            d(doc, x2, ty + g, rightx, ty + g,  150, direction="up" )    
            d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    

            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x3, y3)    

    # 우측 전체 치수선
    d(doc, x2, y2, x3, y3, 220, direction="right" )  

    ###########################################################################
    # P5 전개도 그리기
    ###########################################################################

    rx = pagex + P5_width + 1200                         
    x1 = rx
    y1 = pagey
    x2 = x1 + P5_width - (panel_width+5)*2
    y2 = y1    
    x3 = x2
    y3 = y2 + panel_wing + 4 
    x4 = x3 + panel_wing + 4 
    y4 = y3 
    x5 = x4 
    y5 = y4 + 14.5 if br == 1.5 else y4 + 16
    x6 = x5 + 45 if br == 1.5 else x5 + 47
    y6 = y5 
    x7 = x6 
    y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
    x8 = x7 - 45 if br == 1.5 else x7 - 47 
    y8 = y7 
    x9 = x8 
    y9 = y8 + 14.5 if br == 1.5 else y8 + 16
    x10 = x9 - (panel_wing + 4)
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_wing + 4 
    x12 = x11 - P5_width + (panel_width+5)*2
    y12 = y11
    x13 = x12 
    y13 = y12 - (panel_wing + 4)
    x14 = x13 - (panel_wing + 4)
    y14 = y13
    x15 = x14 
    y15 = y14 - 14.5 if br == 1.5 else y14 - 16
    x16 = x15 - 45 if br == 1.5 else x15 - 47
    y16 = y15 
    x17 = x16 
    y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
    x18 = x17 + 45 if br == 1.5 else x17 + 47
    y18 = y17 
    x19 = x18
    y19 = y18 - (panel_wing + 4)
    x20 = x19 + (panel_wing + 4)
    y20 = y19 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 20
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                     
    gap = 0
    gap = - 1.5 if br == 1.5 else - 1
    length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
    hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
    leftx = x17 + (panel_width*2 + panel_wing - P5_holegap - br * 4 )
    rightx = x6 - (panel_width+panel_wing - P5_holegap - br * 2 )
    ty = y6

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "8x16_vertical")
            insert_block(rightx, ty + g, "8x16_vertical")
        if index == 0 :
            d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x11, y11)    
    # 장공치수선 그리기    좌,우 떨어짐
    for index, g in enumerate(hole):
        if index == 5 :
            d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
            d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )                        
        
    yp_bottom = y1
    yp_upper = y11

    rb_list = panel_rib(P5_width, P5_handrailxpos)    
    # print(f"P5 패널의 종보강 위치: {rb_list}")
    # print(f"P5 핸드레일 위치: {P5_handrailxpos}")
    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            text = "%%C3"
            dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="up")                    
            # 5mm 치수선표시
            d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
            d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

        circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
        circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
        if index == 0 :
            d(doc, x16, y16, bp, y11, 200, direction="down")
        else:
            dc(doc, bp,y11)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x7,y7)     

    if handrail_height > 0 :
        # 핸드레일 그리기       
        for index, g in enumerate(P5_handrailxpos):            
            if g is not None : 
                tx = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
                ty = y6 + handrail_height - 1  if br == 1 else y6 + handrail_height - 1.5 
                if len(P5_handrailxpos) == 1 :
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    d(doc, tx, ty , x6 , ty , 100  , direction="up")                    
                    d(doc, tx, ty , x17 , ty , 100  , direction="up")                    
                    d(doc, x2, y2, tx , ty , 280, direction="right")  
                    # 보강자리에서 간격 X 축 치수선
                    d(doc, bp, ty, tx , ty , 180, direction="down")  
                else:
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    if index == 0 :
                        d(doc, x16 , ty , tx, ty , 100  , direction="up") 
                    else:                         
                        dc(doc, tx , ty )
                        dc(doc, x6 , ty )
                        # 보강자리에서 간격 X 축 치수선
                        d(doc, x2, y2, tx , ty , 280, direction="right") 
                        d(doc, bp, ty, tx , ty , 180, direction="down")  
                       
    # 9파이 팝너트 연결홀 상부/하부
    P5_hole = [P5_hole1, P5_hole2, P5_hole3, P5_hole4]   

    limit_point = [P5_width]
    tx = x16 + 30 if br == 1.5 else x16 + 32
    upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
    lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point
    # 상부의 연결홀
    for index, hole in enumerate(P5_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
            if index == 0 :
                holeupperx = tx + sum                               
                holeuppery = upper_ty                       
                text = "%%C9 M6 POPNUT(머리5mm)"
                dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="up")                
                d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

            elif index == len(hole_variables) - 1 :
                dc(doc, x7, y7)                   
            else:
                dc(doc, tx + sum, upper_ty)                                   
    # 하부에 연결홀 타공
    sum = 0
    for index, hole in enumerate(P5_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
            if index == 0 :
                holelowerx = tx + sum                               
                holelowery = lower_ty                          
                d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

            elif index == len(hole_variables) - 1 :
                dc(doc, x6, y6)                   
            else:
                dc(doc, tx + sum, lower_ty)
                
    # 상부치수선    
    d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
    dc(doc, x9 , y9)    
    dc(doc, x7, y7)
    # 상부 전체치수선
    d(doc, x16, y16, x7 ,y7, 250, direction="up")

    # 하부치수선    
    d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
    d(doc, x2, y2, x6 ,y6, 110, direction="down")        
    # 하부 2단 절곡 만나는 곳 치수선
    d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
    dc(doc, x4 , y4)    
    dc(doc, x6 , y6)
    # 하부 전체치수선
    d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
    
    # 오른쪽 15mm 표기
    d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
    # 오른쪽 최종 치수선
    d(doc, x11, y11 , x7, y7, 300, direction="right")
    dc(doc, x6, y6)
    dc(doc, x2, y2)    

    # 왼쪽 치수선 20mm 
    d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
    d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
    # 왼쪽 치수선 전체
    d(doc, x12, y12, x1, y1, 280, direction="left")

    # 모자보강 Y위치 저장 y3
    rib_posy = y3    

    #######################################  
    # P5,P7 단면도 (상부에 위치한)
    #######################################  
    x1 = x1 - panel_width + 6
    y1 = pagey + CH + 794
    x2 = x1 - panel_wing
    y2 = y1 
    x3 = x2
    y3 = y2 - panel_width
    x4 = x3 + P5_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - panel_width + thickness*2
    x10 = x9 - P5_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_width - thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    # B작업 표기
    if P5_width == P7_width :
        insert_block(x5 + 700 , y5,"b_work")

    x13 = x3
    y13 = y3 + P5_holegap
    x14 = x4
    y14 = y4 + P5_holegap
    
    line(doc, x13-10, y13, x13+10, y13, layer="CL") 
    line(doc, x14-10, y14, x14+10, y14, layer="CL") 
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 150, direction='up')   
    d(doc, x6, y6, x5, y5, 150, direction='up')   
    # 좌측    
    d(doc, x13-10, y13, x3, y3, 100, direction='left')      
    d(doc, x2, y2, x3, y3, 180, direction='left')  

    # 전체하부
    d(doc, x3, y3, x4, y4, 350, direction='down')              
    d(doc, x14+10, y14, x4, y4, 130, direction='right')    

    x13, y13 =  x1-10, y3 + P5_holegap    
    d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
    d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')   
    rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
    # 하단 날개 23 표기 width 25 -2
    
    P5_hole = [P5_hole4, P5_hole3, P5_hole2, P5_hole1]     
    limit_point = [P5_width]
    tx = x3 
    ty = y3 + P5_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P5_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 270, direction="down" , option='reverse')                                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)        

    # 본판과 역순으로 정렬
    # reverse_P5_handrailxpos = P5_handrailxpos[::-1]
    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P5_handrailxpos):            
            if g is not None : 
                tx = x3 + g                
                d(doc, tx, y3, x3 , y3 - 10 , 130 + index*40, direction="down")                    
                line(doc, tx , y3 + 10 , tx , y3 - 10 , layer='CLphantom')  

    # 보강자리 표시
    rb_list = panel_rib(P5_width, P5_handrailxpos)    
    for index, g in enumerate(rb_list):        
        bp = x3 + g
        line(doc, bp, y3-10 , bp , y3+10, layer='0')                  
        if index == 0 :
            d(doc, bp, y3-10, x3, y3, 80, direction="down",option='reverse')
        else:
            dc(doc, bp,y3-10)

    # P5, P7은 side panel과 결합하니, 홀의 결합위치가 다르다. 주의)
    line(doc, x3 + (panel_width-P5_holegap) , y4 + 10 ,x3 + (panel_width-P5_holegap) , y4 - 10 , layer='CLphantom')  
    d(doc,  x3 + (panel_width-P5_holegap) , y3 - 10 , x3 , y3 , 50, direction="down")

    #######################################  
    # P5,P7 단면도 (우측, 상부위치 아님)
    #######################################  
    top_panel_width = panel_width - 2
    x1 = pagex + P5_width*2 + 1000*2
    y1 = pagey + CH
    x2 = x1 
    y2 = y1 + panel_wing
    x3 = x2 - top_panel_width
    y3 = y2 
    x4 = x3 
    y4 = y3 - CPH
    x5 = x4 + top_panel_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_wing
    x7 = x6 - thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - panel_wing + thickness
    x9 = x8 - top_panel_width + thickness*2
    y9 = y8 
    x10 = x9 
    y10 = y9 + CPH - thickness*2
    x11 = x10 + top_panel_width - thickness*2
    y11 = y10 
    x12 = x11 
    y12 = y11 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3 + P5_holegap
    y13 = y3
    x14 = x4 + P5_holegap
    y14 = y4
    
    line(doc, x13, y13+10, x13, y13-10, layer="CL")
    line(doc, x14, y14+10, x14, y14-10, layer="CL")
    d(doc, x1, y1, x2, y2, 150, direction='right')
    d(doc, x3, y3, x13, y13+10, 80, direction='up')
    d(doc, x3, y3, x2, y2, 180, direction='up')
    d(doc, x14, y14-10, x4, y4, 100, direction='down')
    d(doc, x4, y4, x5, y5, 180, direction='down')

    d(doc, x3, y3, x4, y4, 100, direction='left')
    d(doc, x6, y6, x5, y5, 150, direction='right')

    ##################### 코멘트 ##########################
    mx = frameXpos + P5_width*2 + 3000
    my = frameYpos +2000     
    page_comment(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + P5_width*2 + 3500
    my = frameYpos +2000             
    desx = mx - 1300
    desy = my + 1000
    unitsu = 1
    if P5_width == P7_width :
        text = 'REAR PANEL(#5,#7)'
        unitsu= 2
    else:
        text = 'REAR PANEL(#5)'        

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')  
    frameXpos = frameXpos + TargetXscale + 400


############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################


    #########################################################################################
    # 9page P6 
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 6851 
    TargetYscale = 4870 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
        
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "REAR PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # P6 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
    ###################################################
    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx + panel_wing
    y1 = ry + CH + 500
    x2 = x1 - panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 + P6_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 + thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  + panel_width - thickness*2
    x10 = x9 - P6_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 - panel_width + thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   
    
    x13, y13 =  x1-10, y3-P6_holegap
    line(doc, x3-10, y3-P6_holegap, x3+ 10, y3-P6_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y4-P6_holegap, x4+ 10, y4-P6_holegap , layer='CLphantom') # '구성선' 회색선
    rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')
    
    # 전면 벽 판넬 변수 목록 초기화
    P6_hole = [P6_hole1, P6_hole2, P6_hole3, P6_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P6_width]
    tx = x3 
    ty = y3 - P6_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P6_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)                   
       
    d(doc,  x3 , y3, x4, y4, 173, direction="up")
    d(doc,  x13 , y13, x3, y3, 140, direction="left")
    d(doc,  x5 , y5, x4, y4, 190, direction="right")

    d(doc,  x6, y6, x5 , y5,  80, direction="down")    
    d(doc,  x1 , y1, x2, y2, 80, direction="down")     

    # 모자보강 Y위치 저장 y3
    rib_posy = y3

    #############################################################
    # P6 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
    # P6 조립도 본체구성 표현
    #############################################################
        
    ry = pagey 

    rectangle(doc, rx, ry , rx+ P6_width, ry+CPH, layer='0')
    rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
    rectangle(doc, rx + P6_width , ry , rx+P6_width-panel_wing , ry+CPH , layer='0')

    # 세로 날개 표시 panel_wing
    line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
    line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
    line(doc, rx + P6_width - panel_wing, ry  ,rx + P6_width - panel_wing , ry + CPH, layer='0')
    line(doc, rx + P6_width - thickness, ry  ,rx + P6_width - thickness , ry + CPH, layer='22')

    # 상부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P6_width -  panel_wing - 4 ,ry+CPH , layer='0')
    line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P6_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
    # 하부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P6_width -  panel_wing - 4 ,ry,  layer='0')
    line(doc, rx + panel_wing + 4, ry+thickness , rx + P6_width -  panel_wing - 4 ,ry+thickness,  layer='22')


    # 중심선은 핸드레일 홀과 간섭이 없는지를 살펴야 한다. 그리고 새로 설정해야 한다.
    # line(doc, rx, ry + FH, rx+ P6_width, ry + FH, layer='magentaphantom')

    x1 = rx 
    y1 = ry 
    x2 = x1 + P6_width
    y2 = y1    
    x3 = x2 
    y3 = y2 + CPH
    x4 = x3 - P6_width
    y4 = y3 

    # 팝너트 표시하기    
    P6_hole = [P6_hole1, P6_hole2, P6_hole3, P6_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P6_width]
    tx = rx
    ty = ry+CPH    
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P6_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6_popnut")
                insert_block(tx + sum, ry,"M6_popnut_upset")
            if index == 0 :
                d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)         

    # 상부 전체치수
    d(doc,  rx , ry+CPH, rx + P6_width , ry+CPH, 120, direction="up")

    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P6_handrailxpos):            
            if g is not None : 
                tx = x2 - g
                insert_block(tx , y2 + handrail_height , "handrail_bracket")                
                d(doc, tx, y2 + handrail_height , x2 , y2 + handrail_height , 100 + index*100, direction="down")                    
                line(doc, tx , rib_posy + 10 , tx , rib_posy - panel_width - 10 , layer='CLphantom')  

    d(doc, x1, y1, tx , y2 + handrail_height , 150, direction="left")    

    yp_bottom = ry  + 1
    yp_upper = ry + CPH - 1

    rb_list = panel_rib(P6_width, P6_handrailxpos)    
    # print(f"P6 패널의 종보강 위치: {rb_list}")
    # print(f"P6 핸드레일 위치: {P6_handrailxpos}")
    for index, g in enumerate(rb_list):
        bp = rx + P6_width - g
        xlist = [bp , bp-40 ,bp-20 ,bp + 20 ,bp + 40 ]       
        # 모자보강
        rectangle(doc, xlist[2] , yp_bottom, xlist[3] , yp_upper, layer='0')
        rectangle(doc, xlist[1] , yp_bottom+panel_wing+1, xlist[4] , yp_upper-panel_wing-1, layer='구성선') # 구성선은 회색선    
        line(doc, xlist[0] , yp_bottom, xlist[0] , yp_upper, layer='CLphantom')  
        # 치수선
        # print (f"index = {index}, x : {bp}")        
        # print (f" len(rb_list) = { len(rb_list)}" )        
        if index == 0:
            d(doc, x3, y3,  bp , y4, 150, direction="down")     
        else:
            dc(doc, bp,y3)

        # 단면도에 모자보강 위치 표시하기
        line(doc, bp , rib_posy + 10 , bp , rib_posy - panel_width - 10 , layer='0')  
            
        # 5x10 장공 용접홀          
        insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
        insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")     
                

    if len(rb_list)-1 > 0 :  # 마지막인 경우
        dc(doc, x4,y4)            

    # 장공홀 표현하기 M6_nut
    gap = 0    
    length = CPH - 85 + popnut_height 
    hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
    leftx = x1 + 1.5
    rightx = x2 - 1.5
    ty = y2

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "M6_nut")
            insert_block(rightx, ty + g, "M6_nut")
        if index == 0 :
            d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="up")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x3, y3)    

    # 우측 전체 치수선
    d(doc, x2, y2, x3, y3, 220, direction="right" )  

    ###########################################################################
    # P6 전개도 그리기
    ###########################################################################

    rx = pagex + P6_width + 1200                         
    x1 = rx
    y1 = pagey
    x2 = x1 + P6_width - (panel_width+5)*2
    y2 = y1    
    x3 = x2
    y3 = y2 + panel_wing + 4 
    x4 = x3 + panel_wing + 4 
    y4 = y3 
    x5 = x4 
    y5 = y4 + 14.5 if br == 1.5 else y4 + 16
    x6 = x5 + 45 if br == 1.5 else x5 + 47
    y6 = y5 
    x7 = x6 
    y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
    x8 = x7 - 45 if br == 1.5 else x7 - 47 
    y8 = y7 
    x9 = x8 
    y9 = y8 + 14.5 if br == 1.5 else y8 + 16
    x10 = x9 - (panel_wing + 4)
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_wing + 4 
    x12 = x11 - P6_width + (panel_width+5)*2
    y12 = y11
    x13 = x12 
    y13 = y12 - (panel_wing + 4)
    x14 = x13 - (panel_wing + 4)
    y14 = y13
    x15 = x14 
    y15 = y14 - 14.5 if br == 1.5 else y14 - 16
    x16 = x15 - 45 if br == 1.5 else x15 - 47
    y16 = y15 
    x17 = x16 
    y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
    x18 = x17 + 45 if br == 1.5 else x17 + 47
    y18 = y17 
    x19 = x18
    y19 = y18 - (panel_wing + 4)
    x20 = x19 + (panel_wing + 4)
    y20 = y19 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 20
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                     
    gap = 0
    gap = - 1.5 if br == 1.5 else - 1
    length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
    hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
    leftx = x17 + (panel_width+panel_wing - P6_holegap - br * 2 )
    rightx = x6 - (panel_width+panel_wing - P6_holegap - br * 2 )
    ty = y6

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "8x16_vertical")
            insert_block(rightx, ty + g, "8x16_vertical")
        if index == 0 :
            d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="up")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x11, y11)    
    # 장공치수선 그리기    좌,우 떨어짐
    for index, g in enumerate(hole):
        if index == 4 :
            d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
            d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )        

    yp_bottom = y1
    yp_upper = y11

    rb_list = panel_rib(P6_width, P6_handrailxpos)    
    # print(f"P6 패널의 종보강 위치: {rb_list}")
    # print(f"P6 핸드레일 위치: {P6_handrailxpos}")
    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            text = "%%C3"
            dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="up")                    
            # 5mm 치수선표시
            d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
            d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

        circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
        circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
        if index == 0 :
            d(doc, x16, y16, bp, y11, 200, direction="down")
        else:
            dc(doc, bp,y11)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x7,y7)     

    if handrail_height > 0 :
        # 핸드레일 그리기       
        for index, g in enumerate(P6_handrailxpos):            
            if g is not None : 
                tx = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
                ty = y6 + handrail_height - 1  if br == 1 else y6 + handrail_height - 1.5 
                if len(P6_handrailxpos) == 1 :
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    d(doc, tx, ty , x6 , ty , 100  , direction="up")                    
                    d(doc, tx, ty , x17 , ty , 100  , direction="up")                    
                    d(doc, x2, y2, tx , ty , 280, direction="right")  
                    # 보강자리에서 간격 X 축 치수선
                    d(doc, bp, ty, tx , ty , 180, direction="down")  
                else:
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    if index == 0 :
                        d(doc, x16 , ty , tx, ty , 100  , direction="up") 
                    else:                         
                        dc(doc, tx , ty )
                        dc(doc, x6 , ty )
                        # 보강자리에서 간격 X 축 치수선
                        d(doc, x2, y2, tx , ty , 280, direction="right") 
                        d(doc, bp, ty, tx , ty , 180, direction="down")  
                  
     
    # 9파이 팝너트 연결홀 상부/하부
    P6_hole = [P6_hole1, P6_hole2, P6_hole3, P6_hole4]   

    limit_point = [P6_width]
    tx = x16 + 30 if br == 1.5 else x16 + 32
    upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
    lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point
    # 상부의 연결홀
    for index, hole in enumerate(P6_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
            if index == 0 :
                holeupperx = tx + sum                               
                holeuppery = upper_ty                       
                text = "%%C9 M6 POPNUT(머리5mm)"
                dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="up")                
                d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

            elif index == len(hole_variables) - 1 :
                dc(doc, x7, y7)                   
            else:
                dc(doc, tx + sum, upper_ty)                                   
    # 하부에 연결홀 타공
    sum = 0
    for index, hole in enumerate(P6_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
            if index == 0 :
                holelowerx = tx + sum                               
                holelowery = lower_ty                          
                d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

            elif index == len(hole_variables) - 1 :
                dc(doc, x6, y6)                   
            else:
                dc(doc, tx + sum, lower_ty)                                   
                
    # 상부치수선    
    d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
    dc(doc, x9 , y9)    
    dc(doc, x7, y7)
    # 상부 전체치수선
    d(doc, x16, y16, x7 ,y7, 250, direction="up")

    # 하부치수선    
    d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
    d(doc, x2, y2, x6 ,y6, 110, direction="down")        
    # 하부 2단 절곡 만나는 곳 치수선
    d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
    dc(doc, x4 , y4)    
    dc(doc, x6 , y6)
    # 하부 전체치수선
    d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
    
    # 오른쪽 15mm 표기
    d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
    # 오른쪽 최종 치수선
    d(doc, x11, y11 , x7, y7, 300, direction="right")
    dc(doc, x6, y6)
    dc(doc, x2, y2)    

    # 왼쪽 치수선 20mm 
    d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
    d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
    # 왼쪽 치수선 전체
    d(doc, x12, y12, x1, y1, 280, direction="left")
   

    #######################################  
    # P6 단면도 (상부에 위치한)
    #######################################  

    x1 = x1 - panel_width + 6
    y1 = pagey + CH + 800
    x2 = x1 - panel_wing
    y2 = y1 
    x3 = x2
    y3 = y2 - panel_width
    x4 = x3 + P6_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - panel_width + thickness*2
    x10 = x9 - P6_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_width - thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3
    y13 = y3 + P6_holegap
    x14 = x4
    y14 = y4 + P6_holegap
    
    line(doc, x13-10, y13, x13+10, y13, layer="CL") 
    line(doc, x14-10, y14, x14+10, y14, layer="CL") 
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 150, direction='up')   
    d(doc, x6, y6, x5, y5, 150, direction='up')   
    # 좌측    
    d(doc, x13-10, y13, x3, y3, 100, direction='left')      
    d(doc, x2, y2, x3, y3, 180, direction='left')  

    # 전체하부
    d(doc, x3, y3, x4, y4, 350, direction='down')              
    d(doc, x14+10, y14, x4, y4, 130, direction='right')    

    x13, y13 =  x1-10, y3 + P6_holegap        
    rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
    # 하단 날개 23 표기 width 25 -2
    d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
    d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')  

    P6_hole = [P6_hole4, P6_hole3, P6_hole2, P6_hole1]     
    limit_point = [P6_width]
    tx = x3 
    ty = y3 + P6_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P6_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 280, direction="down" , option='reverse')                                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)        

    # 보강위치 단면도 표기
    rb_list = panel_rib(P6_width, P6_handrailxpos)        
    preX = x3
    for index, g in enumerate(rb_list):      
        bp = x3 + g
        line(doc, bp, y3-10 , bp , y3+10, layer='0')                  
        d(doc, preX, y3-10, bp, y3, 170, direction="down")
        preX = bp            
    dc(doc, x4,y4)   
          
    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P6_handrailxpos):            
            if g is not None : 
                tx = x3 + g                
                d(doc, tx, y3, x3 , y3 - 10 , 90 + index*40, direction="down")                    
                line(doc, tx , y3 + 10 , tx , y3 - 10 , layer='CLphantom')                    

    #######################################  
    # P6 단면도 (우측)
    #######################################  
    top_panel_width = panel_width - 2
    x1 = pagex + P6_width*2 + 1000*2
    y1 = pagey + CH
    x2 = x1 
    y2 = y1 + panel_wing
    x3 = x2 - top_panel_width
    y3 = y2 
    x4 = x3 
    y4 = y3 - CPH
    x5 = x4 + top_panel_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_wing
    x7 = x6 - thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - panel_wing + thickness
    x9 = x8 - top_panel_width + thickness*2
    y9 = y8 
    x10 = x9 
    y10 = y9 + CPH - thickness*2
    x11 = x10 + top_panel_width - thickness*2
    y11 = y10 
    x12 = x11 
    y12 = y11 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3 + P6_holegap
    y13 = y3
    x14 = x4 + P6_holegap
    y14 = y4
    
    line(doc, x13, y13+10, x13, y13-10, layer="CL")
    line(doc, x14, y14+10, x14, y14-10, layer="CL")
    d(doc, x1, y1, x2, y2, 150, direction='right')
    d(doc, x3, y3, x13, y13+10, 80, direction='up')
    d(doc, x3, y3, x2, y2, 180, direction='up')
    d(doc, x14, y14-10, x4, y4, 100, direction='down')
    d(doc, x4, y4, x5, y5, 180, direction='down')

    d(doc, x3, y3, x4, y4, 100, direction='left')
    d(doc, x6, y6, x5, y5, 150, direction='right')

    ##################### 코멘트 ##########################
    mx = frameXpos + P6_width*2 + 3000
    my = frameYpos +2000     
    page_comment(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + P6_width*2 + 4000
    my = frameYpos +2000             
    desx = mx - 1300
    desy = my + 1000    
    text = 'REAR PANEL(#6)' 
    unitsu = SU

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')   
    
    frameXpos = frameXpos + TargetXscale + 400



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################


    #########################################################################################
    # 10page transom 
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 2730 + (OP-900) 
    TargetYscale = 1965 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
        
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "CAR TRANSOM ASS", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # TRANSOM 일체형 판넬 조립도 (도면의 상부에 위치한 단면도) 평면도
    ###################################################
    

    transom_thickness = 30 # column_width와 다름, 주의요함

    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx - 200
    y1 = ry + 1000 + (CH-2500) - 80
    x2 = x1 + OP
    y2 = y1    
    x3 = x2 
    y3 = y2 + column_width
    x4 = x3 - OP
    y4 = y3 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   

    line(doc, x1, y1+thickness, x2, y1+thickness, layer="22")    # cyan hidden line
    line(doc, x4, y4-thickness, x3, y4-thickness, layer="22")    # cyan hidden line
    
    slot_ypos = y3 - 15
    slot_gap = 25
    slot_startX = 50
    line(doc, x1+20, y3-15, x3-20, y3-15 , layer='CLphantom') # '구성선' 회색선
    insert_block(x1 + slot_startX, slot_ypos,"8x16_vertical_draw")
    insert_block(x1 + slot_startX+slot_gap, slot_ypos,"8x16_vertical_draw")
    insert_block(x1 + slot_startX+slot_gap*2, slot_ypos,"8x16_vertical_draw")
    insert_block(x3 - slot_startX, slot_ypos,"8x16_vertical_draw")
    insert_block(x3 - slot_startX-slot_gap, slot_ypos,"8x16_vertical_draw")
    insert_block(x3 - slot_startX-slot_gap*2, slot_ypos,"8x16_vertical_draw")
    d(doc,  x4 , y4, x1 + slot_startX, slot_ypos, 100, direction="up")       
    d(doc,  x3 , y3, x3 - slot_startX, slot_ypos, 100, direction="up")       
    
    # 중간 5개홀 
    slot_gap = 75
    slot_startX = OP/2
    insert_block(x1 + slot_startX, slot_ypos,"8x16_vertical_draw")
    insert_block(x1 + slot_startX+slot_gap, slot_ypos,"8x16_vertical_draw")
    insert_block(x1 + slot_startX+slot_gap*2, slot_ypos,"8x16_vertical_draw")    
    insert_block(x1 + slot_startX-slot_gap, slot_ypos,"8x16_vertical_draw")
    insert_block(x1 + slot_startX-slot_gap*2, slot_ypos,"8x16_vertical_draw")    
               
    d(doc,  x3 , y3, x4, y4, 200, direction="up")
    d(doc,  x3 , slot_ypos, x3, y3, 100, direction="right")

    rectangle(doc, x1,y1,x3,y1+15,layer="0")
    rectangle(doc, x4,y4,x3,y3-30,layer="0")
    # 보강 63 x 40 표현 양쪽 끝단
    rectangle(doc, x1+thickness,y1+15,x1+thickness+40,y1+15+63-15,layer="0")
    rectangle(doc, x2-thickness,y1+15,x2-thickness-40,y1+15+63-15,layer="0")

    #############################################################
    # 일체형 transom  조립도 본체 만들기
    # 조립도 본체구성 표현
    #############################################################

    y1 = ry + 300 + (CH-2500) 
    x2 = x1 + OP
    y2 = y1    
    x3 = x2 
    y3 = y2 + TR_TRH
    x4 = x3 - OP
    y4 = y3 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   

    line(doc, x1, y1+thickness, x2, y1+thickness, layer="22")    # cyan hidden line
    line(doc, x4, y4-thickness, x3, y4-thickness, layer="22")    # cyan hidden line

    d(doc, x4+0.5 , y4, x4, y4, 100, direction="up")    
    d(doc, x4 , y4, x4+40, y4, 100, direction="up")    
    d(doc, x3-0.5 , y3, x3, y3, 100, direction="up")    
    d(doc, x3 , y3, x3-40, y3, 100, direction="up")    

    rectangle(doc, x1,y1,x3,y1+30,layer="0")
    # 보강 표현 양쪽 끝단
    rectangle(doc, x1+thickness,y1+thickness,x1-thickness+40,y4-thickness,layer="0")
    rectangle(doc, x2-thickness,y1+thickness,x3+thickness-40,y4-thickness,layer="0")
        
    slot_gap = 25
    slot_startX = x1 + OP/2
                   
    # 중심선
    line(doc, slot_startX, y3 + 30, slot_startX, y1 - 30 , layer='CLphantom')


    ###########################################################################
    # transom 왼쪽 단면도
    ###########################################################################
    first_wing = 30
    second_wing = 15

    x1 = x1 - 250
    y1 = y4 
    x2 = x1 - 15
    y2 = y1    
    x3 = x2
    y3 = y2 - TR_TRH 
    x4 = x3 + column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing
    x6 = x5 - second_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + second_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - first_wing + thickness*2
    x10 = x9 - column_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + TR_TRH - thickness*2
    x12 = x11 + 15 - thickness
    y12 = y11

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")    

    line(doc, x2 + 8 , y1 + 10 , x2 + 8 ,  y1 - 10 , layer='CLphantom') # '구성선' 회색선  
                     
    # 안에 들어가는 보강표현하기
    xx1 = x1 + 3 + 15 + thickness
    yy1 = y1 - 2
    xx2 = xx1 - 33 + thickness
    yy2 = yy1    
    xx3 = xx2
    yy3 = y3 + 2
    xx4 = xx3 + 63
    yy4 = yy3 
    xx5 = xx4 
    yy5 = yy4 + 30
    xx6 = xx5 - 30 - thickness
    yy6 = yy5 
    
    prev_x, prev_y = xx1, yy1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'xx{i}'), eval(f'yy{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, xx1, yy1, layer="0")      
                     
    line(doc, xx2 + thickness , yy1 , xx2 + thickness  ,  yy3 , layer='22') # '구성선' 회색선           

    holex1 = x2 + 18
    holey1 = y2 - 50            
    holex2 = x3 + 18
    holey2 = y3 + 50            
    holex3 = x3 + 43
    holey3 = y3 + 20

    insert_block(holex1, holey1,"8x16_vertical_draw")        
    insert_block(holex2, holey2,"8x16_vertical_draw")        
    insert_block(holex3, holey3,"8x16_vertical_draw")     

    line(doc,holex1 , holey1+20 , holex1  ,  holey2-20 , layer='CLphantom') # '구성선' 회색선       

    d(doc, x2 , y2, holex1, holey1, 100, direction="up", option='reverse')   
    d(doc, x2 , y2, holex1, holey1, 50, direction="left")   
    dc(doc, holex2,holey2)
    dc(doc, x3,y3, option='reverse')   
    d(doc, x2 , y2, x3, y3, 130, direction="left")   
    d(doc, holex2 , holey2, holex3 , holey3,  100, direction="down")   
    d(doc, x3 , y3, holex3 , holey3,  180, direction="down")   
    d(doc, x3 , y3 , x4 , y4 ,  260, direction="down")   
    

    ###########################################################################
    # transom 오른쪽 상세 단면도
    ###########################################################################

    first_wing = 30
    second_wing = 15

    x1 = rx + OP + 500
    y1 = ry + (CH-2500) + 1150 - 150
    x2 = x1 - first_wing
    y2 = y1    
    x3 = x2
    y3 = y2 - TR_TRH 
    x4 = x3 + column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing
    x6 = x5 - second_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + second_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - first_wing + thickness*2
    x10 = x9 - column_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + TR_TRH - thickness*2
    x12 = x11 + 15 - thickness
    y12 = y11

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")    
    
    # 중간 적색선 위치 2개 (치수선 용도)
    x13 = x2 + first_wing/2
    y13 = y1 + 10 
    x14 = x6 + second_wing/2
    y14 = y6 + 10 
    line(doc, x13, y1 + 10 ,x13 ,  y1 - 10 , layer='CLphantom') # '구성선' 회색선  
    line(doc, x14, y6 + 10 ,x14 ,  y6 - 10 , layer='CLphantom') # '구성선' 회색선  

    # 절곡도 문구 넣기
    put_commentLine(x3 - 50, y3 - 350)    

    d(doc, x2 , y2, x13, y13, 50, direction="up", option='reverse')   
    d(doc, x2 , y2, x1, y1, 130, direction="up", option='reverse')   
    d(doc, x2 , y2, x3, y3, 100, direction="left")       
    d(doc, x3 , y3, x4, y4, 100, direction="down")   
    d(doc, x4 , y4, x5, y5, 100, direction="right", option='reverse')   
    d(doc, x5 , y5, x14, y14, 50, direction="up", option='reverse')   
    d(doc, x5 , y5, x6, y6, 130, direction="up", option='reverse')       
    
    ##################### 코멘트 ##########################
    mx = frameXpos + 1000 + (OP-900) 
    my = frameYpos + 600
    page_comment_small(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + 1000 + (OP-900) 
    my = frameYpos + 100
    desx = mx - 1200
    desy = my + 400    
    text = 'CAR TRANSOM ASY' 
    unitsu = SU

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 30 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -50 , 30, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 100 , 30, str(textstr), layer='0')   
    
    frameXpos = frameXpos + TargetXscale + 400



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################


    #########################################################################################
    # 11page transom 실제 전개도 및 보강 전개도
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 3452 + (OP-900) 
    TargetYscale = 2460 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
        
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "TRANSOM BRACKET", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # TRANSOM 일체형 전개도 실제 가공품
    ###################################################
    rx = math.floor(pagex)
    ry = math.floor(pagey)

    transom_thickness = 30

    first_wing = 30
    second_wing = 15

    x1 = rx - 400
    y1 = ry + 800 + (CH-2500)
    x2 = x1 + OP - 4
    y2 = y1    
    x3 = x2
    y3 = y2 + 15 
    x4 = x3 + 2
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing + TRH + column_width + transom_thickness + second_wing - br*8 - 15
    x6 = x5 - OP
    y6 = y5 
    x7 = x6 
    y7 = y6 - (first_wing + TRH + column_width + transom_thickness + second_wing - br*8 - 15)
    x8 = x7 + 2
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")   
    
    slot_ypos = y6 - 15
    slot_gap = 25
    slot_startX = 50    

    slotx1 = x7 + slot_startX
    slotx2 = x7 + slot_startX+slot_gap
    slotx3 = x7 + slot_startX+slot_gap*2
    
    slotx9 = x5 - slot_startX
    slotx10 = x5 - slot_startX-slot_gap
    slotx11 = x5 - slot_startX-slot_gap*2

    insert_block(slotx1, slot_ypos,"8x16_vertical")
    insert_block(slotx2, slot_ypos,"8x16_vertical")
    insert_block(slotx3, slot_ypos,"8x16_vertical")
    insert_block(slotx9, slot_ypos, "8x16_vertical")
    insert_block(slotx10, slot_ypos,"8x16_vertical")
    insert_block(slotx11, slot_ypos,"8x16_vertical")

    # 중간 5개홀 
    slot_gap = 75
    slot_startX = OP/2
    slotx4 = x7 + slot_startX-slot_gap*2
    slotx5 = x7 + slot_startX-slot_gap
    slotx6 = x7 + slot_startX
    slotx7 = x7 + slot_startX+slot_gap
    slotx8 = x7 + slot_startX+slot_gap*2

    insert_block(slotx4, slot_ypos,"8x16_vertical")
    insert_block(slotx5, slot_ypos,"8x16_vertical")
    insert_block(slotx6, slot_ypos,"8x16_vertical")    
    insert_block(slotx7, slot_ypos,"8x16_vertical")
    insert_block(slotx8, slot_ypos,"8x16_vertical")    

    d(doc,  x6 , y6, slotx2, slot_ypos, 120, direction="up", option='reverse')       
    dc(doc, slotx6, slot_ypos)
    dc(doc, slotx10, slot_ypos)
    dc(doc, x5, y5)    
               
    d(doc,  slotx2 , slot_ypos, slotx1, slot_ypos, 50, direction="up")       
    d(doc,  slotx2 , slot_ypos, slotx3, slot_ypos, 50, direction="up")       
    d(doc,  slotx4 , slot_ypos, slotx6, slot_ypos, 50, direction="up")       
    d(doc,  slotx8 , slot_ypos, slotx6, slot_ypos, 50, direction="up")       
    d(doc,  slotx10 , slot_ypos, slotx9, slot_ypos, 50, direction="up")       
    d(doc,  slotx10 , slot_ypos, slotx11, slot_ypos, 50, direction="up")       

    # 왼쪽 치수선
    d(doc,  x6 , y6, slotx1, slot_ypos, 120, direction="left")       
    d(doc,  x7 , y7, x1, y1, 120, direction="left")       
    d(doc,  x4 , y4, x2, y2, 120, direction="right")       
    d(doc,  x5 , y5, x2, y2, 220, direction="right")    

    # 지시선 추가
    text = "8*16"
    dim_leader(doc,  slotx3, slot_ypos, slotx3 + 100, slot_ypos - 100,   text, direction="up")          

    # 우성인 경우는 6파이 홀 타공해줌
    # 일단 우성꺼로 생각하고 만든다.
    holex1 = x6 + OP/2
    holey1 = y1 + second_wing + column_width/2 + transom_thickness - br*4

    circle_cross(doc,holex1,holey1,6,layer="레이져")
    d(doc,  holex1 , y1, holex1, holey1, 100, direction="right")     
    # 지시선 추가
    text = "비상램프 %%c6 (우성만 가공)"
    dim_leader(doc,  holex1, holey1, holex1 - 150, holey1 +  150,   text, direction="up")       

    # 하부 전체치수
    d(doc,  x7 , y7, holex1, holey1, 220, direction="down")        
    d(doc,  x4 , y4, holex1, holey1, 220, direction="down")        

    # M5 육각 (십자마크)
    markx1 = x1 + 150 -2
    markx2 = x2 - 150 +2
    cross(doc, markx1, y1 + 7, 3.5, layer='레이져')
    cross(doc, markx2, y2 + 7, 3.5, layer='레이져')
    d(doc,  x7 , y7, markx1, y1+7, 120, direction="down")    
    d(doc,  x4 , y4, markx2, y2+7, 120, direction="down")    
    d(doc,  markx1 , y1, markx1, y1+7, 150, direction="right")    

    # 지시선 추가
    text = "M5육각"
    dim_leader(doc,  markx1, y1 + 7, markx1 - 100, y1 + 7 +  150,   text, direction="up")       

    # 좌우 2mm 표현
    d(doc,  x7 , y7, x1, y1, 50, direction="down")    
    d(doc,  x4 , y4, x2, y2, 50, direction="down")    

    

    ###########################################################################
    # transom 오른쪽 상세 단면도
    ###########################################################################

    first_wing = 30
    second_wing = 15

    x1 = rx + OP + 150
    y1 = ry + (CH-2500) + 1250 
    x2 = x1 - first_wing
    y2 = y1    
    x3 = x2
    y3 = y2 - TR_TRH 
    x4 = x3 + column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing
    x6 = x5 - second_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + second_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - first_wing + thickness*2
    x10 = x9 - column_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + TR_TRH - thickness*2
    x12 = x11 + 15 - thickness
    y12 = y11

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")    
    
    # 중간 적색선 위치 2개 (치수선 용도)
    x13 = x2 + first_wing/2
    y13 = y1 + 10 
    x14 = x6 + second_wing/2
    y14 = y6 + 10 
    x15 = x3 + column_width/2
    y15 = y3  
    line(doc, x13, y1 + 10 ,x13 ,  y1 - 10 , layer='CLphantom') # '구성선' 회색선  
    line(doc, x14, y6 + 10 ,x14 ,  y6 - 10 , layer='CLphantom') # '구성선' 회색선  
    line(doc, x15, y15 + 10 ,x15 ,  y15 - 10 , layer='CLphantom') # '구성선' 회색선  

    # 절곡도 문구 넣기
    put_commentLine(x3 - 50, y3 - 350)    

    d(doc, x2 , y2, x13, y13, 50, direction="up", option='reverse')   
    d(doc, x2 , y2, x1, y1, 130, direction="up", option='reverse')   
    d(doc, x2 , y2, x3, y3, 100, direction="left")           
    d(doc, x4 , y4, x5, y5, 100, direction="right", option='reverse')   
    d(doc, x5 , y5, x14, y14, 50, direction="up", option='reverse')   
    d(doc, x5 , y5, x6, y6, 130, direction="up", option='reverse')       

    d(doc, x15 , y15-10, x4, y4, 180, direction="down")   
    d(doc, x3 , y3, x4, y4, 250, direction="down")   


    ###########################################################################
    # transom 보강 단면도 ( 위, 아래 3미리 총 6mm 빠지는 크기임)
    ###########################################################################
    first_wing = 30
    second_wing = 33

    x1 = rx + OP + 150 + 600
    y1 = ry + (CH-2500) + 1250 - 200
    x2 = x1 - second_wing
    y2 = y1    
    x3 = x2
    y3 = y2 - TR_TRH + 6  # 보강은 6mm 작은것이다.
    x4 = x3 + column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing
    x6 = x5 - second_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + second_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - first_wing + thickness*2
    x10 = x9 - column_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + TR_TRH - 6 - thickness*2
    x12 = x11 + second_wing - thickness
    y12 = y11
                     
    # 안에 들어가는 보강표현하기
    xx1 = x1 
    yy1 = y1 
    xx2 = xx1 - second_wing 
    yy2 = yy1    
    xx3 = xx2
    yy3 = y3 
    xx4 = xx3 + 63
    yy4 = yy3 
    xx5 = xx4 
    yy5 = yy4 + 30
    xx6 = xx5 - 30
    yy6 = yy5 
    
    prev_x, prev_y = xx1, yy1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'xx{i}'), eval(f'yy{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, xx1, yy1, layer="0")      
                     
    line(doc, x2 + 16 , y1 + 10 , x2 + 16 ,  y1 - 10 , layer='CLphantom') # '구성선' 회색선                           

    holex1 = x2 + 16
    holey1 = y2 - 47            
    holex2 = x3 + 16
    holey2 = y3 + 47            
    holex3 = x3 + 41
    holey3 = y3 + 17

    insert_block(holex1, holey1,"8x16_vertical_draw")        
    insert_block(holex2, holey2,"8x16_vertical_draw")        
    insert_block(holex3, holey3,"8x16_vertical_draw")     

    line(doc,holex1 , holey1+20 , holex1  ,  holey2-20 , layer='CLphantom') # '구성선' 회색선       

    d(doc, x2 , y2, holex1, holey1, 100, direction="up", option='reverse')   
    d(doc, x2 , y2, holex1, holey1, 120, direction="left")   
    dc(doc, holex2,holey2)
    dc(doc, x3,y3, option='reverse')   
    d(doc, x2 , y2, x3, y3, 230, direction="left")   
    d(doc, holex2 , holey2, holex3 , holey3,  60, direction="left")   
    d(doc, holex2 , holey2, holex3 , holey3,  100, direction="down")   
    d(doc, x3 , y3, holex3 , holey3,  180, direction="down")   
    d(doc, x3 , y3 , xx4 , yy4 ,  260, direction="down")   
    

    ###########################################################################
    # transom 보강 위쪽 'ㄴ'자 형태 평면도?
    ###########################################################################
    first_wing = 40
    second_wing = 63
    thickval = 1.6

    x1 = x2
    y1 = y1 + 300
    x2 = x1 
    y2 = y1 - first_wing 
    x3 = x2 + second_wing
    y3 = y2
    x4 = x3
    y4 = y3 + thickval 
    x5 = x4 - second_wing + thickval
    y5 = y4 
    x6 = x5 
    y6 = y5 + first_wing - thickval
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")      
                     
    line(doc, x2 + 16 , y2 + 10 , x2 + 16 ,  y2 - 10 , layer='CLphantom')  # '구성선' 회색선                           
    line(doc, x2 + 41 , y2 + 10 , x2 + 41 ,  y2 - 10 , layer='CLphantom')  # '구성선' 회색선                           

    d(doc, x1 , y1 , x2 , y2,  150, direction="left")   
    d(doc, x1 , y1 , x4 , y4 ,  150, direction="up")   
    

    ###########################################################################
    # transom 보강 전개도
    ###########################################################################
    first_wing = 30
    second_wing = 70

    x1 = x1 + 600
    y1 = ry + (CH-2500) + 1250 - 200
    x2 = x1 - second_wing
    y2 = y1    
    x3 = x2
    y3 = y2 - TR_TRH + 6  # 보강은 6mm 작은것이다.
    x4 = x3 + column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing
    x6 = x5 - second_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + second_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - first_wing + thickness*2
    x10 = x9 - column_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + TR_TRH - 6 - thickness*2
    x12 = x11 + second_wing - thickness
    y12 = y11
                     
    # 안에 들어가는 보강표현하기
    xx1 = x1 
    yy1 = y1 
    xx2 = xx1 - second_wing 
    yy2 = yy1    
    xx3 = xx2
    yy3 = y3 
    xx4 = xx3 + 100.3
    yy4 = yy3 
    xx5 = xx4 
    yy5 = yy4 + 30
    xx6 = xx5 - 30.3
    yy6 = yy5 
    
    prev_x, prev_y = xx1, yy1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'xx{i}'), eval(f'yy{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, xx1, yy1, layer="레이져")      
                     
    holex1 = x2 + 53.3
    holey1 = y2 - 47            
    holex2 = x3 + 53.3
    holey2 = y3 + 47            
    holex3 = x3 + 78.3
    holey3 = y3 + 17

    insert_block(holex1, holey1,"8x16_vertical")        
    insert_block(holex2, holey2,"8x16_vertical")        
    insert_block(holex3, holey3,"8x16_vertical")     

    d(doc, x2 , y2, holex1, holey1, 100, direction="up", option='reverse')   
    d(doc, holex1, holey1,  xx5, yy5, 100, direction="up")
    d(doc, x2 , y2, holex1, holey1, 120, direction="left")   
    dc(doc, holex2,holey2)
    dc(doc, x3,y3, option='reverse')   
    d(doc, x2 , y2, x3, y3, 230, direction="left")   
    d(doc, holex2 , holey2, holex3 , holey3,  110, direction="left")   
    d(doc, holex2 , holey2, holex3 , holey3,  100, direction="down")   
    d(doc, x3 , y3, holex3 , holey3,  180, direction="down" , option='reverse')    
    d(doc, x3 , y3 , xx4 , yy4 ,  260, direction="down")   
    d(doc, xx4 , yy4 ,  holex3 , holey3,  150, direction="right")   
    d(doc, xx4 , yy4 ,  xx5 , yy5,  250, direction="right")   

    # 지시선 추가
    text = "8*16"
    dim_leader(doc,  holex2, holey2,  holex2 + 100, holey2+ 150,  text, direction="up")      
    
    ##################### part 설명 - 전개도 ##########################
    mx = x1 - 300
    my = y3 - 500
    desx = mx 
    desy = my 
    text = 'TRANSOM BRACKET' 
    unitsu = SU * 2

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 30 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"
    draw_Text(doc, desx , desy -50 , 30, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} EA (좌/우) SET"    
    draw_Text(doc, desx , desy - 100 , 30, str(textstr), layer='0')       


    ##################### 전개도 ##########################
    mx = x3
    my = y3 - 350
    text = '전 개 도'
    put_commentLine_string(mx, my, text) 
           
    ##################### 절곡도 ##########################
    mx = frameXpos + 1000 + (OP-900) 
    my = frameYpos + 800
    page_comment_small(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + 1000 + (OP-900) 
    my = frameYpos + 300
    desx = mx - 1200
    desy = my + 600    
    text = 'TRANSOM' 
    unitsu = SU

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 30 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -50 , 30, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 100 , 30, str(textstr), layer='0')   
    
    frameXpos = frameXpos + TargetXscale + 400



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################


    #########################################################################################
    # 12page transom backcover
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 2400 + (OP-900) 
    TargetYscale = 1750 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
        
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "CAR TRANSOM BACK COVER", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # CAR TRANSOM BACK COVER 
    ###################################################

    transom_thickness = 30 # column_width와 다름, 주의요함

    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx - 300
    y1 = ry + 800 
  
    insert_block(x1,  y1 ,"transom_cover")
  
    #############################################################
    # 일체형 transom BACK COVER 전개도
    #############################################################

    x1 = rx + 200
    y1 = ry + 800 
    x2 = x1 + 140 - 3
    y2 = y1    
    x3 = x2
    y3 = y2 + 8 
    x4 = x3 + 6
    y4 = y3 
    x5 = x4 
    y5 = y4 - 8
    x6 = x5 + OP-300 - 6
    y6 = y5 
    x7 = x6 
    y7 = y6 + 8
    x8 = x7 + 6
    y8 = y7 
    x9 = x8 
    y9 = y8 - 8
    x10 = x9 + 140 - 3
    y10 = y9 
    x11 = x10 
    y11 = y10 + 150
    x12 = x11 - OP + 20
    y12 = y11

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        if i == 4 :
            draw_arc(doc, x3, y3, x4, y4, 3, direction='up')
        elif i == 8 :
            draw_arc(doc, x7, y7, x8, y8, 3, direction='up')
        else:
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")   

    line(doc, x3 + 3 , y3 + 10 , x3 + 3 ,  y3 - 10 , layer='CLphantom')  # '구성선' 회색선    
    line(doc, x7 + 3 , y7 + 10 , x7 + 3 ,  y7 - 10 , layer='CLphantom')  # '구성선' 회색선    

    d(doc, x3+3 , y3+3, x1 , y1, 110, direction="left")    
    d(doc, x11 , y11, x10 , y10, 150, direction="right")    
    d(doc, x3 , y3, x4, y4, 100, direction="up")    
    d(doc, x1 , y1, x3+3, y1, 100, direction="down")    
    dc(doc, x7+3,y1)
    dc(doc, x10,y10)
    d(doc, x1 , y1, x10, y10, 200, direction="down")    
                   
    ##################### part 설명  ##########################
    mx = frameXpos + 1500 + (OP-900) 
    my = frameYpos + 400
    desx = mx - 1200
    desy = my + 400    
    text = 'CAR TRANSOM BACK COVER' 
    unitsu = SU

    textstr = f"* 일체형 CAR TRANSOM의 BACK COVER임."    
    draw_Text(doc, desx , desy+70 , 30 , str(textstr), layer='0')    
    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 30 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : 445 1.5T/1.2T 가능 "
    draw_Text(doc, desx , desy -50 , 30, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 100 , 30, str(textstr), layer='0')   
    
    frameXpos = frameXpos + TargetXscale + 400






















####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
# 분체형 1page Assy draw_page2
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################

def draw_page2():     
    global args  #수정할때는 global 선언이 필요하다. 단순히 읽기만 할때는 필요없다.    
    global start_time
    global drawdate, deadlinedate, text_style, exit_program, program_message, formatted_date, text_style_name
    global CW_raw, CD_raw, panel_thickness, su, LCframeMaterial, LCplateMaterial
    global input_CD, input_CW,CD,CW,drawdate_str , deadlinedate_str, drawdate_str_short, deadlinedate_str_short    
    global doc, msp , T5_is, text_style, distanceXpos, distanceYpos, thickness
    global P1_material, P1_width, P1_widthReal, P1_holegap, P1_hole1, P1_hole2, P1_hole3, P1_hole4, P1_COPType
    global P2_material, P2_width, P2_widthReal, P2_holegap, P2_hole1, P2_hole2, P2_hole3, P2_hole4, P2_COPType
    global P3_material, P3_width, P3_widthReal, P3_holegap, P3_hole1, P3_hole2, P3_hole3, P3_hole4, P3_COPType
    global P4_material, P4_width, P4_widthReal, P4_holegap, P4_hole1, P4_hole2, P4_hole3, P4_hole4, P4_COPType
    global P5_material, P5_width, P5_widthReal, P5_holegap, P5_hole1, P5_hole2, P5_hole3, P5_hole4, P5_COPType
    global P6_material, P6_width, P6_widthReal, P6_holegap, P6_hole1, P6_hole2, P6_hole3, P6_hole4, P6_COPType
    global P7_material, P7_width, P7_widthReal, P7_holegap, P7_hole1, P7_hole2, P7_hole3, P7_hole4, P7_COPType
    global P8_material, P8_width, P8_widthReal, P8_holegap, P8_hole1, P8_hole2, P8_hole3, P8_hole4, P8_COPType
    global P9_material, P9_width, P9_widthReal, P9_holegap, P9_hole1, P9_hole2, P9_hole3, P9_hole4, P9_COPType
    global P10_material, P10_width, P10_widthReal, P10_holegap, P10_hole1, P10_hole2, P10_hole3, P10_hole4, P10_COPType
    global P11_material, P11_width, P11_widthReal, P11_holegap, P11_hole1, P11_hole2, P11_hole3, P11_hole4, P11_COPType
    global column_width

    abs_x = 2000
    abs_y = 0

    #### 분리형은 column_width +5 키워준다. 일체형 기준 80이면 분리형은 85, 5mm 돌출 자동계산
    column_width = column_width + 5

    # HRsidegap 리스트 초기화
    HRsidegap = []
    if handrailSidegap1 is not None:
        HRsidegap.append(handrailSidegap1)
    if handrailSidegap2 is not None:
        HRsidegap.append(handrailSidegap2)
    if handrailSidegap3 is not None:
        HRsidegap.append(handrailSidegap3)
    if handrailSidegap4 is not None:
        HRsidegap.append(handrailSidegap4)
    if handrailSidegap5 is not None:
        HRsidegap.append(handrailSidegap5)    

    # Rear Handrail            
    HRreargap = []
    if handrailReargap1 is not None:
        HRreargap.append(handrailReargap1)
    if handrailReargap2 is not None:
        HRreargap.append(handrailReargap2)
    if handrailReargap3 is not None:
        HRreargap.append(handrailReargap3)
    if handrailReargap4 is not None:
        HRreargap.append(handrailReargap4)
    if handrailReargap5 is not None:
        HRreargap.append(handrailReargap5)            

    if handrail_height > 0 :
        P1_handrailxpos = {''}        

        panel_widths = {'P2': P2_width, 'P3': P3_width, 'P4': P4_width}    
        # 함수 호출 및 결과 확인 (필요한 경우 테스트 코드 작성)
        panel_name_to_search = 'P2'
        P2_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P2_handrailxpos}")

        panel_name_to_search = 'P3'
        P3_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P3_handrailxpos}")

        panel_name_to_search = 'P4'
        P4_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P4_handrailxpos}")

        # 오른쪽 벽면은 기존의 리스트를 역순으로 리스트 정리한다. 비 대칭일경우를 대비해서 코드를 이렇게 짠다.
        HRsidegap_reversed = list(reversed(HRsidegap))

        panel_widths = {'P8': P8_width, 'P9': P9_width, 'P10': P10_width}    
        
        panel_name_to_search = 'P8'
        P8_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap_reversed)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P8_handrailxpos}")

        panel_name_to_search = 'P9'
        P9_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap_reversed)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P9_handrailxpos}")

        panel_name_to_search = 'P10'
        P10_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRsidegap_reversed)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P10_handrailxpos}")

        # rear  핸드레일 홀    
        panel_widths = {'P5': P5_width, 'P6': P6_width, 'P7': P7_width}    
        
        panel_name_to_search = 'P5'
        P5_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRreargap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P5_handrailxpos}")

        panel_name_to_search = 'P6'
        P6_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRreargap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P6_handrailxpos}")

        panel_name_to_search = 'P7'
        P7_handrailxpos = calculate_handrail_hole_coordinates(panel_name_to_search, panel_widths, HRreargap)
        # print(f"핸드레일 홀의 x좌표 ({panel_name_to_search}): {P7_handrailxpos}")


    ##################################################################################################
    # ASSY 판넬배열도 1page
    ##################################################################################################
    # 0,0은 좌측 하단 기준 판넬 기준점을 기억하자 

    # 도면틀 넣기
    BasicXscale = 6851
    BasicYscale = 4115
    TargetXscale = CW + 3390
    TargetYscale = CD + 1700
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
    # print("1page 스케일 비율 : " + str(frame_scale))   
    frameYpos = abs_y - 1700 * frame_scale     
    insert_frame(abs_x-1500  , frameYpos  , frame_scale, "drawings_frame", "CAGE ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   
    
    # 각 P변수들에 대한 그룹화
    p_variables = [
        [P1_hole1, P1_hole2, P1_hole4, P1_width],
        [P2_hole1, P2_hole2, P2_hole4, P2_width],
        [P3_hole1, P3_hole2, P3_hole4, P3_width],
        [P4_hole1, P4_hole2, P4_hole4, P4_width],
        [P5_hole1, P5_hole2, P5_hole4, P5_width],
        [P6_hole1, P6_hole2, P6_hole4, P6_width],
        [P7_hole1, P7_hole2, P7_hole4, P7_width],
        [P8_hole1, P8_hole2, P8_hole4, P8_width],
        [P9_hole1, P9_hole2, P9_hole4, P9_width],
        [P10_hole1, P10_hole2, P10_hole4, P10_width],
        [P11_hole1, P11_hole2, P11_hole4, P11_width]
    ]

    # 각 그룹에 대한 계산 실행
    for holes in p_variables:
        if holes[1] is None or holes[1] == 0:
            # 계산 수행 후 새로운 값을 할당
            holes[1] = holes[3] - (holes[0] + holes[2])

    # 필요한 경우, 결과를 다시 튜플로 변환
    P1_hole2, P2_hole2, P3_hole2, P4_hole2, P5_hole2, P6_hole2, P7_hole2, P8_hole2, P9_hole2, P10_hole2, P11_hole2 = [holes[1] for holes in p_variables]

    # 변수 목록 초기화
    hole_variables = [P2_hole1, P2_hole2, P2_hole3, P2_hole4, 
                    P3_hole1, P3_hole2, P3_hole3, P3_hole4, 
                    P4_hole1, P4_hole2, P4_hole3, P4_hole4]
    
    # print (f"p_variables : {p_variables}")
    # print (f"side holes : {hole_variables}")

    limit_point = [P2_width, P2_width + P3_width, P2_width + P3_width + P4_width]
    # leftholes 리스트 초기화
    leftholes = []
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 leftholes에 추가
    for hole in hole_variables:
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                leftholes.append(hole)
                draw_circle(doc, abs_x - P1_holegap, abs_y + sum, 8, layer='0')
                # print(f"side sum: {sum}")

    # 오른쪽 벽 판넬 변수 목록 초기화
    hole_variables = [P8_hole1, P8_hole2, P8_hole3, P8_hole4, 
                    P9_hole1, P9_hole2, P9_hole3, P9_hole4, 
                    P10_hole1, P10_hole2, P10_hole3, P10_hole4]    

    limit_point = [P10_width, P10_width + P9_width, P10_width + P9_width + P8_width]
    rx = abs_x + P5_width + P6_width + P7_width - panel_width * 2 + P9_holegap
    # rightholes 리스트 초기화
    rightholes = []
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(hole_variables): 
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                rightholes.append(hole)
                draw_circle(doc, rx , abs_y + sum, 8, layer='0')        
                if index == 0 :
                    d(doc, rx + panel_width - P9_holegap , abs_y , rx  , abs_y + sum , 151, direction="right" ,option='reverse' )    
                else:
                    dc(doc,rx  , abs_y + sum)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, rx + panel_width - P9_holegap, abs_y + sum)      

    #############################################################
    # 우측 치수선
    #############################################################
    # 우측 2단 치수선
    ry = abs_y
    rx = abs_x + P5_width + P6_width + P7_width - panel_width    
    d(doc, rx, ry , rx , ry + P10_width, 264, direction="right")
    dc(doc, rx , ry + P10_width  + P9_width )    
    dc(doc, rx , ry + P10_width  + P9_width + P8_width )    

    # 우측 3단 치수선
    tstr = f"{P8_width+P9_width+P10_width}[INSIDE]"
    d(doc, rx, ry , rx , ry + P10_width + P9_width + P8_width, 374, direction="right", text=tstr)

    # 후면 벽 판넬 변수 목록 초기화
    # 후면 벽 치수선표기
    hole_variables = [P5_hole1, P5_hole2, P5_hole3, P5_hole4, 
                    P6_hole1, P6_hole2, P6_hole3, P6_hole4, 
                    P7_hole1, P7_hole2, P7_hole3, P7_hole4]
    
    limit_point = [P5_width, P5_width + P6_width, P5_width + P6_width + P7_width]
    rx = abs_x - panel_width
    ry = abs_y + P2_width + P3_width + P4_width

    rearholes = []
    sum = 0

    # 뒷벽 
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(hole_variables):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                rearholes.append(hole)
                draw_circle(doc, rx + sum , ry + P6_holegap , 8, layer='0')
                # print(f"side sum: {sum}")
                if index == 0 :
                    d(doc, rx, ry + panel_width, rx + sum, ry + P6_holegap, 76, direction="up" , option='reverse')    
                else:
                    dc(doc, rx + sum, ry + P6_holegap)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, rx + sum, ry + panel_width)                   

    # 상부 2단 치수선
    d(doc, rx, ry + panel_width, rx + P5_width, ry + panel_width, 160, direction="up")                      
    dc(doc,  rx + P5_width + P6_width, ry + panel_width )                   
    dc(doc,  rx + P5_width + P6_width + P7_width, ry + panel_width )                   
    # 상부 3단 치수선
    d(doc, rx, ry + panel_width, rx + P5_width + P6_width + P7_width, ry + panel_width, 246, direction="up")

    # 전면 벽 판넬 변수 목록 초기화
    hole_variables = [P1_hole1, P1_hole2, P1_hole3, P1_hole4, OP+column_thickness*2 , P11_hole1, P11_hole2, P11_hole3, P11_hole4]
    frontholes = []    
    
    limit_point = [P1_width, P1_width + OP + column_thickness*2 , P1_width + OP + P11_width + column_thickness*2]
    rx = abs_x - panel_width
    ry = abs_y 
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(hole_variables):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                draw_circle(doc, rx + sum , ry - P1_holegap , 8, layer='0')
                
    # P1 치수선                
    hole_variables = [P1_hole1, P1_hole2, P1_hole3, P1_hole4]       
    rx = abs_x - panel_width
    ry = abs_y 
    sum = 0    
    for index, hole in enumerate(hole_variables):  
        if hole is not None and hole > 0:
            sum += hole
            if index == 0 :
                d(doc,  rx , ry - panel_width, rx + sum, ry - P1_holegap, 164, direction="down" , option='reverse')    
            else:
                dc(doc, rx + sum, ry - P1_holegap)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, rx + sum, ry - P1_holegap)              
   
    # P11 치수선
    hole_variables = [P11_hole1, P11_hole2, P11_hole3, P11_hole4] 
    rx = abs_x + P1_width - panel_width + OP + column_thickness*2
    ry = abs_y 
    sum = 0    
    for index, hole in enumerate(hole_variables):  
        if hole is not None and hole > 0:
            sum += hole
            if index == 0 :
                d(doc,  rx , ry - panel_width, rx + sum, ry - P11_holegap, 164, direction="down" , option='reverse')    
            else:
                dc(doc, rx + sum, ry - P11_holegap)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, rx + sum, ry - P11_holegap)        

    rx = abs_x - panel_width          

    # 컬럼보다 분리형은 5mm 작게 한다.
    tr_column_width = column_width - 5        

    # 하단 2단 치수선 (OP표현 치수선라인)
    d(doc, rx, ry - panel_width , rx + P1_width + column_thickness, ry - tr_column_width, 215, direction="down")                      
    dc(doc,  rx + P1_width + column_thickness + OP, ry - tr_column_width, text=f"{OP}[OP]") 
    dc(doc,  rx + P1_width + column_thickness*2 + OP + P11_width  , ry - panel_width)

    # 컬럼 column_thickness 치수선    
    d(doc, rx + P1_width ,  ry - tr_column_width , rx + P1_width + column_thickness, ry - tr_column_width , 170, direction="down")                      
    d(doc, rx + P1_width + column_thickness + OP,  ry - tr_column_width , rx + P1_width + column_thickness*2 + OP, ry - tr_column_width , 170, direction="down")                      

    # 하단 3단 치수선 25 panel_width 표현
    d(doc, rx, ry - panel_width , rx + panel_width, ry , 350, direction="down", option='reverse')                      
    dc(doc, rx + column_thickness*2 + P1_width + OP + P11_width - panel_width, ry , text=f"{P1_width+OP+P11_width - panel_width*2}[INSIDE]") 
    dc(doc,  rx + P1_width+OP+P11_width + column_thickness * 2 , ry - panel_width)
                
    # 컬럼하부에 브라켓 위치지정  (사각 빠찌형태)
    transom_upperwing = 30   
    rx = abs_x + P1_width + column_thickness - panel_width - column_BottomHoleHorizontal
    ry = abs_y - column_BottomHoleVertical
    d(doc, abs_x + P1_width-panel_width + column_thickness, abs_y, rx, ry, 150, direction="up")
    d(doc, abs_x + P1_width-panel_width + column_thickness, abs_y, rx, ry, 200, direction="right")    
    insert_block(rx , ry , "assy_bottombase_left")             
    # 오른쪽 형상
    rx = abs_x + P1_width + column_thickness - panel_width  + OP + column_BottomHoleHorizontal                       
    insert_block(rx , ry , "assy_bottombase_right")      

    # 출입구 OP 형상 그리기
    rx = abs_x + P1_width - panel_width + column_thickness
    # 컬럼보다 분리형은 5mm 작게 한다.
    tr_column_width = column_width - 5
    ry = abs_y - tr_column_width
    rectangle(doc, rx,ry,rx + OP, ry + tr_column_width, layer='2')
    # 좌우 보강 표현  (좌)  
    rectangle(doc, rx,ry,rx+40.5, ry+ 36.5, layer='2')    
    # 좌우 보강 표현  (우)  
    rectangle(doc, rx+OP-40.5,ry,rx+OP, ry+ 36.5, layer='2')    
    # 상부 날개 표현
    ry = abs_y - transom_upperwing
    rectangle(doc, rx,ry,rx+OP, ry, layer='2')
    # M볼트 표현하기     
    # Ensure that hole variables are initialized to 0 if they are None
    hole_variables = [TR_upperhole1, TR_upperhole2, TR_upperhole3, TR_upperhole4]
    hole_variables = [0 if hole is None else hole for hole in hole_variables]

    # Now you can safely calculate the limit_point
    limit_point = [TR_upperhole1 + TR_upperhole2 + TR_upperhole3 + TR_upperhole4]
    ry = abs_y - transom_upperwing / 2
    transom_upperholes = []    
    total_holes_sum = 0  
    lastpos = 0  
    # print(f"hole_variables : {hole_variables}")

    for index, hole in enumerate(hole_variables):  
        if hole > 0:
            total_holes_sum += hole
            if total_holes_sum not in limit_point:
                transom_upperholes.append(hole)
                m14(doc, rx + total_holes_sum, ry)
                if index > 0 :
                    if index == 1 :
                        d(doc,  rx + lastpos, ry , rx + total_holes_sum, ry , 78, direction="up" )
                    else:
                        dc(doc, rx + total_holes_sum, ry - P11_holegap)                               
                lastpos = total_holes_sum

    # P1번 COP 적용시 그려주기
    rx = abs_x - panel_width                    
    if P1_COPType == 'COP 적용':
        COP_assy_height = 47.5
        xrectangle(doc, rx + P1_width/2 - COP_width/2, abs_y - COP_assy_height, rx + P1_width/2 - COP_width/2 + COP_width,abs_y , layer='0' )
                

    panel_wing = 11
    column_startx = abs_x - panel_width + P1_width 
    # P1옆 컬럼    
    line(doc, column_startx , abs_y - column_thickness , column_startx  , abs_y + 5 , layer='문자') # 노란색
    lt(doc,  column_thickness , 0  , layer='문자')
    lt(doc,  0 , - column_width , layer='문자')
    lt(doc,   - column_thickness  , 0 , layer='문자')    
    lt(doc,   0  ,panel_wing  , layer='문자')    
    # P1 분리형은 컬럼만큼 빠짐 
    line(doc, abs_x - panel_width + panel_wing , abs_y - panel_width , abs_x - panel_width  , abs_y - panel_width , layer='0')
    lt(doc,  0  , panel_width , layer='0')
    lt(doc,  P1_width , 0  , layer='0')
    lt(doc,  0 , - panel_width , layer='0')
    lt(doc,   - panel_wing  , 0 , layer='0')
    # P2    
    line(doc, abs_x - panel_width , abs_y  + panel_wing  , abs_x - panel_width  , abs_y  , layer='0')
    lt(doc,  panel_width ,  0 , layer='0')
    lt(doc,  0 , P2_width , layer='0')
    lt(doc,  - panel_width ,  0  , layer='0')
    lt(doc,  0 ,  - panel_wing , layer='0')
    # P3
    rx = abs_x
    ry = abs_y + P2_width
    line(doc, rx - panel_width , ry  + panel_wing  , rx - panel_width  , ry  , layer='0')
    lt(doc,  panel_width ,  0 , layer='0')
    lt(doc,  0 , P3_width , layer='0')
    lt(doc,  - panel_width ,  0  , layer='0')
    lt(doc,  0 ,  - panel_wing , layer='0')
    # P4
    rx = abs_x
    ry = abs_y + P2_width  + P3_width 
    line(doc, rx - panel_width , ry  + panel_wing  , rx - panel_width  , ry  , layer='0')
    lt(doc,  panel_width ,  0 , layer='0')
    lt(doc,  0 , P4_width , layer='0')
    lt(doc,  - panel_width ,  0  , layer='0')
    lt(doc,  0 ,  - panel_wing , layer='0')
    # P5
    rx = abs_x 
    ry = abs_y + P2_width + P3_width + P4_width 
    line(doc, rx - panel_width + panel_wing , ry  + panel_width  , rx - panel_width , ry  + panel_width  , layer='0')
    lt(doc,  0 , - panel_width  , layer='0')
    lt(doc,  P5_width , 0  , layer='0')
    lt(doc,  0 ,  panel_width , layer='0')
    lt(doc,   - panel_wing , 0 , layer='0')    
    # P6
    rx = abs_x + P5_width 
    ry = abs_y + P2_width + P3_width + P4_width
    line(doc, rx - panel_width + panel_wing , ry  + panel_width, rx - panel_width , ry  + panel_width  , layer='0')
    lt(doc,  0 , - panel_width , layer='0')
    lt(doc,  P6_width , 0 , layer='0')
    lt(doc,  0 , panel_width , layer='0')
    lt(doc,  - panel_wing , 0, layer='0')          
    # P7
    rx = abs_x + P5_width + P6_width 
    ry = abs_y + P2_width + P3_width + P4_width
    line(doc, rx - panel_width + panel_wing , ry + panel_width, rx - panel_width , ry  + panel_width  , layer='0')
    lt(doc,  0 , - panel_width , layer='0')
    lt(doc,  P7_width , 0 , layer='0')
    lt(doc,  0 , panel_width , layer='0')
    lt(doc,  - panel_wing , 0, layer='0')                  
    # P8 우측벽시작
    rx = abs_x + P5_width + P6_width + P7_width - panel_width
    ry = abs_y + P10_width + P9_width + P8_width
    line(doc, rx   , ry  - panel_wing  , rx   , ry  , layer='0')
    lt(doc,  - panel_width , 0, layer='0')
    lt(doc,  0, - P8_width  , layer='0')
    lt(doc,  panel_width, 0 , layer='0')
    lt(doc,  0,  panel_wing , layer='0')          
    # P9 우측벽
    rx = abs_x + P5_width + P6_width + P7_width - panel_width
    ry = abs_y + P10_width + P9_width 
    line(doc, rx   , ry  - panel_wing  , rx   , ry  , layer='0')
    lt(doc,  - panel_width , 0, layer='0')
    lt(doc,  0, - P9_width  , layer='0')
    lt(doc,  panel_width, 0 , layer='0')
    lt(doc,  0,  panel_wing , layer='0')      
    # P10 우측벽
    rx = abs_x + P5_width + P6_width + P7_width - panel_width
    ry = abs_y + P10_width 
    line(doc, rx   , ry  - panel_wing  , rx   , ry  , layer='0')
    lt(doc,  - panel_width , 0, layer='0')
    lt(doc,  0, - P10_width  , layer='0')
    lt(doc,  panel_width, 0 , layer='0')
    lt(doc,  0,  panel_wing , layer='0')          
    # P11 전면
    rx = abs_x + P5_width + P6_width + P7_width - panel_width
    ry = abs_y 
    line(doc, rx - panel_wing  , ry  - panel_width , rx  , ry - panel_width , layer='0')
    lt(doc,  0 ,  panel_width , layer='0')
    lt(doc,  - P11_width , 0 , layer='0')
    lt(doc,  0 , - panel_width , layer='0')
    lt(doc,  panel_wing , 0 , layer='0')

    column_startx = rx - P11_width 
    # P1옆 컬럼      (노란색)
    line(doc, column_startx , abs_y - column_thickness , column_startx  , abs_y + 5 , layer='문자') # 노란색
    lt(doc,  - column_thickness , 0  , layer='문자')
    lt(doc,  0 , - column_width , layer='문자')
    lt(doc,   column_thickness  , 0 , layer='문자')    
    lt(doc,   0  ,panel_wing  , layer='문자')  

    rx = abs_x 
    rxnext = abs_x + P5_width + P6_width + P7_width  - panel_width*2
    ry = abs_y
    gap = 0
    # 리스트의 총 길이를 구함
    total_length = len(HRsidegap)    
    for index, g in enumerate(HRsidegap):
        gap += g
        if g is not None and index < total_length - 1:  # 마지막 요소를 제외하고 실행
            line(doc, rx - 20, ry + gap, rx + 20, ry + gap, layer='3')
            line(doc, rxnext - 20, ry + gap, rxnext + 20, ry + gap, layer='3')
            if index == 0 :
                d(doc, rx-panel_width, ry, rx, ry+gap, 90, direction="left" )                            
            else:
                dc(doc, rx, ry+gap)        
    dc(doc, rx-panel_width, ry+gap)                      

    rx = abs_x - panel_width    
    ry = abs_y + P2_width + P3_width + P4_width 
    gap = 0    
    # 리스트의 총 길이를 구함
    total_length = len(HRreargap)

    for index, g in enumerate(HRreargap):
        gap += g
        if g is not None and index < total_length - 1:  # 마지막 요소를 제외하고 실행
            line(doc, rx + gap, ry - 20, rx + gap, ry + 20, layer='3')
        if index == 0 :
            d(doc, rx, ry, rx + gap, ry-20, 110, direction="down" )    
        else:
            dc(doc, rx + gap, ry-20)    

    # P1~P11 화면에 부호 출력하기
    numprint(doc,abs_x+P1_width/2 ,abs_y + 60 , 'P01', layer='문자')
    numprint(doc,abs_x+P1_width+OP+P11_width/2 ,abs_y + 60 , 'P11', layer='문자')
    numprint(doc,abs_x+100 ,abs_y + P2_width/2 , 'P02', layer='문자')
    numprint(doc,abs_x+100 ,abs_y + P2_width + P3_width/2 , 'P03', layer='문자')
    numprint(doc,abs_x+100 ,abs_y + P2_width + P3_width + P4_width/2 , 'P04', layer='문자')
    numprint(doc,abs_x + P5_width /2 + 50 ,abs_y + P2_width + P3_width + P4_width - 50 , 'P05', layer='문자')
    numprint(doc,abs_x + P5_width  + P6_width/2+ 50 ,abs_y + P2_width + P3_width + P4_width - 50 , 'P06', layer='문자')
    numprint(doc,abs_x + P5_width  + P6_width + P7_width/2 + 50 ,abs_y + P2_width + P3_width + P4_width - 50 , 'P07', layer='문자')
    numprint(doc,abs_x + P5_width  + P6_width + P7_width - 130 ,abs_y + P2_width + P3_width + P4_width/2 , 'P08', layer='문자')
    numprint(doc,abs_x + P5_width  + P6_width + P7_width - 130 ,abs_y + P2_width + P3_width/2 , 'P09', layer='문자')
    numprint(doc,abs_x + P5_width  + P6_width + P7_width - 130 ,abs_y + P2_width/2, 'P10', layer='문자')

    #############################################################
    # Assy 단면도 그리기 1page
    #############################################################
    rx = abs_x - 930
    ry = abs_y - 170
    insert_block(rx,ry,"panel_section")
    # FH 바닥마감
    d(doc, rx+231.3 , ry- 236.2 , rx + 231.3 , ry - 277.5, 70, direction="right", text=f"바닥두께:{FH}" )
    # KH, KPH
    d(doc, rx+231.3 , ry- 277.5 , rx + 102.8 , ry - 30.9, 200, direction="right" , text=f"{KPH}" )
    d(doc, rx + 102.8 , ry - 30.9, rx + 127.7 , ry , 200, direction="right" , text=f"5" )
    dc(doc,rx + 127.7 , ry + 1920 , text=f"WH={CPH}" )
    dc(doc,rx + 238.8 , ry + 1957.8 , text=f"5" )
    d(doc, rx+231.3 , ry- 236.2 , rx + 238.8 , ry + 1957.8 , 250, direction="right", text=f"{CH}[CH]" )
    d(doc, rx + 238.8 - 60.9 - 111.1 , ry+1787.8 + 132.2 + 30.9 , rx + 238.8  - 111.1, ry+1787.8 + 132.2, 150, direction="up" , text=f"{P1_holegap}" )

    # ASY 코멘트 달기
    text = f"발주처 : {company}"
    rx = abs_x + (P1_width+OP) / 3
    ry = abs_y + (P2_width+P3_width)
    draw_Text(doc, rx, ry, 40, text, layer='0')
    text = f"인승 : {person} , {usage} , 헤더 : {doorDevice}"    
    ry -= 80
    draw_Text(doc, rx, ry, 40, text, layer='0')
    text = f"CW : {CW} , CD : {CD}"    
    ry -= 80
    draw_Text(doc, rx, ry, 40, text, layer='0')
    text = f"Handrail 높이 : {handrail_height}"    
    ry -= 80
    draw_Text(doc, rx, ry, 40, text, layer='0')
    text = f"COP 가로:{COP_width}x가로:{COP_height}x높이:{COP_bottomHeight}"    
    ry -= 80
    draw_Text(doc, rx, ry, 40, text, layer='0')
    text = f"HOP 가로:{HOP_width}x가로:{HOP_height}x높이:{HOP_bottomHeight}"    
    ry -= 80
    draw_Text(doc, rx, ry, 40, text, layer='0')

    #############################################################
    # Assy 분리형 오른쪽에 표시한 단면도 그리기 1page 2번판넬 자료 응용
    #############################################################    
        #######################################  
        # P2,P8 단면도 (상부에 위치한 자료 응용) 홀은 가상으로 표현함... M6
        #######################################  

    pagex ,  pagey = abs_x + CW + 1300 , abs_y + 300
    # 임시로 폭을 지정함 형상만 보여주기 위함
    assy_width = 325

    x1 = pagex - panel_width + 6
    y1 = pagey 
    x2 = x1 - panel_wing
    y2 = y1 
    x3 = x2
    y3 = y2 - panel_width
    x4 = x3 + assy_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - panel_width + thickness*2
    x10 = x9 - assy_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_width - thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3
    y13 = y3 + P2_holegap
    x14 = x4
    y14 = y4 +P2_holegap
    
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 150, direction='up')   
    d(doc, x6, y6, x5, y5, 150, direction='up')   

    x13, y13 =  x1-10, y3 + P2_holegap
    line(doc, x3-10, y3+P2_holegap, x3+ 10, y3+P2_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y3+P2_holegap, x4+ 10, y3+P2_holegap , layer='CLphantom') # '구성선' 회색선
    # 좌측    
    d(doc, x13-10, y13, x3, y3, 100, direction='left')      
    d(doc, x2, y2, x3, y3, 180, direction='left')  

    d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
    rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
    # 하단 날개 23 표기 width 25 -2
    d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')   

    sample_hole = [P2_hole1, 325 - P2_hole1, 0, 0]      # 325 샘플에 맞춘 홀
    limit_point = [assy_width]
    tx = x3 
    ty = y3 + P2_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(sample_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                insert_block(tx + sum, ty,"M6")                
             

    #######################################  
    # 분리형 ASSY 단면도 (우측) - 응용  
    #######################################  
    top_panel_width = panel_width - 2
    x1 = pagex + assy_width*2 - 1100
    y1 = pagey + CPH/2 - 450
    x2 = x1 
    y2 = y1 + panel_wing
    x3 = x2 - top_panel_width
    y3 = y2 
    x4 = x3 
    y4 = y3 - CPH/2
    x5 = x4 + top_panel_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_wing
    x7 = x6 - thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - panel_wing + thickness
    x9 = x8 - top_panel_width + thickness*2
    y9 = y8 
    x10 = x9 
    y10 = y9 + CPH/2 - thickness*2
    x11 = x10 + top_panel_width - thickness*2
    y11 = y10 
    x12 = x11 
    y12 = y11 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3 + P2_holegap
    y13 = y3
    x14 = x4 + P2_holegap
    y14 = y4
    
    line(doc, x13, y13+10, x13, y13-10, layer="CL")
    line(doc, x14, y14+10, x14, y14-10, layer="CL")
    d(doc, x1, y1, x2, y2, 150, direction='right')
    d(doc, x3, y3, x13, y13+10, 80, direction='up')
    d(doc, x3, y3, x2, y2, 180, direction='up')
    d(doc, x14, y14-10, x4, y4, 100, direction='down')
    d(doc, x4, y4, x5, y5, 180, direction='down')

    # 줄임을 나타내는 사선 2개 평행선 긋기
    line(doc, x3 -80 , y3 - CPH/4 + 20, x3 +80 , y3 - CPH/4 + 60, layer="0")
    line(doc, x3 -80 , y3 - CPH/4 - 20, x3 +80 , y3 - CPH/4 + 20, layer="0")

    text = f"{CPH}"
    d(doc, x3, y3, x4, y4, 100, text = CPH , direction='left')

    d(doc, x6, y6, x5, y5, 150, direction='right')

    TargetYscale = TargetYscale*frame_scale

    frameXpos = abs_x + TargetXscale * frame_scale + 1100    



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

    #########################################################################################
    # 2page P1, P11 분리형 (일체형의 P1,P8 도면 응용)
    #########################################################################################
      
    if P1_COPType == 'COP 적용' :
        #########################################################################################
        # 7page P1, P11 COP 적용        
        #########################################################################################
        # 도면틀 넣기    
        BasicXscale = 6851
        BasicYscale = 4870
        TargetXscale = 6851 
        TargetYscale = 4870 + (CH-2500) 
        if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
            frame_scale = TargetXscale/BasicXscale
        else:
            frame_scale = TargetYscale/BasicYscale    

        # print("2page 스케일 비율 : " + str(frame_scale))           
        insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "FRONT PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

        pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

        ###################################################
        # P1 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
        ###################################################
        rx = math.floor(pagex) - 400
        ry = math.floor(pagey)

        x1 = rx + panel_wing
        y1 = ry + CH + 500
        x2 = x1 - panel_wing 
        y2 = y1    
        x3 = x2 
        y3 = y2 + panel_width
        x4 = x3 + P1_width
        y4 = y3 
        x5 = x4 
        y5 = y4 - panel_width
        x6 = x5 - panel_wing
        y6 = y5 
        x7 = x6 
        y7 = y6 + thickness
        x8 = x7 + panel_wing - thickness
        y8 = y7 
        x9 = x8 
        y9 = y8  + panel_width - thickness*2
        x10 = x9 - P1_width + thickness*2
        y10 = y9 
        x11 = x10 
        y11 = y10 - panel_width + thickness*2
        x12 = x11 + panel_wing - thickness
        y12 = y11 

        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 12
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="0")   
        
        x13, y13 = x3 + panel_width-P1_holegap , y3+10 # 연결홀 표현하는 적색선
        x14, y14 = x4 + 10 , y4 - P1_holegap # 연결홀 표현하는 적색선
        line(doc, x3 + panel_width-P1_holegap , y3 + 10, x3 + panel_width-P1_holegap, y3 - 10, layer='CLphantom') # '구성선' 회색선 방향이 P2와 결합되게
        line(doc, x4-10, y4-P1_holegap, x4+ 10, y4-P1_holegap , layer='CLphantom') # '구성선' 회색선        
        rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')
        
        P1_hole = [P1_hole1, P1_hole2, P1_hole3, P1_hole4]   
        
        limit_point = [P1_width]
        tx = x3 
        ty = y3 - P1_holegap
        sum = 0        
        for index, hole in enumerate(P1_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                    
                    insert_block(tx + sum, ty,"M6")
                if index == 0 :
                    d(doc,  x3 , y3, tx + sum, ty, 163, direction="up" , option='reverse')                    
                else:
                    dc(doc, tx + sum, ty)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, tx + sum, ty)                   
        
        d(doc,  x3 , y3, x4, y4, 273, direction="up")
        d(doc,  x13 , y13, x3, y3, 50, direction="up")
        d(doc,  x4 , y4, x14, y14, 190, direction="right")
        d(doc,  x5 , y5, x4, y4, 290, direction="right")

        d(doc,  x6, y6, x5 , y5,  80, direction="down")    
        d(doc,  x1 , y1, x2, y2, 80, direction="down")     

        # 모자보강 Y위치 저장 y3
        rib_posy = y3

        #############################################################
        # P1 분리형태 조립도 본체 만들기 (보강, 홀위치)
        # P1 조립도 본체구성 표현
        #############################################################            
        ry = pagey 

        rectangle(doc, rx, ry , rx+ P1_width, ry+CPH, layer='0')
        rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
        rectangle(doc, rx + P1_width , ry , rx+P1_width-panel_wing , ry+CPH , layer='0')

        # 세로 날개 표시 panel_wing
        line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
        line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
        line(doc, rx + P1_width - panel_wing, ry  ,rx + P1_width - panel_wing , ry + CPH, layer='0')
        line(doc, rx + P1_width - thickness, ry  ,rx + P1_width - thickness , ry + CPH, layer='22')

        # 상부 날개 표시
        rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P1_width -  panel_wing - 4 ,ry+CPH , layer='0')
        line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P1_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
        # 하부 날개 표시
        rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P1_width -  panel_wing - 4 ,ry,  layer='0')
        line(doc, rx + panel_wing + 4, ry+thickness , rx + P1_width -  panel_wing - 4 ,ry+thickness,  layer='22')

        x1 = rx 
        y1 = ry 
        x2 = x1 + P1_width
        y2 = y1    
        x3 = x2 
        y3 = y2 + CPH
        x4 = x3 - P1_width
        y4 = y3 

        # 팝너트 표시하기    
        P1_hole = [P1_hole1, P1_hole2, P1_hole3, P1_hole4]   

        # print (f"hole val : {hole_variables}")
        limit_point = [P1_width]
        tx = rx
        ty = ry+CPH    
        sum = 0
        # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
        for index, hole in enumerate(P1_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:
                    frontholes.append(hole)
                    insert_block(tx + sum, ty,"M6_popnut")
                    insert_block(tx + sum, ry,"M6_popnut_upset")
                if index == 0 :
                    d(doc,  x4 , y4, tx + sum, ty, 163, direction="up" , option='reverse')                    
                else:
                    dc(doc, tx + sum, ty)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, tx + sum, ty)         

        # 상부 전체치수
        d(doc,  rx , ry+CPH, rx + P1_width , ry+CPH, 250, direction="up")

        yp_bottom = ry  + 1
        yp_upper = ry + CPH - 1

        P1_handrailxpos=[COP_centerdistance]
        rb_list = panel_rib_COP(P1_width, P1_handrailxpos, COP_width, option='reverse')

        # print(f"P1 새로운 함수 적용 COP 종보강 위치: {rb_list}")                
        # 리스트를 역순으로 조립도는 역순이다. 
        rb_list_reversed = rb_list[::-1]
        #  rb_list_reversed = rb_list
        # print(f"P1 새로운 함수 적용 COP 종보강 위치 rb_list_reversed: {rb_list_reversed}")                
        # print(f"P1 rb_list_reversed 새로운 함수 적용 COP 종보강 위치: {rb_list_reversed}")        
        for index, g in enumerate(rb_list_reversed):        
            bp = rx +  g
            if index == 0 :
                xlist = [bp , bp-10 ,bp+10 ,bp - 8 ,bp - 10, bp+15, bp+10 ]       
                # 25 COP보강 5,10,8,2 = 25 좌우 개념이 있음
                rectangle(doc, xlist[1] , yp_bottom, xlist[2] , yp_upper, layer='0')
                rectangle(doc, xlist[5] , yp_bottom+panel_wing+1, xlist[6] , yp_upper-panel_wing-1, layer='0')
                line(doc, xlist[3] , yp_bottom, xlist[3] , yp_upper, layer='2')                
                line(doc, bp , yp_bottom, bp , yp_upper, layer='CLphantom')                  
                d(doc, x3, y3,  bp , y4, 150, direction="down")     
            elif index == 1 :
                # 우측기준으로 계산하기
                rx_reverse = rx + P1_width - COP_centerdistance
                xlist = [bp , bp+10 ,bp-10 ,bp - 8 ,bp - 10, bp+15, bp+10 ]       
                # 25 COP보강 5,10,8,2 = 25 좌우 개념이 있음
                # COP 상단
                COP_box_upperY = ry + COP_bottomHeight + COP_height + 1
                COP_box_lowerY = ry + COP_bottomHeight - 1

                # COP 상하 고정 Bracket
                # 하부
                bp1 = rx+P1_width-COP_centerdistance-COP_width/2-1  # basic point
                bp2 = rx+P1_width-COP_centerdistance+COP_width/2+1  # basic point  
                yp_bottom_bottom = ry + COP_bottomHeight - 30 -1
                yp_bottom_upper = ry +  COP_bottomHeight - 1
                rectangle(doc, bp1, yp_bottom_bottom,bp2, yp_bottom_upper, layer='0')
                rectangle(doc, bp1, yp_bottom_upper,bp2, yp_bottom_upper-1.6, layer='0')
                # COP 상하 고정 Bracket
                # 상부
                yp_top_bottom = ry + COP_bottomHeight + COP_height + 1
                yp_top_upper = ry +  COP_bottomHeight + COP_height + 30 + 1
                rectangle(doc, bp1, yp_top_bottom,bp2, yp_top_upper, layer='0')
                rectangle(doc, bp1, yp_top_bottom,bp2, yp_top_bottom+1.6, layer='0')    
                distancex = bp
                distancey = y3
                dc(doc, bp,y3)                            
            else:
                xlist = [bp , bp+10 ,bp-10 ,bp+8 ,bp+10, bp-15, bp-10 ]       
                # 25 COP보강 5,10,8,2 = 25 좌우 개념이 있음
                rectangle(doc, xlist[1] , yp_bottom, xlist[2] , yp_upper, layer='0')
                rectangle(doc, xlist[5] , yp_bottom+panel_wing+1, xlist[6] , yp_upper-panel_wing-1, layer='0')
                line(doc, xlist[3] , yp_bottom, xlist[3] , yp_upper, layer='2')                
                line(doc, bp , yp_bottom, bp , yp_upper, layer='CLphantom')                  
                dc(doc, bp,y3)

            # 단면도에 모자보강 위치 표시하기 ( COP 타공자리 중심점)
            line(doc, bp , rib_posy + 10 , bp , rib_posy - panel_width - 10 , layer='0')  
                
            # 5x10 장공 용접홀          
            insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
            insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")                         

        if len(rb_list)-1 > 0 :  # 마지막인 경우
            dc(doc, x4,y4)          

        # COP_ditance 치수
        d(doc, distancex, distancey,  x3 , y3, 70, direction="up")  

        # 단면도에  ( COP 타공자리 중심점)
        line(doc, distancex, rib_posy - panel_width + 10 , distancex , rib_posy - panel_width - 10 , layer='CL')              
    
        #################################
        # COP 타공
        ##################################    
        tx1 = x1 + P1_width - COP_centerdistance - COP_width/2
        ty1 = y1 + COP_bottomHeight 
        tx2 = tx1 + COP_width
        ty2 = ty1
        tx3 = tx2
        ty3 = ty2 + COP_height
        tx4 = tx3 - COP_width
        ty4 = ty3
        rectangle(doc, tx1 , ty1, tx3, ty3, layer="0" )
        tx5=(tx1+tx2)/2
        ty5=ty1
        tx6=(tx3+tx4)/2
        ty6=ty3
        line(doc, tx5-COP_holegap/2, ty5-10,  tx5-COP_holegap/2 , ty5+10,  layer='CLphantom')    
        line(doc, tx5+COP_holegap/2, ty5-10,  tx5+COP_holegap/2 , ty5+10,  layer='CLphantom')    
        line(doc, tx5-COP_holegap/2, ty6-10,  tx5-COP_holegap/2 , ty6+10,  layer='CLphantom')    
        line(doc, tx5+COP_holegap/2, ty6-10,  tx5+COP_holegap/2 , ty6+10,  layer='CLphantom')    

        d(doc, tx5-COP_holegap/2, ty5-10, tx5+COP_holegap/2 , ty5+10, 70, direction='up')
        d(doc, tx4, ty4, tx3, ty3, 100, direction='up')
        d(doc, tx4, ty4, tx1, ty1, 60, direction='left')
        dc(doc, tx4, y1)       

        # 장공홀 표현하기 M6_nut
        gap = 0    
        length = CPH - 85 + popnut_height 
        hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
        leftx = x1 + 1.5
        rightx = x2 - 1.5
        ty = y2

        for index, g in enumerate(hole):
            gap += g
            if g is not None : 
                insert_block(leftx, ty + g, "M6_nut")
                insert_block(rightx, ty + g, "M6_nut")
            if index == 0 :
                d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    
                # 슬롯등 지시선 추가
                text = "8x16"
                dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="up")
            else:
                dc(doc, rightx, ty + g)    
        dc(doc, x3, y3)    

        # 우측 전체 치수선
        d(doc, x2, y2, x3, y3, 220, direction="right" )  

        ###########################################################################
        # P1 전개도 그리기
        ###########################################################################

        rx = pagex + P1_width + 350                         
        x1 = rx
        y1 = pagey
        x2 = x1 + P1_width - (panel_width+5)*2
        y2 = y1    
        x3 = x2
        y3 = y2 + panel_wing + 4 
        x4 = x3 + panel_wing + 4 
        y4 = y3 
        x5 = x4 
        y5 = y4 + 14.5 if br == 1.5 else y4 + 16
        x6 = x5 + 45 if br == 1.5 else x5 + 47
        y6 = y5 
        x7 = x6 
        y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
        x8 = x7 - 45 if br == 1.5 else x7 - 47 
        y8 = y7 
        x9 = x8 
        y9 = y8 + 14.5 if br == 1.5 else y8 + 16
        x10 = x9 - (panel_wing + 4)
        y10 = y9 
        x11 = x10 
        y11 = y10 + panel_wing + 4 
        x12 = x11 - P1_width + (panel_width+5)*2
        y12 = y11
        x13 = x12 
        y13 = y12 - (panel_wing + 4)
        x14 = x13 - (panel_wing + 4)
        y14 = y13
        x15 = x14 
        y15 = y14 - 14.5 if br == 1.5 else y14 - 16
        x16 = x15 - 45 if br == 1.5 else x15 - 47
        y16 = y15 
        x17 = x16 
        y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
        x18 = x17 + 45 if br == 1.5 else x17 + 47
        y18 = y17 
        x19 = x18
        y19 = y18 - (panel_wing + 4)
        x20 = x19 + (panel_wing + 4)
        y20 = y19 

        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 20
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                        
        gap = 0
        gap = - 1.5 if br == 1.5 else - 1
        length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
        hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
        leftx = x17 + (panel_width+panel_wing - P1_holegap - br * 2 )
        rightx = x6 - (panel_width+panel_wing + panel_width - P1_holegap - br * 4 )
        ty = y6

        for index, g in enumerate(hole):
            gap += g
            if g is not None : 
                insert_block(leftx, ty + g, "8x16_vertical")
                insert_block(rightx, ty + g, "8x16_vertical")
            if index == 0 :
                d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
                # 슬롯등 지시선 추가
                text = "8x16"
                dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="up")
            else:
                dc(doc, rightx, ty + g)    
        dc(doc, x11, y11)    
        # 장공치수선 그리기    좌,우 떨어짐
        for index, g in enumerate(hole):
            if index == 4 :
                d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
                d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )       


        #################################
        # 세화정공 헤더표시 (십자표시)
        #################################
        # 장공표시 #P01, P111은 일체형일 경우 만들어본다.
        hole = [90, 50, 90 , 50]
        limit = TRH
        xp = x7 - 11 - 11

        # 확인 요함 바닥에서 연신율부분 1.2, 1.5 차이점 확인요함
        holeypos = y6 + OPH - KH - popnut_height - 0.5 if br == 1.5 else y6 + OPH - KH - popnut_height - 1
        gap = 0    
        for index, g in enumerate(hole):
            gap += g
            if g is not None : 
                cross10(doc, xp, holeypos + gap)
                if index == 1 :
                    d(doc, xp, holeypos+ pre_gap, xp, holeypos + gap, 230, direction="right", option='reverse' )    
                elif index != 0 and index != len(hole)-1 :
                    dc(doc, xp, holeypos + gap)               
                else:
                    dc(doc, xp, holeypos + gap)                            
            pre_gap = gap 
                
        # 지시선 추가 4-M8육각
        text = "4-M8육각"
        dim_leader(doc,  xp, holeypos + gap , x10+200, y10 + 150,   text, direction="up")                    


        yp_bottom = y1
        yp_upper = y11

        rb_list = panel_rib_COP(P1_width, P1_handrailxpos, COP_width)
        # 역순리스틑 정렬
        # rb_list = rb_list[::-1]

        # print(f"전개도  적용 COP 종보강 위치: {rb_list}")             
        for index, g in enumerate(rb_list):         
            bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
            line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
            if index == 0 :
                text = "%%C3"
                dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="left")                    
                # 5mm 치수선표시
                d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
                d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

            circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
            circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

        for index, g in enumerate(rb_list):        
            bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
            if index == 0 :
                # 보강위치 가로 치수 
                d(doc, x16, y16, bp, y11, 300, direction="down")
            else:
                dc(doc, bp,y11)

        if len(rb_list) > 0 :  # 마지막인 경우
            dc(doc, x7,y7)     
                            
        # 9파이 팝너트 연결홀 상부/하부
        P1_hole = [P1_hole1, P1_hole2, P1_hole3, P1_hole4]   

        limit_point = [P1_width]
        tx = x16 + 30 if br == 1.5 else x16 + 32
        upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
        lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
        sum = 0
        # 각 변수에 대해 값이 0보다 크고 limit_point
        # 상부의 연결홀
        for index, hole in enumerate(P1_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                
                    circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                    circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                if index == 0 :
                    holeupperx = tx + sum                               
                    holeuppery = upper_ty                       
                    text = "%%C9 M6 POPNUT(머리5mm)"
                    dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="left")                
                    d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

                elif index == len(hole_variables) - 1 :
                    dc(doc, x7, y7)                   
                else:
                    dc(doc, tx + sum, upper_ty)                                   
        # 하부에 연결홀 타공
        sum = 0
        for index, hole in enumerate(P1_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                
                    circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                    circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
                if index == 0 :
                    holelowerx = tx + sum                               
                    holelowery = lower_ty                          
                    d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

                elif index == len(hole_variables) - 1 :
                    dc(doc, x6, y6)                   
                else:
                    dc(doc, tx + sum, lower_ty)        

        #################################
        # COP 타공 (전개도 laser layer)  COP_centerdistance 이 값으로 중앙위치 지정함
        ##################################    
        tx1 = x16  
        tx1 = x17 + panel_wing + panel_width + COP_centerdistance - COP_width/2  - 4 if br == 1 else x17 + panel_wing + panel_width + COP_centerdistance - COP_width/2  - 6
        ty1 = y6 + COP_bottomHeight if br == 1 else y6 + COP_bottomHeight - 1.5
        tx2 = tx1 + COP_width
        ty2 = ty1
        tx3 = tx2
        ty3 = ty2 + COP_height
        tx4 = tx3 - COP_width
        ty4 = ty3
        rectangle(doc, tx1 , ty1, tx3, ty3, layer="레이져" )
        tx5=(tx1+tx2)/2
        ty5=ty1
        tx6=(tx3+tx4)/2
        ty6=ty3        
        
        d(doc, tx4, ty4, tx3, ty3, 100, direction='up')
        d(doc, tx4, ty4, tx1, ty1, extract_abs(x16, tx1) + 120, direction='left')
        dc(doc, tx4, y1)       
                    
        # 상부치수선    
        d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
        dc(doc, x9 , y9)    
        dc(doc, x7, y7)
        # 상부 전체치수선
        d(doc, x16, y16, x7 ,y7, 250, direction="up")

        # 하부치수선    
        d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
        d(doc, x2, y2, x6 ,y6, 110, direction="down")        
        # 하부 2단 절곡 만나는 곳 치수선
        d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
        dc(doc, x4 , y4)    
        dc(doc, x6 , y6)
        # 하부 전체치수선
        d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
        
        # 오른쪽 15mm 표기
        d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
        # 오른쪽 최종 치수선
        d(doc, x11, y11 , x7, y7, 300, direction="right")
        dc(doc, x6, y6)
        dc(doc, x2, y2)    

        # 왼쪽 치수선 20mm 
        d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
        d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
        # 왼쪽 치수선 전체
        d(doc, x12, y12, x1, y1, 280, direction="left")
    

        #######################################  
        # P1 단면도 (상부 위치) P10과 연결홀 위치 주의
        #######################################  

        x1 = x1 - panel_width + 6
        y1 = pagey + CH + 800
        x2 = x1 - panel_wing
        y2 = y1 
        x3 = x2
        y3 = y2 - panel_width
        x4 = x3 + P1_width
        y4 = y3 
        x5 = x4 
        y5 = y4 + panel_width
        x6 = x5 - panel_wing
        y6 = y5 
        x7 = x6 
        y7 = y6 - thickness
        x8 = x7 + panel_wing - thickness
        y8 = y7 
        x9 = x8 
        y9 = y8 - panel_width + thickness*2
        x10 = x9 - P1_width + thickness*2
        y10 = y9 
        x11 = x10 
        y11 = y10 + panel_width - thickness*2
        x12 = x11 + panel_wing - thickness
        y12 = y11
        
        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 12
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="0")     

        x13 = x3
        y13 = y3 + P1_holegap
        x14 = x4 - panel_width + P1_holegap
        y14 = y4 
        
        line(doc, x13-10, y13, x13+10, y13, layer="CL") 
        line(doc, x14, y14 -10, x14, y14 +10, layer="CL") 

        # COP_centerdistance 표시
        line(doc, x3 + COP_centerdistance, y3 + 10, x3 + COP_centerdistance, y3 - 10, layer="0") 
        d(doc, x3, y3, x3 + COP_centerdistance, y3 - 10, 120, direction='down')  

        # 상부 치수선
        d(doc, x1, y1, x2, y2, 150, direction='up')   
        d(doc, x6, y6, x5, y5, 150, direction='up')   
        # 좌측    
        d(doc, x13-10, y13, x3, y3, 100, direction='left')      
        d(doc, x2, y2, x3, y3, 180, direction='left')  

        # 전체하부
        d(doc, x3, y3, x4, y4, 350, direction='down')   
        # P10과 연결홀 방향선           
        d(doc, x14, y14-10, x4, y4, 130, direction='down')    

        x13, y13 =  x1-10, y3 + P1_holegap        
        rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
        # 하단 날개 23 표기 width 25 -2
        d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
        d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')           

        P1_hole = [P1_hole4, P1_hole3, P1_hole2, P1_hole1]     
        limit_point = [P1_width]
        tx = x3
        ty = y3 + P1_holegap
        sum = 0
        # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
        for index, hole in enumerate(P1_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                
                    insert_block(tx + sum, ty,"M6")
                if index == 0 :
                    d(doc,  x3 , y3, tx + sum, ty, 250, direction="down" , option='reverse')                                    
                else:
                    dc(doc, tx + sum, ty)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, tx + sum, ty)        
   

    # 보강 3개 위치 표시
    # yp_bottom = y3 - 10
    # yp_upper = y3 + 10

    # rb_list = panel_rib_HOP(P1_width, P1_handrailxpos, COP_width, option='reverse')        
    # for index, g in enumerate(rb_list):         
    #     bp = x3 + g
        # line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        # if index == 0 :
        #     d(doc, x3,  y3 , bp , yp_bottom , 150, direction="down")               
        # else:
        #     dc(doc, bp , yp_bottom)

    # if len(rb_list) > 0 :  # 마지막인 경우
    #     dc(doc, x4,y4)                          

    #######################################  
    # P1 단면도 (우측)
    #######################################  
    top_panel_width = panel_width - 2
    x1 = pagex + P1_width*2 + 3500
    y1 = pagey + CH
    x2 = x1 
    y2 = y1 + panel_wing
    x3 = x2 - top_panel_width
    y3 = y2 
    x4 = x3 
    y4 = y3 - CPH
    x5 = x4 + top_panel_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_wing
    x7 = x6 - thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - panel_wing + thickness
    x9 = x8 - top_panel_width + thickness*2
    y9 = y8 
    x10 = x9 
    y10 = y9 + CPH - thickness*2
    x11 = x10 + top_panel_width - thickness*2
    y11 = y10 
    x12 = x11 
    y12 = y11 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3 + P1_holegap
    y13 = y3
    x14 = x4 + P1_holegap
    y14 = y4
    
    line(doc, x13, y13+10, x13, y13-10, layer="CL")
    line(doc, x14, y14+10, x14, y14-10, layer="CL")
    d(doc, x1, y1, x2, y2, 150, direction='right')
    d(doc, x3, y3, x13, y13+10, 80, direction='up')
    d(doc, x3, y3, x2, y2, 180, direction='up')
    d(doc, x14, y14-10, x4, y4, 100, direction='down')
    d(doc, x4, y4, x5, y5, 180, direction='down')

    d(doc, x3, y3, x4, y4, 100, direction='left')
    d(doc, x6, y6, x5, y5, 150, direction='right')

    ##################### 코멘트 ##########################
    mx = frameXpos + P1_width*2 + 4000
    my = frameYpos + 1500     
    page_comment(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + P1_width*2 + 5000
    my = frameYpos + 3500
    desx = mx - 1300
    desy = my + 1000
    unitsu = 0    
    text = 'FRONT PANEL(#1,#11)'
    unitsu= 2

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')   



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

    #########################################################################################
    # P11, P11 같으면 하나만 표시  (P5 응용해서 만듬)
    #########################################################################################
   
    ###################################################
    # P11 분리형 조립도 (도면의 상부 ) 평면도
    ###################################################
    rx = math.floor(pagex) + P1_width*3 + 1900
    ry = math.floor(pagey)

    x1 = rx + panel_wing
    y1 = ry + CH + 500
    x2 = x1 - panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 + P11_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 + thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  + panel_width - thickness*2
    x10 = x9 - P11_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 - panel_width + thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   
    
    x13, y13 =  x1-10, y3-P11_holegap    
    rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')
    line(doc, x3-10, y3-P11_holegap, x3+ 10, y3-P11_holegap , layer='CLphantom') # '구성선' 회색선    
    
    # 전면 벽 판넬 변수 목록 초기화
    P11_hole = [P11_hole1, P11_hole2, P11_hole3, P11_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P11_width]
    tx = x3 
    ty = y3 - P11_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P11_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 170, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)               

    d(doc,  x3 , y3, x4, y4, 250, direction="up")
    d(doc,  x13 , y13, x3, y3, 140, direction="left")
    d(doc,  x5 , y5, x4, y4, 190, direction="right")
    d(doc,  x6, y6, x5 , y5,  80, direction="down")    
    d(doc,  x1 , y1, x2, y2, 80, direction="down")     

    # P11, P11은 side panel과 결합하니, 홀의 결합위치가 다르다. 주의)
    line(doc, x4 - (panel_width-P11_holegap) , y4 + 10 , x4 - (panel_width-P11_holegap) , y4 - 10 , layer='CLphantom')  
    d(doc, x4 , y4 , x4 - (panel_width-P11_holegap) , y4 + 10 , 50, direction="up")
                      

    # 모자보강 Y위치 저장 y3
    rib_posy = y3

    #############################################################
    # P11 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
    # P11 조립도 본체구성 표현
    #############################################################
            
    ry = pagey 

    rectangle(doc, rx, ry , rx+ P11_width, ry+CPH, layer='0')
    rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
    rectangle(doc, rx + P11_width , ry , rx+P11_width-panel_wing , ry+CPH , layer='0')

    # 세로 날개 표시 panel_wing
    line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
    line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
    line(doc, rx + P11_width - panel_wing, ry  ,rx + P11_width - panel_wing , ry + CPH, layer='0')
    line(doc, rx + P11_width - thickness, ry  ,rx + P11_width - thickness , ry + CPH, layer='22')

    # 상부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P11_width -  panel_wing - 4 ,ry+CPH , layer='0')
    line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P11_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
    # 하부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P11_width -  panel_wing - 4 ,ry,  layer='0')
    line(doc, rx + panel_wing + 4, ry+thickness , rx + P11_width -  panel_wing - 4 ,ry+thickness,  layer='22')

    x1 = rx 
    y1 = ry 
    x2 = x1 + P11_width
    y2 = y1    
    x3 = x2 
    y3 = y2 + CPH
    x4 = x3 - P11_width
    y4 = y3 

    # 팝너트 표시하기    
    P11_hole = [P11_hole1, P11_hole2, P11_hole3, P11_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P11_width]
    tx = rx
    ty = ry+CPH    
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P11_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6_popnut")
                insert_block(tx + sum, ry,"M6_popnut_upset")
            if index == 0 :
                d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)         

    # 상부 전체치수
    d(doc,  rx , ry+CPH, rx + P11_width , ry+CPH, 120, direction="up")

    yp_bottom = ry  + 1
    yp_upper = ry + CPH - 1

    P11_handrailxpos = [0]  # 핸드레일 표현하지 않을때 0을 전달한다.
    rb_list = panel_rib(P11_width, P11_handrailxpos)    
    # print(f"P11 패널의 종보강 위치: {rb_list}")
    # print(f"P11 핸드레일 위치: {P11_handrailxpos}")
    for index, g in enumerate(rb_list):
        bp = rx + P11_width - g
        xlist = [bp , bp-40 ,bp-20 ,bp + 20 ,bp + 40 ]       
        # 모자보강
        rectangle(doc, xlist[2] , yp_bottom, xlist[3] , yp_upper, layer='0')
        rectangle(doc, xlist[1] , yp_bottom+panel_wing+1, xlist[4] , yp_upper-panel_wing-1, layer='구성선') # 구성선은 회색선    
        line(doc, xlist[0] , yp_bottom, xlist[0] , yp_upper, layer='CLphantom')  
        # 치수선
        # print (f"index = {index}, x : {bp}")        
        # print (f" len(rb_list) = { len(rb_list)}" )        
        if index == 0:
            d(doc, x3, y3,  bp , y4, 150, direction="down")     
        else:
            dc(doc, bp,y3)

        # 단면도에 모자보강 위치 표시하기
        line(doc, bp , rib_posy + 10 , bp , rib_posy - panel_width - 10 , layer='0')  
            
        # 5x10 장공 용접홀          
        insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
        insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")                     

    if len(rb_list)-1 > 0 :  # 마지막인 경우
        dc(doc, x4,y4)            

    # 장공홀 표현하기 M6_nut
    gap = 0    
    length = CPH - 85 + popnut_height 
    hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
    leftx = x1 + 1.5
    rightx = x2 - (panel_width - P11_holegap)
    ty = y2

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "M6_nut")
            # insert_block(rightx, ty + g, "M6_nut")
            circle_cross(doc, rightx, ty + g , 9, layer='0')    # P4와 연결되는 홀 기둥

        if index == 0 :
            d(doc, x2, ty + g, rightx, ty + g,  150, direction="up" )    
            d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    

            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x3, y3)    

    # 우측 전체 치수선
    d(doc, x2, y2, x3, y3, 220, direction="right" )  

    ###########################################################################
    # P11 전개도 그리기
    ###########################################################################

    rx = pagex + P11_width*2 + 1200                         
    x1 = rx
    y1 = pagey
    x2 = x1 + P11_width - (panel_width+5)*2
    y2 = y1    
    x3 = x2
    y3 = y2 + panel_wing + 4 
    x4 = x3 + panel_wing + 4 
    y4 = y3 
    x5 = x4 
    y5 = y4 + 14.5 if br == 1.5 else y4 + 16
    x6 = x5 + 45 if br == 1.5 else x5 + 47
    y6 = y5 
    x7 = x6 
    y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
    x8 = x7 - 45 if br == 1.5 else x7 - 47 
    y8 = y7 
    x9 = x8 
    y9 = y8 + 14.5 if br == 1.5 else y8 + 16
    x10 = x9 - (panel_wing + 4)
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_wing + 4 
    x12 = x11 - P11_width + (panel_width+5)*2
    y12 = y11
    x13 = x12 
    y13 = y12 - (panel_wing + 4)
    x14 = x13 - (panel_wing + 4)
    y14 = y13
    x15 = x14 
    y15 = y14 - 14.5 if br == 1.5 else y14 - 16
    x16 = x15 - 45 if br == 1.5 else x15 - 47
    y16 = y15 
    x17 = x16 
    y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
    x18 = x17 + 45 if br == 1.5 else x17 + 47
    y18 = y17 
    x19 = x18
    y19 = y18 - (panel_wing + 4)
    x20 = x19 + (panel_wing + 4)
    y20 = y19 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 20
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                     
    gap = 0
    gap = - 1.5 if br == 1.5 else - 1
    length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
    hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
    leftx = x17 + (panel_width*2 + panel_wing - P11_holegap - br * 4 )
    rightx = x6 - (panel_width+panel_wing - P11_holegap - br * 2 )
    ty = y6

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "8x16_vertical")
            insert_block(rightx, ty + g, "8x16_vertical")
        if index == 0 :
            d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x11, y11)    
    # 장공치수선 그리기    좌,우 떨어짐
    for index, g in enumerate(hole):
        if index == 5 :
            d(doc, x17, ty + g, leftx, ty + g, 150, direction="down" )                        
            d(doc, rightx, ty + g, x6, ty + g, 150, direction="down" )       


    #################################
    # 세화정공 헤더표시 (십자표시)
    #################################
    # 장공표시 #P01, P111은 일체형일 경우 만들어본다.
    hole = [90, 50, 90 , 50]
    limit = TRH
    xp = x17 + 11 + 11

    # 확인 요함 바닥에서 연신율부분 1.2, 1.5 차이점 확인요함
    holeypos = y6 + OPH - KH - popnut_height - 0.5 if br == 1.5 else y6 + OPH - KH - popnut_height - 1
    gap = 0    
    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            cross10(doc, xp, holeypos + gap)
            if index == 1 :
                d(doc, xp, holeypos+ pre_gap, xp, holeypos + gap, 150, direction="left", option='reverse' )    
            elif index != 0 and index != len(hole)-1 :
                dc(doc, xp, holeypos + gap )     
            else:
                dc(doc, xp, holeypos + gap , option='reverse' )  
        pre_gap = gap 
            
    # 지시선 추가 4-M8육각
    text = "4-M8육각"
    dim_leader(doc,  xp, holeypos + gap , xp-300, holeypos + gap  + 250,   text, direction="up")                    
        
    yp_bottom = y1
    yp_upper = y11

    rb_list = panel_rib(P11_width, P11_handrailxpos)    
    # print(f"P11 패널의 종보강 위치: {rb_list}")
    # print(f"P11 핸드레일 위치: {P11_handrailxpos}")
    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            text = "%%C3"
            dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="up")                    
            # 5mm 치수선표시
            d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
            d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

        circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
        circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
        if index == 0 :
            d(doc, x16, y16, bp, y11, 450, direction="down")
        else:
            dc(doc, bp,y11)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x7,y7)     
              
    # 9파이 팝너트 연결홀 상부/하부
    P11_hole = [P11_hole1, P11_hole2, P11_hole3, P11_hole4]   

    limit_point = [P11_width]
    tx = x16 + 30 if br == 1.5 else x16 + 32
    upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
    lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point
    # 상부의 연결홀
    for index, hole in enumerate(P11_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
            if index == 0 :
                holeupperx = tx + sum                               
                holeuppery = upper_ty                       
                text = "%%C9 M6 POPNUT(머리5mm)"
                dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="up")                
                d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

            elif index == len(hole_variables) - 1 :
                dc(doc, x7, y7)                   
            else:
                dc(doc, tx + sum, upper_ty)                                   
    # 하부에 연결홀 타공
    sum = 0
    for index, hole in enumerate(P11_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
            if index == 0 :
                holelowerx = tx + sum                               
                holelowery = lower_ty                          
                d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

            elif index == len(hole_variables) - 1 :
                dc(doc, x6, y6)                   
            else:
                dc(doc, tx + sum, lower_ty)
                
    # 상부치수선    
    d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
    dc(doc, x9 , y9)    
    dc(doc, x7, y7)
    # 상부 전체치수선
    d(doc, x16, y16, x7 ,y7, 250, direction="up")

    # 하부치수선    
    d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
    d(doc, x2, y2, x6 ,y6, 110, direction="down")        
    # 하부 2단 절곡 만나는 곳 치수선
    d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
    dc(doc, x4 , y4)    
    dc(doc, x6 , y6)
    # 하부 전체치수선
    d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
    
    # 오른쪽 15mm 표기
    d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
    # 오른쪽 최종 치수선
    d(doc, x11, y11 , x7, y7, 300, direction="right")
    dc(doc, x6, y6)
    dc(doc, x2, y2)    

    # 왼쪽 치수선 20mm 
    d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
    d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
    # 왼쪽 치수선 전체
    d(doc, x12, y12, x1, y1, 280, direction="left")

    # 모자보강 Y위치 저장 y3
    rib_posy = y3    

    #######################################  
    # P11,P11 단면도 (상부에 위치한)
    #######################################  
    x1 = x1 - panel_width + 6
    y1 = pagey + CH + 794
    x2 = x1 - panel_wing
    y2 = y1 
    x3 = x2
    y3 = y2 - panel_width
    x4 = x3 + P11_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - panel_width + thickness*2
    x10 = x9 - P11_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_width - thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3
    y13 = y3 + P11_holegap
    x14 = x4
    y14 = y4 + P11_holegap
    
    line(doc, x14-10, y14, x14+10, y14, layer="CL") 
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 150, direction='up')   
    d(doc, x6, y6, x5, y5, 150, direction='up')   
    # 좌측        
    d(doc, x2, y2, x3, y3, 180, direction='left')  

    # 전체하부
    d(doc, x3, y3, x4, y4, 350, direction='down')              
    d(doc, x14+10, y14, x4, y4, 130, direction='right')    

    x13, y13 =  x1-10, y3 + P11_holegap    
    d(doc, x3 + 100, y3 + P11_holegap , x3 + 100 , y3, 50, direction="left")
    d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')   
    rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
    # 하단 날개 23 표기 width 25 -2
    
    P11_hole = [P11_hole4, P11_hole3, P11_hole2, P11_hole1]     
    limit_point = [P11_width]
    tx = x3 
    ty = y3 + P11_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P11_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 270, direction="down" , option='reverse')                                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)        

    # 보강자리 표시
    rb_list = panel_rib(P11_width, P11_handrailxpos)    
    for index, g in enumerate(rb_list):        
        bp = x3 + g
        line(doc, bp, y3-10 , bp , y3+10, layer='0')                  
        if index == 0 :
            d(doc, bp, y3-10, x3, y3, 80, direction="down",option='reverse')
        else:
            dc(doc, bp,y3-10)

    # P11, P11은 side panel과 결합하니, 홀의 결합위치가 다르다. 주의)
    line(doc, x3 + (panel_width-P11_holegap) , y4 + 10 ,x3 + (panel_width-P11_holegap) , y4 - 10 , layer='CLphantom')  
    d(doc,  x3 + (panel_width-P11_holegap) , y3 - 10 , x3 , y3 , 50, direction="down")

    
    frameXpos = frameXpos + TargetXscale + 400


############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################


    ###################################################
    # 3page 보강 bracket
    ###################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 1200 + CPH 
    TargetYscale = 1500 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    # print("3page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "BRACKET DETAIL", f"WH:{CPH}", "drawing number")   

    ###################################################
    # 3page 모자보강 등 bracket P4형태에서 정보를 가져옴
    ###################################################
    
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale    
    rib_length = CPH - 2

    x1 = pagex 
    y1 = pagey + 1400
    x2 = x1 + rib_length - 12*2 
    y2 = y1    
    x3 = x2
    y3 = y2 + 39.1
    x4 = x3 + 12
    y4 = y3 
    x5 = x4 
    y5 = y4 + 38
    x6 = x5 - 12
    y6 = y5 
    x7 = x6 
    y7 = y6 + 39.1
    x8 = x7 - rib_length + 12*2 
    y8 = y7 
    x9 = x8 
    y9 = y8 - 39.1
    x10 = x9 - 12
    y10 = y9 
    x11 = x10 
    y11 = y10 - 38
    x12 = x11 + 12
    y12 = y11

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x10 가로방향 장공 레이져 layer
    x13 , y13 =  x11+6,(y10+y11)/2
    x14 , y14 =  x4-6,(y10+y11)/2
    insert_block(x13 , y13 ,"5x10_horizontal_laser") 
    insert_block(x14 , y14 ,"5x10_horizontal_laser") 
    dim_leader(doc, x13 , y13, x13+100 , y13+100,direction="right", text="2-5x10" )
      
    # 상부 치수선
    d(doc, x10,y10,x13,y13,200,direction="up")
    d(doc, x5,y5,x14,y14,200,direction="up")
    # 하부 치수선
    d(doc, x11,y11,x1,y1,100,direction="down")
    d(doc, x4,y4,x2,y2,100 ,direction="down")
    d(doc, x11,y11,x4,y4,200,direction="down")
    # 좌측 치수
    d(doc, x8,y8,x13,y13,100,direction="left")
    dc(doc, x1,y1 , option='reverse')
    d(doc, x8,y8,x1,y1,170,direction="left")
    # 우측 치수
    d(doc, x7,y7,x5,y5,120,direction="right", option='reverse')
    d(doc, x7,y7,x5,y5,120,direction="right", option='reverse')
    d(doc, x5,y5,x4,y4, 60,direction="right", option='reverse')    
    d(doc, x7,y7,x2, y2, 210,direction="right")

    # 분리형 보강산출 (일체형과 다른 부분 있음)
    global P1_height, P2_height, P3_height, P4_height, P5_height
    global P6_height, P7_height, P8_height, P9_height, P10_height, P11_height

    P1_height  = 100
    P2_height  = 0
    P3_height  = 0
    P4_height  = 0
    P5_height  = 0
    P6_height  = 0
    P7_height  = 0
    P8_height  = 100 if handrail_height > 0 else 0
    P9_height  = 0
    P10_height = 0
    P11_height = 0

    rib_width80_total, rib_width25_total = total_ribs()
    rib_width25_total = 4
    # print(f"80mm 보강 개수: {rib_width80_total}, 25mm 보강 개수: {rib_width25_total}")     

    # description    
    desx = x1 + rib_length/2 - 300
    desy = y1 - 300
    textstr = f"Part Name : 모자 보강"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 116.2 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {rib_width80_total * SU} EA"      
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')           

    ################
    # 단면도 그리기
    ################    
    rib_wing = 20
    rib_height = 23.5
    rib_top_width = 40
    rib_thickness = 1.6

    x1 = x1 - 420
    y1 = y1 + 35
    x2 = x1
    y2 = y1 + rib_wing - rib_thickness
    x3 = x2 + rib_height - rib_thickness
    y3 = y2 
    x4 = x3
    y4 = y3 + rib_top_width
    x5 = x4 - rib_height + rib_thickness
    y5 = y4 
    x6 = x5 
    y6 = y5 + rib_wing - rib_thickness
    x7 = x6 - rib_thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - rib_wing
    x9 = x8 + rib_height - rib_thickness
    y9 = y8 
    x10 = x9 
    y10 = y9 - rib_top_width + rib_thickness*2
    x11 = x10 - rib_height + rib_thickness
    y11 = y10
    x12 = x11 
    y12 = y11 - rib_wing

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     
      
    # 하부 치수선
    d(doc, x12,y12,x3,y3,150,direction="down")
    # 좌측 치수
    d(doc, x8,y8,x7,y7,80,direction="left")
    d(doc, x11,y11,x12,y12,80,direction="left")
    # 우측 치수    
    d(doc, x4, y4, x3, y3, 80, direction="right", option='reverse')

    ###################################################
    # 3page HOP 보강 'ㄷ'자 보강 좌측 하단 bracket
    ###################################################    
    rx = x1
    ry = y1

    rib_length = HOP_bottomHeight  - 4
    x1 = rx + 300
    y1 = ry - 900
    x2 = x1 + rib_length - 12 - 35 
    y2 = y1    
    x3 = x2
    y3 = y2 + 26
    x4 = x3 + 35
    y4 = y3 
    x5 = x4 
    y5 = y4 + 38
    x6 = x5 - rib_length
    y6 = y5 
    x7 = x6 
    y7 = y6 - 19
    x8 = x7 + 12
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x10 가로방향 장공 레이져 layer
    x9 , y9 =  x6+5,(y6+y7)/2
    x10 , y10 =  x5-5,(y6+y7)/2
    draw_circle(doc, x9,y9, 5,layer="레이져")
    draw_circle(doc, x10,y10, 5,layer="레이져")
      
    # 상부 치수선
    d(doc, x9,y9,x6,y6,80,direction="up")
    d(doc, x6,y6,x5,y5,150,direction="up")
    # 하부 치수선
    d(doc, x1,y1,x7,y7,80,direction="down")
    d(doc, x4,y4,x2,y2,106 ,direction="down")
    # 좌측 치수    
    d(doc, x9,y9,x6,y6,106 ,direction="left")
    d(doc, x7,y7,x6,y6,170,direction="left")
    # 우측 치수
    d(doc, x2,y2,x5,y5,200,direction="right")
    d(doc, x4,y4,x2,y2,120,direction="right")

    # description    
    desx = x1 + rib_length/2 - 200
    desy = y1 - 300
    textstr = f"Part Name : HOP 하부 보강"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 64 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ################
    # 단면도 그리기 'ㄷ'자 형태
    ################
    rib_topwing = 20
    rib_bottomwing = 25    
    rib_top_width = 23.5
    rib_thickness = 1.6

    x1 = x1 - 350
    y1 = y1 + 35
    x2 = x1 - rib_topwing 
    y2 = y1
    x3 = x2 
    y3 = y2 - rib_top_width
    x4 = x3 + rib_bottomwing
    y4 = y3 
    x5 = x4
    y5 = y4 + rib_thickness
    x6 = x5 - rib_bottomwing + rib_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 + rib_top_width - rib_thickness*2
    x8 = x7 + rib_topwing - rib_thickness
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x8 = x2 + 10
    y8 = y2

    line(doc, x8,y8-10, x8,y8+10, layer='0')
      
    # 상부 치수선
    d(doc, x8,y8,x2,y2,100,direction="up")
    d(doc, x1,y1,x2,y2,180,direction="up")
    # 하부
    d(doc, x3,y3,x4,y4,150,direction="down")
    # 좌측 치수
    d(doc, x3,y3,x2,y2,100,direction="left")
    

    ###################################################
    # 3page HOP 상단 보강 'ㄷ'자 보강 우측 하단 bracket
    ###################################################

    HOP_upper_rib_length = CPH - HOP_bottomHeight - HOP_height - 7

    x1 = rx + 400 * 2 + HOP_bottomHeight
    y1 = ry - 900
    x2 = x1 + HOP_upper_rib_length - 12 - 35
    y2 = y1    
    x3 = x2
    y3 = y2 + 26
    x4 = x3 + 35
    y4 = y3 
    x5 = x4 
    y5 = y4 + 38
    x6 = x5 - HOP_upper_rib_length
    y6 = y5 
    x7 = x6 
    y7 = y6 - 19
    x8 = x7 + 12
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x10 가로방향 장공 레이져 layer
    x9 , y9 =  x6+5,(y6+y7)/2
    x10 , y10 =  x5-5,(y6+y7)/2
    draw_circle(doc, x9,y9,5,layer="레이져")
    draw_circle(doc, x10,y10,5,layer="레이져")
      
    # 상부 치수선
    d(doc, x9,y9,x6,y6,80,direction="up")
    d(doc, x6,y6,x5,y5,150,direction="up")
    # 하부 치수선
    d(doc, x1,y1,x7,y7,80,direction="down")
    d(doc, x4,y4,x2,y2,106 ,direction="down")
    # 좌측 치수    
    d(doc, x9,y9,x6,y6,106 ,direction="left")
    d(doc, x7,y7,x6,y6,170,direction="left")
    # 우측 치수
    d(doc, x2,y2,x5,y5,200,direction="right")
    d(doc, x4,y4,x2,y2,120,direction="right")

    # description    
    desx = x1 + HOP_upper_rib_length/2 - 250
    desy = y1 - 300
    textstr = f"Part Name : HOP 상부 보강"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 64 x {str(HOP_upper_rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')    

    frameXpos = frameXpos + TargetXscale + 400

    ###################################################
    # 4page 보강 COP bracket 등 7가지 부속
    ###################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 1800 + CPH 
    TargetYscale = 1500 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    # print("3page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "BRACKET DETAIL", f"WH:{CPH}", "drawing number")   

    ###################################################
    # 4page Front 상하 보강 'ㄷ'자 보강 좌측 하단 bracket
    ###################################################
    
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale    
    rib_length = CPH - 2

    rx = math.floor(pagex - 100)
    ry = math.floor(pagey + 1800)

    # rib_length = P1_width  - 5
    # x1 = rx
    # y1 = ry
    # x2 = x1 + rib_length 
    # y2 = y1    
    # x3 = x2
    # y3 = y2 + 76.6
    # x4 = x3 - rib_length
    # y4 = y3 

    # prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    # lastNum = 4
    # for i in range(1, lastNum + 1):
    #     curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
    #     line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
    #     prev_x, prev_y = curr_x, curr_y
    # line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # # 8x20 가로방향 장공 
    # x5 , y5 =  x4+(frontholes[-1]-2.5), y4 - 10
    # x6 , y6 =  x3-(frontholes[0]-2.5), y3 - 10

    # # print (f"frontholes : {frontholes}")
    # # draw_circle(doc, x9,y9,2.5,layer="레이져")
    # insert_block(x5,y5,"8x20_horizontal_laser")
    # insert_block(x6,y6,"8x20_horizontal_laser")
      
    # # 상부 치수선
    # d(doc, x4,y4,x5,y5,80,direction="up",option='reverse')
    # dc(doc, x6,y6)
    # dc(doc, x3,y3)
    # # 하부 치수선
    # d(doc, x1,y1,x2,y2,80,direction="down")    
    # # 우측 치수
    # d(doc, x6,y6,x3,y3,180,direction="right")
    # d(doc, x2,y2,x3,y3,260,direction="right")

    # # description    
    # desx = x1 + rib_length/2 - 300
    # desy = y1 - 300
    # textstr = f"Part Name : P1,P11 상하 보강"    
    # draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    # textstr = f"Mat.Spec : EGI 1.6T"    
    # draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    # textstr = f"Size : 76.6 x {str(rib_length)} mm"    
    # draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    # textstr = f"Quantity : {SU*4} EA"    
    # draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ##################################
    # 단면도 그리기 'ㄷ'자 형태
    ##################################    
    rib_topwing = 21
    rib_bottomwing = 21
    rib_top_width = 40
    rib_thickness = 1.6

    x1 = x1 - 250
    y1 = y1 + 35
    x2 = x1 - rib_topwing 
    y2 = y1
    x3 = x2 
    y3 = y2 - rib_top_width
    x4 = x3 + rib_bottomwing
    y4 = y3 
    x5 = x4
    y5 = y4 + rib_thickness
    x6 = x5 - rib_bottomwing + rib_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 + rib_top_width - rib_thickness*2
    x8 = x7 + rib_topwing - rib_thickness
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x8 = x2+10
    y8 = y2

    line(doc, x8,y8-10, x8,y8+10, layer='0')
      
    # 상부 치수선
    d(doc, x8,y8,x2,y2,100,direction="up")
    d(doc, x1,y1,x2,y2,180,direction="up")
    # 하부
    d(doc, x3,y3,x4,y4,150,direction="down")
    # 좌측 치수
    d(doc, x3,y3,x2,y2,80,direction="left")

    ###################################################
    # 4page '역 ㄴ'자 1번 11번 하부 컬럼이나 일체형 기둥 고정용 바닥 bracket
    ###################################################

    rx = math.floor(pagex + P1_width + 900)
    ry = pagey + 1800

    rib_length = 30
    x1 = rx
    y1 = ry
    x2 = x1 + rib_length 
    y2 = y1    
    x3 = x2
    y3 = y2 + 100.5
    x4 = x3 - rib_length
    y4 = y3 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 8x16 세로방향 장공 
    x5 , y5 =  x1+15, y1 + 24 - (column_BottomHoleHorizontal)

    # print (f"frontholes : {frontholes}")
    # draw_circle(doc, x9,y9,2.5,layer="레이져")
    insert_block(x5,y5,"8x16_vertical")
      
    # 하부 치수선
    d(doc, x5,y5,x2,y2,80,direction="down")
    d(doc, x1,y1,x2,y2,140,direction="down")
    
    # 우측 치수    
    d(doc, x2,y2,x3,y3,260,direction="right")
    # 좌측 치수
    d(doc, x5,y5,x1,y1,60,direction="left")

    # description    
    desx = x1 + rib_length/2 - 300
    desy = y1 - 300
    textstr = f"Part Name : COLUMN BRACKET"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 2.0T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 100.5 x 30 mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU*2} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ################
    # 단면도 하부 컬럼 '역 ㄴ'자 형태
    ################    

    rib_bottomwing = 24
    rib_height = 80
    rib_thickness = 2.0

    x1 = rx -  350
    y1 = y1 + 35
    x2 = x1 + rib_bottomwing 
    y2 = y1
    x3 = x2 
    y3 = y2 + rib_height
    x4 = x3 - rib_thickness
    y4 = y3 
    x5 = x4  
    y5 = y4 - rib_height + rib_thickness
    x6 = x5 - rib_bottomwing + rib_thickness
    y6 = y5

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x7 = x2 - (column_BottomHoleHorizontal)
    y7 = y2

    line(doc, x7,y7-10, x7,y7+10, layer='0')
        
    # 하부
    d(doc, x7,y7-10,x2,y2,100,direction="down")
    d(doc, x1,y1,x2,y2,160,direction="down")
    # 우측 치수
    d(doc, x2,y2,x3,y3,80,direction="right")

    ###################################################
    # 4page H/R bracket 
    ###################################################

    rx = math.floor(pagex + P1_width + 900 + 1000 )
    ry = pagey + 1800

    rib_length = 30
    x1 = rx
    y1 = ry
    x2 = x1 + rib_length 
    y2 = y1    
    x3 = x2
    y3 = y2 + 50
    x4 = x3 - rib_length
    y4 = y3 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 12파이 단공 
    x5 , y5 =  x1+15, y1 + 25 
    draw_circle(doc, x5,y5, 12,layer='레이져')
    dim_leader(doc, x5,y5, x5+150, y5+250, direction='right', text='%%c12 Hole')
      
    # 하부 치수선
    d(doc, x5,y5,x1,y1,80,direction="down")
    d(doc, x1,y1,x2,y2,140,direction="down")
    
    # 우측 치수    
    d(doc, x5,y5,x2,y2,150,direction="right")
    d(doc, x2,y2,x3,y3,250,direction="right")
    

    # description    
    # 핸드레일 개소를 계산해야 함.
    handrailhole_total = (len(HRsidegap)-1)*2 + len(HRreargap)-1
    # print (f"len(HRsidegap) {len(HRsidegap)} list {HRsidegap},  len(HRreargap) { len(HRreargap)} list {HRreargap}")
    desx = x1 + rib_length/2 - 200
    desy = y1 - 300
    textstr = f"Part Name : handrail bracket"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 2.0T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 50 x 30 mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU*handrailhole_total} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               


    ###################################################
    # 4page 종보강 'ㄷ'자  1.6T 따임 형태
    ###################################################
    
    rx = math.floor(pagex - 150)
    ry = pagey + 1000

    rib_length = CPH  - 2
    x1 = rx 
    y1 = ry 
    x2 = x1 + rib_length - 12 - 12 
    y2 = y1    
    x3 = x2
    y3 = y2 + 44.1
    x4 = x3 + 12
    y4 = y3 
    x5 = x4 
    y5 = y4 + 19
    x6 = x5 - rib_length
    y6 = y5 
    x7 = x6 
    y7 = y6 - 19
    x8 = x7 + 12
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x8 가로방향 장공 레이져 layer
    x9 , y9 =  x6+6,(y6+y7)/2
    x10 , y10 =  x5-6,(y6+y7)/2
    insert_block(x9,y9,"5x8_horizontal_laser")
    insert_block(x10,y10,"5x8_horizontal_laser")
      
    # 상부 치수선
    d(doc, x9,y9,x6,y6,50,direction="up")
    d(doc, x6,y6,x5,y5,100,direction="up")
    # 하부 치수선
    d(doc, x1,y1,x7,y7,80,direction="down")
    d(doc, x4,y4,x2,y2,106 ,direction="down")
    # 좌측 치수    
    d(doc, x9,y9,x6,y6,106 ,direction="left")
    d(doc, x7,y7,x6,y6,170,direction="left")
    # 우측 치수
    d(doc, x2,y2,x5,y5,200,direction="right")
    d(doc, x4,y4,x2,y2,120,direction="right")

    # description    
    desx = x5 + 400
    desy = y1 + 100
    textstr = f"Part Name : 종보강"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 63.1 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {(rib_width25_total) * SU} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ##########################
    # 단면도 그리기 'ㄷ'자 형태
    ##########################    
    rib_topwing = 20
    rib_bottomwing = 25    
    rib_top_width = 23.5
    rib_thickness = 1.6

    x1 = x1 - 350
    y1 = y1 + 35
    x2 = x1 - rib_topwing 
    y2 = y1
    x3 = x2 
    y3 = y2 - rib_top_width
    x4 = x3 + rib_bottomwing
    y4 = y3 
    x5 = x4
    y5 = y4 + rib_thickness
    x6 = x5 - rib_bottomwing + rib_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 + rib_top_width - rib_thickness*2
    x8 = x7 + rib_topwing - rib_thickness
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x8 = x2+10
    y8 = y2

    line(doc, x8,y8-10, x8,y8+10, layer='0')
      
    # 상부 치수선
    d(doc, x8,y8,x2,y2,100,direction="up")
    d(doc, x1,y1,x2,y2,180,direction="up")
    # 하부
    d(doc, x3,y3,x4,y4,150,direction="down")
    # 좌측 치수
    d(doc, x3,y3,x2,y2,100,direction="left")
    

    ###################################################
    # 4page 종보강 'ㄷ'자  1.6T 따임없음 형태
    # 일체형일때  종보강 길이는  판넬 전체길이에서 상,하보강 붙이는면40 으로 작업해서 전체길이에서 82mm 뺀값으로 종보강값구합니다.
    ###################################################
    
    rx = math.floor(pagex - 150)
    ry = pagey + 550

    # rib_length = CH  - 82
    # x1 = rx 
    # y1 = ry 
    # x2 = x1 + rib_length 
    # y2 = y1    
    # x3 = x2 
    # y3 = y2 + 63.1
    # x4 = x3 - rib_length
    # y4 = y3 

    # prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    # lastNum = 4
    # for i in range(1, lastNum + 1):
    #     curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
    #     line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
    #     prev_x, prev_y = curr_x, curr_y
    # line(doc, prev_x, prev_y, x1, y1, layer="레이져")     
    
    # # 하부 치수선
    # d(doc, x1,y1,x2,y2,80,direction="down")    
    # # 우측 치수
    # d(doc, x2,y2,x3,y3,100,direction="right",option='reverse')

    # # description    
    # desx = x2 + 400
    # desy = y1 + 100
    # textstr = f"Part Name : 종보강"    
    # draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    # textstr = f"Mat.Spec : EGI 1.6T"    
    # draw_Text(doc, desx , desy - 70 , 35, str(textstr), layer='0')    
    # textstr = f"Size : 63.1 x {str(rib_length)} mm"    
    # draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    # textstr = f"Quantity : 수량산출 필요 {SU} EA"    
    # draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    # ##########################
    # # 단면도 그리기 'ㄷ'자 형태
    # ##########################    
    # rib_topwing = 20
    # rib_bottomwing = 25    
    # rib_top_width = 23.5
    # rib_thickness = 1.6

    # x1 = x1 - 350
    # y1 = y1 + 35
    # x2 = x1 - rib_topwing 
    # y2 = y1
    # x3 = x2 
    # y3 = y2 - rib_top_width
    # x4 = x3 + rib_bottomwing
    # y4 = y3 
    # x5 = x4
    # y5 = y4 + rib_thickness
    # x6 = x5 - rib_bottomwing + rib_thickness
    # y6 = y5 
    # x7 = x6 
    # y7 = y6 + rib_top_width - rib_thickness*2
    # x8 = x7 + rib_topwing - rib_thickness
    # y8 = y7 

    # prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    # lastNum = 8
    # for i in range(1, lastNum + 1):
    #     curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
    #     line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
    #     prev_x, prev_y = curr_x, curr_y
    # line(doc, prev_x, prev_y, x1, y1, layer="0")     

    # x8 = x2+10
    # y8 = y2
      
    # # 상부 치수선    
    # d(doc, x1,y1,x2,y2,60,direction="up")
    # # 하부
    # d(doc, x3,y3,x4,y4,100,direction="down")
    # # 좌측 치수
    # d(doc, x3,y3,x2,y2,100,direction="left")


    ###################################################
    # 4page COP 고정 bracket '역 ㄱ'자 형태
    ###################################################
    
    rx = math.floor(pagex - 150)
    ry = pagey + 100

    rib_length = COP_width + 2
    mid_cut_length = COP_holegap/2  # 타공간격
    remain_length = (rib_length - mid_cut_length)/2
    x1 = rx 
    y1 = ry 
    x2 = x1 + rib_length
    y2 = y1    
    x3 = x2
    y3 = y2 + 50.3
    x4 = x3 - remain_length
    y4 = y3 
    x5 = x4 
    y5 = y4 - 23
    x6 = x5 - mid_cut_length
    y6 = y5 
    x7 = x6 
    y7 = y6 + 23
    x8 = x7 - remain_length
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x8 가로방향 장공 레이져 layer
    x9 , y9 =  x7 -  COP_holegap/4  , y7 - 10
    x10 , y10 =  x4 + COP_holegap/4  , y4 - 10
    insert_block(x9,y9,"cross_mark") # + 선
    insert_block(x10,y10,"cross_mark") 
    dim_leader(doc, x10,y10, x10+150, y10+200, direction='right', text='2-M6육각')
      
    # 상부 치수선
    d(doc, x7,y7,x4,y4,50,direction="up")
    d(doc, x9,y9,x10,y10,120,direction="up")
    # 하부 치수선
    d(doc, x1,y1,x2,y2,80,direction="down")
    # 좌측 치수    
    d(doc, x9,y9,x8,y8,80 ,direction="left")
    # 우측 치수
    d(doc, x5,y5,x3,y3,60 + extract_abs(x3,x5) , direction="right")
    d(doc, x3,y3,x2,y2,120,direction="right")

    # description    
    desx = x2 + 300
    desy = y1 + 100
    textstr = f"Part Name : COP 고정 bracket"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 50.3 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU*2} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ##########################
    # 단면도 '역 ㄱ'자 형태
    ##########################    
    rib_topwing = 23    
    rib_top_width = 30
    rib_thickness = 1.6

    x1 = x1 - 350
    y1 = y1 - 50
    x2 = x1 - rib_topwing 
    y2 = y1
    x3 = x2 
    y3 = y2 - rib_top_width
    x4 = x3 + rib_thickness
    y4 = y3 
    x5 = x4
    y5 = y4 + rib_top_width - rib_thickness
    x6 = x5 + rib_topwing - rib_thickness
    y6 = y5 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x8 = x2+13
    y8 = y2

    line(doc, x8,y8-10, x8,y8+10, layer='0')
      
    # 상부 치수선
    d(doc, x8,y8,x2,y2,100,direction="up")
    d(doc, x1,y1,x2,y2,180,direction="up")    
    # 좌측 치수
    d(doc, x3,y3,x2,y2,100,direction="left")

    ###################################################
    # 4page HOP 고정 bracket '역 ㄱ'자 형태 (두번째 전개도)
    ###################################################
    
    rx = math.floor(pagex + 1400)

    rib_length = HOP_width + 2
    mid_cut_length = HOP_holegap/3
    remain_length = (rib_length - mid_cut_length)/2
    x1 = rx 
    y1 = ry 
    x2 = x1 + rib_length
    y2 = y1    
    x3 = x2
    y3 = y2 + 50.3
    x4 = x3 - remain_length
    y4 = y3 
    x5 = x4 
    y5 = y4 - 23
    x6 = x5 - mid_cut_length
    y6 = y5 
    x7 = x6 
    y7 = y6 + 23
    x8 = x7 - remain_length
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")     

    # 5x8 가로방향 장공 레이져 layer
    x9 , y9 =  x7 - HOP_holegap/3 , y7 - 10
    x10 , y10 =  x4 + HOP_holegap/3 , y4 - 10
    insert_block(x9,y9,"cross_mark") # + 선
    insert_block(x10,y10,"cross_mark") 
    dim_leader(doc, x10,y10, x10+150, y10+200, direction='right', text='2-M6육각')
      
    # 상부 치수선
    d(doc, x7,y7, x4,y4,50,direction="up")
    d(doc, x9,y9,x10,y10,120,direction="up")
    
    # 하부 치수선
    d(doc, x1,y1,x2,y2,80,direction="down")
    # 좌측 치수    
    d(doc, x9,y9,x8,y8,80 ,direction="left")
    # 우측 치수
    d(doc, x5,y5,x3,y3,60 + extract_abs(x3,x5) , direction="right")
    d(doc, x3,y3,x2,y2,120,direction="right")

    # description
    desx = x2 + 400
    desy = y1 + 100
    textstr = f"Part Name : HOP 고정 bracket"
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 50.3 x {str(rib_length)} mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU*2} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')        

    frameXpos = frameXpos + TargetXscale + 400







    #########################################################################################
    # 5page P2, P8 같으면 하나만 표시
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 6851 
    TargetYscale = 4870 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    # print("page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "SIDE PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # P2 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
    ###################################################
    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx + panel_wing
    y1 = ry + CH + 500
    x2 = x1 - panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 + P2_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 + thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  + panel_width - thickness*2
    x10 = x9 - P2_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 - panel_width + thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   
    
    x13, y13 =  x1-10, y3-P2_holegap
    line(doc, x3-10, y3-P2_holegap, x3 + 10, y3-P2_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y4-P2_holegap, x4 + 10, y4-P2_holegap , layer='CLphantom') # '구성선' 회색선
    rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')

    # A작업 표기
    if P2_width == P8_width :
        insert_block(x4 + 230 , y4 + 320,"a_work")
    
    # 전면 벽 판넬 변수 목록 초기화
    P2_hole = [P2_hole1, P2_hole2, P2_hole3, P2_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P2_width]
    tx = x3 
    ty = y3 - P2_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P2_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)               

    d(doc,  x3 , y3, x4, y4, 173, direction="up")
    d(doc,  x13 , y13, x3, y3, 140, direction="left")
    d(doc,  x5 , y5, x4, y4, 190, direction="right")
    d(doc,  x6, y6, x5 , y5,  80, direction="down")    
    d(doc,  x1 , y1, x2, y2, 80, direction="down")     

    # 모자보강 Y위치 저장 y3
    rib_posy = y3

    #############################################################
    # P2 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
    # P2 조립도 본체구성 표현
    #############################################################
            
    ry = pagey 

    rectangle(doc, rx, ry , rx+ P2_width, ry+CPH, layer='0')
    rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
    rectangle(doc, rx + P2_width , ry , rx+P2_width-panel_wing , ry+CPH , layer='0')

    # 세로 날개 표시 panel_wing
    line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
    line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
    line(doc, rx + P2_width - panel_wing, ry  ,rx + P2_width - panel_wing , ry + CPH, layer='0')
    line(doc, rx + P2_width - thickness, ry  ,rx + P2_width - thickness , ry + CPH, layer='22')

    # 상부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P2_width -  panel_wing - 4 ,ry+CPH , layer='0')
    line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P2_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
    # 하부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P2_width -  panel_wing - 4 ,ry,  layer='0')
    line(doc, rx + panel_wing + 4, ry+thickness , rx + P2_width -  panel_wing - 4 ,ry+thickness,  layer='22')

    x1 = rx 
    y1 = ry 
    x2 = x1 + P2_width
    y2 = y1    
    x3 = x2 
    y3 = y2 + CPH
    x4 = x3 - P2_width
    y4 = y3 

    # 팝너트 표시하기    
    P2_hole = [P2_hole1, P2_hole2, P2_hole3, P2_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P2_width]
    tx = rx
    ty = ry+CPH    
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P2_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6_popnut")
                insert_block(tx + sum, ry,"M6_popnut_upset")
            if index == 0 :
                d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)         

    # 상부 전체치수
    d(doc,  rx , ry+CPH, rx + P2_width , ry+CPH, 120, direction="up")

    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P2_handrailxpos):            
            if g is not None : 
                tx = x2 - g
                insert_block(tx , y2 + handrail_height , "handrail_bracket")                
                d(doc, tx, y2 + handrail_height , x2 , y2 + handrail_height , 100 + index*100, direction="down")                    
                line(doc, tx , rib_posy + 10 , tx , rib_posy - 10 , layer='CLphantom')  

    d(doc, x1, y1, tx , y2 + handrail_height , 150, direction="left")    

    yp_bottom = ry  + 1
    yp_upper = ry + CPH - 1

    rb_list = panel_rib(P2_width, P2_handrailxpos)    
    # print(f"P2 패널의 종보강 위치: {rb_list}")
    # print(f"P2 핸드레일 위치: {P2_handrailxpos}")
    for index, g in enumerate(rb_list):
        bp = rx + P2_width - g
        xlist = [bp , bp-40 ,bp-20 ,bp + 20 ,bp + 40 ]       
        # 모자보강
        rectangle(doc, xlist[2] , yp_bottom, xlist[3] , yp_upper, layer='0')
        rectangle(doc, xlist[1] , yp_bottom+panel_wing+1, xlist[4] , yp_upper-panel_wing-1, layer='구성선') # 구성선은 회색선    
        line(doc, xlist[0] , yp_bottom, xlist[0] , yp_upper, layer='CLphantom')  
        # 치수선
        # print (f"index = {index}, x : {bp}")        
        # print (f" len(rb_list) = { len(rb_list)}" )        
        if index == 0:
            d(doc, x3, y3,  bp , y4, 150, direction="down")     
        else:
            dc(doc, bp,y3)

        # 단면도에 모자보강 위치 표시하기
        line(doc, bp , rib_posy + 10 , bp , rib_posy - 10 , layer='0')  
            
        # 5x10 장공 용접홀          
        insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
        insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")                     

    if len(rb_list)-1 > 0 :  # 마지막인 경우
        dc(doc, x4,y4)            

    # 장공홀 표현하기 M6_nut
    gap = 0    
    length = CPH - 85 + popnut_height 
    hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
    leftx = x1 + 1.5
    rightx = x2 - 1.5
    ty = y2

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "M6_nut")
            insert_block(rightx, ty + g, "M6_nut")
        if index == 0 :
            d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x3, y3)    

    # 우측 전체 치수선
    d(doc, x2, y2, x3, y3, 220, direction="right" )  

    ###########################################################################
    # P2 전개도 그리기
    ###########################################################################

    rx = pagex + P2_width + 1200                         
    x1 = rx
    y1 = pagey
    x2 = x1 + P2_width - (panel_width+5)*2
    y2 = y1    
    x3 = x2
    y3 = y2 + panel_wing + 4 
    x4 = x3 + panel_wing + 4 
    y4 = y3 
    x5 = x4 
    y5 = y4 + 14.5 if br == 1.5 else y4 + 16
    x6 = x5 + 45 if br == 1.5 else x5 + 47
    y6 = y5 
    x7 = x6 
    y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
    x8 = x7 - 45 if br == 1.5 else x7 - 47 
    y8 = y7 
    x9 = x8 
    y9 = y8 + 14.5 if br == 1.5 else y8 + 16
    x10 = x9 - (panel_wing + 4)
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_wing + 4 
    x12 = x11 - P2_width + (panel_width+5)*2
    y12 = y11
    x13 = x12 
    y13 = y12 - (panel_wing + 4)
    x14 = x13 - (panel_wing + 4)
    y14 = y13
    x15 = x14 
    y15 = y14 - 14.5 if br == 1.5 else y14 - 16
    x16 = x15 - 45 if br == 1.5 else x15 - 47
    y16 = y15 
    x17 = x16 
    y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
    x18 = x17 + 45 if br == 1.5 else x17 + 47
    y18 = y17 
    x19 = x18
    y19 = y18 - (panel_wing + 4)
    x20 = x19 + (panel_wing + 4)
    y20 = y19 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 20
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                     
    gap = 0
    gap = - 1.5 if br == 1.5 else - 1
    length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
    hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
    leftx = x17 + (panel_width+panel_wing - P2_holegap - br * 2 )
    rightx = x6 - (panel_width+panel_wing - P2_holegap - br * 2 )
    ty = y6

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "8x16_vertical")
            insert_block(rightx, ty + g, "8x16_vertical")
        if index == 0 :
            d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x11, y11)    

    # 장공치수선 그리기    좌,우 떨어짐
    for index, g in enumerate(hole):
        if index == 4 :
            d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
            d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )        

    yp_bottom = y1
    yp_upper = y11

    rb_list = panel_rib(P2_width, P2_handrailxpos)    
    # print(f"P2 패널의 종보강 위치: {rb_list}")
    # print(f"P2 핸드레일 위치: {P2_handrailxpos}")
    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            text = "%%C3"
            dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="left")                    
            # 5mm 치수선표시
            d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
            d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

        circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
        circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
        if index == 0 :
            d(doc, x16, y16, bp, y11, 200, direction="down")
        else:
            dc(doc, bp,y11)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x7,y7)     

    if handrail_height > 0 :
        # 핸드레일 그리기       
        for index, g in enumerate(P2_handrailxpos):            
            if g is not None : 
                tx = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
                ty = y6 + handrail_height - 1  if br == 1 else y6 + handrail_height - 1.5 
                if len(P2_handrailxpos) == 1 :
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    d(doc, tx, ty , x6 , ty , 100  , direction="up")                    
                    d(doc, tx, ty , x17 , ty , 100  , direction="up")                    
                    d(doc, x2, y2, tx , ty , 280, direction="right")  
                    # 보강자리에서 간격 X 축 치수선
                    d(doc, bp, ty, tx , ty , 180, direction="down")  
                else:
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    if index == 0 :
                        d(doc, x16 , ty , tx, ty , 100  , direction="up") 
                    else:                         
                        dc(doc, tx , ty )
                        dc(doc, x6 , ty )
                        # 보강자리에서 간격 X 축 치수선
                        d(doc, x2, y2, tx , ty , 280, direction="right") 
                        d(doc, bp, ty, tx , ty , 180, direction="down")  
                  
     
    # 9파이 팝너트 연결홀 상부/하부
    P2_hole = [P2_hole1, P2_hole2, P2_hole3, P2_hole4]   

    limit_point = [P2_width]
    tx = x16 + 30 if br == 1.5 else x16 + 32
    upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
    lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point
    # 상부의 연결홀
    for index, hole in enumerate(P2_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
            if index == 0 :
                holeupperx = tx + sum                               
                holeuppery = upper_ty                       
                text = "%%C9 M6 POPNUT(머리5mm)"
                dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="left")                
                d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

            elif index == len(hole_variables) - 1 :
                dc(doc, x7, y7)                   
            else:
                dc(doc, tx + sum, upper_ty)                                   
    # 하부에 연결홀 타공
    sum = 0
    for index, hole in enumerate(P2_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
            if index == 0 :
                holelowerx = tx + sum                               
                holelowery = lower_ty                          
                d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

            elif index == len(hole_variables) - 1 :
                dc(doc, x6, y6)                   
            else:
                dc(doc, tx + sum, lower_ty)      
                              
                
    # 상부치수선    
    d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
    dc(doc, x9 , y9)    
    dc(doc, x7, y7)
    # 상부 전체치수선
    d(doc, x16, y16, x7 ,y7, 250, direction="up")

    # 하부치수선    
    d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
    d(doc, x2, y2, x6 ,y6, 110, direction="down")        
    # 하부 2단 절곡 만나는 곳 치수선
    d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
    dc(doc, x4 , y4)    
    dc(doc, x6 , y6)
    # 하부 전체치수선
    d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
    
    # 오른쪽 15mm 표기
    d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
    # 오른쪽 최종 치수선
    d(doc, x11, y11 , x7, y7, 300, direction="right")
    dc(doc, x6, y6)
    dc(doc, x2, y2)    

    # 왼쪽 치수선 20mm 
    d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
    d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
    # 왼쪽 치수선 전체
    d(doc, x12, y12, x1, y1, 280, direction="left")
   

    #######################################  
    # P2,P8 단면도 (상부에 위치한)
    #######################################  

    x1 = x1 - panel_width + 6
    y1 = pagey + CH + 800
    x2 = x1 - panel_wing
    y2 = y1 
    x3 = x2
    y3 = y2 - panel_width
    x4 = x3 + P2_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - panel_width + thickness*2
    x10 = x9 - P2_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_width - thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    # B작업 표기
    if P2_width == P8_width and P4_width == P10_width :
        insert_block(x5 + 700 , y5,"b_work")

    x13 = x3
    y13 = y3 + P2_holegap
    x14 = x4
    y14 = y4 +P2_holegap
    
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 150, direction='up')   
    d(doc, x6, y6, x5, y5, 150, direction='up')   

    # 전체하부
    d(doc, x3, y3, x4, y4, 350, direction='down')              
    d(doc, x14+10, y14, x4, y4, 130, direction='right')    

    x13, y13 =  x1-10, y3 + P2_holegap
    line(doc, x3-10, y3+P2_holegap, x3+ 10, y3+P2_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y3+P2_holegap, x4+ 10, y3+P2_holegap , layer='CLphantom') # '구성선' 회색선
    # 좌측    
    d(doc, x13-10, y13, x3, y3, 100, direction='left')      
    d(doc, x2, y2, x3, y3, 180, direction='left')  

    d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
    rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
    # 하단 날개 23 표기 width 25 -2
    d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')   

    P2_hole = [P2_hole4, P2_hole3, P2_hole2, P2_hole1]     
    limit_point = [P2_width]
    tx = x3 
    ty = y3 + P2_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P2_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 280, direction="down" , option='reverse')                                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)        

    # 보강위치 단면도 표기
    rb_list = panel_rib(P2_width, P2_handrailxpos)        
    for index, g in enumerate(rb_list):      
        bp = x3 + g
        line(doc, bp, y3-10 , bp , y3+10, layer='0')                  
        if index == 0 :
            d(doc, bp, y3-10, x3, y3, 80, direction="down",option='reverse')
        else:
            dc(doc, bp,y3-10)
          
    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P2_handrailxpos):            
            if g is not None : 
                tx = x3 + g                
                d(doc, tx, y3, x3 , y3 - 10 , 130 + index*40, direction="down")                    
                line(doc, tx , y3 + 10 , tx , y3 - 10 , layer='CLphantom')            

    #######################################  
    # P2,P8 단면도 (우측)
    #######################################  
    top_panel_width = panel_width - 2
    x1 = pagex + P2_width*2 + 1000*2
    y1 = pagey + CH
    x2 = x1 
    y2 = y1 + panel_wing
    x3 = x2 - top_panel_width
    y3 = y2 
    x4 = x3 
    y4 = y3 - CPH
    x5 = x4 + top_panel_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_wing
    x7 = x6 - thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - panel_wing + thickness
    x9 = x8 - top_panel_width + thickness*2
    y9 = y8 
    x10 = x9 
    y10 = y9 + CPH - thickness*2
    x11 = x10 + top_panel_width - thickness*2
    y11 = y10 
    x12 = x11 
    y12 = y11 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3 + P2_holegap
    y13 = y3
    x14 = x4 + P2_holegap
    y14 = y4
    
    line(doc, x13, y13+10, x13, y13-10, layer="CL")
    line(doc, x14, y14+10, x14, y14-10, layer="CL")
    d(doc, x1, y1, x2, y2, 150, direction='right')
    d(doc, x3, y3, x13, y13+10, 80, direction='up')
    d(doc, x3, y3, x2, y2, 180, direction='up')
    d(doc, x14, y14-10, x4, y4, 100, direction='down')
    d(doc, x4, y4, x5, y5, 180, direction='down')

    d(doc, x3, y3, x4, y4, 100, direction='left')
    d(doc, x6, y6, x5, y5, 150, direction='right')

    ##################### 코멘트 ##########################
    mx = frameXpos + P2_width*2 + 3000
    my = frameYpos +2000     
    page_comment(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + P2_width*2 + 3500
    my = frameYpos +2000             
    desx = mx - 1300
    desy = my + 1000
    unitsu = 0
    if P2_width == P8_width :
        text = 'SIDE PANEL(#2,#8)'
        unitsu= 2
    else:
        text = 'SIDE PANEL(#2)'        
    if P4_width == P10_width :
        text += ', SIDE PANEL(#4,#10)'
        unitsu += 2

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material}{Spec}"
    draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')  
    frameXpos = frameXpos + TargetXscale + 400


############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

    # for i in range(2, 11):
    #     rib_list = panel_rib(i*100, P2_handrailxpos)
    #     print(f"P2 width : {i*100} , 패널의 종보강 위치: {rib_list}")         

    #########################################################################################
    # 6page P3, P9 같으면 하나만 표시
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 6851 
    TargetYscale = 4870 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    # print("page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "SIDE PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # P3 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
    ###################################################
    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx + panel_wing
    y1 = ry + CH + 500
    x2 = x1 - panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 + P3_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 + thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  + panel_width - thickness*2
    x10 = x9 - P3_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 - panel_width + thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   
    
    x13, y13 =  x1-10, y3-P3_holegap
    line(doc, x3-10, y3-P3_holegap, x3+ 10, y3-P3_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y4-P3_holegap, x4+ 10, y4-P3_holegap , layer='CLphantom') # '구성선' 회색선
    rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')

    # A작업 표기
    if P3_width == P9_width and P3_COPType != 'HOP 적용' and P9_COPType != 'HOP 적용' :
        insert_block(x4 + 230 , y4 + 320,"a_work")
    
    # 전면 벽 판넬 변수 목록 초기화
    P3_hole = [P3_hole1, P3_hole2, P3_hole3, P3_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P3_width]
    tx = x3 
    ty = y3 - P3_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P3_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)                   
       
    d(doc,  x3 , y3, x4, y4, 173, direction="up")
    d(doc,  x13 , y13, x3, y3, 140, direction="left")
    d(doc,  x5 , y5, x4, y4, 190, direction="right")

    d(doc,  x6, y6, x5 , y5,  80, direction="down")    
    d(doc,  x1 , y1, x2, y2, 80, direction="down")     

    # 모자보강 Y위치 저장 y3
    rib_posy = y3

    #############################################################
    # P3 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
    # P3 조립도 본체구성 표현
    #############################################################
        
    ry = pagey 

    rectangle(doc, rx, ry , rx+ P3_width, ry+CPH, layer='0')
    rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
    rectangle(doc, rx + P3_width , ry , rx+P3_width-panel_wing , ry+CPH , layer='0')

    # 세로 날개 표시 panel_wing
    line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
    line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
    line(doc, rx + P3_width - panel_wing, ry  ,rx + P3_width - panel_wing , ry + CPH, layer='0')
    line(doc, rx + P3_width - thickness, ry  ,rx + P3_width - thickness , ry + CPH, layer='22')

    # 상부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P3_width -  panel_wing - 4 ,ry+CPH , layer='0')
    line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P3_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
    # 하부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P3_width -  panel_wing - 4 ,ry,  layer='0')
    line(doc, rx + panel_wing + 4, ry+thickness , rx + P3_width -  panel_wing - 4 ,ry+thickness,  layer='22')


    # 중심선은 핸드레일 홀과 간섭이 없는지를 살펴야 한다. 그리고 새로 설정해야 한다.
    # line(doc, rx, ry + FH, rx+ P3_width, ry + FH, layer='magentaphantom')
    x1 = rx 
    y1 = ry 
    x2 = x1 + P3_width
    y2 = y1    
    x3 = x2 
    y3 = y2 + CPH
    x4 = x3 - P3_width
    y4 = y3 

    # 팝너트 표시하기    
    P3_hole = [P3_hole1, P3_hole2, P3_hole3, P3_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P3_width]
    tx = rx
    ty = ry+CPH    
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P3_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6_popnut")
                insert_block(tx + sum, ry,"M6_popnut_upset")
            if index == 0 :
                d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)         

    # 상부 전체치수
    d(doc,  rx , ry+CPH, rx + P3_width , ry+CPH, 120, direction="up")

    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P3_handrailxpos):            
            if g is not None : 
                tx = x2 - g
                insert_block(tx , y2 + handrail_height , "handrail_bracket")                
                d(doc, tx, y2 + handrail_height , x2 , y2 + handrail_height , 100 + index*100, direction="down")                    
                line(doc, tx , rib_posy + 10 , tx , rib_posy - panel_width - 10 , layer='CLphantom')  

    d(doc, x1, y1, tx , y2 + handrail_height , 150, direction="left")    

    yp_bottom = ry  + 1
    yp_upper = ry + CPH - 1

    rb_list = panel_rib(P3_width, P3_handrailxpos)    
    # print(f"P3 패널의 종보강 위치: {rb_list}")
    # print(f"P3 핸드레일 위치: {P3_handrailxpos}")
    for index, g in enumerate(rb_list):
        bp = rx + P3_width - g
        xlist = [bp , bp-40 ,bp-20 ,bp + 20 ,bp + 40 ]       
        # 모자보강
        rectangle(doc, xlist[2] , yp_bottom, xlist[3] , yp_upper, layer='0')
        rectangle(doc, xlist[1] , yp_bottom+panel_wing+1, xlist[4] , yp_upper-panel_wing-1, layer='구성선') # 구성선은 회색선    
        line(doc, xlist[0] , yp_bottom, xlist[0] , yp_upper, layer='CLphantom')  
        # 치수선
        # print (f"index = {index}, x : {bp}")        
        # print (f" len(rb_list) = { len(rb_list)}" )        
        if index == 0:
            d(doc, x3, y3,  bp , y4, 150, direction="down")     
        else:
            dc(doc, bp,y3)

        # 단면도에 모자보강 위치 표시하기
        line(doc, bp , rib_posy + 10 , bp , rib_posy - panel_width - 10 , layer='0')  
            
        # 5x10 장공 용접홀          
        insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
        insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")     
                

    if len(rb_list)-1 > 0 :  # 마지막인 경우
        dc(doc, x4,y4)            

    # 장공홀 표현하기 M6_nut
    gap = 0    
    length = CPH - 85 + popnut_height 
    hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
    leftx = x1 + 1.5
    rightx = x2 - 1.5
    ty = y2

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "M6_nut")
            insert_block(rightx, ty + g, "M6_nut")
        if index == 0 :
            d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x3, y3)    

    # 우측 전체 치수선
    d(doc, x2, y2, x3, y3, 220, direction="right" )  

    ###########################################################################
    # P3 전개도 그리기
    ###########################################################################

    rx = pagex + P3_width + 1200                         
    x1 = rx
    y1 = pagey
    x2 = x1 + P3_width - (panel_width+5)*2
    y2 = y1    
    x3 = x2
    y3 = y2 + panel_wing + 4 
    x4 = x3 + panel_wing + 4 
    y4 = y3 
    x5 = x4 
    y5 = y4 + 14.5 if br == 1.5 else y4 + 16
    x6 = x5 + 45 if br == 1.5 else x5 + 47
    y6 = y5 
    x7 = x6 
    y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
    x8 = x7 - 45 if br == 1.5 else x7 - 47 
    y8 = y7 
    x9 = x8 
    y9 = y8 + 14.5 if br == 1.5 else y8 + 16
    x10 = x9 - (panel_wing + 4)
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_wing + 4 
    x12 = x11 - P3_width + (panel_width+5)*2
    y12 = y11
    x13 = x12 
    y13 = y12 - (panel_wing + 4)
    x14 = x13 - (panel_wing + 4)
    y14 = y13
    x15 = x14 
    y15 = y14 - 14.5 if br == 1.5 else y14 - 16
    x16 = x15 - 45 if br == 1.5 else x15 - 47
    y16 = y15 
    x17 = x16 
    y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
    x18 = x17 + 45 if br == 1.5 else x17 + 47
    y18 = y17 
    x19 = x18
    y19 = y18 - (panel_wing + 4)
    x20 = x19 + (panel_wing + 4)
    y20 = y19 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 20
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                     
    gap = 0
    gap = - 1.5 if br == 1.5 else - 1
    length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
    hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
    leftx = x17 + (panel_width+panel_wing - P3_holegap - br * 2 )
    rightx = x6 - (panel_width+panel_wing - P3_holegap - br * 2 )
    ty = y6

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "8x16_vertical")
            insert_block(rightx, ty + g, "8x16_vertical")
        if index == 0 :
            d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x11, y11)    
    # 장공치수선 그리기    좌,우 떨어짐
    for index, g in enumerate(hole):
        if index == 4 :
            d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
            d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )        

    yp_bottom = y1
    yp_upper = y11

    rb_list = panel_rib(P3_width, P3_handrailxpos)    
    # print(f"P3 패널의 종보강 위치: {rb_list}")
    # print(f"P3 핸드레일 위치: {P3_handrailxpos}")
    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            text = "%%C3"
            dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="left")                    
            # 5mm 치수선표시
            d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
            d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

        circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
        circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
        if index == 0 :
            d(doc, x16, y16, bp, y11, 200, direction="down")
        else:
            dc(doc, bp,y11)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x7,y7)     

    if handrail_height > 0 :
        # 핸드레일 그리기       
        for index, g in enumerate(P3_handrailxpos):            
            if g is not None : 
                tx = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
                ty = y6 + handrail_height - 1  if br == 1 else y6 + handrail_height - 1.5 
                if len(P3_handrailxpos) == 1 :
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    d(doc, tx, ty , x6 , ty , 100  , direction="up")                    
                    d(doc, tx, ty , x17 , ty , 100  , direction="up")                    
                    d(doc, x2, y2, tx , ty , 280, direction="right")  
                    # 보강자리에서 간격 X 축 치수선
                    d(doc, bp, ty, tx , ty , 180, direction="down")  
                else:
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    if index == 0 :
                        d(doc, x16 , ty , tx, ty , 100  , direction="up") 
                    else:                         
                        dc(doc, tx , ty )
                        dc(doc, x6 , ty )
                        # 보강자리에서 간격 X 축 치수선
                        d(doc, x2, y2, tx , ty , 280, direction="right") 
                        d(doc, bp, ty, tx , ty , 180, direction="down")  
                  
     
    # 9파이 팝너트 연결홀 상부/하부
    P3_hole = [P3_hole1, P3_hole2, P3_hole3, P3_hole4]   

    limit_point = [P3_width]
    tx = x16 + 30 if br == 1.5 else x16 + 32
    upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
    lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point
    # 상부의 연결홀
    for index, hole in enumerate(P3_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
            if index == 0 :
                holeupperx = tx + sum                               
                holeuppery = upper_ty                       
                text = "%%C9 M6 POPNUT(머리5mm)"
                dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="left")                
                d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

            elif index == len(hole_variables) - 1 :
                dc(doc, x7, y7)                   
            else:
                dc(doc, tx + sum, upper_ty)                                   
    # 하부에 연결홀 타공
    sum = 0
    for index, hole in enumerate(P3_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
            if index == 0 :
                holelowerx = tx + sum                               
                holelowery = lower_ty                          
                d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

            elif index == len(hole_variables) - 1 :
                dc(doc, x6, y6)                   
            else:
                dc(doc, tx + sum, lower_ty)                                   
                
    # 상부치수선    
    d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
    dc(doc, x9 , y9)    
    dc(doc, x7, y7)
    # 상부 전체치수선
    d(doc, x16, y16, x7 ,y7, 250, direction="up")

    # 하부치수선    
    d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
    d(doc, x2, y2, x6 ,y6, 110, direction="down")        
    # 하부 2단 절곡 만나는 곳 치수선
    d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
    dc(doc, x4 , y4)    
    dc(doc, x6 , y6)
    # 하부 전체치수선
    d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
    
    # 오른쪽 15mm 표기
    d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
    # 오른쪽 최종 치수선
    d(doc, x11, y11 , x7, y7, 300, direction="right")
    dc(doc, x6, y6)
    dc(doc, x2, y2)    

    # 왼쪽 치수선 20mm 
    d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
    d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
    # 왼쪽 치수선 전체
    d(doc, x12, y12, x1, y1, 280, direction="left")
   

    #######################################  
    # P3 단면도 (상부에 위치한)
    #######################################  

    x1 = x1 - panel_width + 6
    y1 = pagey + CH + 800
    x2 = x1 - panel_wing
    y2 = y1 
    x3 = x2
    y3 = y2 - panel_width
    x4 = x3 + P3_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - panel_width + thickness*2
    x10 = x9 - P3_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_width - thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    # B작업 표기
    if P3_width == P8_width and P4_width == P10_width :
        insert_block(x5 + 700 , y5,"b_work")

    x13 = x3
    y13 = y3 + P3_holegap
    x14 = x4
    y14 = y4 + P3_holegap
    
    line(doc, x13-10, y13, x13+10, y13, layer="CL") 
    line(doc, x14-10, y14, x14+10, y14, layer="CL") 
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 150, direction='up')   
    d(doc, x6, y6, x5, y5, 150, direction='up')   
    # 좌측    
    d(doc, x13-10, y13, x3, y3, 100, direction='left')      
    d(doc, x2, y2, x3, y3, 180, direction='left')  

    # 전체하부
    d(doc, x3, y3, x4, y4, 350, direction='down')              
    d(doc, x14+10, y14, x4, y4, 130, direction='right')    

    x13, y13 =  x1-10, y3 + P3_holegap        
    rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
    # 하단 날개 23 표기 width 25 -2
    d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
    d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')  

    P3_hole = [P3_hole4, P3_hole3, P3_hole2, P3_hole1]     
    limit_point = [P3_width]
    tx = x3 
    ty = y3 + P3_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P3_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 280, direction="down" , option='reverse')                                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)        

    # 보강위치 단면도 표기
    rb_list = panel_rib(P3_width, P3_handrailxpos)        
    preX = x3
    for index, g in enumerate(rb_list):      
        bp = x3 + g
        line(doc, bp, y3-10 , bp , y3+10, layer='0')                  
        d(doc, preX, y3-10, bp, y3, 170, direction="down")
        preX = bp            
    dc(doc, x4,y4)   
          
    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P3_handrailxpos):            
            if g is not None : 
                tx = x3 + g                
                d(doc, tx, y3, x3 , y3 - 10 , 90 + index*40, direction="down")                    
                line(doc, tx , y3 + 10 , tx , y3 - 10 , layer='CLphantom')                    

    #######################################  
    # P3 단면도 (우측)
    #######################################  
    top_panel_width = panel_width - 2
    x1 = pagex + P3_width*2 + 1000*2
    y1 = pagey + CH
    x2 = x1 
    y2 = y1 + panel_wing
    x3 = x2 - top_panel_width
    y3 = y2 
    x4 = x3 
    y4 = y3 - CPH
    x5 = x4 + top_panel_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_wing
    x7 = x6 - thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - panel_wing + thickness
    x9 = x8 - top_panel_width + thickness*2
    y9 = y8 
    x10 = x9 
    y10 = y9 + CPH - thickness*2
    x11 = x10 + top_panel_width - thickness*2
    y11 = y10 
    x12 = x11 
    y12 = y11 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3 + P3_holegap
    y13 = y3
    x14 = x4 + P3_holegap
    y14 = y4
    
    line(doc, x13, y13+10, x13, y13-10, layer="CL")
    line(doc, x14, y14+10, x14, y14-10, layer="CL")
    d(doc, x1, y1, x2, y2, 150, direction='right')
    d(doc, x3, y3, x13, y13+10, 80, direction='up')
    d(doc, x3, y3, x2, y2, 180, direction='up')
    d(doc, x14, y14-10, x4, y4, 100, direction='down')
    d(doc, x4, y4, x5, y5, 180, direction='down')

    d(doc, x3, y3, x4, y4, 100, direction='left')
    d(doc, x6, y6, x5, y5, 150, direction='right')

    ##################### 코멘트 ##########################
    mx = frameXpos + P3_width*2 + 3000
    my = frameYpos +2000     
    page_comment(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + P3_width*2 + 4000
    my = frameYpos +2000             
    desx = mx - 1300
    desy = my + 1000
    unitsu = 0
    if P3_width == P9_width and P3_COPType != 'HOP 적용' and P9_COPType != 'HOP 적용' :
        text = 'SIDE PANEL(#3,#9)'
        unitsu= 2
    else:
        text = 'SIDE PANEL(#3)' 
        unitsu = 1

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')   
    
    frameXpos = frameXpos + TargetXscale + 400



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
       
    if P9_COPType == 'HOP 적용' or P3_COPType == 'HOP 적용' :
        #########################################################################################
        # 7page P9, P3 HOP 적용        
        #########################################################################################
        # 도면틀 넣기    
        BasicXscale = 6851
        BasicYscale = 4870
        TargetXscale = 6851 
        TargetYscale = 4870 + (CH-2500) 
        if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
            frame_scale = TargetXscale/BasicXscale
        else:
            frame_scale = TargetYscale/BasicYscale    

        # print("2page 스케일 비율 : " + str(frame_scale))           
        insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "SIDE PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

        pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

        ###################################################
        # P9 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
        ###################################################
        rx = math.floor(pagex)
        ry = math.floor(pagey)

        x1 = rx + panel_wing
        y1 = ry + CH + 500
        x2 = x1 - panel_wing 
        y2 = y1    
        x3 = x2 
        y3 = y2 + panel_width
        x4 = x3 + P9_width
        y4 = y3 
        x5 = x4 
        y5 = y4 - panel_width
        x6 = x5 - panel_wing
        y6 = y5 
        x7 = x6 
        y7 = y6 + thickness
        x8 = x7 + panel_wing - thickness
        y8 = y7 
        x9 = x8 
        y9 = y8  + panel_width - thickness*2
        x10 = x9 - P9_width + thickness*2
        y10 = y9 
        x11 = x10 
        y11 = y10 - panel_width + thickness*2
        x12 = x11 + panel_wing - thickness
        y12 = y11 

        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 12
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="0")   
        
        x13, y13 =  x1-10, y3-P9_holegap
        line(doc, x3-10, y3-P2_holegap, x3+ 10, y3-P2_holegap , layer='CLphantom') # '구성선' 회색선
        line(doc, x4-10, y4-P2_holegap, x4+ 10, y4-P2_holegap , layer='CLphantom') # '구성선' 회색선        
        rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')

        # A작업 표기
        if P3_width == P9_width and P3_COPType != 'HOP 적용' and P9_COPType != 'HOP 적용' :
            insert_block(x4 + 230 , y4 + 320,"a_work")
        
        P9_hole = [P9_hole1, P9_hole2, P9_hole3, P9_hole4]   
        
        limit_point = [P9_width]
        tx = x3 
        ty = y3 - P9_holegap
        sum = 0        
        for index, hole in enumerate(P9_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                    
                    insert_block(tx + sum, ty,"M6")
                if index == 0 :
                    d(doc,  x3 , y3, tx + sum, ty, 63, direction="up" , option='reverse')                    
                else:
                    dc(doc, tx + sum, ty)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, tx + sum, ty)                   
        
        d(doc,  x3 , y3, x4, y4, 173, direction="up")
        d(doc,  x13 , y13, x3, y3, 140, direction="left")
        d(doc,  x5 , y5, x4, y4, 190, direction="right")

        d(doc,  x6, y6, x5 , y5,  80, direction="down")    
        d(doc,  x1 , y1, x2, y2, 80, direction="down")     

        # 모자보강 Y위치 저장 y3
        rib_posy = y3

        #############################################################
        # P9 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
        # P9 조립도 본체구성 표현
        #############################################################            
        ry = pagey 

        rectangle(doc, rx, ry , rx+ P9_width, ry+CPH, layer='0')
        rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
        rectangle(doc, rx + P9_width , ry , rx+P9_width-panel_wing , ry+CPH , layer='0')

        # 세로 날개 표시 panel_wing
        line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
        line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
        line(doc, rx + P9_width - panel_wing, ry  ,rx + P9_width - panel_wing , ry + CPH, layer='0')
        line(doc, rx + P9_width - thickness, ry  ,rx + P9_width - thickness , ry + CPH, layer='22')

        # 상부 날개 표시
        rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P9_width -  panel_wing - 4 ,ry+CPH , layer='0')
        line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P9_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
        # 하부 날개 표시
        rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P9_width -  panel_wing - 4 ,ry,  layer='0')
        line(doc, rx + panel_wing + 4, ry+thickness , rx + P9_width -  panel_wing - 4 ,ry+thickness,  layer='22')

        x1 = rx 
        y1 = ry 
        x2 = x1 + P9_width
        y2 = y1    
        x3 = x2 
        y3 = y2 + CPH
        x4 = x3 - P9_width
        y4 = y3 

        # 팝너트 표시하기    
        P9_hole = [P9_hole1, P9_hole2, P9_hole3, P9_hole4]   

        # print (f"hole val : {hole_variables}")
        limit_point = [P9_width]
        tx = rx
        ty = ry+CPH    
        sum = 0
        # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
        for index, hole in enumerate(P9_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:
                    frontholes.append(hole)
                    insert_block(tx + sum, ty,"M6_popnut")
                    insert_block(tx + sum, ry,"M6_popnut_upset")
                if index == 0 :
                    d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
                else:
                    dc(doc, tx + sum, ty)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, tx + sum, ty)         

        # 상부 전체치수
        d(doc,  rx , ry+CPH, rx + P9_width , ry+CPH, 120, direction="up")

        if handrail_height > 0 :       
            # 핸드레일 그리기        
            for index, g in enumerate(P9_handrailxpos):            
                if g is not None : 
                    tx = x2 - g
                    insert_block(tx , y2 + handrail_height , "handrail_bracket")                
                    d(doc, tx, y2 + handrail_height , x2 , y2 + handrail_height , 100 + index*100, direction="down")                    
                    line(doc, tx , rib_posy + 10 , tx , rib_posy - panel_width - 10 , layer='CLphantom')  

        d(doc, x1, y1, tx , y2 + handrail_height , 150, direction="left")    

        yp_bottom = ry  + 1
        yp_upper = ry + CPH - 1

        rb_list = panel_rib_HOP(P9_width, P9_handrailxpos, HOP_width)
        # print(f"P9 새로운 함수 적용 HOP 종보강 위치: {rb_list}")                
        # 리스트를 역순으로 조립도는 역순이다. 
        rb_list_reversed = rb_list[::-1]
        # print(f"P9 rb_list_reversed 새로운 함수 적용 HOP 종보강 위치: {rb_list_reversed}")        
        for index, g in enumerate(rb_list_reversed):        
            bp = rx +  g
            if index == 0 :
                xlist = [bp , bp-10 ,bp+10 ,bp - 8 ,bp - 10, bp+15, bp+10 ]       
                # 25 HOP보강 5,10,8,2 = 25 좌우 개념이 있음
                rectangle(doc, xlist[1] , yp_bottom, xlist[2] , yp_upper, layer='0')
                rectangle(doc, xlist[5] , yp_bottom+panel_wing+1, xlist[6] , yp_upper-panel_wing-1, layer='0')
                line(doc, xlist[3] , yp_bottom, xlist[3] , yp_upper, layer='2')                
                line(doc, bp , yp_bottom, bp , yp_upper, layer='CLphantom')                  
                d(doc, x3, y3,  bp , y4, 150, direction="down")     
            elif index == 1 :
                xlist = [bp , bp+10 ,bp-10 ,bp - 8 ,bp - 10, bp+15, bp+10 ]       
                # 25 HOP보강 5,10,8,2 = 25 좌우 개념이 있음
                # HOP 상단
                HOP_box_upperY = ry + HOP_bottomHeight + HOP_height + 1
                HOP_box_lowerY = ry + HOP_bottomHeight - 1

                # box 보강 (상부, 하부 30x23 'ㄱ'자 보강)
                rectangle(doc, rx + P9_width/2 - HOP_width/2, HOP_box_upperY, rx + P9_width/2 + HOP_width/2, HOP_box_upperY + 30, layer='0')
                line(doc, rx + P9_width/2 - HOP_width/2, HOP_box_upperY + 1.6 , rx + P9_width/2 + HOP_width/2, HOP_box_upperY + 1.6, layer='구성선')
                rectangle(doc, rx + P9_width/2 - HOP_width/2, HOP_box_lowerY, rx + P9_width/2 + HOP_width/2, HOP_box_lowerY - 30, layer='0')
                line(doc, rx + P9_width/2 - HOP_width/2, HOP_box_lowerY - 1.6 , rx + P9_width/2 + HOP_width/2, HOP_box_lowerY - 1.6, layer='구성선')                
                
                rectangle(doc, xlist[1] , HOP_box_upperY, xlist[2] , yp_upper, layer='0')
                rectangle(doc, xlist[5] , HOP_box_upperY + 30, xlist[6] , yp_upper-panel_wing-1, layer='0')
                line(doc, xlist[3] , HOP_box_upperY, xlist[3] , yp_upper, layer='2')                
                line(doc, bp , yp_upper, bp , HOP_box_upperY, layer='CLphantom')                  
                # HOP 밑단
                rectangle(doc, xlist[1] , yp_bottom, xlist[2] , HOP_box_lowerY, layer='0')
                rectangle(doc, xlist[5] , yp_bottom+panel_wing+1, xlist[6] , HOP_box_lowerY-30, layer='0')
                line(doc, xlist[3] , yp_bottom, xlist[3] , HOP_box_lowerY, layer='2')                
                line(doc, bp , yp_bottom, bp , HOP_box_lowerY, layer='CLphantom')      
                dc(doc, bp,y3)                            
            else:
                xlist = [bp , bp+10 ,bp-10 ,bp+8 ,bp+10, bp-15, bp-10 ]       
                # 25 HOP보강 5,10,8,2 = 25 좌우 개념이 있음
                rectangle(doc, xlist[1] , yp_bottom, xlist[2] , yp_upper, layer='0')
                rectangle(doc, xlist[5] , yp_bottom+panel_wing+1, xlist[6] , yp_upper-panel_wing-1, layer='0')
                line(doc, xlist[3] , yp_bottom, xlist[3] , yp_upper, layer='2')                
                line(doc, bp , yp_bottom, bp , yp_upper, layer='CLphantom')                  
                dc(doc, bp,y3)

            # 단면도에 모자보강 위치 표시하기
            line(doc, bp , rib_posy + 10 , bp , rib_posy - panel_width - 10 , layer='0')  
                
            # 5x10 장공 용접홀          
            insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
            insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")                         

        if len(rb_list)-1 > 0 :  # 마지막인 경우
            dc(doc, x4,y4)          
    
        #################################
        # HOP 타공
        ##################################    
        tx1 = x1 + P9_width/2 - HOP_width/2
        ty1 = y1 + HOP_bottomHeight 
        tx2 = tx1 + HOP_width
        ty2 = ty1
        tx3 = tx2
        ty3 = ty2 + HOP_height
        tx4 = tx3 - HOP_width
        ty4 = ty3
        rectangle(doc, tx1 , ty1, tx3, ty3, layer="0" )
        tx5=(tx1+tx2)/2
        ty5=ty1
        tx6=(tx3+tx4)/2
        ty6=ty3
        line(doc, tx5-HOP_holegap/2, ty5-10,  tx5-HOP_holegap/2 , ty5+10,  layer='CLphantom')    
        line(doc, tx5+HOP_holegap/2, ty5-10,  tx5+HOP_holegap/2 , ty5+10,  layer='CLphantom')    
        line(doc, tx5-HOP_holegap/2, ty6-10,  tx5-HOP_holegap/2 , ty6+10,  layer='CLphantom')    
        line(doc, tx5+HOP_holegap/2, ty6-10,  tx5+HOP_holegap/2 , ty6+10,  layer='CLphantom')    

        d(doc, tx5-HOP_holegap/2, ty5-10, tx5+HOP_holegap/2 , ty5+10, 70, direction='up')
        d(doc, tx4, ty4, tx3, ty3, 100, direction='up')
        d(doc, tx4, ty4, tx1, ty1, 60, direction='left')
        dc(doc, tx4, y1)       

        # 장공홀 표현하기 M6_nut
        gap = 0    
        length = CPH - 85 + popnut_height 
        hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
        leftx = x1 + 1.5
        rightx = x2 - 1.5
        ty = y2

        for index, g in enumerate(hole):
            gap += g
            if g is not None : 
                insert_block(leftx, ty + g, "M6_nut")
                insert_block(rightx, ty + g, "M6_nut")
            if index == 0 :
                d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    
                # 슬롯등 지시선 추가
                text = "8x16"
                dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
            else:
                dc(doc, rightx, ty + g)    
        dc(doc, x3, y3)    

        # 우측 전체 치수선
        d(doc, x2, y2, x3, y3, 220, direction="right" )  

        ###########################################################################
        # P9 전개도 그리기
        ###########################################################################

        rx = pagex + P9_width + 1200                         
        x1 = rx
        y1 = pagey
        x2 = x1 + P9_width - (panel_width+5)*2
        y2 = y1    
        x3 = x2
        y3 = y2 + panel_wing + 4 
        x4 = x3 + panel_wing + 4 
        y4 = y3 
        x5 = x4 
        y5 = y4 + 14.5 if br == 1.5 else y4 + 16
        x6 = x5 + 45 if br == 1.5 else x5 + 47
        y6 = y5 
        x7 = x6 
        y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
        x8 = x7 - 45 if br == 1.5 else x7 - 47 
        y8 = y7 
        x9 = x8 
        y9 = y8 + 14.5 if br == 1.5 else y8 + 16
        x10 = x9 - (panel_wing + 4)
        y10 = y9 
        x11 = x10 
        y11 = y10 + panel_wing + 4 
        x12 = x11 - P9_width + (panel_width+5)*2
        y12 = y11
        x13 = x12 
        y13 = y12 - (panel_wing + 4)
        x14 = x13 - (panel_wing + 4)
        y14 = y13
        x15 = x14 
        y15 = y14 - 14.5 if br == 1.5 else y14 - 16
        x16 = x15 - 45 if br == 1.5 else x15 - 47
        y16 = y15 
        x17 = x16 
        y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
        x18 = x17 + 45 if br == 1.5 else x17 + 47
        y18 = y17 
        x19 = x18
        y19 = y18 - (panel_wing + 4)
        x20 = x19 + (panel_wing + 4)
        y20 = y19 

        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 20
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                        
        gap = 0
        gap = - 1.5 if br == 1.5 else - 1
        length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
        hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
        leftx = x17 + (panel_width+panel_wing - P9_holegap - br * 2 )
        rightx = x6 - (panel_width+panel_wing - P9_holegap - br * 2 )
        ty = y6

        for index, g in enumerate(hole):
            gap += g
            if g is not None : 
                insert_block(leftx, ty + g, "8x16_vertical")
                insert_block(rightx, ty + g, "8x16_vertical")
            if index == 0 :
                d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
                # 슬롯등 지시선 추가
                text = "8x16"
                dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
            else:
                dc(doc, rightx, ty + g)    
        dc(doc, x11, y11)    
        # 장공치수선 그리기    좌,우 떨어짐
        for index, g in enumerate(hole):
            if index == 4 :
                d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
                d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )            

        yp_bottom = y1
        yp_upper = y11

        rb_list = panel_rib_HOP(P9_width, P9_handrailxpos, HOP_width, option='reverse')
        # print(f"전개도  적용 HOP 종보강 위치: {rb_list}")             
        for index, g in enumerate(rb_list):         
            bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
            line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
            if index == 0 :
                text = "%%C3"
                dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="left")                    
                # 5mm 치수선표시
                d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
                d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

            circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
            circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

        for index, g in enumerate(rb_list):        
            bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
            if index == 0 :
                d(doc, x16, y16, bp, y11, 200, direction="down")
            else:
                dc(doc, bp,y11)

        if len(rb_list) > 0 :  # 마지막인 경우
            dc(doc, x7,y7)     

        if handrail_height > 0 :
            # 핸드레일 그리기       
            for index, g in enumerate(P9_handrailxpos):            
                if g is not None : 
                    tx = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
                    ty = y6 + handrail_height - 1  if br == 1 else y6 + handrail_height - 1.5 
                    if len(P9_handrailxpos) == 1 :
                        circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                        d(doc, tx, ty , x6 , ty , 150  , direction="down")                    
                        d(doc, tx, ty , x17 , ty , 150  , direction="down")                    
                        d(doc, x2, y2, tx , ty , 280, direction="right")                          
                    else:
                        circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                        if index == 0 :
                            d(doc, x16 , ty , tx, ty , 150  , direction="down") 
                        else:                         
                            dc(doc, tx , ty )
                            dc(doc, x6 , ty )
                            # 보강자리에서 간격 X 축 치수선
                            d(doc, x2, y2, tx , ty , 280, direction="right") 
                            d(doc, bp, ty, tx , ty , 350, direction="down")  
                            
        # 9파이 팝너트 연결홀 상부/하부
        P9_hole = [P9_hole1, P9_hole2, P9_hole3, P9_hole4]   

        limit_point = [P9_width]
        tx = x16 + 30 if br == 1.5 else x16 + 32
        upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
        lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
        sum = 0
        # 각 변수에 대해 값이 0보다 크고 limit_point
        # 상부의 연결홀
        for index, hole in enumerate(P9_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                
                    circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                    circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                if index == 0 :
                    holeupperx = tx + sum                               
                    holeuppery = upper_ty                       
                    text = "%%C9 M6 POPNUT(머리5mm)"
                    dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="left")                
                    d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

                elif index == len(hole_variables) - 1 :
                    dc(doc, x7, y7)                   
                else:
                    dc(doc, tx + sum, upper_ty)                                   
        # 하부에 연결홀 타공
        sum = 0
        for index, hole in enumerate(P9_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                
                    circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                    circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
                if index == 0 :
                    holelowerx = tx + sum                               
                    holelowery = lower_ty                          
                    d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

                elif index == len(hole_variables) - 1 :
                    dc(doc, x6, y6)                   
                else:
                    dc(doc, tx + sum, lower_ty)        

        #################################
        # HOP 타공 (전개도 laser layer)
        ##################################    
        tx1 = x16  
        tx1 = x17 + panel_wing + panel_width + P9_width/2 - HOP_width/2  - 4 if br == 1 else x17 + panel_wing + panel_width + P9_width/2 - HOP_width/2  - 6
        ty1 = y6 + HOP_bottomHeight if br == 1 else y6 + HOP_bottomHeight - 1.5
        tx2 = tx1 + HOP_width
        ty2 = ty1
        tx3 = tx2
        ty3 = ty2 + HOP_height
        tx4 = tx3 - HOP_width
        ty4 = ty3
        rectangle(doc, tx1 , ty1, tx3, ty3, layer="레이져" )
        tx5=(tx1+tx2)/2
        ty5=ty1
        tx6=(tx3+tx4)/2
        ty6=ty3        
        
        d(doc, tx4, ty4, tx3, ty3, 100, direction='up')
        d(doc, tx4, ty4, tx1, ty1, extract_abs(x16, tx1) + 120, direction='left')
        dc(doc, tx4, y1)       
                    
        # 상부치수선    
        d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
        dc(doc, x9 , y9)    
        dc(doc, x7, y7)
        # 상부 전체치수선
        d(doc, x16, y16, x7 ,y7, 250, direction="up")

        # 하부치수선    
        d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
        d(doc, x2, y2, x6 ,y6, 110, direction="down")        
        # 하부 2단 절곡 만나는 곳 치수선
        d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
        dc(doc, x4 , y4)    
        dc(doc, x6 , y6)
        # 하부 전체치수선
        d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
        
        # 오른쪽 15mm 표기
        d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
        # 오른쪽 최종 치수선
        d(doc, x11, y11 , x7, y7, 300, direction="right")
        dc(doc, x6, y6)
        dc(doc, x2, y2)    

        # 왼쪽 치수선 20mm 
        d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
        d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
        # 왼쪽 치수선 전체
        d(doc, x12, y12, x1, y1, 280, direction="left")
    

        #######################################  
        # P9 단면도 (상부에 위치한)
        #######################################  

        x1 = x1 - panel_width + 6
        y1 = pagey + CH + 800
        x2 = x1 - panel_wing
        y2 = y1 
        x3 = x2
        y3 = y2 - panel_width
        x4 = x3 + P9_width
        y4 = y3 
        x5 = x4 
        y5 = y4 + panel_width
        x6 = x5 - panel_wing
        y6 = y5 
        x7 = x6 
        y7 = y6 - thickness
        x8 = x7 + panel_wing - thickness
        y8 = y7 
        x9 = x8 
        y9 = y8 - panel_width + thickness*2
        x10 = x9 - P9_width + thickness*2
        y10 = y9 
        x11 = x10 
        y11 = y10 + panel_width - thickness*2
        x12 = x11 + panel_wing - thickness
        y12 = y11
        
        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 12
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="0")     

        # B작업 표기
        if P3_width == P9_width and P3_COPType != 'HOP 적용' and P9_COPType != 'HOP 적용' :
            insert_block(x5 + 700 , y5,"b_work")

        x13 = x3
        y13 = y3 + P9_holegap
        x14 = x4
        y14 = y4 + P9_holegap
        
        line(doc, x13-10, y13, x13+10, y13, layer="CL") 
        line(doc, x14-10, y14, x14+10, y14, layer="CL") 
        # 상부 치수선
        d(doc, x1, y1, x2, y2, 150, direction='up')   
        d(doc, x6, y6, x5, y5, 150, direction='up')   
        # 좌측    
        d(doc, x13-10, y13, x3, y3, 100, direction='left')      
        d(doc, x2, y2, x3, y3, 180, direction='left')  

        # 전체하부
        d(doc, x3, y3, x4, y4, 350, direction='down')              
        d(doc, x14+10, y14, x4, y4, 130, direction='right')    

        x13, y13 =  x1-10, y3 + P9_holegap        
        rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
        # 하단 날개 23 표기 width 25 -2
        d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
        d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')           

        P9_hole = [P9_hole4, P9_hole3, P9_hole2, P9_hole1]     
        limit_point = [P9_width]
        tx = x3
        ty = y3 + P9_holegap
        sum = 0
        # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
        for index, hole in enumerate(P9_hole):  
            if hole is not None and hole > 0:
                sum += hole
                if sum not in limit_point:                
                    insert_block(tx + sum, ty,"M6")
                if index == 0 :
                    d(doc,  x3 , y3, tx + sum, ty, 250, direction="down" , option='reverse')                                    
                else:
                    dc(doc, tx + sum, ty)                   
            else:
                if index == len(hole_variables) - 1 :
                    dc(doc, tx + sum, ty)        
   
    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P9_handrailxpos):            
            if g is not None : 
                tx = x3 + g                
                d(doc, tx, y3, x3 , y3 - 10 , 90 + index*40, direction="down")                    
                line(doc, tx , y3 + 10 , tx , y3 - 10 , layer='CLphantom')                 

    # 보강 3개 위치 표시
    yp_bottom = y3 - 10
    yp_upper = y3 + 10

    rb_list = panel_rib_HOP(P9_width, P9_handrailxpos, HOP_width, option='reverse')        
    for index, g in enumerate(rb_list):         
        bp = x3 + g
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            d(doc, x3,  y3 , bp , yp_bottom , 150, direction="down")               
        else:
            dc(doc, bp , yp_bottom)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x4,y4)                          

        #######################################  
        # P9 단면도 (우측)
        #######################################  
        top_panel_width = panel_width - 2
        x1 = pagex + P9_width*2 + 1000*2
        y1 = pagey + CH
        x2 = x1 
        y2 = y1 + panel_wing
        x3 = x2 - top_panel_width
        y3 = y2 
        x4 = x3 
        y4 = y3 - CPH
        x5 = x4 + top_panel_width
        y5 = y4 
        x6 = x5 
        y6 = y5 + panel_wing
        x7 = x6 - thickness
        y7 = y6 
        x8 = x7 
        y8 = y7 - panel_wing + thickness
        x9 = x8 - top_panel_width + thickness*2
        y9 = y8 
        x10 = x9 
        y10 = y9 + CPH - thickness*2
        x11 = x10 + top_panel_width - thickness*2
        y11 = y10 
        x12 = x11 
        y12 = y11 - panel_wing + thickness
        
        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 12
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="0")     

        x13 = x3 + P9_holegap
        y13 = y3
        x14 = x4 + P9_holegap
        y14 = y4
        
        line(doc, x13, y13+10, x13, y13-10, layer="CL")
        line(doc, x14, y14+10, x14, y14-10, layer="CL")
        d(doc, x1, y1, x2, y2, 150, direction='right')
        d(doc, x3, y3, x13, y13+10, 80, direction='up')
        d(doc, x3, y3, x2, y2, 180, direction='up')
        d(doc, x14, y14-10, x4, y4, 100, direction='down')
        d(doc, x4, y4, x5, y5, 180, direction='down')

        d(doc, x3, y3, x4, y4, 100, direction='left')
        d(doc, x6, y6, x5, y5, 150, direction='right')

        ##################### 코멘트 ##########################
        mx = frameXpos + P9_width*2 + 3000
        my = frameYpos +2000     
        page_comment(mx, my)
        
        ##################### part 설명  ##########################
        mx = frameXpos + P9_width*2 + 4000
        my = frameYpos +2000             
        desx = mx - 1300
        desy = my + 1000
        unitsu = 0
        if P9_width == P9_width and P9_COPType == '' and P9_COPType == '':
            text = 'SIDE PANEL(#3,#9)'
            unitsu= 2
        else:
            text = 'SIDE PANEL(#9)' 
            unitsu = 1

        textstr = f"Part Name : {text}"    
        draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
        textstr = f"Mat.Spec : {Material} {Spec}"
        draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
        textstr = f"Quantity : {unitsu} SET"    
        draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')   
        
        frameXpos = frameXpos + TargetXscale + 400



###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################








    #########################################################################################
    # 8page P5, P7 같으면 하나만 표시
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 6851 
    TargetYscale = 4870 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    # print("2page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "REAR PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # P5 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
    ###################################################
    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx + panel_wing
    y1 = ry + CH + 500
    x2 = x1 - panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 + P5_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 + thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  + panel_width - thickness*2
    x10 = x9 - P5_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 - panel_width + thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   
    
    x13, y13 =  x1-10, y3-P5_holegap    
    rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')
    line(doc, x3-10, y3-P5_holegap, x3+ 10, y3-P5_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y4-P5_holegap, x4+ 10, y4-P5_holegap , layer='CLphantom') # '구성선' 회색선    

    # A작업 표기
    if P5_width == P7_width :
        insert_block(x4 + 230 , y4 + 320,"a_work")
    
    # 전면 벽 판넬 변수 목록 초기화
    P5_hole = [P5_hole1, P5_hole2, P5_hole3, P5_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P5_width]
    tx = x3 
    ty = y3 - P5_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P5_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 170, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)               

    d(doc,  x3 , y3, x4, y4, 250, direction="up")
    d(doc,  x13 , y13, x3, y3, 140, direction="left")
    d(doc,  x5 , y5, x4, y4, 190, direction="right")
    d(doc,  x6, y6, x5 , y5,  80, direction="down")    
    d(doc,  x1 , y1, x2, y2, 80, direction="down")     

    # P5, P7은 side panel과 결합하니, 홀의 결합위치가 다르다. 주의)
    line(doc, x4 - (panel_width-P5_holegap) , y4 + 10 , x4 - (panel_width-P5_holegap) , y4 - 10 , layer='CLphantom')  
    d(doc, x4 , y4 , x4 - (panel_width-P5_holegap) , y4 + 10 , 50, direction="up")

    if handrail_height > 0 :       
        # 핸드레일 위치 표시 및 치수선
        for index, g in enumerate(P5_handrailxpos):            
            if g is not None : 
                tx = x4 - g                
                d(doc, x4, y4 , tx , y4 + 10 , 100 , direction="up")                                    

    # 모자보강 Y위치 저장 y3
    rib_posy = y3

    #############################################################
    # P5 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
    # P5 조립도 본체구성 표현
    #############################################################
            
    ry = pagey 

    rectangle(doc, rx, ry , rx+ P5_width, ry+CPH, layer='0')
    rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
    rectangle(doc, rx + P5_width , ry , rx+P5_width-panel_wing , ry+CPH , layer='0')

    # 세로 날개 표시 panel_wing
    line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
    line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
    line(doc, rx + P5_width - panel_wing, ry  ,rx + P5_width - panel_wing , ry + CPH, layer='0')
    line(doc, rx + P5_width - thickness, ry  ,rx + P5_width - thickness , ry + CPH, layer='22')

    # 상부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P5_width -  panel_wing - 4 ,ry+CPH , layer='0')
    line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P5_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
    # 하부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P5_width -  panel_wing - 4 ,ry,  layer='0')
    line(doc, rx + panel_wing + 4, ry+thickness , rx + P5_width -  panel_wing - 4 ,ry+thickness,  layer='22')

    x1 = rx 
    y1 = ry 
    x2 = x1 + P5_width
    y2 = y1    
    x3 = x2 
    y3 = y2 + CPH
    x4 = x3 - P5_width
    y4 = y3 

    # 팝너트 표시하기    
    P5_hole = [P5_hole1, P5_hole2, P5_hole3, P5_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P5_width]
    tx = rx
    ty = ry+CPH    
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P5_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6_popnut")
                insert_block(tx + sum, ry,"M6_popnut_upset")
            if index == 0 :
                d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)         

    # 상부 전체치수
    d(doc,  rx , ry+CPH, rx + P5_width , ry+CPH, 120, direction="up")

    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P5_handrailxpos):            
            if g is not None : 
                tx = x2 - g
                insert_block(tx , y2 + handrail_height , "handrail_bracket")                
                d(doc, tx, y2 + handrail_height , x2 , y2 + handrail_height , 100 + index*100, direction="down")                    
                line(doc, tx , rib_posy + 10 , tx , rib_posy - panel_width - 10 , layer='CLphantom')  

    d(doc, x1, y1, tx , y2 + handrail_height , 150, direction="left")    

    yp_bottom = ry  + 1
    yp_upper = ry + CPH - 1

    rb_list = panel_rib(P5_width, P5_handrailxpos)    
    # print(f"P5 패널의 종보강 위치: {rb_list}")
    # print(f"P5 핸드레일 위치: {P5_handrailxpos}")
    for index, g in enumerate(rb_list):
        bp = rx + P5_width - g
        xlist = [bp , bp-40 ,bp-20 ,bp + 20 ,bp + 40 ]       
        # 모자보강
        rectangle(doc, xlist[2] , yp_bottom, xlist[3] , yp_upper, layer='0')
        rectangle(doc, xlist[1] , yp_bottom+panel_wing+1, xlist[4] , yp_upper-panel_wing-1, layer='구성선') # 구성선은 회색선    
        line(doc, xlist[0] , yp_bottom, xlist[0] , yp_upper, layer='CLphantom')  
        # 치수선
        # print (f"index = {index}, x : {bp}")        
        # print (f" len(rb_list) = { len(rb_list)}" )        
        if index == 0:
            d(doc, x3, y3,  bp , y4, 150, direction="down")     
        else:
            dc(doc, bp,y3)

        # 단면도에 모자보강 위치 표시하기
        line(doc, bp , rib_posy + 10 , bp , rib_posy - panel_width - 10 , layer='0')  
            
        # 5x10 장공 용접홀          
        insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
        insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")                     

    if len(rb_list)-1 > 0 :  # 마지막인 경우
        dc(doc, x4,y4)            

    # 장공홀 표현하기 M6_nut
    gap = 0    
    length = CPH - 85 + popnut_height 
    hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
    leftx = x1 + 1.5
    rightx = x2 - (panel_width - P5_holegap)
    ty = y2

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "M6_nut")
            # insert_block(rightx, ty + g, "M6_nut")
            circle_cross(doc, rightx, ty + g , 9, layer='0')    # P4와 연결되는 홀 기둥

        if index == 0 :
            d(doc, x2, ty + g, rightx, ty + g,  150, direction="up" )    
            d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    

            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x3, y3)    

    # 우측 전체 치수선
    d(doc, x2, y2, x3, y3, 220, direction="right" )  

    ###########################################################################
    # P5 전개도 그리기
    ###########################################################################

    rx = pagex + P5_width + 1200                         
    x1 = rx
    y1 = pagey
    x2 = x1 + P5_width - (panel_width+5)*2
    y2 = y1    
    x3 = x2
    y3 = y2 + panel_wing + 4 
    x4 = x3 + panel_wing + 4 
    y4 = y3 
    x5 = x4 
    y5 = y4 + 14.5 if br == 1.5 else y4 + 16
    x6 = x5 + 45 if br == 1.5 else x5 + 47
    y6 = y5 
    x7 = x6 
    y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
    x8 = x7 - 45 if br == 1.5 else x7 - 47 
    y8 = y7 
    x9 = x8 
    y9 = y8 + 14.5 if br == 1.5 else y8 + 16
    x10 = x9 - (panel_wing + 4)
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_wing + 4 
    x12 = x11 - P5_width + (panel_width+5)*2
    y12 = y11
    x13 = x12 
    y13 = y12 - (panel_wing + 4)
    x14 = x13 - (panel_wing + 4)
    y14 = y13
    x15 = x14 
    y15 = y14 - 14.5 if br == 1.5 else y14 - 16
    x16 = x15 - 45 if br == 1.5 else x15 - 47
    y16 = y15 
    x17 = x16 
    y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
    x18 = x17 + 45 if br == 1.5 else x17 + 47
    y18 = y17 
    x19 = x18
    y19 = y18 - (panel_wing + 4)
    x20 = x19 + (panel_wing + 4)
    y20 = y19 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 20
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                     
    gap = 0
    gap = - 1.5 if br == 1.5 else - 1
    length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
    hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
    leftx = x17 + (panel_width*2 + panel_wing - P5_holegap - br * 4 )
    rightx = x6 - (panel_width+panel_wing - P5_holegap - br * 2 )
    ty = y6

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "8x16_vertical")
            insert_block(rightx, ty + g, "8x16_vertical")
        if index == 0 :
            d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x11, y11)    
    # 장공치수선 그리기    좌,우 떨어짐
    for index, g in enumerate(hole):
        if index == 5 :
            d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
            d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )                        
        
    yp_bottom = y1
    yp_upper = y11

    rb_list = panel_rib(P5_width, P5_handrailxpos)    
    # print(f"P5 패널의 종보강 위치: {rb_list}")
    # print(f"P5 핸드레일 위치: {P5_handrailxpos}")
    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            text = "%%C3"
            dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="left")                    
            # 5mm 치수선표시
            d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
            d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

        circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
        circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
        if index == 0 :
            d(doc, x16, y16, bp, y11, 200, direction="down")
        else:
            dc(doc, bp,y11)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x7,y7)     

    if handrail_height > 0 :
        # 핸드레일 그리기       
        for index, g in enumerate(P5_handrailxpos):            
            if g is not None : 
                tx = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
                ty = y6 + handrail_height - 1  if br == 1 else y6 + handrail_height - 1.5 
                if len(P5_handrailxpos) == 1 :
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    d(doc, tx, ty , x6 , ty , 100  , direction="up")                    
                    d(doc, tx, ty , x17 , ty , 100  , direction="up")                    
                    d(doc, x2, y2, tx , ty , 280, direction="right")  
                    # 보강자리에서 간격 X 축 치수선
                    d(doc, bp, ty, tx , ty , 180, direction="down")  
                else:
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    if index == 0 :
                        d(doc, x16 , ty , tx, ty , 100  , direction="up") 
                    else:                         
                        dc(doc, tx , ty )
                        dc(doc, x6 , ty )
                        # 보강자리에서 간격 X 축 치수선
                        d(doc, x2, y2, tx , ty , 280, direction="right") 
                        d(doc, bp, ty, tx , ty , 180, direction="down")  
                       
    # 9파이 팝너트 연결홀 상부/하부
    P5_hole = [P5_hole1, P5_hole2, P5_hole3, P5_hole4]   

    limit_point = [P5_width]
    tx = x16 + 30 if br == 1.5 else x16 + 32
    upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
    lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point
    # 상부의 연결홀
    for index, hole in enumerate(P5_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
            if index == 0 :
                holeupperx = tx + sum                               
                holeuppery = upper_ty                       
                text = "%%C9 M6 POPNUT(머리5mm)"
                dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="left")                
                d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

            elif index == len(hole_variables) - 1 :
                dc(doc, x7, y7)                   
            else:
                dc(doc, tx + sum, upper_ty)                                   
    # 하부에 연결홀 타공
    sum = 0
    for index, hole in enumerate(P5_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
            if index == 0 :
                holelowerx = tx + sum                               
                holelowery = lower_ty                          
                d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

            elif index == len(hole_variables) - 1 :
                dc(doc, x6, y6)                   
            else:
                dc(doc, tx + sum, lower_ty)
                
    # 상부치수선    
    d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
    dc(doc, x9 , y9)    
    dc(doc, x7, y7)
    # 상부 전체치수선
    d(doc, x16, y16, x7 ,y7, 250, direction="up")

    # 하부치수선    
    d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
    d(doc, x2, y2, x6 ,y6, 110, direction="down")        
    # 하부 2단 절곡 만나는 곳 치수선
    d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
    dc(doc, x4 , y4)    
    dc(doc, x6 , y6)
    # 하부 전체치수선
    d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
    
    # 오른쪽 15mm 표기
    d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
    # 오른쪽 최종 치수선
    d(doc, x11, y11 , x7, y7, 300, direction="right")
    dc(doc, x6, y6)
    dc(doc, x2, y2)    

    # 왼쪽 치수선 20mm 
    d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
    d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
    # 왼쪽 치수선 전체
    d(doc, x12, y12, x1, y1, 280, direction="left")

    # 모자보강 Y위치 저장 y3
    rib_posy = y3    

    #######################################  
    # P5,P7 단면도 (상부에 위치한)
    #######################################  
    x1 = x1 - panel_width + 6
    y1 = pagey + CH + 794
    x2 = x1 - panel_wing
    y2 = y1 
    x3 = x2
    y3 = y2 - panel_width
    x4 = x3 + P5_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - panel_width + thickness*2
    x10 = x9 - P5_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_width - thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    # B작업 표기
    if P5_width == P7_width :
        insert_block(x5 + 700 , y5,"b_work")

    x13 = x3
    y13 = y3 + P5_holegap
    x14 = x4
    y14 = y4 + P5_holegap
    
    line(doc, x13-10, y13, x13+10, y13, layer="CL") 
    line(doc, x14-10, y14, x14+10, y14, layer="CL") 
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 150, direction='up')   
    d(doc, x6, y6, x5, y5, 150, direction='up')   
    # 좌측    
    d(doc, x13-10, y13, x3, y3, 100, direction='left')      
    d(doc, x2, y2, x3, y3, 180, direction='left')  

    # 전체하부
    d(doc, x3, y3, x4, y4, 350, direction='down')              
    d(doc, x14+10, y14, x4, y4, 130, direction='right')    

    x13, y13 =  x1-10, y3 + P5_holegap    
    d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
    d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')   
    rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
    # 하단 날개 23 표기 width 25 -2
    
    P5_hole = [P5_hole4, P5_hole3, P5_hole2, P5_hole1]     
    limit_point = [P5_width]
    tx = x3 
    ty = y3 + P5_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P5_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 270, direction="down" , option='reverse')                                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)        

    # 본판과 역순으로 정렬
    # reverse_P5_handrailxpos = P5_handrailxpos[::-1]
    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P5_handrailxpos):            
            if g is not None : 
                tx = x3 + g                
                d(doc, tx, y3, x3 , y3 - 10 , 130 + index*40, direction="down")                    
                line(doc, tx , y3 + 10 , tx , y3 - 10 , layer='CLphantom')  

    # 보강자리 표시
    rb_list = panel_rib(P5_width, P5_handrailxpos)    
    for index, g in enumerate(rb_list):        
        bp = x3 + g
        line(doc, bp, y3-10 , bp , y3+10, layer='0')                  
        if index == 0 :
            d(doc, bp, y3-10, x3, y3, 80, direction="down",option='reverse')
        else:
            dc(doc, bp,y3-10)

    # P5, P7은 side panel과 결합하니, 홀의 결합위치가 다르다. 주의)
    line(doc, x3 + (panel_width-P5_holegap) , y4 + 10 ,x3 + (panel_width-P5_holegap) , y4 - 10 , layer='CLphantom')  
    d(doc,  x3 + (panel_width-P5_holegap) , y3 - 10 , x3 , y3 , 50, direction="down")

    #######################################  
    # P5,P7 단면도 (우측, 상부위치 아님)
    #######################################  
    top_panel_width = panel_width - 2
    x1 = pagex + P5_width*2 + 1000*2
    y1 = pagey + CH
    x2 = x1 
    y2 = y1 + panel_wing
    x3 = x2 - top_panel_width
    y3 = y2 
    x4 = x3 
    y4 = y3 - CPH
    x5 = x4 + top_panel_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_wing
    x7 = x6 - thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - panel_wing + thickness
    x9 = x8 - top_panel_width + thickness*2
    y9 = y8 
    x10 = x9 
    y10 = y9 + CPH - thickness*2
    x11 = x10 + top_panel_width - thickness*2
    y11 = y10 
    x12 = x11 
    y12 = y11 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3 + P5_holegap
    y13 = y3
    x14 = x4 + P5_holegap
    y14 = y4
    
    line(doc, x13, y13+10, x13, y13-10, layer="CL")
    line(doc, x14, y14+10, x14, y14-10, layer="CL")
    d(doc, x1, y1, x2, y2, 150, direction='right')
    d(doc, x3, y3, x13, y13+10, 80, direction='up')
    d(doc, x3, y3, x2, y2, 180, direction='up')
    d(doc, x14, y14-10, x4, y4, 100, direction='down')
    d(doc, x4, y4, x5, y5, 180, direction='down')

    d(doc, x3, y3, x4, y4, 100, direction='left')
    d(doc, x6, y6, x5, y5, 150, direction='right')

    ##################### 코멘트 ##########################
    mx = frameXpos + P5_width*2 + 3000
    my = frameYpos +2000     
    page_comment(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + P5_width*2 + 3500
    my = frameYpos +2000             
    desx = mx - 1300
    desy = my + 1000
    unitsu = 1
    if P5_width == P7_width :
        text = 'REAR PANEL(#5,#7)'
        unitsu= 2
    else:
        text = 'REAR PANEL(#5)'        

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')  
    frameXpos = frameXpos + TargetXscale + 400


############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################


    #########################################################################################
    # 9page P6 
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 6851 
    TargetYscale = 4870 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
        
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "REAR PANEL ASY", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # P6 분리형 조립도 (도면의 상부에 위치한 단면도) 평면도
    ###################################################
    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx + panel_wing
    y1 = ry + CH + 500
    x2 = x1 - panel_wing 
    y2 = y1    
    x3 = x2 
    y3 = y2 + panel_width
    x4 = x3 + P6_width
    y4 = y3 
    x5 = x4 
    y5 = y4 - panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 + thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8  + panel_width - thickness*2
    x10 = x9 - P6_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 - panel_width + thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   
    
    x13, y13 =  x1-10, y3-P6_holegap
    line(doc, x3-10, y3-P6_holegap, x3+ 10, y3-P6_holegap , layer='CLphantom') # '구성선' 회색선
    line(doc, x4-10, y4-P6_holegap, x4+ 10, y4-P6_holegap , layer='CLphantom') # '구성선' 회색선
    rectangle(doc, x1+4, y3-thickness , x6 - 4, y6+2, layer='구성선')
    
    # 전면 벽 판넬 변수 목록 초기화
    P6_hole = [P6_hole1, P6_hole2, P6_hole3, P6_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P6_width]
    tx = x3 
    ty = y3 - P6_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P6_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)                   
       
    d(doc,  x3 , y3, x4, y4, 173, direction="up")
    d(doc,  x13 , y13, x3, y3, 140, direction="left")
    d(doc,  x5 , y5, x4, y4, 190, direction="right")

    d(doc,  x6, y6, x5 , y5,  80, direction="down")    
    d(doc,  x1 , y1, x2, y2, 80, direction="down")     

    # 모자보강 Y위치 저장 y3
    rib_posy = y3

    #############################################################
    # P6 분리형태 조립도 본체 만들기 (보강, 홀위치, 핸드레일 등 표시)
    # P6 조립도 본체구성 표현
    #############################################################
        
    ry = pagey 

    rectangle(doc, rx, ry , rx+ P6_width, ry+CPH, layer='0')
    rectangle(doc, rx+panel_wing , ry , rx+panel_wing , ry+CPH, layer='0')
    rectangle(doc, rx + P6_width , ry , rx+P6_width-panel_wing , ry+CPH , layer='0')

    # 세로 날개 표시 panel_wing
    line(doc, rx + panel_wing, ry  , rx + panel_wing , ry + CPH, layer='0')
    line(doc, rx + thickness, ry  , rx + thickness , ry + CPH, layer='22')
    line(doc, rx + P6_width - panel_wing, ry  ,rx + P6_width - panel_wing , ry + CPH, layer='0')
    line(doc, rx + P6_width - thickness, ry  ,rx + P6_width - thickness , ry + CPH, layer='22')

    # 상부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+CPH-panel_wing  , rx + P6_width -  panel_wing - 4 ,ry+CPH , layer='0')
    line(doc, rx + panel_wing + 4, ry+CPH- thickness , rx + P6_width -  panel_wing - 4 ,ry+CPH-thickness,  layer='22')
    # 하부 날개 표시
    rectangle(doc, rx + panel_wing + 4, ry+panel_wing  , rx + P6_width -  panel_wing - 4 ,ry,  layer='0')
    line(doc, rx + panel_wing + 4, ry+thickness , rx + P6_width -  panel_wing - 4 ,ry+thickness,  layer='22')


    # 중심선은 핸드레일 홀과 간섭이 없는지를 살펴야 한다. 그리고 새로 설정해야 한다.
    # line(doc, rx, ry + FH, rx+ P6_width, ry + FH, layer='magentaphantom')

    x1 = rx 
    y1 = ry 
    x2 = x1 + P6_width
    y2 = y1    
    x3 = x2 
    y3 = y2 + CPH
    x4 = x3 - P6_width
    y4 = y3 

    # 팝너트 표시하기    
    P6_hole = [P6_hole1, P6_hole2, P6_hole3, P6_hole4]   

    # print (f"hole val : {hole_variables}")
    limit_point = [P6_width]
    tx = rx
    ty = ry+CPH    
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P6_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:
                frontholes.append(hole)
                insert_block(tx + sum, ty,"M6_popnut")
                insert_block(tx + sum, ry,"M6_popnut_upset")
            if index == 0 :
                d(doc,  x4 , y4, tx + sum, ty, 63, direction="up" , option='reverse')                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)         

    # 상부 전체치수
    d(doc,  rx , ry+CPH, rx + P6_width , ry+CPH, 120, direction="up")

    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P6_handrailxpos):            
            if g is not None : 
                tx = x2 - g
                insert_block(tx , y2 + handrail_height , "handrail_bracket")                
                d(doc, tx, y2 + handrail_height , x2 , y2 + handrail_height , 100 + index*100, direction="down")                    
                line(doc, tx , rib_posy + 10 , tx , rib_posy - panel_width - 10 , layer='CLphantom')  

    d(doc, x1, y1, tx , y2 + handrail_height , 150, direction="left")    

    yp_bottom = ry  + 1
    yp_upper = ry + CPH - 1

    rb_list = panel_rib(P6_width, P6_handrailxpos)    
    # print(f"P6 패널의 종보강 위치: {rb_list}")
    # print(f"P6 핸드레일 위치: {P6_handrailxpos}")
    for index, g in enumerate(rb_list):
        bp = rx + P6_width - g
        xlist = [bp , bp-40 ,bp-20 ,bp + 20 ,bp + 40 ]       
        # 모자보강
        rectangle(doc, xlist[2] , yp_bottom, xlist[3] , yp_upper, layer='0')
        rectangle(doc, xlist[1] , yp_bottom+panel_wing+1, xlist[4] , yp_upper-panel_wing-1, layer='구성선') # 구성선은 회색선    
        line(doc, xlist[0] , yp_bottom, xlist[0] , yp_upper, layer='CLphantom')  
        # 치수선
        # print (f"index = {index}, x : {bp}")        
        # print (f" len(rb_list) = { len(rb_list)}" )        
        if index == 0:
            d(doc, x3, y3,  bp , y4, 150, direction="down")     
        else:
            dc(doc, bp,y3)

        # 단면도에 모자보강 위치 표시하기
        line(doc, bp , rib_posy + 10 , bp , rib_posy - panel_width - 10 , layer='0')  
            
        # 5x10 장공 용접홀          
        insert_block(bp, yp_upper - 6 , "5x10_vertical_draw")            
        insert_block(bp, yp_bottom + 6 ,"5x10_vertical_draw")     
                

    if len(rb_list)-1 > 0 :  # 마지막인 경우
        dc(doc, x4,y4)            

    # 장공홀 표현하기 M6_nut
    gap = 0    
    length = CPH - 85 + popnut_height 
    hole = calculate_splitholeArray(135, 400, CPH , length ) #length는 상단 마지막홀 계산 분리형
    leftx = x1 + 1.5
    rightx = x2 - 1.5
    ty = y2

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "M6_nut")
            insert_block(rightx, ty + g, "M6_nut")
        if index == 0 :
            d(doc, x2, y2, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x3, y3)    

    # 우측 전체 치수선
    d(doc, x2, y2, x3, y3, 220, direction="right" )  

    ###########################################################################
    # P6 전개도 그리기
    ###########################################################################

    rx = pagex + P6_width + 1200                         
    x1 = rx
    y1 = pagey
    x2 = x1 + P6_width - (panel_width+5)*2
    y2 = y1    
    x3 = x2
    y3 = y2 + panel_wing + 4 
    x4 = x3 + panel_wing + 4 
    y4 = y3 
    x5 = x4 
    y5 = y4 + 14.5 if br == 1.5 else y4 + 16
    x6 = x5 + 45 if br == 1.5 else x5 + 47
    y6 = y5 
    x7 = x6 
    y7 = y6 + CPH - 3 if br == 1.5 else y6 + CPH - 2
    x8 = x7 - 45 if br == 1.5 else x7 - 47 
    y8 = y7 
    x9 = x8 
    y9 = y8 + 14.5 if br == 1.5 else y8 + 16
    x10 = x9 - (panel_wing + 4)
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_wing + 4 
    x12 = x11 - P6_width + (panel_width+5)*2
    y12 = y11
    x13 = x12 
    y13 = y12 - (panel_wing + 4)
    x14 = x13 - (panel_wing + 4)
    y14 = y13
    x15 = x14 
    y15 = y14 - 14.5 if br == 1.5 else y14 - 16
    x16 = x15 - 45 if br == 1.5 else x15 - 47
    y16 = y15 
    x17 = x16 
    y17 = y16 - CPH + 3 if br == 1.5 else y16 - CPH + 2
    x18 = x17 + 45 if br == 1.5 else x17 + 47
    y18 = y17 
    x19 = x18
    y19 = y18 - (panel_wing + 4)
    x20 = x19 + (panel_wing + 4)
    y20 = y19 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 20
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
                     
    gap = 0
    gap = - 1.5 if br == 1.5 else - 1
    length = CPH - 85 + popnut_height + 1.5 if br == 1.5 else CPH - 85 + popnut_height + 1
    hole = calculate_splitholeArray(135 + gap, 400, CPH , length+gap*2 ) #length는 상단 마지막홀 계산 분리형
    leftx = x17 + (panel_width+panel_wing - P6_holegap - br * 2 )
    rightx = x6 - (panel_width+panel_wing - P6_holegap - br * 2 )
    ty = y6

    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(leftx, ty + g, "8x16_vertical")
            insert_block(rightx, ty + g, "8x16_vertical")
        if index == 0 :
            d(doc, x6, y6, rightx, ty + g, 120, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  rightx, ty + g, rightx-100, ty + g + 100,   text, direction="left")
        else:
            dc(doc, rightx, ty + g)    
    dc(doc, x11, y11)    
    # 장공치수선 그리기    좌,우 떨어짐
    for index, g in enumerate(hole):
        if index == 4 :
            d(doc, x17, ty + g, leftx, ty + g, 100, direction="down" )                        
            d(doc, rightx, ty + g, x6, ty + g, 100, direction="down" )        

    yp_bottom = y1
    yp_upper = y11

    rb_list = panel_rib(P6_width, P6_handrailxpos)    
    # print(f"P6 패널의 종보강 위치: {rb_list}")
    # print(f"P6 핸드레일 위치: {P6_handrailxpos}")
    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
        line(doc, bp , yp_bottom , bp , yp_upper, layer='CLphantom')                  
        if index == 0 :
            text = "%%C3"
            dim_leader(doc, bp , yp_bottom + 5, bp + 50 , yp_bottom + 100 , text, direction="left")                    
            # 5mm 치수선표시
            d(doc, bp, y12 - 5 , bp , y12  , 20, direction="left")  
            d(doc, bp, y1 + 5 , bp , y1 , 20, direction="left")               

        circle_cross(doc, bp , yp_upper - 5 , 5, layer='레이져')                 
        circle_cross(doc, bp , yp_bottom + 5 , 5, layer='레이져')    

    for index, g in enumerate(rb_list):        
        bp = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6         
        if index == 0 :
            d(doc, x16, y16, bp, y11, 200, direction="down")
        else:
            dc(doc, bp,y11)

    if len(rb_list) > 0 :  # 마지막인 경우
        dc(doc, x7,y7)     

    if handrail_height > 0 :
        # 핸드레일 그리기       
        for index, g in enumerate(P6_handrailxpos):            
            if g is not None : 
                tx = x17 + g + panel_wing + panel_width - 4 if br == 1 else x17 + g + panel_wing + panel_width - 6 
                ty = y6 + handrail_height - 1  if br == 1 else y6 + handrail_height - 1.5 
                if len(P6_handrailxpos) == 1 :
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    d(doc, tx, ty , x6 , ty , 100  , direction="up")                    
                    d(doc, tx, ty , x17 , ty , 100  , direction="up")                    
                    d(doc, x2, y2, tx , ty , 280, direction="right")  
                    # 보강자리에서 간격 X 축 치수선
                    d(doc, bp, ty, tx , ty , 180, direction="down")  
                else:
                    circle_cross(doc, tx , ty, HRRearHolesize, layer='레이져')
                    if index == 0 :
                        d(doc, x16 , ty , tx, ty , 100  , direction="up") 
                    else:                         
                        dc(doc, tx , ty )
                        dc(doc, x6 , ty )
                        # 보강자리에서 간격 X 축 치수선
                        d(doc, x2, y2, tx , ty , 280, direction="right") 
                        d(doc, bp, ty, tx , ty , 180, direction="down")  
                  
     
    # 9파이 팝너트 연결홀 상부/하부
    P6_hole = [P6_hole1, P6_hole2, P6_hole3, P6_hole4]   

    limit_point = [P6_width]
    tx = x16 + 30 if br == 1.5 else x16 + 32
    upper_ty = y12 - 18.5 if br == 1.5 else y12 - 20   
    lower_ty = y1 + 18.5 if br == 1.5 else y1 + 20
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point
    # 상부의 연결홀
    for index, hole in enumerate(P6_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , upper_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
            if index == 0 :
                holeupperx = tx + sum                               
                holeuppery = upper_ty                       
                text = "%%C9 M6 POPNUT(머리5mm)"
                dim_leader(doc,  holeupperx, holeuppery, holeupperx - 350, holeuppery +  400,   text, direction="left")                
                d(doc,  x16 , y16,holeupperx, holeuppery,  80, direction="up", option='reverse')                               

            elif index == len(hole_variables) - 1 :
                dc(doc, x7, y7)                   
            else:
                dc(doc, tx + sum, upper_ty)                                   
    # 하부에 연결홀 타공
    sum = 0
    for index, hole in enumerate(P6_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')
                circle_cross(doc, tx + sum , lower_ty, 9 , layer='레이져')                
            if index == 0 :
                holelowerx = tx + sum                               
                holelowery = lower_ty                          
                d(doc,  x17 , y17, holelowerx , holelowery ,  200, direction="down", option='reverse')                                            

            elif index == len(hole_variables) - 1 :
                dc(doc, x6, y6)                   
            else:
                dc(doc, tx + sum, lower_ty)                                   
                
    # 상부치수선    
    d(doc, x16, y16, x14 ,y14, 150, direction="up", option='reverse' )
    dc(doc, x9 , y9)    
    dc(doc, x7, y7)
    # 상부 전체치수선
    d(doc, x16, y16, x7 ,y7, 250, direction="up")

    # 하부치수선    
    d(doc, x17, y17, x1 ,y1, 110, direction="down", option='reverse' )
    d(doc, x2, y2, x6 ,y6, 110, direction="down")        
    # 하부 2단 절곡 만나는 곳 치수선
    d(doc, x17, y17, x19 ,y19, 250, direction="down", option='reverse' )
    dc(doc, x4 , y4)    
    dc(doc, x6 , y6)
    # 하부 전체치수선
    d(doc, x17, y17, x6 ,y6, 330, direction="down", option='reverse' )
    
    # 오른쪽 15mm 표기
    d(doc, x4 , y4 , x2, y2, extract_abs(x4,x2) + 120, direction="right")
    # 오른쪽 최종 치수선
    d(doc, x11, y11 , x7, y7, 300, direction="right")
    dc(doc, x6, y6)
    dc(doc, x2, y2)    

    # 왼쪽 치수선 20mm 
    d(doc, x12, y12, holeupperx, holeuppery, 150, direction="left")
    d(doc, x1, y1, holelowerx, holelowery, 150, direction="left")
    # 왼쪽 치수선 전체
    d(doc, x12, y12, x1, y1, 280, direction="left")
   

    #######################################  
    # P6 단면도 (상부에 위치한)
    #######################################  

    x1 = x1 - panel_width + 6
    y1 = pagey + CH + 800
    x2 = x1 - panel_wing
    y2 = y1 
    x3 = x2
    y3 = y2 - panel_width
    x4 = x3 + P6_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + panel_width
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - panel_width + thickness*2
    x10 = x9 - P6_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + panel_width - thickness*2
    x12 = x11 + panel_wing - thickness
    y12 = y11
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3
    y13 = y3 + P6_holegap
    x14 = x4
    y14 = y4 + P6_holegap
    
    line(doc, x13-10, y13, x13+10, y13, layer="CL") 
    line(doc, x14-10, y14, x14+10, y14, layer="CL") 
    # 상부 치수선
    d(doc, x1, y1, x2, y2, 150, direction='up')   
    d(doc, x6, y6, x5, y5, 150, direction='up')   
    # 좌측    
    d(doc, x13-10, y13, x3, y3, 100, direction='left')      
    d(doc, x2, y2, x3, y3, 180, direction='left')  

    # 전체하부
    d(doc, x3, y3, x4, y4, 350, direction='down')              
    d(doc, x14+10, y14, x4, y4, 130, direction='right')    

    x13, y13 =  x1-10, y3 + P6_holegap        
    rectangle(doc, x1+4, y3+thickness , x6 - 4, y1-2, layer='구성선')    
    # 하단 날개 23 표기 width 25 -2
    d(doc, x3 + 100, y3 + P5_holegap , x3 + 100 , y3, 50, direction="left")
    d(doc, x3 + 140, y1-2 , x3 + 140, y3, 20, direction='left')  

    P6_hole = [P6_hole4, P6_hole3, P6_hole2, P6_hole1]     
    limit_point = [P6_width]
    tx = x3 
    ty = y3 + P6_holegap
    sum = 0
    # 각 변수에 대해 값이 0보다 크고 limit_point에 없으면 rightholes에 추가
    for index, hole in enumerate(P6_hole):  
        if hole is not None and hole > 0:
            sum += hole
            if sum not in limit_point:                
                insert_block(tx + sum, ty,"M6")
            if index == 0 :
                d(doc,  x3 , y3, tx + sum, ty, 280, direction="down" , option='reverse')                                    
            else:
                dc(doc, tx + sum, ty)                   
        else:
            if index == len(hole_variables) - 1 :
                dc(doc, tx + sum, ty)        

    # 보강위치 단면도 표기
    rb_list = panel_rib(P6_width, P6_handrailxpos)        
    preX = x3
    for index, g in enumerate(rb_list):      
        bp = x3 + g
        line(doc, bp, y3-10 , bp , y3+10, layer='0')                  
        d(doc, preX, y3-10, bp, y3, 170, direction="down")
        preX = bp            
    dc(doc, x4,y4)   
          
    if handrail_height > 0 :       
        # 핸드레일 그리기        
        for index, g in enumerate(P6_handrailxpos):            
            if g is not None : 
                tx = x3 + g                
                d(doc, tx, y3, x3 , y3 - 10 , 90 + index*40, direction="down")                    
                line(doc, tx , y3 + 10 , tx , y3 - 10 , layer='CLphantom')                    

    #######################################  
    # P6 단면도 (우측)
    #######################################  
    top_panel_width = panel_width - 2
    x1 = pagex + P6_width*2 + 1000*2
    y1 = pagey + CH
    x2 = x1 
    y2 = y1 + panel_wing
    x3 = x2 - top_panel_width
    y3 = y2 
    x4 = x3 
    y4 = y3 - CPH
    x5 = x4 + top_panel_width
    y5 = y4 
    x6 = x5 
    y6 = y5 + panel_wing
    x7 = x6 - thickness
    y7 = y6 
    x8 = x7 
    y8 = y7 - panel_wing + thickness
    x9 = x8 - top_panel_width + thickness*2
    y9 = y8 
    x10 = x9 
    y10 = y9 + CPH - thickness*2
    x11 = x10 + top_panel_width - thickness*2
    y11 = y10 
    x12 = x11 
    y12 = y11 - panel_wing + thickness
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x13 = x3 + P6_holegap
    y13 = y3
    x14 = x4 + P6_holegap
    y14 = y4
    
    line(doc, x13, y13+10, x13, y13-10, layer="CL")
    line(doc, x14, y14+10, x14, y14-10, layer="CL")
    d(doc, x1, y1, x2, y2, 150, direction='right')
    d(doc, x3, y3, x13, y13+10, 80, direction='up')
    d(doc, x3, y3, x2, y2, 180, direction='up')
    d(doc, x14, y14-10, x4, y4, 100, direction='down')
    d(doc, x4, y4, x5, y5, 180, direction='down')

    d(doc, x3, y3, x4, y4, 100, direction='left')
    d(doc, x6, y6, x5, y5, 150, direction='right')

    ##################### 코멘트 ##########################
    mx = frameXpos + P6_width*2 + 3000
    my = frameYpos +2000     
    page_comment(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + P6_width*2 + 4000
    my = frameYpos +2000             
    desx = mx - 1300
    desy = my + 1000    
    text = 'REAR PANEL(#6)' 
    unitsu = SU

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 70 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -150 , 70, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 300 , 70, str(textstr), layer='0')   
    
    frameXpos = frameXpos + TargetXscale + 400



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################


    #########################################################################################
    # 10page transom 
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 2730 + (OP-900) 
    TargetYscale = 1965 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
        
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "CAR TRANSOM ASS", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # TRANSOM 일체형 판넬 조립도 (도면의 상부에 위치한 단면도) 평면도
    ###################################################

    tr_column_width = column_width - 5    

    transom_thickness = 30 # tr_column_width와 다름, 주의요함

    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx - 200
    y1 = ry + 1000 + (CH-2500) - 80
    x2 = x1 + OP
    y2 = y1    
    x3 = x2 
    y3 = y2 + tr_column_width
    x4 = x3 - OP
    y4 = y3 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   

    line(doc, x1, y1+thickness, x2, y1+thickness, layer="22")    # cyan hidden line
    line(doc, x4, y4-thickness, x3, y4-thickness, layer="22")    # cyan hidden line
    
    slot_ypos = y3 - 15
    slot_gap = 25
    slot_startX = 50
    line(doc, x1+20, y3-15, x3-20, y3-15 , layer='CLphantom') # '구성선' 회색선
    insert_block(x1 + slot_startX, slot_ypos,"8x16_vertical_draw")
    insert_block(x1 + slot_startX+slot_gap, slot_ypos,"8x16_vertical_draw")
    insert_block(x1 + slot_startX+slot_gap*2, slot_ypos,"8x16_vertical_draw")
    insert_block(x3 - slot_startX, slot_ypos,"8x16_vertical_draw")
    insert_block(x3 - slot_startX-slot_gap, slot_ypos,"8x16_vertical_draw")
    insert_block(x3 - slot_startX-slot_gap*2, slot_ypos,"8x16_vertical_draw")
    d(doc,  x4 , y4, x1 + slot_startX, slot_ypos, 100, direction="up")       
    d(doc,  x3 , y3, x3 - slot_startX, slot_ypos, 100, direction="up")       
    
    # 중간 5개홀 
    slot_gap = 75
    slot_startX = OP/2
    insert_block(x1 + slot_startX, slot_ypos,"8x16_vertical_draw")
    insert_block(x1 + slot_startX+slot_gap, slot_ypos,"8x16_vertical_draw")
    insert_block(x1 + slot_startX+slot_gap*2, slot_ypos,"8x16_vertical_draw")    
    insert_block(x1 + slot_startX-slot_gap, slot_ypos,"8x16_vertical_draw")
    insert_block(x1 + slot_startX-slot_gap*2, slot_ypos,"8x16_vertical_draw")    
               
    d(doc,  x3 , y3, x4, y4, 200, direction="up")
    d(doc,  x3 , slot_ypos, x3, y3, 100, direction="right")

    rectangle(doc, x1,y1,x3,y1+15,layer="0")
    rectangle(doc, x4,y4,x3,y3-30,layer="0")
    # 보강 63 x 40 표현 양쪽 끝단
    rectangle(doc, x1+thickness,y1+15,x1+thickness+40,y1+15+63-15,layer="0")
    rectangle(doc, x2-thickness,y1+15,x2-thickness-40,y1+15+63-15,layer="0")

    #############################################################
    # 일체형 transom  조립도 본체 만들기
    # 조립도 본체구성 표현
    #############################################################

    y1 = ry + 300 + (CH-2500) 
    x2 = x1 + OP
    y2 = y1    
    x3 = x2 
    y3 = y2 + TR_TRH
    x4 = x3 - OP
    y4 = y3 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")   

    line(doc, x1, y1+thickness, x2, y1+thickness, layer="22")    # cyan hidden line
    line(doc, x4, y4-thickness, x3, y4-thickness, layer="22")    # cyan hidden line

    d(doc, x4+0.5 , y4, x4, y4, 100, direction="up")    
    d(doc, x4 , y4, x4+40, y4, 100, direction="up")    
    d(doc, x3-0.5 , y3, x3, y3, 100, direction="up")    
    d(doc, x3 , y3, x3-40, y3, 100, direction="up")    

    rectangle(doc, x1,y1,x3,y1+30,layer="0")
    # 보강 표현 양쪽 끝단
    rectangle(doc, x1+thickness,y1+thickness,x1-thickness+40,y4-thickness,layer="0")
    rectangle(doc, x2-thickness,y1+thickness,x3+thickness-40,y4-thickness,layer="0")
        
    slot_gap = 25
    slot_startX = x1 + OP/2
                   
    # 중심선
    line(doc, slot_startX, y3 + 30, slot_startX, y1 - 30 , layer='CLphantom')


    ###########################################################################
    # transom 왼쪽 단면도
    ###########################################################################
    first_wing = 30
    second_wing = 15

    x1 = x1 - 250
    y1 = y4 
    x2 = x1 - 15
    y2 = y1    
    x3 = x2
    y3 = y2 - TR_TRH 
    x4 = x3 + tr_column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing
    x6 = x5 - second_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + second_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - first_wing + thickness*2
    x10 = x9 - tr_column_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + TR_TRH - thickness*2
    x12 = x11 + 15 - thickness
    y12 = y11

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")    

    line(doc, x2 + 8 , y1 + 10 , x2 + 8 ,  y1 - 10 , layer='CLphantom') # '구성선' 회색선  
                     
    # 안에 들어가는 보강표현하기
    xx1 = x1 + 3 + 15 + thickness
    yy1 = y1 - 2
    xx2 = xx1 - 33 + thickness
    yy2 = yy1    
    xx3 = xx2
    yy3 = y3 + 2
    xx4 = xx3 + 63
    yy4 = yy3 
    xx5 = xx4 
    yy5 = yy4 + 30
    xx6 = xx5 - 30 - thickness
    yy6 = yy5 
    
    prev_x, prev_y = xx1, yy1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'xx{i}'), eval(f'yy{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, xx1, yy1, layer="0")      
                     
    line(doc, xx2 + thickness , yy1 , xx2 + thickness  ,  yy3 , layer='22') # '구성선' 회색선           

    holex1 = x2 + 18
    holey1 = y2 - 50            
    holex2 = x3 + 18
    holey2 = y3 + 50            
    holex3 = x3 + 43
    holey3 = y3 + 20

    insert_block(holex1, holey1,"8x16_vertical_draw")        
    insert_block(holex2, holey2,"8x16_vertical_draw")        
    insert_block(holex3, holey3,"8x16_vertical_draw")     

    line(doc,holex1 , holey1+20 , holex1  ,  holey2-20 , layer='CLphantom') # '구성선' 회색선       

    d(doc, x2 , y2, holex1, holey1, 100, direction="up", option='reverse')   
    d(doc, x2 , y2, holex1, holey1, 50, direction="left")   
    dc(doc, holex2,holey2)
    dc(doc, x3,y3, option='reverse')   
    d(doc, x2 , y2, x3, y3, 130, direction="left")   
    d(doc, holex2 , holey2, holex3 , holey3,  100, direction="down")   
    d(doc, x3 , y3, holex3 , holey3,  180, direction="down")   
    d(doc, x3 , y3 , x4 , y4 ,  260, direction="down")   
    

    ###########################################################################
    # transom 오른쪽 상세 단면도
    ###########################################################################

    first_wing = 30
    second_wing = 15

    x1 = rx + OP + 500
    y1 = ry + (CH-2500) + 1150 - 150
    x2 = x1 - first_wing
    y2 = y1    
    x3 = x2
    y3 = y2 - TR_TRH 
    x4 = x3 + tr_column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing
    x6 = x5 - second_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + second_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - first_wing + thickness*2
    x10 = x9 - tr_column_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + TR_TRH - thickness*2
    x12 = x11 + 15 - thickness
    y12 = y11

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")    
    
    # 중간 적색선 위치 2개 (치수선 용도)
    x13 = x2 + first_wing/2
    y13 = y1 + 10 
    x14 = x6 + second_wing/2
    y14 = y6 + 10 
    line(doc, x13, y1 + 10 ,x13 ,  y1 - 10 , layer='CLphantom') # '구성선' 회색선  
    line(doc, x14, y6 + 10 ,x14 ,  y6 - 10 , layer='CLphantom') # '구성선' 회색선  

    # 절곡도 문구 넣기
    put_commentLine(x3 - 50, y3 - 350)    

    d(doc, x2 , y2, x13, y13, 50, direction="up", option='reverse')   
    d(doc, x2 , y2, x1, y1, 130, direction="up", option='reverse')   
    d(doc, x2 , y2, x3, y3, 100, direction="left")       
    d(doc, x3 , y3, x4, y4, 100, direction="down")   
    d(doc, x4 , y4, x5, y5, 100, direction="right", option='reverse')   
    d(doc, x5 , y5, x14, y14, 50, direction="up", option='reverse')   
    d(doc, x5 , y5, x6, y6, 130, direction="up", option='reverse')       
    
    ##################### 코멘트 ##########################
    mx = frameXpos + 1000 + (OP-900) 
    my = frameYpos + 600
    page_comment_small(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + 1000 + (OP-900) 
    my = frameYpos + 100
    desx = mx - 1200
    desy = my + 400    
    text = 'CAR TRANSOM ASY' 
    unitsu = SU

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 30 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -50 , 30, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 100 , 30, str(textstr), layer='0')   
    
    frameXpos = frameXpos + TargetXscale + 400



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################


    #########################################################################################
    # 11page transom 실제 전개도 및 보강 전개도
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 3452 + (OP-900) 
    TargetYscale = 2460 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
        
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "TRANSOM BRACKET", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    # column_width는 분리형인 경우 tr_column_width 산출 필요
    tr_column_width = column_width - 5

    ###################################################
    # TRANSOM 일체형 전개도 실제 가공품
    ###################################################
    rx = math.floor(pagex)
    ry = math.floor(pagey)

    transom_thickness = 30

    first_wing = 30
    second_wing = 15

    x1 = rx - 400
    y1 = ry + 800 + (CH-2500)
    x2 = x1 + OP - 4
    y2 = y1    
    x3 = x2
    y3 = y2 + 15 
    x4 = x3 + 2
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing + TRH + tr_column_width + transom_thickness + second_wing - br*8 - 15
    x6 = x5 - OP
    y6 = y5 
    x7 = x6 
    y7 = y6 - (first_wing + TRH + tr_column_width + transom_thickness + second_wing - br*8 - 15)
    x8 = x7 + 2
    y8 = y7 

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 8
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")   
    
    slot_ypos = y6 - 15
    slot_gap = 25
    slot_startX = 50    

    slotx1 = x7 + slot_startX
    slotx2 = x7 + slot_startX+slot_gap
    slotx3 = x7 + slot_startX+slot_gap*2
    
    slotx9 = x5 - slot_startX
    slotx10 = x5 - slot_startX-slot_gap
    slotx11 = x5 - slot_startX-slot_gap*2

    insert_block(slotx1, slot_ypos,"8x16_vertical")
    insert_block(slotx2, slot_ypos,"8x16_vertical")
    insert_block(slotx3, slot_ypos,"8x16_vertical")
    insert_block(slotx9, slot_ypos, "8x16_vertical")
    insert_block(slotx10, slot_ypos,"8x16_vertical")
    insert_block(slotx11, slot_ypos,"8x16_vertical")

    # 중간 5개홀 
    slot_gap = 75
    slot_startX = OP/2
    slotx4 = x7 + slot_startX-slot_gap*2
    slotx5 = x7 + slot_startX-slot_gap
    slotx6 = x7 + slot_startX
    slotx7 = x7 + slot_startX+slot_gap
    slotx8 = x7 + slot_startX+slot_gap*2

    insert_block(slotx4, slot_ypos,"8x16_vertical")
    insert_block(slotx5, slot_ypos,"8x16_vertical")
    insert_block(slotx6, slot_ypos,"8x16_vertical")    
    insert_block(slotx7, slot_ypos,"8x16_vertical")
    insert_block(slotx8, slot_ypos,"8x16_vertical")    

    d(doc,  x6 , y6, slotx2, slot_ypos, 120, direction="up", option='reverse')       
    dc(doc, slotx6, slot_ypos)
    dc(doc, slotx10, slot_ypos)
    dc(doc, x5, y5)    
               
    d(doc,  slotx2 , slot_ypos, slotx1, slot_ypos, 50, direction="up")       
    d(doc,  slotx2 , slot_ypos, slotx3, slot_ypos, 50, direction="up")       
    d(doc,  slotx4 , slot_ypos, slotx6, slot_ypos, 50, direction="up")       
    d(doc,  slotx8 , slot_ypos, slotx6, slot_ypos, 50, direction="up")       
    d(doc,  slotx10 , slot_ypos, slotx9, slot_ypos, 50, direction="up")       
    d(doc,  slotx10 , slot_ypos, slotx11, slot_ypos, 50, direction="up")       

    # 왼쪽 치수선
    d(doc,  x6 , y6, slotx1, slot_ypos, 120, direction="left")       
    d(doc,  x7 , y7, x1, y1, 120, direction="left")       
    d(doc,  x4 , y4, x2, y2, 120, direction="right")       
    d(doc,  x5 , y5, x2, y2, 220, direction="right")    

    # 지시선 추가
    text = "8*16"
    dim_leader(doc,  slotx3, slot_ypos, slotx3 + 100, slot_ypos - 100,   text, direction="right")          

    # 우성인 경우는 6파이 홀 타공해줌
    # 일단 우성꺼로 생각하고 만든다.
    holex1 = x6 + OP/2
    holey1 = y1 + second_wing + tr_column_width/2 + transom_thickness - br*4

    circle_cross(doc,holex1,holey1,6,layer="레이져")
    d(doc,  holex1 , y1, holex1, holey1, 100, direction="right")     
    # 지시선 추가
    text = "비상램프 %%c6 (우성만 가공)"
    dim_leader(doc,  holex1, holey1, holex1 - 150, holey1 +  150,   text, direction="right")       

    # 하부 전체치수
    d(doc,  x7 , y7, holex1, holey1, 220, direction="down")        
    d(doc,  x4 , y4, holex1, holey1, 220, direction="down")        

    # M5 육각 (십자마크)
    markx1 = x1 + 150 -2
    markx2 = x2 - 150 +2
    cross(doc, markx1, y1 + 7, 3.5, layer='레이져')
    cross(doc, markx2, y2 + 7, 3.5, layer='레이져')
    d(doc,  x7 , y7, markx1, y1+7, 120, direction="down")    
    d(doc,  x4 , y4, markx2, y2+7, 120, direction="down")    
    d(doc,  markx1 , y1, markx1, y1+7, 150, direction="right")    

    # 지시선 추가
    text = "M5육각"
    dim_leader(doc,  markx1, y1 + 7, markx1 - 100, y1 + 7 +  150,   text, direction="right")       

    # 좌우 2mm 표현
    d(doc,  x7 , y7, x1, y1, 50, direction="down")    
    d(doc,  x4 , y4, x2, y2, 50, direction="down")    

    

    ###########################################################################
    # transom 오른쪽 상세 단면도
    ###########################################################################

    first_wing = 30
    second_wing = 15

    x1 = rx + OP + 150
    y1 = ry + (CH-2500) + 1250 
    x2 = x1 - first_wing
    y2 = y1    
    x3 = x2
    y3 = y2 - TR_TRH 
    x4 = x3 + tr_column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing
    x6 = x5 - second_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + second_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - first_wing + thickness*2
    x10 = x9 - tr_column_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + TR_TRH - thickness*2
    x12 = x11 + 15 - thickness
    y12 = y11

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")    
    
    # 중간 적색선 위치 2개 (치수선 용도)
    x13 = x2 + first_wing/2
    y13 = y1 + 10 
    x14 = x6 + second_wing/2
    y14 = y6 + 10 
    x15 = x3 + tr_column_width/2
    y15 = y3  
    line(doc, x13, y1 + 10 ,x13 ,  y1 - 10 , layer='CLphantom') # '구성선' 회색선  
    line(doc, x14, y6 + 10 ,x14 ,  y6 - 10 , layer='CLphantom') # '구성선' 회색선  
    line(doc, x15, y15 + 10 ,x15 ,  y15 - 10 , layer='CLphantom') # '구성선' 회색선  

    # 절곡도 문구 넣기
    put_commentLine(x3 - 50, y3 - 350)    

    d(doc, x2 , y2, x13, y13, 50, direction="up", option='reverse')   
    d(doc, x2 , y2, x1, y1, 130, direction="up", option='reverse')   
    d(doc, x2 , y2, x3, y3, 100, direction="left")           
    d(doc, x4 , y4, x5, y5, 100, direction="right", option='reverse')   
    d(doc, x5 , y5, x14, y14, 50, direction="up", option='reverse')   
    d(doc, x5 , y5, x6, y6, 130, direction="up", option='reverse')       

    d(doc, x15 , y15-10, x4, y4, 180, direction="down")   
    d(doc, x3 , y3, x4, y4, 250, direction="down")   


    ###########################################################################
    # transom 보강 단면도 ( 위, 아래 3미리 총 6mm 빠지는 크기임)
    ###########################################################################
    first_wing = 30
    second_wing = 33

    x1 = rx + OP + 150 + 600
    y1 = ry + (CH-2500) + 1250 - 200
    x2 = x1 - second_wing
    y2 = y1    
    x3 = x2
    y3 = y2 - TR_TRH + 6  # 보강은 6mm 작은것이다.
    x4 = x3 + tr_column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing
    x6 = x5 - second_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + second_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - first_wing + thickness*2
    x10 = x9 - tr_column_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + TR_TRH - 6 - thickness*2
    x12 = x11 + second_wing - thickness
    y12 = y11
                     
    # 안에 들어가는 보강표현하기
    xx1 = x1 
    yy1 = y1 
    xx2 = xx1 - second_wing 
    yy2 = yy1    
    xx3 = xx2
    yy3 = y3 
    xx4 = xx3 + 63
    yy4 = yy3 
    xx5 = xx4 
    yy5 = yy4 + 30
    xx6 = xx5 - 30
    yy6 = yy5 
    
    prev_x, prev_y = xx1, yy1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'xx{i}'), eval(f'yy{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, xx1, yy1, layer="0")      
                     
    line(doc, x2 + 16 , y1 + 10 , x2 + 16 ,  y1 - 10 , layer='CLphantom') # '구성선' 회색선                           

    holex1 = x2 + 16
    holey1 = y2 - 47            
    holex2 = x3 + 16
    holey2 = y3 + 47            
    holex3 = x3 + 41
    holey3 = y3 + 17

    insert_block(holex1, holey1,"8x16_vertical_draw")        
    insert_block(holex2, holey2,"8x16_vertical_draw")        
    insert_block(holex3, holey3,"8x16_vertical_draw")     

    line(doc,holex1 , holey1+20 , holex1  ,  holey2-20 , layer='CLphantom') # '구성선' 회색선       

    d(doc, x2 , y2, holex1, holey1, 100, direction="up", option='reverse')   
    d(doc, x2 , y2, holex1, holey1, 120, direction="left")   
    dc(doc, holex2,holey2)
    dc(doc, x3,y3, option='reverse')   
    d(doc, x2 , y2, x3, y3, 230, direction="left")   
    d(doc, holex2 , holey2, holex3 , holey3,  60, direction="left")   
    d(doc, holex2 , holey2, holex3 , holey3,  100, direction="down")   
    d(doc, x3 , y3, holex3 , holey3,  180, direction="down")   
    d(doc, x3 , y3 , xx4 , yy4 ,  260, direction="down")   
    

    ###########################################################################
    # transom 보강 위쪽 'ㄴ'자 형태 평면도?
    ###########################################################################
    first_wing = 40
    second_wing = 63
    thickval = 1.6

    x1 = x2
    y1 = y1 + 300
    x2 = x1 
    y2 = y1 - first_wing 
    x3 = x2 + second_wing
    y3 = y2
    x4 = x3
    y4 = y3 + thickval 
    x5 = x4 - second_wing + thickval
    y5 = y4 
    x6 = x5 
    y6 = y5 + first_wing - thickval
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")      
                     
    line(doc, x2 + 16 , y2 + 10 , x2 + 16 ,  y2 - 10 , layer='CLphantom')  # '구성선' 회색선                           
    line(doc, x2 + 41 , y2 + 10 , x2 + 41 ,  y2 - 10 , layer='CLphantom')  # '구성선' 회색선                           

    d(doc, x1 , y1 , x2 , y2,  150, direction="left")   
    d(doc, x1 , y1 , x4 , y4 ,  150, direction="up")   
    

    ###########################################################################
    # transom 보강 전개도
    ###########################################################################
    first_wing = 30
    second_wing = 70

    x1 = x1 + 600
    y1 = ry + (CH-2500) + 1250 - 200
    x2 = x1 - second_wing
    y2 = y1    
    x3 = x2
    y3 = y2 - TR_TRH + 6  # 보강은 6mm 작은것이다.
    x4 = x3 + tr_column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + first_wing
    x6 = x5 - second_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + second_wing - thickness
    y8 = y7 
    x9 = x8 
    y9 = y8 - first_wing + thickness*2
    x10 = x9 - tr_column_width + thickness*2
    y10 = y9 
    x11 = x10 
    y11 = y10 + TR_TRH - 6 - thickness*2
    x12 = x11 + second_wing - thickness
    y12 = y11
                     
    # 안에 들어가는 보강표현하기
    xx1 = x1 
    yy1 = y1 
    xx2 = xx1 - second_wing 
    yy2 = yy1    
    xx3 = xx2
    yy3 = y3 
    xx4 = xx3 + 100.3
    yy4 = yy3 
    xx5 = xx4 
    yy5 = yy4 + 30
    xx6 = xx5 - 30.3
    yy6 = yy5 
    
    prev_x, prev_y = xx1, yy1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'xx{i}'), eval(f'yy{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, xx1, yy1, layer="레이져")      
                     
    holex1 = x2 + 53.3
    holey1 = y2 - 47            
    holex2 = x3 + 53.3
    holey2 = y3 + 47            
    holex3 = x3 + 78.3
    holey3 = y3 + 17

    insert_block(holex1, holey1,"8x16_vertical")        
    insert_block(holex2, holey2,"8x16_vertical")        
    insert_block(holex3, holey3,"8x16_vertical")     

    d(doc, x2 , y2, holex1, holey1, 100, direction="up", option='reverse')   
    d(doc, holex1, holey1,  xx5, yy5, 100, direction="up")
    d(doc, x2 , y2, holex1, holey1, 120, direction="left")   
    dc(doc, holex2,holey2)
    dc(doc, x3,y3, option='reverse')   
    d(doc, x2 , y2, x3, y3, 230, direction="left")   
    d(doc, holex2 , holey2, holex3 , holey3,  110, direction="left")   
    d(doc, holex2 , holey2, holex3 , holey3,  100, direction="down")   
    d(doc, x3 , y3, holex3 , holey3,  180, direction="down" , option='reverse')    
    d(doc, x3 , y3 , xx4 , yy4 ,  260, direction="down")   
    d(doc, xx4 , yy4 ,  holex3 , holey3,  150, direction="right")   
    d(doc, xx4 , yy4 ,  xx5 , yy5,  250, direction="right")   

    # 지시선 추가
    text = "8*16"
    dim_leader(doc,  holex2, holey2,  holex2 + 100, holey2+ 150,  text, direction="right")      
    
    ##################### part 설명 - 전개도 ##########################
    mx = x1 - 300
    my = y3 - 500
    desx = mx 
    desy = my 
    text = 'TRANSOM BRACKET' 
    unitsu = SU * 2

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 30 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 1.6T"
    draw_Text(doc, desx , desy -50 , 30, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} EA (좌/우) SET"    
    draw_Text(doc, desx , desy - 100 , 30, str(textstr), layer='0')       


    ##################### 전개도 ##########################
    mx = x3
    my = y3 - 350
    text = '전 개 도'
    put_commentLine_string(mx, my, text) 
           
    ##################### 절곡도 ##########################
    mx = frameXpos + 1000 + (OP-900) 
    my = frameYpos + 800
    page_comment_small(mx, my)
    
    ##################### part 설명  ##########################
    mx = frameXpos + 1000 + (OP-900) 
    my = frameYpos + 300
    desx = mx - 1200
    desy = my + 600    
    text = 'TRANSOM' 
    unitsu = SU

    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 30 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Material} {Spec}"
    draw_Text(doc, desx , desy -50 , 30, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 100 , 30, str(textstr), layer='0')   
    
    frameXpos = frameXpos + TargetXscale + 400



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################


    #########################################################################################
    # 12page transom backcover
    #########################################################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 2400 + (OP-900) 
    TargetYscale = 1750 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
        
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "CAR TRANSOM BACK COVER", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   
    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale

    ###################################################
    # CAR TRANSOM BACK COVER 
    ###################################################

    transom_thickness = 30 # column_width와 다름, 주의요함

    rx = math.floor(pagex)
    ry = math.floor(pagey)

    x1 = rx - 300
    y1 = ry + 800 
  
    insert_block(x1,  y1 ,"transom_cover")
  
    #############################################################
    # 일체형 transom BACK COVER 전개도
    #############################################################

    x1 = rx + 200
    y1 = ry + 800 
    x2 = x1 + 140 - 3
    y2 = y1    
    x3 = x2
    y3 = y2 + 8 
    x4 = x3 + 6
    y4 = y3 
    x5 = x4 
    y5 = y4 - 8
    x6 = x5 + OP-300 - 6
    y6 = y5 
    x7 = x6 
    y7 = y6 + 8
    x8 = x7 + 6
    y8 = y7 
    x9 = x8 
    y9 = y8 - 8
    x10 = x9 + 140 - 3
    y10 = y9 
    x11 = x10 
    y11 = y10 + 150
    x12 = x11 - OP + 20
    y12 = y11

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        if i == 4 :
            draw_arc(doc, x3, y3, x4, y4, 3, direction='up')
        elif i == 8 :
            draw_arc(doc, x7, y7, x8, y8, 3, direction='up')
        else:
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")   

    line(doc, x3 + 3 , y3 + 10 , x3 + 3 ,  y3 - 10 , layer='CLphantom')  # '구성선' 회색선    
    line(doc, x7 + 3 , y7 + 10 , x7 + 3 ,  y7 - 10 , layer='CLphantom')  # '구성선' 회색선    

    d(doc, x3+3 , y3+3, x1 , y1, 110, direction="left")    
    d(doc, x11 , y11, x10 , y10, 150, direction="right")    
    d(doc, x3 , y3, x4, y4, 100, direction="up")    
    d(doc, x1 , y1, x3+3, y1, 100, direction="down")    
    dc(doc, x7+3,y1)
    dc(doc, x10,y10)
    d(doc, x1 , y1, x10, y10, 200, direction="down")    
                   
    ##################### part 설명  ##########################
    mx = frameXpos + 1500 + (OP-900) 
    my = frameYpos + 400
    desx = mx - 1200
    desy = my + 400    
    text = 'CAR TRANSOM BACK COVER' 
    unitsu = SU

    textstr = f"* 일체형 CAR TRANSOM의 BACK COVER임."    
    draw_Text(doc, desx , desy+70 , 30 , str(textstr), layer='0')    
    textstr = f"Part Name : {text}"    
    draw_Text(doc, desx , desy , 30 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : 445 1.5T/1.2T 가능 "
    draw_Text(doc, desx , desy -50 , 30, str(textstr), layer='0')    
    textstr = f"Quantity : {unitsu} SET"    
    draw_Text(doc, desx , desy - 100 , 30, str(textstr), layer='0')   
    
    frameXpos = frameXpos + TargetXscale + 400



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

    ###################################################
    # 13page 컬럼 우측위치한 전개도 (P1 일체형 전개도 응용)
    ###################################################
    # 도면틀 넣기    
    BasicXscale = 6851
    BasicYscale = 4870
    TargetXscale = 6851 
    TargetYscale = 4870 + (CH-2500) 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    

    current_page = 2
    # print("{current_page} page 스케일 비율 : " + str(frame_scale))           
    insert_frame(frameXpos-784 , frameYpos  , frame_scale, "drawings_frame", "CAR COLUMN", f"CH:{CH}, KP:{KH}+{FH}, WH:{CPH}", "drawing number")   

    pagex ,  pagey = frameXpos , frameYpos + 1123 * frame_scale    

    x1 = math.floor(pagex)
    y1 = math.floor(pagey) - 100
    x2 = x1 + panel_wing + column_thickness*3 + column_width - panel_width/2 - br*8
    y2 = y1    
    x3 = x2 + panel_width/2 # 끝기준 장공 위치
    y3 = y2 
    x4 = x3
    y4 = y3 + FH
    x5 = x4 
    y5 = y4 + OPH 
    x6 = x5 
    y6 = y5 + CH - OPH - FH 
    x7 = x6 + (panel_width/2  ) * - 1
    y7 = y6 
    x8 = x7 - ( panel_wing + column_thickness*3 + column_width - panel_width/2 - br*8) + (panel_wing + column_thickness+51)  
    y8 = y7 
    x9 = x8 
    y9 = y8  - CH + OPH + FH  + 30  # 일체형은 40, 컬럼은 30
    x10 = x1 
    y10 = y9 
    x11 = x10 
    y11 = y10 - 30  # 일체형은 40, 컬럼은 30
    x12 = x11 
    y12 = y11 - OPH

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
      
    #절곡라인  (히든선 : 세로 CLphantom)      
    line(doc, x2, y2, x7, y7,  layer='CLphantom')
    #절곡라인  (히든선 : 가로 magentaphantom)      
    line(doc, x11-30, y11, x5, y5,  layer='magentaphantom')
    line(doc, x12-30, y12, x4, y4,  layer='magentaphantom')

    # 하부 치수선
    d(doc, x1,y1,x3,y3,200,direction="down")
    d(doc, x2,y2,x3,y3,125,direction="down")

    # 장공표시 #P01, P11은 일체형일 경우 만들어본다.
    gap = 0
    hole = calculate_holeArray(KPH+popnut_height+135, 400, KPH+popnut_height+OPH+200 , CH)
    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(x2, y2 + g, "8x16_vertical")
        if index == 0 :
            d(doc, x2, y3, x2, y2 + g, 180, direction="right" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  x2, y2 + g, x2-100, y2 + g + 100,   text, direction="left")
        else:
            dc(doc, x2, y2 + g)    
    dc(doc, x6, y6)    

    # 8x16 수평모양 slot 장공 3개 위치 지정
    tx = x11 + panel_wing + column_thickness + column_width - 20 - br * 4
    ty = y11 + 50
    tx1 = tx - column_thickness  # 일체형은 25, 컬럼은 30   5mm 돌출때문에 차이남
    ty1 = y11 + TRH - 50 
    insert_block(tx, ty, "8x16_vertical")    
    insert_block(tx, ty1, "8x16_vertical")   
    ty2 = y11 + 15  #  일체형은 20, 컬럼은 15
    insert_block(tx1, ty2, "8x16_horizontal")    
    d(doc, tx ,ty2 ,tx, ty, 171, direction="right", option='reverse' )
    dc(doc, tx , ty1)
    dc(doc, tx, y8)
    d(doc, tx1, ty2, tx1, y11, 80, direction="right")

    # 장공 치수선
    d(doc, x10, y10, tx1, ty2, 60, direction="up")
    d(doc, x10, y10, x8, y8, 100, direction="up")
    d(doc, x10, y10, tx, ty1, 240, direction="up")
    d(doc, tx, ty,  tx1, ty2, 85, direction="down")

    # 왼쪽 치수선
    d(doc, x8, y8, x10, y10, 180, direction="left")
    dc(doc, x11, y11,option='reverse')
    d(doc, x8, y8, x11, y11, 260, direction="left")
    dc(doc, x12, y12)
    dc(doc, x1, y1,option='reverse')

    #################################
    # 세화정공 헤더표시
    ##################################
    # 장공표시 #P01, P11은 일체형일 경우 만들어본다.
    hole = [90, 50, 90 , 50]
    limit = TRH
    xp = x3-panel_wing -11
    gap = 0    
    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            cross10(doc, xp, y5 + gap)
        if index == 1 :
            d(doc, xp, y5+ pre_gap, xp, y5 + gap, 250, direction="right", option='reverse' )    
        elif index != 0 :
            dc(doc, xp, y5 + gap)   
        pre_gap = gap 
            
    # 지시선 추가 4-M8육각
    text = "4-M8육각"
    dim_leader(doc,  xp, y5 + gap , x6+200, y6 + 150,   text, direction="right")    

    #######################################
    # 13page 컬럼 단면도 (P1 단면도 응용)
    #######################################
    x1 = x1 + panel_wing 
    y1 = pagey + CH + 500 + column_width - panel_wing
    x2 = x1 - panel_wing   
    y2 = y1 
    x3 = x2 
    y3 = y2 - column_thickness
    x4 = x3 + column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + column_thickness
    x6 = x5 - column_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + column_thickness - thickness 
    y8 = y7 
    x9 = x8 
    y9 = y8  - column_thickness + thickness*2
    x10 = x9 - column_width + thickness*2 
    y10 = y9 
    x11 = x10 
    y11 = y10 + column_thickness - thickness*2 
    x12 = x11 + panel_wing - thickness  
    y12 = y11    
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x15 = x4 - 20
    y15 = y4 
    x16 = x15 - 30
    y16 = y15 
    x17 = x6 + panel_width/2
    y17 = y6

    line(doc, x15, y15 - 10, x15, y15 +10, layer="0")     
    line(doc, x16 , y16 -10, x16, y16 +10 , layer="0")     
    line(doc, x17, y17-10, x17, y17+10, layer="0")     
    
    d(doc, x1, y1, x2, y2, 100, direction='up')   
    d(doc, x2, y2, x3, y3, 100, direction='left')       
    d(doc, x4, y4, x5, y5, 100, direction='right')  
    d(doc, x6, y6, x5, y5, 200, direction='up')  
    d(doc, x6, y6, x17, y17, 100, direction='up')  

    d(doc, x15, y15-10, x4, y4,  70, direction='down')  
    d(doc, x16, y16-10, x15, y15-10,  145, direction='down')  
    d(doc, x16, y16-10, x3, y3,  220, direction='down')      
    d(doc, x3, y3, x4, y4, 300, direction='down')  

    # description    
    desx = x1 - 200
    desy = y1 + 450
    textstr = f"Part Name : CAR COLUMN #1"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Spec}"    
    draw_Text(doc, desx , desy -60 , 35, str(textstr), layer='0')    
    textstr = f"Quantity : {SU} EA"    
    draw_Text(doc, desx , desy - 120 , 35, str(textstr), layer='0')        

    ###################################################
    # 컬럼 전개도 반대쪽 (P11 일체형 전개도 응용)
    ###################################################

    rx = math.floor(pagex + column_width + column_thickness + panel_width + panel_wing *2 + 1000 )  # 1000은 두 객체의 간격   
    ry = math.floor(pagey) - 100

    x1 = rx 
    y1 = ry
    x2 = x1 + panel_width/2   # panel_width/2는 끝기준 장공 위치
    y2 = y1    
    x3 = x2 + panel_wing + column_thickness*3 + column_width - panel_width/2 - br*8 
    y3 = y2 
    x4 = x3
    y4 = y3 + FH
    x5 = x4 
    y5 = y4 + OPH 
    x6 = x5 
    y6 = y5 + 30   # 일체형은 40, 컬럼은 30
    x7 = x6  - (column_thickness + panel_wing + column_width - br*4 - 30) 
    y7 = y6 
    x8 = x7 
    y8 = y7 + CH - OPH - FH  - 30   # 일체형은 40, 컬럼은 30
    x9 = x1 + (panel_width/2) 
    y9 = y8  
    x10 = x1 
    y10 = y9 
    x11 = x10 
    y11 = y10 + (CH - OPH - FH ) * -1
    x12 = x11 
    y12 = y11 - OPH

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="레이져")      
      
    #절곡라인  (히든선 : 세로 CLphantom)      
    line(doc, x2, y2, x9, y9,  layer='CLphantom')
    #절곡라인  (히든선 : 가로 magentaphantom)      
    line(doc, x11-30, y11, x5, y5,  layer='magentaphantom')
    line(doc, x12-30, y12, x4, y4,  layer='magentaphantom')

    # 하부 치수선
    d(doc, x1,y1,x3,y3, 200,direction="down")
    d(doc, x2,y2,x1,y1, 125,direction="down")

    # 장공표시 #P01, P11은 일체형일 경우 만들어본다.
    gap = 0
    hole = calculate_holeArray(KPH+popnut_height+135, 400, KPH+popnut_height+OPH+200 , CH)
    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            insert_block(x2, y2 + g, "8x16_vertical")
        if index == 0 :
            d(doc, x1, y1, x2, y2 + g, 180, direction="left" )    
            # 슬롯등 지시선 추가
            text = "8x16"
            dim_leader(doc,  x2, y2 + g, x2+100, y2 + g + 100,   text, direction="right")
        else:
            dc(doc, x2, y2 + g)

    dc(doc, x10, y10)

    # 8x16 slot 장공 3개 위치 지정
    tx = x5 + (panel_wing + column_thickness + column_width - 20 - br * 4 ) * -1
    ty = y5 + 50
    tx1 = tx + column_thickness  # 일체형은 25, 컬럼은 30   5mm 돌출때문에 차이남
    ty1 = y5 + TRH - 50 
    insert_block(tx, ty, "8x16_vertical")    
    insert_block(tx, ty1, "8x16_vertical")   
    tx2 = tx1
    ty2 = y5 + 15 #  일체형은 20, 컬럼은 15
    insert_block(tx1, ty2, "8x16_horizontal")    
    # 왼쪽 장공 치수선
    d(doc, tx, ty2, tx1 ,ty , 171, direction="left")
    dc(doc, tx , ty1)
    dc(doc, tx,  y8 ,option='reverse' )
    d(doc, tx1, ty2, tx1, y5, 130, direction="left" )

    # 장공 치수선
    d(doc, x6, y6, tx2, ty2, 60, direction="up")
    d(doc, x6, y6, x8, y8, 100, direction="up")
    d(doc, x6, y6, tx, ty1, 240, direction="up")
    d(doc, tx, ty,  tx1, ty2, 85, direction="down")

    # 우측 치수선
    d(doc, x8, y8, x6, y6, 180, direction="right")
    dc(doc, x5, y5)
    d(doc, x8, y8, x5, y5, 260, direction="right")
    dc(doc, x12, y12)
    dc(doc, x1, y1)
    d(doc, x3, y3, x8, y8, 360, direction="right")    

    #################################
    # 세화정공 헤더표시 (십자표시)
    #################################
    # 장공표시 #P01, P111은 일체형일 경우 만들어본다.
    hole = [90, 50, 90 , 50]
    limit = TRH
    xp = x10 + panel_wing + 11
    gap = 0    
    for index, g in enumerate(hole):
        gap += g
        if g is not None : 
            cross10(doc, xp, y5 + gap)
            if index == 1 :
                d(doc, xp, y5+ pre_gap, xp, y5 + gap, 300, direction="left", option='reverse' )    
            elif index != 0 and index != len(hole)-1 :
                dc(doc, xp, y5 + gap)               
            else:
                dc(doc, xp, y5 + gap, option='reverse')                            
        pre_gap = gap 
            
    # 지시선 추가 4-M8육각
    text = "4-M8육각"
    dim_leader(doc,  xp, y5 + gap , x10-200, y10 + 150,   text, direction="left")    

    #######################################
    # 13page 우측 컬럼 단면도 (P11 단면도 응용)
    #######################################
    rx = x12 + panel_width  + panel_wing*2 - br*5
    ry = pagey + CH + 500 + column_width - panel_wing

    x1 = rx 
    y1 = ry
    x2 = x1 - column_thickness   
    y2 = y1 
    x3 = x2 
    y3 = y2 - column_thickness
    x4 = x3 + column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + column_thickness
    x6 = x5 - panel_wing
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + panel_wing - thickness 
    y8 = y7 
    x9 = x8 
    y9 = y8  - column_thickness + thickness*2
    x10 = x9 - column_width + thickness*2 
    y10 = y9 
    x11 = x10 
    y11 = y10 + column_thickness - thickness*2 
    x12 = x11 + column_thickness - thickness  
    y12 = y11    
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x15 = x3 + 20
    y15 = y3 
    x16 = x15 + 30
    y16 = y15 
    x17 = x2 + panel_width/2
    y17 = y2

    line(doc, x15, y15 - 10, x15, y15 +10, layer="0")     
    line(doc, x16 , y16 -10, x16, y16 +10 , layer="0")     
    line(doc, x17, y17-10, x17, y17+10, layer="0")     
    
    d(doc, x1, y1, x2, y2, 200, direction='up')   
    d(doc, x2, y2, x3, y3, 100, direction='left')       
    d(doc, x4, y4, x5, y5, 100, direction='right')  
    d(doc, x6, y6, x5, y5, 100, direction='up')  
    d(doc, x17, y17, x2, y2,  100, direction='up')  

    d(doc,  x3, y3, x15, y15-10,  70, direction='down')  
    d(doc, x16, y16-10, x15, y15-10,  145, direction='down')  
    d(doc, x16, y16-10, x4, y4,  220, direction='down')      
    d(doc, x3, y3, x4, y4, 300, direction='down')  

    # description    
    desx = x1 - 200
    desy = y1 + 450
    textstr = f"Part Name : CAR COLUMN #2"     
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : {Spec}"    
    draw_Text(doc, desx , desy -60 , 35, str(textstr), layer='0')    
    textstr = f"Quantity : {SU} EA"    
    draw_Text(doc, desx , desy - 120 , 35, str(textstr), layer='0')        




    ###################################################
    # '역 ㄴ'자 1번 11번 하부 컬럼이나 일체형 기둥 고정용 바닥 bracket
    ###################################################

    rx = math.floor(pagex) + 5000
    ry = pagey + 1500

    rib_length = 30
    x1 = rx
    y1 = ry
    x2 = x1 + rib_length 
    y2 = y1    
    x3 = x2
    y3 = y2 + 100.5
    x4 = x3 - rib_length
    y4 = y3 

    # 참고용이므로 '레이져'가 아닌 '0' 사용
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 4
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    # 8x16 세로방향 장공 
    x5 , y5 =  x1+15, y1 + 24 - (column_BottomHoleHorizontal)

    # print (f"frontholes : {frontholes}")
    # draw_circle(doc, x9,y9,2.5,layer="레이져")
    insert_block(x5,y5,"8x16_vertical_draw")
      
    # 하부 치수선
    d(doc, x5,y5,x2,y2,80,direction="down")
    d(doc, x1,y1,x2,y2,140,direction="down")
    
    # 우측 치수    
    d(doc, x2,y2,x3,y3,260,direction="right")
    # 좌측 치수
    d(doc, x5,y5,x1,y1,60,direction="left")

    # description    
    desx = x1 + rib_length/2 - 300
    desy = y1 - 300
    textstr = f"Part Name : COLUMN BRACKET"    
    draw_Text(doc, desx , desy , 35 , str(textstr), layer='0')    
    textstr = f"Mat.Spec : EGI 2.0T"    
    draw_Text(doc, desx , desy -70 , 35, str(textstr), layer='0')    
    textstr = f"Size : 100.5 x 30 mm"    
    draw_Text(doc, desx , desy - 140 , 35, str(textstr), layer='0')        
    textstr = f"Quantity : {SU*2} EA"    
    draw_Text(doc, desx , desy - 210 , 35, str(textstr), layer='0')               

    ################
    # 단면도 하부 컬럼 '역 ㄴ'자 형태
    ################    

    rib_bottomwing = 24
    rib_height = 80
    rib_thickness = 2.0

    x1 = rx -  350
    y1 = y1 + 35
    x2 = x1 + rib_bottomwing 
    y2 = y1
    x3 = x2 
    y3 = y2 + rib_height
    x4 = x3 - rib_thickness
    y4 = y3 
    x5 = x4  
    y5 = y4 - rib_height + rib_thickness
    x6 = x5 - rib_bottomwing + rib_thickness
    y6 = y5

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 6
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x7 = x2 - (column_BottomHoleHorizontal)
    y7 = y2

    line(doc, x7,y7-10, x7,y7+10, layer='0')
        
    # 하부
    d(doc, x7,y7-10,x2,y2,100,direction="down")
    d(doc, x1,y1,x2,y2,160,direction="down")
    # 우측 치수
    d(doc, x2,y2,x3,y3,80,direction="right")


    #######################################
    # 13page 컬럼 단면도 - 설명자료
    #######################################
    rx = math.floor(pagex) + 3500
    ry = pagey + 1700

    rectangle(doc, rx-500, ry+1000, rx + 2000, ry-1500)
     
    x1 = rx + panel_wing 
    y1 = ry
    x2 = x1 - panel_wing   
    y2 = y1 
    x3 = x2 
    y3 = y2 - column_thickness
    x4 = x3 + column_width
    y4 = y3 
    x5 = x4 
    y5 = y4 + column_thickness
    x6 = x5 - column_thickness
    y6 = y5 
    x7 = x6 
    y7 = y6 - thickness
    x8 = x7 + column_thickness - thickness 
    y8 = y7 
    x9 = x8 
    y9 = y8  - column_thickness + thickness*2
    x10 = x9 - column_width + thickness*2 
    y10 = y9 
    x11 = x10 
    y11 = y10 + column_thickness - thickness*2 
    x12 = x11 + panel_wing - thickness  
    y12 = y11    
    
    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 12
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
        prev_x, prev_y = curr_x, curr_y
    line(doc, prev_x, prev_y, x1, y1, layer="0")     

    x15 = x4 - 20
    y15 = y4 
    x16 = x15 - 30
    y16 = y15 
    x17 = x6 + panel_width/2
    y17 = y6

    center_x, center_y = x3 + panel_wing + thickness + 15, y3 + thickness + column_BottomHoleHorizontal

    insert_block(center_x, center_y , "8x16_horizontal_draw")

    assx , assy = x2 + 150  , y3 - 800
    insert_block(assx , assy, "column_assembly")

    # 컬럼 고정용 브라켓 그려주기
    rectangle(doc, x1, y1 + thickness , x1 + 30, y3 + thickness)
    rectangle(doc, x1, y3 + thickness , x1 + 30, y3 + thickness + 2 )

    d(doc, x1, y1 + thickness , x1 + 30, y1 + thickness,  100, direction='up')
    d(doc, center_x, center_y , x3, y3,  100, direction='down')
    d(doc, center_x, center_y , x4, y4,  100, direction='down')    
    d(doc, x3, y3, x4, y4, 200, direction='down')  
    d(doc, x3, y3,center_x, center_y , 150, direction='left')  

    # description    
    desx = x1 - 400
    desy = y1 + 400
    textstr = f"#1,2 조립도"    
    draw_Text(doc, desx , desy , 100 , str(textstr), layer='0')    

    desx = x1 - 300
    desy = y1 - 1200    
    textstr = f"#1,2 조립(접착) "    
    draw_Text(doc, desx , desy , 100 , str(textstr), layer='0')    

    frameXpos = frameXpos + TargetXscale + 400

    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################
    ############################################################












# @Gooey(program_name='Jamb cladding 자동작도 프로그램 ver01', tabbed_groups=True, navigation='Tabbed')
@Gooey(encoding='utf-8', program_name='엘리베이터 판넬 자동작도 프로그램', tabbed_groups=True, navigation='Tabbed', show_success_modal=False,  default_size=(800, 600))

def main():
    global args  #수정할때는 global 선언이 필요하다. 단순히 읽기만 할때는 필요없다.    
    global start_time
    global workplace, drawdate, deadlinedate, lctype, secondord, text_style, exit_program, Vcut_rate, Vcut, program_message, formatted_date, text_style_name
    global CW_raw, CD_raw, panel_thickness, thickness,  LCframeMaterial, LCplateMaterial
    global input_CD, input_CW,CD,CW,drawdate_str , deadlinedate_str, drawdate_str_short, deadlinedate_str_short
    global doc, msp , text_style, OP, KPH, OPH, br, TRH

    # 현재 날짜와 시간을 가져옵니다.
    current_datetime = datetime.now()

    # 2023-12-10 원하는 형식으로 날짜를 문자열로 변환합니다.
    formatted_date = current_datetime.strftime('%Y-%m-%d')

    # 현재 날짜와 시간을 '년월일_시분초' 형식으로 가져옴
    # current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    current_time = datetime.now().strftime("%H%M%S")

    # print (f"xlsm_files {xlsm_files}")

    # .xlsm 파일이 없을 경우 오류 메시지를 출력하고 실행을 중단
    if not xlsm_files:
        raise FileNotFoundError(".xlsm 파일이 excel파일 폴더에 없습니다. 확인바랍니다.")

    # 찾은 .xlsm 파일 목록 순회
    for file_path in xlsm_files:

        # 엑셀 파일 열기
        # file_path = xlsm_files[0]
        workbook = openpyxl.load_workbook(file_path, data_only=True)

        sheet_name = '발주(수정)'  # 원하는 시트명으로 변경 기본정보가 있는 시트
        sheet = workbook[sheet_name]

        # doc = ezdxf.readfile(os.path.join(application_path, 'dimstyle', 'style1.dxf'))
        doc = ezdxf.readfile(os.path.join(application_path, 'dimstyle', 'miraestyle.dxf'))
        msp = doc.modelspace()                

        variable_names = {
            "D2": "company",
            "D3": "workplace",
            "P2": "drawnby",
            "P3": "issuedate",
            "W2": "usage",
            "D6": "openType",
            "G6": "person",
            "J6": "SU",
            "M6": "carOP",
            "P6": "carOPH",
            "S6": "KH",
            "V6": "FH",
            "D7": "Material",
            "P7": "Spec",
            "D8": "thickness_string",
            "J8": "Vcut",
            "P8": "doorDevice",
            "A12": "CW",
            "D12": "CD",
            "G12": "CH",
            "J12": "popnut_height",
            "M12": "CPH",
            "V11": "SIDE",
            "V12": "REAR",
            "A14": "WF",
            "D14": "WS",
            "G14": "WSM",
            "J14": "WR",
            "M14": "WRM",
            "Q14": "trimMaterial",
            "S14": "TR1",
            "T14": "TR2",
            "U14": "TR3",
            "V14": "TR4",
            "W14": "TR5",
            "X14": "TR6",
            "D17": "P1_material",
            "H17": "P1_width",
            "J17": "P1_widthReal",
            "L17": "P1_holegap",
            "O17": "P1_hole1",
            "Q17": "P1_hole2",
            "S17": "P1_hole3",
            "U17": "P1_hole4",
            "W17": "P1_COPType",
            "D18": "P2_material",
            "H18": "P2_width",
            "J18": "P2_widthReal",
            "L18": "P2_holegap",
            "O18": "P2_hole1",
            "Q18": "P2_hole2",
            "S18": "P2_hole3",
            "U18": "P2_hole4",
            "W18": "P2_COPType",
            "D19": "P3_material",
            "H19": "P3_width",
            "J19": "P3_widthReal",
            "L19": "P3_holegap",
            "O19": "P3_hole1",
            "Q19": "P3_hole2",
            "S19": "P3_hole3",
            "U19": "P3_hole4",
            "W19": "P3_COPType",
            "D20": "P4_material",
            "H20": "P4_width",
            "J20": "P4_widthReal",
            "L20": "P4_holegap",
            "O20": "P4_hole1",
            "Q20": "P4_hole2",
            "S20": "P4_hole3",
            "U20": "P4_hole4",
            "W20": "P4_COPType",
            "D21": "P5_material",
            "H21": "P5_width",
            "J21": "P5_widthReal",
            "L21": "P5_holegap",
            "O21": "P5_hole1",
            "Q21": "P5_hole2",
            "S21": "P5_hole3",
            "U21": "P5_hole4",
            "W21": "P5_COPType",
            "D22": "P6_material",
            "H22": "P6_width",
            "J22": "P6_widthReal",
            "L22": "P6_holegap",
            "O22": "P6_hole1",
            "Q22": "P6_hole2",
            "S22": "P6_hole3",
            "U22": "P6_hole4",
            "W22": "P6_COPType",
            "D23": "P7_material",
            "H23": "P7_width",
            "J23": "P7_widthReal",
            "L23": "P7_holegap",
            "O23": "P7_hole1",
            "Q23": "P7_hole2",
            "S23": "P7_hole3",
            "U23": "P7_hole4",
            "W23": "P7_COPType",
            "D24": "P8_material",
            "H24": "P8_width",
            "J24": "P8_widthReal",
            "L24": "P8_holegap",
            "O24": "P8_hole1",
            "Q24": "P8_hole2",
            "S24": "P8_hole3",
            "U24": "P8_hole4",
            "W24": "P8_COPType",
            "D25": "P9_material",
            "H25": "P9_width",
            "J25": "P9_widthReal",
            "L25": "P9_holegap",
            "O25": "P9_hole1",
            "Q25": "P9_hole2",
            "S25": "P9_hole3",
            "U25": "P9_hole4",
            "W25": "P9_COPType",
            "D26": "P10_material",
            "H26": "P10_width",
            "J26": "P10_widthReal",
            "L26": "P10_holegap",
            "O26": "P10_hole1",
            "Q26": "P10_hole2",
            "S26": "P10_hole3",
            "U26": "P10_hole4",
            "W26": "P10_COPType",
            "D27": "P11_material",
            "H27": "P11_width",
            "J27": "P11_widthReal",
            "L27": "P11_holegap",
            "O27": "P11_hole1",
            "Q27": "P11_hole2",
            "S27": "P11_hole3",
            "U27": "P11_hole4",
            "W27": "P11_COPType",
            "A32": "COP_bottomHeight",
            "C32": "COP_centerdistance",
            "D32": "COP_width",
            "F32": "COP_height",
            "H32": "COP_holegap",
            "J32": "COP_RibType",
            "A35": "HOP_bottomHeight",
            "D35": "HOP_width",
            "F35": "HOP_height",
            "H35": "HOP_holegap",
            "J35": "HOP_RibType",
            "P31": "HRType",
            "V31": "handrail_height",
            "M33": "handrailSidegap1",
            "O33": "handrailSidegap2",
            "Q33": "handrailSidegap3",
            "S33": "handrailSidegap4",
            "U33": "handrailSidegap5",
            "W33": "HRFrontHolesize",
            "M35": "handrailReargap1",
            "O35": "handrailReargap2",
            "Q35": "handrailReargap3",
            "S35": "handrailReargap4",
            "U35": "handrailReargap5",
            "W35": "HRRearHolesize",
            "J38": "KP_material",
            "A43": "TR_OP",
            "C43": "TR_TRH",
            "E43": "TR_upperhole1",
            "G43": "TR_upperhole2",
            "I43": "TR_upperhole3",
            "K43": "TR_upperhole4",
            "M42": "TR_material",
            "Q41": "CPIType",
            "Q42": "CPIHoleWidth",
            "S42": "CPIHoleHeight",
            "W42": "CPIholegap",
            "Y42": "CPIHeight",
            "Q43": "updateCPIHoleWidth",
            "S43": "updateCPIHoleHeight",
            "W43": "updateCPIholegap",
            "Y43": "updateCPIHeight",
            "A47": "COL_Height",
            "D47": "column_thickness",
            "G47": "column_width",
            "J47": "COL_FH",
            "M46": "COL_Material",
            "O47": "column_BottomHoleHorizontal",
            "U47": "column_BottomHoleVertical",
            "A52": "ELB_BottomHeight",
            "D52": "ELB_BoxHorizontal",
            "G52": "ELB_BoxVertical",
            "J52": "ELB_RibType",
            "P50": "CartP_Type",       
            "V50": "CartP_Height",
            "M52": "CartP_holegap1",
            "O52": "CartP_holegap2",
            "Q52": "CartP_holegap3",
            "S52": "CartP_holegap4",
            "U52": "CartP_holegap5",
            "W52": "CartP_HoleSize",
            "X6": "panel_width"
        }

        for cell_ref, var_name in variable_names.items():
            globals()[var_name] = read_excel_value(sheet, cell_ref)

        # 데이터 출력
        data = [(var_name, globals()[var_name]) for cell_ref, var_name in variable_names.items()]
        # for label, value in data:
            # print(f"{label} : {value}")            

        KPH = KH + FH 
        OP = carOP

        # 먼저 변수 존재 여부와 그 값이 None이 아닌지 확인
        for index in range(1, 12):
            width_real_var = f"P{index}_widthReal"
            width_var = f"P{index}_width"
            # print(f"width_real_var {width_real_var} :  width_var {width_var}")   

            # 실제 값이 존재하고 비어있지 않은지 확인
            width_real_value = globals().get(width_real_var)
            if width_real_value is not None and width_real_value.strip() != "":
                globals()[width_var] = width_real_value                
        # updateCPI 관련 조건문
        updateCPIHoleWidth = globals().get("updateCPIHoleWidth")
        if updateCPIHoleWidth is not None and updateCPIHoleWidth.strip() != "":
            CPIHoleWidth = updateCPIHoleWidth
        # 이와 유사한 방식으로 나머지 변수들에 대해서도 적용
        updateCPIHoleHeight = globals().get("updateCPIHoleHeight")
        if updateCPIHoleHeight is not None and updateCPIHoleHeight.strip() != "":
            CPIHoleHeight = updateCPIHoleHeight
        updateCPIholegap = globals().get("updateCPIholegap")
        if updateCPIholegap is not None and updateCPIholegap.strip() != "":
            CPIholegap = updateCPIholegap

        updateCPIHeight = globals().get("updateCPIHeight")
        if updateCPIHeight is not None and updateCPIHeight.strip() != "":
            CPIHeight = updateCPIHeight

        # 초기 변수 할당
        FileSaveAsName = f"{workplace}({company})"
        thickness = float(re.sub("[A-Z]", "", thickness_string))  # 1.5T를 1.5로 숫자 표현

        # 연신율을 결정하는 변수
        if Vcut == "적용":
            br = thickness / 2
        else:
            br = thickness

        WorkTitle = f"업체명 : {company}, 현장명 : {workplace}, Material : {Material}, Spec : {Material}{Spec}, thickness : {thickness}, V-cut : {Vcut}"

        OP = carOP
        OPH = carOPH
        TRH = TR_TRH
        
        # FloorDes = f"CO-{math.floor(carOP)} / {math.floor(person)}인승 (W{math.floor(CW)} X D{math.floor(CD)}) {math.floor(SU)}대분"        

        # 연신율을 결정하는 변수 수정
        if Vcut == "적용":
            if thickness == 1.2:
                br = 0.5
            else:
                br = 1.0
        else:  # No cut인 경우
            if thickness == 1.2:
                br = 1
            else:
                br = 1.5

        # 트림 존재 여부
        global TR1, TR2, TR3, TR4, TR5, TR6
        TR1 = 0  # 혹은 적절한 다른 초기값
        TR2 = 0
        TR3 = 0
        TR4 = 0
        TR5 = 0
        TR6 = 0

        TRIM_IS = 1 if TR1 > 0 or TR2 > 0 or TR3 > 0 or TR4 > 0 or TR5 > 0 or TR6 > 0 else 0

        UnitTotalSET = math.floor(SU)

        # 트림 관련 변수 공백 처리
        TR1 = 0 if isinstance(TR1, str) and TR1.strip() == "" else TR1
        TR2 = 0 if isinstance(TR2, str) and TR2.strip() == "" else TR2
        TR3 = 0 if isinstance(TR3, str) and TR3.strip() == "" else TR3
        TR4 = 0 if isinstance(TR4, str) and TR4.strip() == "" else TR4
        TR5 = 0 if isinstance(TR5, str) and TR5.strip() == "" else TR5
        TR6 = 0 if isinstance(TR6, str) and TR6.strip() == "" else TR6

        # P1부터 P11까지의 hole2와 hole3 변수 처리
        for index in range(1, 12):  # 1부터 11까지 반복
            left_second_var = f"P{index}_hole2"
            right_second_var = f"P{index}_hole3"

            # P{index}_hole2 확인 및 처리
            if isinstance(globals().get(left_second_var, ""), str):
                globals()[left_second_var] = 0 if globals()[left_second_var].strip() == "" else globals()[left_second_var]

            # P{index}_hole3 확인 및 처리
            if isinstance(globals().get(right_second_var, ""), str):
                globals()[right_second_var] = 0 if globals()[right_second_var].strip() == "" else globals()[right_second_var]
        
        # 작도일자 추출
        # drawdate_str = "{0}년 {1:02d}월 {2:02d}일".format(drawdate.year, drawdate.month, drawdate.day)
        # drawdate_str_short = "{0:02d}/{1:02d}".format(drawdate.month, drawdate.day)

        # if input_CD not in [None, '', 0] and input_CW not in [None, '', 0]:
        #     # input_CD와 input_CW가 모두 공백이나 0이 아닌 경우 실행할 코드 강제입력에 대한 처리
        #     CW = input_CD
        #     CD = input_CW
        # else:    
        #     CW = CW_raw - panel_thickness * 2
        #     CD = CD_raw - panel_thickness * 2

        # 파일 이름에 사용할 수 없는 문자 정의        
        invalid_chars = '<>:"/\\|?*'
        # 정규식을 사용하여 유효하지 않은 문자 제거
        cleaned_file_name = re.sub(f'[{re.escape(invalid_chars)}]', '', f"{company}_{workplace}_CW{str(CW)}xCD{str(CD)}_{current_time}")

        # 파이썬이 있는 폴더
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # 결과 파일 이름
        file_name = f"{cleaned_file_name}.dxf"
        # 전체 파일 경로 생성
        full_file_path = os.path.join(script_directory, file_name)        
        file_name = full_file_path

        exit_program = False

        program_message = \
            '''
        프로그램 실행결과입니다.
        -------------------------------------
        {0}
        -------------------------------------
        이용해 주셔서 감사합니다.
        '''    

        # saved_disk_id = load_env_settings()
        # current_disk_id = get_current_disk_id()

        # if saved_disk_id is None or saved_disk_id != current_disk_id:
        #     print("라이센스를 구매해 주세요.")

        #     args = parse_arguments_settings()                    

        #     if args.config:
        #         if args.password == '123456':  # '1234'는 원하는 비밀번호로 변경            
        #             print("라이센스가 설정되었습니다. 다시 시작해 주세요.")
        #             envsettings() 
        #             sys.exit()           
        #         else:
        #             print("잘못된 비밀번호입니다.")
        #             print("라이센스를 구매해 주세요.")
        #             sys.exit()

        # else:
        #     print("환영합니다! 프로그램을 실행합니다.")

        args = parse_arguments()    
        # 숫자로 변수를 선언해 준다.
        
        # 프로그램 시작 시간 기록
        start_time = time.time()

        # print("설정상태 : ")
        # print(args)

        # if args.config:
        #     if args.password == '123456':  # '1234'는 원하는 비밀번호로 변경            
        #         print("라이센스가 설정되었습니다. 다시 시작해 주세요.")
        #         envsettings()            
        #     else:
        #         print("잘못된 비밀번호입니다.")
        #         print("라이센스를 구매해 주세요.")
        #         sys.exit()

        if not args.config:
            if '일체' in doorDevice:
                draw_page1()
            else:
                draw_page2() # 분리형

        file_path = save_file(company, workplace, CW, CD)
        doc.saveas(file_path)
        print(f" 저장 파일명: '{file_name}' 저장 완료!")                

        # # display_message()    
        # end_time = time.time()

        # # 실행 시간 계산
        # execution_time = end_time - start_time

        # # 시간 형식으로 변환
        # hours, remainder = divmod(execution_time, 3600)
        # minutes, seconds = divmod(remainder, 60)

        # parts = []
        # if hours:
        #     parts.append(f"{int(hours)}h")
        # if minutes:
        #     parts.append(f"{int(minutes)}m")
        # parts.append(f"{int(seconds) + 3 }초")  

        # formatted_execution_time = " ".join(parts)

        # # 생성된 파일 이름으로 DXF 파일 저장
        # doc.saveas(file_name)
        # print(f" 실행 시간: {formatted_execution_time}, 파일명: '{file_name}' 저장 완료!")      
        # 
        
        # try:
        #     result = 10 / 0
        #     print("나눗셈 결과:", result)
        # except ZeroDivisionError:
        #     error_message = "0으로 나눌 수 없습니다. 다른 숫자를 입력하세요."
        #     messagebox.showerror("에러", error_message)  # 메시지 박스를 띄웁니다.
        #     sys.exit(1)    # 강제종료하는 것임 (1)

        # 에러 메시지를 아래와 같이 표시할 수 있다.
        # error_message = "0으로 나눌 수 없습니다. 다른 숫자를 입력하세요."
        # messagebox.showerror("에러", error_message)  # 메시지 박스를 띄웁니다.


if __name__ == '__main__':
    main()
    sys.exit()