# 미래기업 코딩수업 실전 프로젝트

import math
import ezdxf
from ezdxf.enums import TextEntityAlignment
import openpyxl
import os
import glob
import os
import sys
import io
from datetime import datetime
import warnings
import tkinter as tk
from tkinter import font

# 전역 변수 초기화
if True:
    BasicXscale, BasicYscale,TargetXscale,TargetYscale, frame_scale = 0,0,0,0,0
    frameXpos = 0
    frameYpos = 0
    thickness = 0    
    br = 0  # bending rate 연신율
    saved_DimXpos = 0
    saved_DimYpos = 0
    saved_Xpos = 0
    saved_Ypos = 0
    saved_direction = "up"
    saved_text_height = 0.30
    saved_text_gap = 0.05
    dimdistance = 0
    dim_horizontalbase = 0
    dim_verticalbase = 0
    distanceXpos = 0
    distanceYpos = 0
    start_time = 0   
    pagex = 0
    pagey = 0
    rx, ry = 0, 0

# 기본 설정
if True:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')    

    # 경고 메시지 필터링
    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.worksheet._reader")

    xlsx_files = glob.glob('c:\mywork\*.xlsx')

    doc = ezdxf.readfile('c:\mywork\mystyle.dxf')    
    msp = doc.modelspace()

    # TEXTSTYLE 정의
    text_style_name = 'H'  # 원하는 텍스트 스타일 이름

def setpos(a, b, c, d):
    global BasicXscale, BasicYscale,TargetXscale,TargetYscale, frame_scale
    BasicXscale, BasicYscale,TargetXscale,TargetYscale = a, b, c, d
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale
    pagex, pagey = frameXpos , frameYpos + 1123 * frame_scale
    rx, ry = pagex , pagey 
    return rx, ry , pagex , pagey, frame_scale

def read_excel_value(sheet, cell):
    value = sheet[cell].value
    if isinstance(value, str):
        try:
            float_value = float(value)  # 문자열을 float로 변환 시도
            if float_value.is_integer():  # 소수점이 없는 경우
                return int(float_value)
            else:  # 소수점이 있는 경우
                return float_value
        except ValueError:
            return value  # 변환할 수 없는 경우 원래 문자열 반환
    return value

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
def draw_slot(doc, x, y, size, direction="가로", option=None, layer='0'):
    """
    Draws a slot (장공) with specified parameters in a DXF document.
    
    Parameters:
    doc (ezdxf.document): The DXF document to draw on.
    x (float): The x-coordinate of the slot's center.
    y (float): The y-coordinate of the slot's center.
    size (str): The size of the slot in the format 'WxH' (e.g., '8x16').
    direction (str): The direction of the slot, either '가로' (horizontal) or '세로' (vertical). Default is '가로'.
    option (str): Optional feature for the slot. If 'cross', draws center lines extending beyond the slot. Default is None.
    layer (str): The layer to draw the slot on. Default is '0'.
    """    
    msp = doc.modelspace()

    # size를 분리하여 폭과 높이 계산
    width, height = map(int, size.lower().split('x'))

    if direction == "가로":
        slot_length = height
        slot_width = width
    else:  # 세로
        slot_length = width
        slot_width = height

    radius = slot_width / 2

    # 중심점을 기준으로 시작점과 끝점 계산
    if direction == "가로":
        start_point = (x - slot_length / 2, y)
        end_point = (x + slot_length / 2, y)
    else:  # 세로
        start_point = (x, y - slot_length / 2)
        end_point = (x, y + slot_length / 2)

    # 직선 부분 그리기
    if direction == "가로":
        msp.add_line((start_point[0], start_point[1] + radius), (end_point[0], end_point[1] + radius), dxfattribs={'layer': layer})
        msp.add_line((start_point[0], start_point[1] - radius), (end_point[0], end_point[1] - radius), dxfattribs={'layer': layer})
    else:  # 세로
        msp.add_line((start_point[0] + radius, start_point[1]), (end_point[0] + radius, end_point[1]), dxfattribs={'layer': layer})
        msp.add_line((start_point[0] - radius, start_point[1]), (end_point[0] - radius, end_point[1]), dxfattribs={'layer': layer})

    # 양 끝의 반원 그리기
    if direction == "가로":
        draw_arc(doc, start_point, radius, 90, 270, layer)
        draw_arc(doc, end_point, radius, -90, 90, layer)
    else:  # 세로
        draw_arc(doc, start_point, radius, 0, 180, layer)
        draw_arc(doc, end_point, radius, 180, 360, layer)

    # 옵션이 "cross"인 경우 중심선을 추가로 그리기
    if option == "cross":
        if direction == "가로":
            msp.add_line((x - slot_length / 2 - 4, y), (x + slot_length / 2 + 4, y), dxfattribs={'layer': 'CL'})
            msp.add_line((x, y - slot_width / 2 - 4), (x, y + slot_width / 2 + 4), dxfattribs={'layer': 'CL'})
        else:  # 세로
            msp.add_line((x - slot_width / 2 - 4, y), (x + slot_width / 2 + 4, y), dxfattribs={'layer': 'CL'})
            msp.add_line((x, y - slot_length / 2 - 4), (x, y + slot_length / 2 + 4), dxfattribs={'layer': 'CL'})
    return msp
