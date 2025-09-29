## 새로운 로직개발 헤밍구조에 대한 통합버전 개발 쪽쟘, 멍텅구리 통합
## 실전 사용하면서 수정사항 반영 B1, B2 크기 조정 pyinstaller 실행 후 반영되는 값 적용
## 작지 양식 일부 수정 라이트케이스 크기 강제입력 부분 추가 24/03/05
## LED는 CD값이 1030인 경우는 기본 -100 처리 후 930이면 950으로, 즉 50단위로 생성해야 한는데, 30이면 30을 버리는 것이 아니라 50으로 만든다.

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
        
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')    

# 전역 변수 초기화
saved_Xpos = 0
saved_Ypos = 0
saved_direction = "up"
saved_text_height = 0.20
saved_text_gap = 0.05
dimdistance = 0
dim_horizontalbase = 0
dim_verticalbase = 0
start_time = 0

workplace = ""
drawdate = None
deadlinedate = None
lctype = ""
secondord = ""
CW_raw = 0
CD_raw = 0
panel_thickness = 0
su = 0
LCframeMaterial = ""
LCplateMaterial = ""
input_CD = 0
input_CW = 0
CD = 0
CW = 0
drawdate_str = ""
deadlinedate_str = ""
T5_is =""

# 폴더 내의 모든 .xlsm 파일을 검색
application_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
excel_saved_file = os.path.join(application_path, 'ceiling_excel')
xlsm_files = glob.glob(os.path.join(excel_saved_file, '*.xlsm'))
jamb_ini = os.path.join(application_path, 'data', 'jamb.json')
license_file_path = os.path.join(application_path, 'data', 'hdsettings.json') # 하드디스크 고유번호 인식

# DXF 파일 로드
doc = ezdxf.readfile(os.path.join(application_path, 'dimstyle', 'ceilingstyle4.dxf'))
msp = doc.modelspace()

# 찾은 .xlsm 파일 목록 출력
# for xlsm_file in xlsm_files:
#     print(xlsm_file)


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

