# 미래기업 코딩수업 테이블 만들기 실전 프로젝트
# 2025/02/09 사장님 요청으로 리뉴얼시작

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
    BscaleX, BscaleY,TXscale,Tyscale, frame_scale = 0,0,0,0,0
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

    xlsx_files = glob.glob('C:\python\makeTable\excel\*.xlsx')

    doc = ezdxf.readfile('C:\python\makeTable\style\style.dxf')    
    msp = doc.modelspace()

    # TEXTSTYLE 정의
    text_style_name = 'JKW'  # 원하는 텍스트 스타일 이름

def setpos(a, b, c, d):
    global BscaleX, BscaleY,TXscale,Tyscale, frame_scale
    BscaleX, BscaleY,TXscale,Tyscale = a, b, c, d
    if(TXscale/BscaleX > Tyscale/BscaleY ):
        frame_scale = TXscale/BscaleX
    else:
        frame_scale = Tyscale/BscaleY
    pagex, pagey = frameXpos , frameYpos + 1123 * frame_scale
    rx, ry = pagex , pagey 
    return rx, ry , pagex , pagey, frame_scale

def dim_leader(doc, start_x, start_y, end_x, end_y, text, text_height=30, direction=None, option=None):

    global saved_DimXpos, saved_DimYpos, saved_text_height, saved_text_gap, saved_direction, dimdistance, dim_horizontalbase, dim_verticalbase, distanceXpos, distanceYpos 
    msp = doc.modelspace()
    layer = '0'        
    text_style_name = 'GHS'            
    # override 설정

    override_settings = {
        'dimasz': 15
    }

    # 텍스트 위치 조정 및 꺾이는 지점 설정

    if option is None:    

        text_offset_x = 20

        text_offset_y = 20

    else:

        text_offset_x = 0

        text_offset_y = 0        

    

    if direction == 'leftToright':

        mid_x = end_x - text_offset_x

        mid_y = end_y  # 텍스트 앞에서 꺾임

        text_position = (end_x, end_y)

    elif direction == 'rightToleft':

        mid_x = end_x + text_offset_x

        mid_y = end_y  # 텍스트 앞에서 꺾임

        text_position = (end_x - len(text) * 22, end_y)

    else:

        mid_x = (start_x + end_x) / 2

        mid_y = (start_y + end_y) / 2

        text_position = (end_x + text_offset_x, end_y + text_offset_y)



    # 지시선 추가

    leader = msp.add_leader(

        vertices=[(start_x, start_y), (mid_x, mid_y-text_height/2), (end_x, end_y-text_height/2)],  # 시작점, 중간점(문자 앞에서 꺾임), 끝점

        dxfattribs={

            'dimstyle': text_style_name,

            'layer': layer,

            'color': 3  # 녹색 (AutoCAD 색상 인덱스에서 3번은 녹색)

        },

        override=override_settings

    )



    if option is None:

        # 텍스트 추가 (선택적)

        if text:

            msp.add_mtext(text, dxfattribs={

                'insert': text_position,

                'layer': layer,

                'char_height': text_height,

                'style': text_style_name,

                'attachment_point': 1,  # 텍스트 정렬 방식 설정

                'color': 2  # 노란색 (AutoCAD 색상 인덱스에서 2번은 노란색)

            })



    return leader
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
def insert_block(doc, x, y, block_name, layer='레이져'):

    # 도면틀 삽입    

    scale = 1

    insert_point = (x, y, scale)



    # 블록 삽입하는 방법           

    doc.modelspace().add_blockref(block_name, insert_point, dxfattribs={

        'xscale': scale,

        'yscale': scale,

        'rotation': 0,

        'layer': layer

    })

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
def calculate_holeArray(startnum, interval, limit):


    # 결과를 저장할 리스트 초기화

    hole_array = []

    # 현재 숫자를 startnum으로 설정

    current_num = startnum

    # current_num이 limit과 length를 넘지 않을 때까지 반복

    while current_num <= limit:

        # 리스트에 현재 숫자 추가

        hole_array.append(current_num)

        # 다음 숫자를 interval만큼 증가

        current_num += interval
    return hole_array