def draw_crossmark(doc, x, y, layer='0'):
    """
    M4 육각 십자선 그림    
    """    
    line(doc, x,y-5,x,y+5,layer=layer)    
    line(doc, x-5,y,x+5,y,layer=layer)    
    return msp
def dim_leader(doc, start_x, start_y, end_x, end_y, text,text_height=30, direction=None, option=None):
    global saved_DimXpos, saved_DimYpos, saved_text_height, saved_text_gap, saved_direction, dimdistance, dim_horizontalbase, dim_verticalbase, distanceXpos, distanceYpos 
   
    direction='up'
    msp = doc.modelspace()
    layer = 'COPY OF ISO-25'        
    text_style_name = 'H'            
    # override 설정
    override_settings = {
        'dimasz': 15
    }

    # 지서선 추가
    leader = msp.add_leader(
        vertices=[(start_x, start_y), (end_x, end_y)],  # 시작점과 끝점
        dxfattribs={
            'dimstyle': text_style_name,
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

    if option is None:
        # 텍스트 추가 (선택적)
        if text:
            msp.add_mtext(text, dxfattribs={
                'insert': text_position,
                'layer': layer,
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
def circle_num(doc, x1, y1, x2, y2, text, option=None):
    msp = doc.modelspace()
    
    # 원 그리기
    radius = 60  # 원하는 반지름 설정
    msp.add_circle(
        center=(x2, y2),
        radius=radius,
        dxfattribs={'layer': '0'}
    )
    
    # 원 내부에 텍스트 추가
    msp.add_mtext(text, dxfattribs={
        'insert': (x2, y2),
        'layer': '0',
        'char_height': 45,        
        'attachment_point': 5  # 텍스트를 중앙에 배치
    })

    if option is None:
        # 원의 중심과 지시선 끝점 좌표를 사용하여 원의 둘레 상의 지시선 시작점 계산
        angle = math.atan2(y1 - y2, x1 - x2)
        start_x = x2 + radius * math.cos(angle)
        start_y = y2 + radius * math.sin(angle)

        # 지시선 그리기
        dim_leader(doc, start_x, start_y, x1, y1, text, text_height=30, direction='up', option='no draw Text')

    return msp
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
def dim_angular(doc, x1, y1, x2, y2, x3, y3, x4, y4, distance=80, direction="left", dimstyle="mydim"):
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
            override={'dimtxt': 0.27, 'dimgap': 0.02, 'dimscl' : 1, 'dimlfac' : 1, 'dimclrt': 7, 'dimdec': 0 } # 선색 백색 소수점 . 표기
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
            override={'dimtxt': 0.27, 'dimgap': 0.02, 'dimscl' : 1, 'dimlfac' : 1, 'dimclrt': 7, 'dimdec': 0 } # 선색 백색 소수점 . 표기
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
            override={'dimtxt': 0.27, 'dimgap': 0.02, 'dimscl' : 1, 'dimlfac' : 1, 'dimclrt': 7, 'dimdec': 0 } # 선색 백색 소수점 . 표기
        )        

    # 치수선의 기하학적 형태 생성
    dimension.render()
    return dimension
def dim_diameter(doc, center, diameter, angle, dimstyle="mydim", override=None):
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
def dim_string(doc, x1, y1, x2, y2, dis,  textstr,  text_height=0.30, text_gap=0.05, direction="up"):
    global saved_DimXpos, saved_DimYpos, saved_text_height, saved_text_gap, saved_direction, dimdistance, dim_horizontalbase, dim_verticalbase

    msp = doc.modelspace()
    dim_style = 'mydim'
    layer = "mydim"

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
def d(doc, x1, y1, x2, y2, dis, text_height=0.30, text_gap=0.05, direction="up", option=None, starbottomtion=None, text=None, dim_style=None):
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

    msp = doc.modelspace()
    layer = "mydim"
    if dim_style is None:        
        dim_style = 'mydim'
    else:        
        dim_style = dim_style

    # 치수값 계산
    dimension_value = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # 소수점 확인
    dimdec = 1 if dimension_value % 1 != 0 else 0

    # override 설정
    override_settings = {      
        'dimtxt': text_height,  
        'dimgap': text_gap if text_gap is not None else 0.05,
        'dimscl': 1,
        'dimlfac': 1,
        'dimclrt': 7,        
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
        if starbottomtion is None:
            distanceYpos = max(y1, y2) + dis
        if text is not None:
            add_dim_args['text'] = text
            return msp.add_linear_dim(**add_dim_args)
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
        if starbottomtion is None:
            distanceYpos = min(y1, y2) - dis
        if text is not None:
            add_dim_args['text'] = text
            return  msp.add_linear_dim(**add_dim_args)
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
            if starbottomtion is None:
                distanceXpos = min(x1, x2) - dis        
        if text is not None:
            add_dim_args['text'] = text
            return  msp.add_linear_dim(**add_dim_args)
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
        if starbottomtion is None:
            distanceXpos = max(x1, x2) + dis
        if text is not None:
            add_dim_args['text'] = text
            return  msp.add_linear_dim(**add_dim_args)
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
        if text is not None:
            add_dim_args['text'] = text
        return msp.add_multi_point_linear_dim(**add_dim_args)

    else:
        raise ValueError("Invalid direction. Use 'up', 'down', 'left', 'right', or 'aligned'.")
def dc(doc, x, y, distance=None, option=None, text=None, dim_style=None) :    
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
    if dim_style is None:        
        dim_style = 'mydim'
    else:        
        dim_style = dim_style               
    d(doc, x1, y1, x2, y2, dimdistance, text_height=saved_text_height, text_gap=saved_text_gap, direction=saved_direction, starbottomtion='continue', text=text,  dim_style = dim_style )
def dim(doc, x1, y1, x2, y2, dis, text_height=0.30, text_gap=0.05, direction="up", option=None, starbottomtion=None, text=None):
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

    msp = doc.modelspace()
    dim_style = 'mydim'
    layer = "mydim"

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
def create_vertical_dim(doc, x1, y1, x2, y2, dis, angle, layer=None, text_height=0.30, text_gap=0.05):
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
        override = {'dimtxt': text_height, 'dimgap': text_gap, 'dimscl': 1, 'dimlfac': 1, 'dimclrt': 7, 'dimdec': dimdec, 'dimtmove': 3  }
    )
def dim_vertical_right(doc, x1, y1, x2, y2, dis, layer="mydim", text_height=0.30,  text_gap=0.07, angle=None):
    return create_vertical_dim(doc, x1, y1, x2, y2, dis, angle, layer, text_height, text_gap)
def dim_vertical_left(doc, x1, y1, x2, y2, dis, layer="mydim", text_height=0.30,  text_gap=0.07):
    return create_vertical_dim(doc, x1, y1, x2, y2, dis, 90, layer, text_height, text_gap)
def create_vertical_dim_string(doc, x1, y1, x2, y2, dis, angle, textstr, text_height=0.30, text_gap=0.07):    
    msp = doc.modelspace()
    dim_style = 'mydim'
    layer = "mydim"
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
        override={'dimtxt': text_height, 'dimgap': text_gap, 'dimscl': 1, 'dimlfac': 1, 'dimclrt': 7, 'dimdec': dimdec,  'dimtmove': 3 , 'text' : textstr      }
    )
def dim_vertical_right_string(doc, x1, y1, x2, y2, dis, textstr, text_height=0.30,  text_gap=0.07):
    return create_vertical_dim_string(doc, x1, y1, x2, y2, dis, 270, textstr, text_height, text_gap)
def dim_vertical_left_string(doc, x1, y1, x2, y2, dis, textstr, text_height=0.30,  text_gap=0.07):
    return create_vertical_dim_string(doc, x1, y1, x2, y2, dis, 90, textstr, text_height, text_gap)
def draw_Text_direction(doc, x, y, size, text, layer=None, rotation = 90):
    # 모델 공간 (2D)을 가져옴
    msp = doc.modelspace()

    text_style_name ='GHS'
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
    msp = doc.modelspace()
    text_style_name ='LGIS'
    text_entity = msp.add_text(
        text,  # 텍스트 내용
        dxfattribs={
            'layer': layer,  # 레이어 지정
            'style': text_style_name,  # 텍스트 스타일 지정
            'height': size,  # 텍스트 높이 (크기) 지정
        }
    )
    text_entity.set_placement((x, y), align=TextEntityAlignment.BOTTOM_LEFT)

def draw_circle(doc, center_x, center_y, radius, layer='0', color='7'):
    msp = doc.modelspace()
    circle = msp.add_circle(center=(center_x, center_y), radius=radius/2, dxfattribs={'layer': layer, 'color' : color})
    return circle


def main():   
    global doc, msp

    for file_path in xlsx_files:
        workbook = openpyxl.load_workbook(file_path, data_only=True)        
        sheet_name = 'Sheet1' 
        sheet = workbook[sheet_name]         

        msp = doc.modelspace()               

        variable_names = {
            "A3": "width",
            "B3": "length",
            "C3": "height"
        }

        for cell_ref, var_name in variable_names.items():
            globals()[var_name] = read_excel_value(sheet, cell_ref)

        # 데이터 출력
        data = [(var_name, globals()[var_name]) for cell_ref, var_name in variable_names.items()]
        for label, value in data:
            print(f"{label} : {value}")      

        # line(doc, 0, 0, globals()['length'], globals()['height'], layer='0')
        # rectangle(doc, 0, 0, globals()['length'], globals()['height'], layer='0')
        # d(doc, 0, globals()['height'], globals()['length'], globals()['height'], 150, direction="up")
        # d(doc, globals()['length'], 0 , globals()['length'], globals()['height'], 150, direction="right")
        # # draw_circle(doc, 0, 0, 100, layer='cl', color='1')
        l=globals()['length']
        h=globals()['height']
        w=globals()['width']
        
        # line(doc, 0, 0, l, 0, layer='0')
        # line(doc, l, 0, l, h, layer='0')
        # line(doc, l, h, l+w, h, layer='0')
        # d(doc, 0, 0, l, 0, 100, direction="down")
        # d(doc, l, 0, l+w, h, 300, direction="right")
        # d(doc, l, h, l+w, h, 100, direction="up")
        
        
        line(doc, 0, 0, 0, -l, layer='0')
        line(doc, 0, -l, -h, -l, layer='0')
        line(doc, -h, -l, -h, -l+w, layer='0')
        d(doc, 0, 0, 0, -l, 100, direction="right")
        d(doc, 0, -l, -h, -l, 100, direction="down")
        d(doc, -h, -l, -h, -l+w, 100, direction="left")
        
        




        # draw_circle(doc, 0, 0, 100, layer='cl', color='1')

        print(f"globals()['length'] : {globals()['length']}") 

        # 현재 날짜와 시간을 가져옵니다.
        current_datetime = datetime.now()

        # 2023-12-10 원하는 형식으로 날짜를 문자열로 변환합니다.
        formatted_date = current_datetime.strftime('%Y-%m-%d')

        # 현재 날짜와 시간을 '년월일_시분초' 형식으로 가져옴        
        current_time = datetime.now().strftime("%H%M%S")

        save_path = "c:\\mywork\\test" + current_time + ".dxf"

        if os.path.exists(save_path):
            print(f"파일 '{save_path}' 이(가) 존재합니다. 덮어씁니다.")
        
        doc.saveas(save_path)
        print(f" 저장 파일명: '{save_path}' 저장 완료!")                

if __name__ == '__main__':
    main()
    sys.exit()