# 환경설정 가져오기(하드공유 번호)
def load_env_settings():
    try:
        with open(license_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get("DiskID")
    except FileNotFoundError:
        return None

def get_current_disk_id():
    return os.popen('wmic diskdrive get serialnumber').read().strip()

# None이면 0을 리턴하는 함수
def validate_or_default(value):
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

def dim_leader_line(doc, start_x, start_y, end_x, end_y, text, layer='JKW', style='0', text_height=22):
    msp = doc.modelspace()

    text_style_name = 'JKW'
        
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

    # 텍스트 추가 (선택적)
    if text:
        msp.add_mtext(text, dxfattribs={
            'insert': (end_x + 10, end_y + 5),  # 텍스트 위치 조정
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

        print(f"prev_x {prev_x}" )
        print(f"prev_y {prev_y}" )
    
    # 마지막으로 첫번째 점과 연결
    line(doc, prev_x, prev_y, firstX , firstY, layer)        

def rectangle(doc, x1, y1, dx, dy, layer=None):
    # 네 개의 선분으로 직사각형 그리기
    line(doc, x1, y1, dx, y1, layer=layer)   
    line(doc, dx, y1, dx, dy, layer=layer)   
    line(doc, dx, dy, x1, dy, layer=layer)   
    line(doc, x1, dy, x1, y1, layer=layer)   

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

def dim_angular(doc, x1, y1, x2, y2, x3, y3, x4, y4, distance=80, direction="left", dimstyle="JKW"):
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

def dim_diameter(doc, center, diameter, angle, dimstyle="JKW", override=None):
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

def dim_string(doc, x1, y1, x2, y2, dis,  textstr,  text_height=0.20, text_gap=0.05, direction="up"):
    msp = doc.modelspace()
    dim_style = 'JKW'
    layer = "JKW"

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

def dim(doc, x1, y1, x2, y2, dis, text_height = None, text_gap=0.02, direction="up", option =None ,startoption=None):    
    global saved_Xpos
    global saved_Ypos
    global saved_text_height
    global saved_text_gap
    global saved_direction
    global dimdistance
    global dim_horizontalbase
    global dim_verticalbase

    # 치수선이 왼쪽 오른쪽 튀어나오게 할때 reverse를 주면 연속으로 치수선 뽑을때 활용한다.
    if( option == 'reverse'):
        saved_Xpos = x1    
        saved_Ypos = y1
    else:
        saved_Xpos = x2    
        saved_Ypos = y2

    if text_height is None :
        text_height = 0.22                

    dimdistance=dis
    saved_text_height = text_height
    saved_text_gap = text_gap
    saved_direction = direction           

    # 연속선 구현을 위한 구문
    if startoption is None :
        if direction == "left":            
            dim_horizontalbase = extract_abs(x1,x2) + dis
        if direction == "right":                        
            dim_horizontalbase = dis - extract_abs(x1,x2) 
        if direction == "up":            
            dim_verticalbase = extract_abs(y1,y2) + dis
        if direction == "down":                        
            dim_verticalbase = dis - extract_abs(y1,y2) 

    # if(direction=='right'):
    #     dim_vertical_right(doc, x1, y1, x2, y2, dis, text_height=text_height)
    #     return
    
    msp = doc.modelspace()
    dim_style = 'JKW'
    layer = "JKW"

    points = [(x1, y1), (x2, y2)]

    # 치수값 계산
    dimension_value = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # 소수점이 있는지 확인
    if dimension_value % 1 != 0:
        dimdec = 1  # 소수점이 있는 경우 소수점 첫째 자리까지 표시
    else:
        dimdec = 0  # 소수점이 없는 경우 소수점 표시 없음

    # # 치수선을 왼쪽에 표시할때는 text_gap 조정
    # if direction == "left" :    
    #     text_gap = text_height*-1 - 0.05

    # override 설정
    override_settings = {
        'dimtxt': text_height,
        'dimgap': 0.02,
        'dimscl': 1,
        'dimlfac': 1,
        'dimclrt': 7,
        'dimdsep': 46,        # 소수점 문자로 표현됨 아니면 콤마 나옴
        'dimdec': dimdec,
        'dimtix': 1  # 필요에 따라 치수선 내부에 텍스트를 표시 이것을 1로 해야 치수선위에 치수선 문자가 정렬되어 보인다
        # 'dimsoxd': 2  # 확장선 바깥으로 텍스트 이동        
    }

    # 방향에 따른 치수선 추가
    if direction == "up":
        return msp.add_linear_dim(
            base=(x1, y1 + dis),
            dimstyle=dim_style,
            p1=(x1, y1),  # 1st measurement point
            p2=(x2, y2),  # 2nd measurement point
            # points=points,
            # dxfattribs={'layer': layer},
            override=override_settings
        )
    elif direction == "down":
        return msp.add_linear_dim(
            dimstyle=dim_style,
            base=(x1, y1 - dis),
            # points=points,
            # dxfattribs={'layer': layer},
            p1=(x1, y1),  # 1st measurement point
            p2=(x2, y2),  # 2nd measurement point            
            override=override_settings
        )
    elif direction == "left":
        anglesetting = 90      
        return msp.add_linear_dim(
            dimstyle=dim_style,
            base=(x1 - dis, y1),
            p1=(x1, y1),  # 1st measurement point
            p2=(x2, y2),  # 2nd measurement point               
            angle = anglesetting,
            # points=points,
            # dxfattribs={'layer': layer},
            override=override_settings
        )
    elif direction == "right":
        anglesetting = -90      
        return msp.add_linear_dim(
            dimstyle=dim_style,
            base=(x1 + dis, y1),
            p1=(x1, y1),  # 1st measurement point
            p2=(x2, y2),  # 2nd measurement point                
            angle = anglesetting,
            # points=points,
            # dxfattribs={'layer': layer},
            override=override_settings
        )
    elif direction == "aligned":
        return msp.add_multi_point_linear_dim(
            dimstyle=dim_style,
            points=points,
            distance=dis,
            dxfattribs={'layer': layer},
            override=override_settings
        )
    else:
        raise ValueError("Invalid direction. Use 'up', 'down', 'left', 'right' , 'aligned' .")

def dimcontinue(doc, x, y) :    
    global saved_Xpos
    global saved_Ypos
    global saved_text_height
    global saved_text_gap
    global saved_direction
    global dimdistance
    global dim_horizontalbase
    global dim_verticalbase

    x1 = saved_Xpos
    y1 = saved_Ypos
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

    print(f"x1 : {x1},  y1 : {y1}, x2 : {x2}, y2 : {y2}, direction : {saved_direction} , dimdistance : {dimdistance}  ")

    # if option is not None :
    #     option = option
    #     # x1, y1 swap x2, y2
    #     tmpx = saved_Xpos
    #     tmpy = saved_Ypos        
    #     saved_Xpos = x2
    #     saved_Ypos = y2
    #     x2 = tmpx
    #     y2 = tmpy    

    dim(doc, x1, y1, x2, y2, dimdistance, text_height=saved_text_height, text_gap=saved_text_gap, direction=saved_direction, startoption='continue')

def dimto(doc, x2, y2, dis, text_height=0.20, text_gap=None, option=None) :    
    global saved_Xpos
    global saved_Ypos
    global saved_text_height
    global saved_text_gap
    global saved_direction

    if text_gap is not None :
        text_gap = saved_text_gap
        saved_text_gap = text_gap

    if text_height is not None :
        text_height = saved_text_height
        saved_text_height = text_height

    # if option is not None :
    #     option = option
    #     # x1, y1 swap x2, y2
    #     tmpx = saved_Xpos
    #     tmpy = saved_Ypos        
    #     saved_Xpos = x2
    #     saved_Ypos = y2
    #     x2 = tmpx
    #     y2 = tmpy    

    dim(doc, saved_Xpos, saved_Ypos, x2, y2, dis, text_height=text_height, text_gap=text_gap, direction=saved_direction, option=option)

def create_vertical_dim(doc, x1, y1, x2, y2, dis, angle, layer=None, text_height=0.20, text_gap=0.07):
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

def dim_vertical_right(doc, x1, y1, x2, y2, dis, layer="JKW", text_height=0.22,  text_gap=0.07, angle=None):
    return create_vertical_dim(doc, x1, y1, x2, y2, dis, angle, layer, text_height, text_gap)

def dim_vertical_left(doc, x1, y1, x2, y2, dis, layer=None, text_height=0.22,  text_gap=0.07):
    return create_vertical_dim(doc, x1, y1, x2, y2, dis, 90, layer, text_height, text_gap)
  
def create_vertical_dim_string(doc, x1, y1, x2, y2, dis, angle, textstr, text_height=0.22, text_gap=0.07):    
    msp = doc.modelspace()
    dim_style = 'JKW'
    layer = "JKW"
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

def dim_vertical_right_string(doc, x1, y1, x2, y2, dis, textstr, text_height=0.22,  text_gap=0.07):
    return create_vertical_dim_string(doc, x1, y1, x2, y2, dis, 270, textstr, text_height, text_gap)

def dim_vertical_left_string(doc, x1, y1, x2, y2, dis, textstr, text_height=0.22,  text_gap=0.07):
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
    DXF 문서에 원을 그리는 함수
    :param doc: ezdxf 문서 객체
    :param center_x: 원의 중심 x 좌표
    :param center_y: 원의 중심 y 좌표
    :param radius: 원의 반지름
    :param layer: 원을 추가할 레이어 이름 (기본값은 '0')
    지름으로 수정 /2 적용
    """
    msp = doc.modelspace()
    circle = msp.add_circle(center=(center_x, center_y), radius=radius/2, dxfattribs={'layer': layer, 'color' : color})
    return circle

# 중심선 적색표기 색상 1 적용 적색
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

def extract_abs(a, b):
    return abs(a - b)    

# 도면틀 삽입
def insert_block( x, y, block_name):    
    scale = 1
    insert_point = (x, y, scale)

    # 블록 삽입하는 방법           
    msp.add_blockref(block_name , insert_point, dxfattribs={
        'xscale': scale,
        'yscale': scale,
        'rotation': 0
    })       

# 도면틀 삽입
def insert_frame( x, y, scale , sep , text):    
    if(sep =="drawings_frame"):
        block_name = "drawings_frame"
        insert_point = (x, y, scale)

        # 블록 삽입하는 방법           
        msp.add_blockref(block_name , insert_point, dxfattribs={
            'xscale': scale,
            'yscale': scale,
            'rotation': 0
        })

        Textstr = f"{text}"       
        draw_Text(doc, x + 2220*scale, y + 220*scale , 23*scale , str(Textstr), '0')
        draw_Text(doc, x + (2200+160)*scale, y + (220-88)*scale   , 23*scale , "Light Case Accessory", '0')
        draw_Text(doc, x + (2200-320)*scale, y + (220-88)*scale   , 23*scale , formatted_date , '0')

def envsettings():
    # 하드디스크 고유번호를 가져오는 코드 (시스템에 따라 다를 수 있음)
    disk_id = os.popen('wmic diskdrive get serialnumber').read().strip()
    data = {"DiskID": disk_id}
    with open(license_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file)

# LED바 길이 계산 (1030, 등도 계산되도록 로직개발)
def CalculateLEDbar(car_length):
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

# Function to adjust coordinates with rounding and adding truncated decimals
def adjust_coordinates(coord1, coord2, coord3):
    adjusted_coord1 = round(coord1)
    decimal_part = coord1 - adjusted_coord1
    adjusted_coord2 = round(coord2 + decimal_part)
    adjusted_coord3 = round(coord3 + (coord2 - adjusted_coord2))

    return adjusted_coord1, adjusted_coord2, adjusted_coord3

def calculate_lc_position_031(inputCW, inputCD):
    # Calculate Y-coordinates for top and bottom holes
    Topholey = inputCD - 40
    Bottomy = 40

    # Initialize the list of x-coordinates for top and bottom holes
    Topholex = []
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

        Topholex = [x1, x2, x3, x4]
        Bottomx = [x1, x2, x3, x4]
    else:
        # For CW < 1400, there are 3 holes
        x1 = 115
        x2 = (inputCW - 115 * 2) / 2 + 115
        x3 = inputCW - 115
        Topholex = [x1, x2, x3]
        Bottomx = [x1, x2, x3]

    # Create a dictionary to hold the coordinates
    lc_positions = {
        'Topholex': Topholex,
        'Topholey': Topholey,
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
        print (f" end_digit : {end_digit}  , side_space : {side_space} , middle_space : {middle_space}")
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



# 좌측 치수선
dim(doc, 800, -5000, 820, -5300, 150,  text_height=0.30, text_gap=0.07, direction="left")
dimcontinue(doc, 800, -5600) 
dimcontinue(doc, 750, -5650) 
dimcontinue(doc, 720, -5700) 
dimcontinue(doc, 820, -5760) 

# 좌측 치수선
dim(doc, 800, -12000, 820, -12300, 250,  text_height=0.30, text_gap=0.07, direction="right")
dimcontinue(doc, 800, -12600) 
dimcontinue(doc, 750, -12650) 
dimcontinue(doc, 720, -12700) 
dimcontinue(doc, 820, -12760) 

dim(doc, 800, -16000, 860, -16005, 100,  text_height=0.30, text_gap=0.07, direction="up")
dimcontinue(doc, 890, -16010) 
dimcontinue(doc, 950, -16030) 
dimcontinue(doc, 1050, -16050) 
dimcontinue(doc, 1230, -16020) 

dim(doc, 800, -18000, 860, -18005, 100,  text_height=0.30, text_gap=0.07, direction="down")
dimcontinue(doc, 890, -18010) 
dimcontinue(doc, 950, -18030) 
dimcontinue(doc, 1050, -18050) 
dimcontinue(doc, 1230, -18020) 