def draw_circle(doc, center_x, center_y, radius, layer='0', color='7'):
    msp = doc.modelspace()
    circle = msp.add_circle(center=(center_x, center_y), radius=radius/2, dxfattribs={'layer': layer, 'color' : color})
    return circle
def insert_frame( x, y, scale , title ):

    # 도면틀 삽입        

    block_name = "drawings_frame"        

    insert_point = (x, y, scale)

    # 블록 삽입하는 방법           
    msp.add_blockref(block_name , insert_point, dxfattribs={
        'xscale': scale,
        'yscale': scale,
        'rotation': 0
    })
    # 현장명 :
    draw_Text(doc, x + 2300 * scale, y + 200 * scale  , 30*scale , f" {title}" , '0')
def setpos(a, b, c, d,e,f):

    global BscaleX, BscaleY,TXscale,Tyscale, frame_scale, frameXpos, frameYpos

    BscaleX, BscaleY,TXscale,Tyscale, frameXpos, frameYpos = a, b, c, d, e, f

    if(TXscale/BscaleX > Tyscale/BscaleY ):

        frame_scale = TXscale/BscaleX

    else:

        frame_scale = Tyscale/BscaleY

    pagex, pagey = frameXpos , frameYpos + 1123 * frame_scale

    rx, ry = pagex , pagey 

    return rx, ry , pagex , pagey, frame_scale, frameXpos, frameYpos



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

        length=globals()['length']
        height=globals()['height']
        width=globals()['width'] 

        # print(f"길이 : {length}, 높이 {height}, 폭 {width}")
       
        thickness=1.6
        wing1=10
        wing2=25

        ############ 상부판 전개도
        startx = 200
        starty = 800
        x1 = startx
        y1 = starty
        
        t=1.5
        w1=25
        
        x1,y1=startx+200,starty+200
        x2,y2=x1+length,y1
        x3,y3=x2,y2+25
        x4,y4=x3+23.5,y3
        x5,y5=x4,y4+width - t * 2
        x6,y6=x5-23.5,y5
        x7,y7=x6,y6+25
        x8,y8=x7-length,y7
        x9,y9=x8,y8-25
        x10,y10=x9-23.5,y9
        x11,y11=x10,y10-(width - t * 2)
        x12,y12=x11+23.5,y11

        # 우측 단면도 Y위치
        RightSectiony = y11 + width
        RightSectionx = x2 + 400

        # 전개도 크기 설정 (정수형 저장)
        platewidth = int(x4 - x10)
        platelength = int(y7 - y1)


        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화

        lastNum = 12
        
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
            prev_x, prev_y = curr_x, curr_y

        line(doc, prev_x, prev_y, x1, y1, layer="0")    
        d(doc, x1,y1,x11,y11, 180, direction="down")
        d(doc, x1,y1,x2,y2,   180, direction="down")
        d(doc, x2,y2,x4,y4,   180, direction="down")
        d(doc, x4,y4,x2,y2, 100, direction="right")
        d(doc, x4,y4,x5,y5, 100, direction="right")
        d(doc, x5,y5,x7,y7, 100, direction="right")
        d(doc, x7,y7,x5,y5, 150, direction="up")
        d(doc, x7,y7,x8,y8, 150, direction="up")
        d(doc, x8,y8,x10,y10, 150, direction="up")
        d(doc, x8,y8,x10,y10, 100, direction="left")
        d(doc, x10,y10,x11,y11, 100, direction="left")
        d(doc, x1,y1,x11,y11, 100, direction="left")


        x13,y13=x1+0.75,y1+24.25
        x14,y14=x2-0.75,y1+24.25
        x15,y15=x14,y7-24.25
        x16,y16=x13,y8-24.25

        # vcut 2개소 표시
        insert_block(doc, x15,y15,  "rightupvcut", layer='0')
        insert_block(doc, x13,y13,  "leftdownvcut", layer='0')

        prev_x, prev_y = x13, y13  # 첫 번째 점으로 초기화

        lastNum = 16

        for i in range(13, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="hidden")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x13, y13, layer="hidden")    

        insert_block(doc,x1+22.5,y1+11.75, "8x20_horizontal", layer='레이져')
        insert_block(doc,x2-22.5,y2+11.75, "8x20_horizontal", layer='레이져')
        insert_block(doc,x7-22.5,y7-11.75, "8x20_horizontal", layer='레이져')
        insert_block(doc,x8+22.5,y7-11.75, "8x20_horizontal", layer='레이져')
        insert_block(doc,x11+11.75,y11+21, "8x20_vertical", layer='레이져')
        insert_block(doc,x4-11.75,y4+21, "8x20_vertical", layer='레이져')
        insert_block(doc,x5-11.75,y5-21, "8x20_vertical", layer='레이져')
        insert_block(doc,x10+11.75,y10-21, "8x20_vertical", layer='레이져')

        # dim_leader(doc, x6 , y6-360 , x6 - 270 , y6-100, "4개소 V-CUT", direction="rightToleft")        

        #상부 절곡도
        x1 = startx + 200
        y1 = starty+width+650
        x2 = x1 - thickness
        y2 = y1    
        x3 = x2  
        y3 = y2 - wing2
        x4 = x3 + length
        y4 = y3 
        x5 = x4 
        y5 = y4 + wing2
        x6 = x5 - thickness
        y6 = y5 
        x7 = x6 
        y7 = y6 - wing2 + thickness
        x8 = x7 - length + thickness*2
        y8 = y7 
        
        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
        lastNum = 8        
        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
            prev_x, prev_y = curr_x, curr_y

        line(doc, prev_x, prev_y, x1, y1, layer="0")     
        d(doc, x2,y2,x3,y3, 80, direction="left")
        d(doc, x3,y3,x4,y4, 80, direction="down")
        d(doc, x4,y4,x5,y5, 80, direction="right")
        
        draw_circle(doc,x3,y3,15, layer='6', color='6')
        draw_circle(doc,x4,y4,15, layer='6', color='6')

        #우측 절곡도        
        x1 = RightSectionx
        y1 = RightSectiony
        x2 = x1
        y2 = y1 + thickness
        x3 = x2 - wing2
        y3 = y2
        x4 = x3
        y4 = y3 - width
        x5 = x4 + wing2
        y5 = y4
        x6 = x5
        y6 = y5 + thickness
        x7 = x6 - wing2 + thickness
        y7 = y6
        x8 = x7 
        y8 = y7 + width - thickness*2
        
        prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화

        lastNum = 8
        
        d(doc, x2,y2,x3,y3, 80, direction="up")
        d(doc, x3,y3,x4,y4, 80, direction="left")
        d(doc, x4,y4,x5,y5, 80, direction="down")
        
        draw_circle(doc,x3,y3,15, layer='6', color='6')
        draw_circle(doc,x4,y4,15, layer='6', color='6')

        for i in range(1, lastNum + 1):
            curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
            line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
            prev_x, prev_y = curr_x, curr_y
        line(doc, prev_x, prev_y, x1, y1, layer="0")     

        # 세로 보강 (장공홀 있는 형태) #####################################################################################
        # 세로 보강 (장공홀 있는 형태) #####################################################################################
        # 세로 보강 (장공홀 있는 형태) #####################################################################################

        startx,starty=startx+50, starty-250
        rectangle(doc, startx,starty, startx+height,starty+77,layer='레이져')
       
        line(doc, startx,starty+38.5, startx+height,starty+38.5, layer="hidden")     
        d(doc, startx,starty+77,startx+height,starty+77, 110, direction="up")
        d(doc, startx+height,starty+38.5,startx+height,starty, 100, direction="right")
        d(doc, startx+height,starty+38.5,startx+height,starty+77, 100, direction="right")
        d(doc, startx+height,starty,startx+height,starty+77, 180, direction="right")

        hole=calculate_holeArray(20, 100, height)

        hole.pop()
       
        gap = 0

        for index, g in enumerate(hole):
            g = math.floor(g)
            gap += g  #누적으로 더하기
            if g is not None : 
                insert_block(doc,startx+g, starty+19.25, "8x20_horizontal")
                insert_block(doc,startx+g, starty+57.75, "8x20_horizontal")

            if index == 0 :
                d(doc, startx+g,starty+57.75, startx,starty+77, 50, direction="up" )    #option="reverse"
            else:
                dc(doc, startx+g, starty+57.75)    

        dc(doc, startx+height, starty+77)    

        draw_Text(doc, RightSectionx - 100, RightSectiony + 250, 40, f"상판, 보강 : L{globals()['length']} X W{globals()['width']} X H{globals()['height']} ", layer="0")
        draw_Text(doc, RightSectionx - 100, RightSectiony + 250+100, 40, f"재질 : SPCC {thickness}T size:{platewidth}x{platelength} 1EA", layer="0")

        draw_Text(doc, startx + height + 400, starty +100, 30, f"재질 : SPCC 1.6T", layer="0")
        draw_Text(doc, startx + height + 400, starty +50, 30, f"크기 : {height} X 77 ", layer="0")
        draw_Text(doc, startx + height + 400, starty , 30, f"수량 : 4 EA", layer="0")

        prex, prey = x2, y2 + g  

        BscaleX,BscaleY = 2813, 1990
        TXscale,Tyscale=length+1250,width+1580

        if(TXscale/BscaleX > Tyscale/BscaleY ):
            frame_scale = TXscale/BscaleX
        else:
            frame_scale = Tyscale/BscaleY

        insert_frame( startx-200, starty-450,  frame_scale, "2단 테이블" )

        ###########  2단 테이블 하부 'ㄷ'자 형태 #############################################################################
        ###########  2단 테이블 하부 'ㄷ'자 형태 #############################################################################
        ###########  2단 테이블 하부 'ㄷ'자 형태 #############################################################################
       
        thickness=1.6
        wing1=10
        wing2=25

        ############ 하부판 전개도
        startx = 200 + length + 3000
        starty = 800
        
        t=1.5

        #################################################################################################
        # 'ㄷ'자 형태에서 날개 한번 떠 꺽임 Vcut 없음
        #################################################################################################
        program = 1
        if program:         

            rx1 = startx
            ry1 = starty
            
            thickness = 1.6            
            vcut = 1.5
            
            # 기본 상판보다 작게 만드는 원리임
            midplate_width = length - 10
            midplate_height = width - 10

            topwing1 = 10
            topwing2 = 30
            btwing1 = 10
            btwing2 = 30
            leftwing1 = 10
            leftwing2 = 30
            rightwing1 = 10
            rightwing2 = 30

            x1, y1 = rx1, ry1
            x2, y2 = x1 + midplate_width - leftwing1 - rightwing1, y1
            x3, y3 = x2, y2 + btwing1 - vcut
            x4, y4 = x3, y3 + 0.5
            x5, y5 = x4 + (rightwing1 - t), y4
            x6, y6 = x5, y5 + rightwing2 
            x7, y7 = x6 + rightwing2 + rightwing1 - vcut*2 - 1 , y6
            x8, y8 = x7 , y7 + vcut 
            x9, y9 = x8, y8 + midplate_height - vcut * 2
            x10, y10 = x9, y9 + vcut
            x11, y11 = x10 - rightwing1 - rightwing2 + vcut * 2 + 1  , y10
            x12, y12 = x11, y11 + topwing2 
            x13, y13 = x12 - rightwing1 + vcut, y12
            x14, y14 = x13, y13 + 0.5
            x15, y15 = x14, y14 + topwing1 - vcut
            x16, y16 = x15 - midplate_width + leftwing1 + rightwing1, y15
            x17, y17 = x16, y16 - topwing1 + vcut
            x18, y18 = x17, y17 - 0.5
            x19, y19 = x18 - leftwing1 + vcut, y18
            x20, y20 = x19, y19 - topwing2 
            x21, y21 = x20 - rightwing1 - rightwing2 + vcut * 2 + 1, y20
            x22, y22 = x21, y21 - vcut
            x23, y23 = x22, y22 - midplate_height + vcut * 2
            x24, y24 = x23, y23 - vcut
            x25, y25 = x24 + leftwing1 + leftwing2 - vcut * 2 - 1 , y24
            x26, y26 = x25, y25 - leftwing2 
            x27, y27 = x26 + leftwing1 - vcut , y26
            x28, y28 = x27, y27 - 0.5

            # 세로 절곡점 찾기
            x29, y29 = x24 + leftwing1 - vcut, y24
            x30, y30 = x25 - 0.5, y25
            x31, y31 = x6 + 0.5, y6
            x32, y32 = x7 - rightwing1 + vcut, y7
            x33, y33 = x10 - rightwing1 + vcut, y10
            x34, y34 = x11 + 0.5, y11
            x35, y35 = x20 - 0.5, y20
            x36, y36 = x21 + leftwing1 - vcut, y22

            # 전개도 사이즈 저장 #1 중판
            midplatesizex2 = x10 - x21
            midplatesizey2 = y15 - y2

            # 중판1보다 4점 추가됨 주의
            prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화

            # 2R 그리기
            Radiusval = 2          
            lastNum = 28
            for i in range(1, lastNum + 1):
                curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
                if i==0:
                    line(doc, prev_x, prev_y , curr_x, curr_y, layer="레이져")
                    prev_x, prev_y = curr_x, curr_y            
                # if i==5 or i==12 or i==19 or i==26 :
                if i==5 :
                    x = curr_x - Radiusval
                    y = curr_y + Radiusval            
                    line(doc, prev_x, prev_y, x , curr_y , layer='레이져')   # 우상향     
                    add_arc_between_points(doc, (x, curr_y), (x + Radiusval, curr_y + Radiusval), Radiusval)
                    x = curr_x 
                    y = curr_y + Radiusval            
                    prev_x, prev_y = x, y
                elif i==12 :
                    x = curr_x - Radiusval
                    y = curr_y - Radiusval            
                    line(doc, prev_x, prev_y, curr_x , y , layer='레이져')   # 좌상향     
                    add_arc_between_points(doc, (curr_x , y) , (x , curr_y) , Radiusval)
                    x = curr_x -  Radiusval             
                    y = curr_y 
                    prev_x, prev_y = x, y
                elif i==19 :
                    x = curr_x + Radiusval
                    y = curr_y - Radiusval            
                    line(doc, prev_x, prev_y, x , curr_y , layer='레이져')   # 우하향     
                    add_arc_between_points(doc, (x , curr_y) , (curr_x , y) , Radiusval)
                    x = curr_x 
                    y = curr_y - Radiusval             
                    prev_x, prev_y = x, y
                elif i==26 :
                    x = curr_x + Radiusval
                    y = curr_y + Radiusval            
                    line(doc, prev_x, prev_y, curr_x , y ,  layer='레이져')   # 우하향     
                    add_arc_between_points(doc,(curr_x , y) , (x , curr_y) , Radiusval)
                    x = curr_x + Radiusval             
                    y = curr_y 
                    prev_x, prev_y = x, y
                else:            
                    line(doc, prev_x, prev_y , curr_x, curr_y, layer="레이져")
                    prev_x, prev_y = curr_x, curr_y

            line(doc, prev_x, prev_y, x1, y1, layer="레이져")      

            # 장공 그리기
            insert_block(doc,x26+16,y26+13.5, "8x20_horizontal", layer='레이져')
            insert_block(doc,x5-16,y5+13.5, "8x20_horizontal", layer='레이져')
            insert_block(doc,x12-16,y12-13.5, "8x20_horizontal", layer='레이져')
            insert_block(doc,x19+16,y19-13.5, "8x20_horizontal", layer='레이져')
            insert_block(doc,x24+22,y24+18, "8x20_vertical", layer='레이져')
            insert_block(doc,x7-22,y7+18, "8x20_vertical", layer='레이져')
            insert_block(doc,x10-22,y10-18, "8x20_vertical", layer='레이져')
            insert_block(doc,x21+22,y21-18, "8x20_vertical", layer='레이져')            
            
            #절곡라인  밴딩 가로 방향      
            line(doc, x28, y28, x3, y3,  layer='hidden')   # 절곡선      
            line(doc, x23, y23, x8, y8,  layer='hidden')   # 절곡선      
            line(doc, x22, y22, x9, y9,  layer='hidden')   # 절곡선      
            line(doc, x17, y17, x14, y14,  layer='hidden')   # 절곡선      

            # 세로절곡선 표현
            line(doc, x36, y36, x29, y29,  layer='hidden')    # 절곡선        
            line(doc, x35, y35, x30, y30,  layer='hidden')    # 절곡선        
            line(doc, x34, y34, x31, y31,  layer='hidden')    # 절곡선        
            line(doc, x33, y33, x32, y32,  layer='hidden')    # 절곡선        
    

            # 상부 치수선
            dim(doc, x36, y36, x21, y21 , 120 , direction="up", option="reverse" )
            dimcontinue(doc, x35, y35)
            dim(doc, x35, y35, x34, y34 , 180 , direction="up")    
            dim(doc, x33, y33, x10, y10 , 120 , direction="up", option="reverse" )
            dimcontinue(doc, x34, y34)    
            # 상부 전체치수
            dim(doc, x21, y21, x10, y10 , 250 , direction="up")

            # 좌측 치수선
            d(doc, x16,  y16, x21, y21 , 150 , direction="left")
            dc(doc, x24, y24)
            dc(doc, x1, y1, option='reverse')
            d(doc, x16, y16 , x1, y1,  290 , direction="left")

            # 하부 치수선
            dim(doc, x1, y1, x26 , y26 , 160 , direction="down" )
            dim(doc, x2, y2, x5 , y5 , 160 , direction="down" )

            dim(doc, x1, y1, x24 , y24 , 240 , direction="down" , option='reverse')
            dimcontinue(doc,  x2, y2)    
            dimcontinue(doc,  x7, y7)      
            dim(doc, x24, y24, x7 , y7 , 350 , direction="down")

            # 우측 치수선
            dim(doc, x14, y14, x15, y15,  220 , direction="right")
            dim(doc,  x9, y9, x14, y14, 250 , direction="right", option='reverse')
            dimcontinue(doc,  x8, y8)
            dimcontinue(doc,  x3, y3)
            dim(doc, x3, y3, x2, y2,  220 , direction="right")   
            dim(doc, x15, y15, x2, y2 , 400 , direction="right")

        # 좌측 단면도 그리기
        # 왼쪽 leftwing1 leftwing2
        # 오른쪽 날개 rightwing1 rightwing2
        # 본판 mainplate = mp 
        # 'ㄷ'자 형상 
        program = 1
        if program:
            mp = midplate_height

            tmpstartx = x1 - 503 - btwing2
            tmpstarty = y1 + btwing1 + topwing1 + topwing2

            x1 = tmpstartx
            y1 = tmpstarty
            x2 = x1 - thickness    
            y2 = y1    
            x3 = x2  
            y3 = y2 - btwing1 
            x4 = x3 + btwing2 
            y4 = y3 
            x5 = x4 
            y5 = y4 + midplate_height
            x6 = x5 - topwing2
            y6 = y5 
            x7 = x6 
            y7 = y6 - topwing1
            x8 = x7 + thickness
            y8 = y7 
            x9 = x8 
            y9 = y8 + topwing1 - thickness
            x10 = x9 + topwing2 - thickness *2
            y10 = y9 
            x11 = x10 
            y11 = y10 - midplate_height + thickness *2
            x12 = x11 - topwing2 + thickness*2
            y12 = y11

            prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
            lastNum = 12
            for i in range(1, lastNum + 1):
                curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
                line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
                prev_x, prev_y = curr_x, curr_y
            line(doc, prev_x, prev_y, x1, y1, layer="0")     

            #vcut 원 그리기
            # draw_circle(doc, x3, y3, 13, layer='0', color='6') 
            # draw_circle(doc, x4, y4, 13, layer='0', color='6') 
            # draw_circle(doc, x5, y5, 13, layer='0', color='6') 
            # draw_circle(doc, x6, y6, 13, layer='0', color='6') 

            # 치수선
            d(doc, x3,y3, x4, y4, 110, direction="down", option='reverse')
            d(doc, x2,y2, x3, y3, 80, direction="left")
            dim(doc, x4,y4, x5, y5, 110, direction="right")
            dim(doc, x6,y6, x5, y5, 100, direction="up")
            dim(doc, x6,y6, x7, y7, 80, direction="left")

            # dim_leader_line(doc, x4, y4 , x4 + 50 , y4-150, "Vcut 4개소")
    
        ###############################################################################
        # 상부 단면도 그리기
        ###############################################################################
        program = 1
        if program:    
            mp = midplate_width

            tmpstartx = rx1 + leftwing1
            tmpstarty = ry1 + 390 + midplate_height + leftwing2*3

            x1 = tmpstartx
            y1 = tmpstarty
            x2 = x1 - leftwing1
            y2 = y1    
            x3 = x2  
            y3 = y2 - leftwing2
            x4 = x3 + mp
            y4 = y3 
            x5 = x4 
            y5 = y4 + rightwing2
            x6 = x5 - rightwing1
            y6 = y5 
            x7 = x6 
            y7 = y6 - thickness
            x8 = x7 + rightwing1 - thickness
            y8 = y7 
            x9 = x8 
            y9 = y8 - rightwing2 + thickness*2
            x10 = x9 - mp + thickness *2
            y10 = y9 
            x11 = x10 
            y11 = y10 + leftwing2 - thickness *2
            x12 = x11 + leftwing1 - thickness
            y12 = y11

            prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
            lastNum = 12
            for i in range(1, lastNum + 1):
                curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
                line(doc, prev_x, prev_y, curr_x, curr_y, layer="0")
                prev_x, prev_y = curr_x, curr_y
            line(doc, prev_x, prev_y, x1, y1, layer="0")     

            #vcut 원 그리기 4개소
            # draw_circle(doc, x2, y2, 13, layer='0', color='6') 
            # draw_circle(doc, x3, y3, 13, layer='0', color='6') 
            # draw_circle(doc, x4, y4, 13, layer='0', color='6') 
            # draw_circle(doc, x5, y5, 13, layer='0', color='6') 

            # 치수선
            dim(doc, x2,y2, x1, y1, 80, direction="up")
            dim(doc, x2,y2, x3, y3, 80, direction="left")
            dim(doc, x5,y5, x4, y4, 80, direction="right")
            dim(doc, x6,y6, x5, y5, 80, direction="up")
            dim(doc, x3,y3, x4, y4, 80, direction="down")
        
            # dim_leader_line(doc, x4, y4 , x4 + 50 , y4 - 100, "Vcut 4개소")

            # 중판 #1 description    
            x1 = startx + 150 
            y1 = starty + 300 
            textstr = f"Part Name : 2단테이블 하단'ㄷ'자 "    
            draw_Text(doc, x1 , y1 , 30 , str(textstr), layer='0')    
            textstr = f"Mat.Spec : SPCC 1.6T"    
            draw_Text(doc, x1 , y1 - 50 , 30, str(textstr), layer='0')    
            textstr = f"Size : {str(int(math.ceil(midplatesizex2*100)/100))} x {str(int(math.ceil(midplatesizey2*100)/100))}mm"    
            draw_Text(doc, x1 , y1 - 100 , 30, str(textstr), layer='0')        
            textstr = f"Quantity : 1 EA"    
            draw_Text(doc, x1 , y1 - 150 , 30, str(textstr), layer='0')     

            BscaleX,BscaleY = 2813, 1990
            TXscale,Tyscale=length+1250,width+1580

            if(TXscale/BscaleX > Tyscale/BscaleY ):
                frame_scale = TXscale/BscaleX
            else:
                frame_scale = Tyscale/BscaleY            

            insert_frame( startx-800, starty-700,  frame_scale, "2단 테이블 하부" )

    program = 1
    if program:
        ####################################################################################################################################################
        # 레이져 도면틀 생성 (공통) 레이져에 배열할때 편리한 기능
        # 1219*1950 철판크기 샘플        
        x1 = 5000+850
        y1 = 5000+130
        x2 = 5000+850+2438
        y2 = y1 + 1219    
        x3 = x1 + 3000
        y3 = y1 +1219
        rectangle(doc, 5000, 5000, 5000+7400 , 5000+ 2340 , layer='0')  
        rectangle(doc,x1 , y1 ,x1 + 2438 , y2 , layer='레이져')  
        dim(doc, x1 , y2 , x2 , y2,  100, direction="up")
        # rectangle(doc, x1+2600 , y1 , x2+2600 , y2 , layer='레이져')  
        # dim(doc, x1+2600, y2, x2+2600, y2, 100, direction="up")
        # dim(doc,  x1 , y1, x1 ,y2 , 150, direction="left")
        rectangle(doc, x3 , y1 , x3+2600 , y2 , layer='레이져')  
        dim(doc, x3, y3, x3+2600, y2, 100, direction="up")
        dim(doc,  x3 , y1, x3 ,y2 , 150, direction="left")

        textstr = f"2단 테이블 제작"    
        draw_Text(doc, 5000+300 , 5000+ 2340 - 200 ,  120, str(textstr), layer='0')        

        y = 5000+ 2340 - 650
        textstr = f"SPCC 1.6tX1219X2438 = 장"
        draw_Text(doc, 5000+780 , y ,  90, str(textstr), layer='0')                    

        ####################################################################################################################

        # print(f"globals()['length'] : {globals()['length']}") 

        # 현재 날짜와 시간을 가져옵니다.
        current_datetime = datetime.now()

        # 2023-12-10 원하는 형식으로 날짜를 문자열로 변환합니다.
        formatted_date = current_datetime.strftime('%Y-%m-%d')

        # 현재 날짜와 시간을 '년월일_시분초' 형식으로 가져옴        
        current_time = datetime.now().strftime("%H%M%S")

        save_path = "C:\\python\\makeTable\\2단 테이블 " + f"길이 {globals()['length']}X 폭 {globals()['width']} X 높이 {globals()['height']} " + current_time + ".dxf"

        if os.path.exists(save_path):
            print(f"파일 '{save_path}' 이(가) 존재합니다. 덮어씁니다.")
        
        doc.saveas(save_path)
        print(f" 저장 파일명: '{save_path}' 저장 완료!")                
      
if __name__ == '__main__':
    main()
    sys.exit()


       