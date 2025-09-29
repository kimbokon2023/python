import ezdxf
import math
    
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
        end_angle=end_angle
    )

    return msp



def add_90_degree_fillet(doc, start1, end1, start2, end2, radius):
    msp = doc.modelspace()

    # 교차점 찾기 (두 직선이 90도로 만난다고 가정)
    intersection_point = find_intersection(start1, end1, start2, end2)

    # 각 직선에 대한 필렛의 접점 계산
    point1 = calculate_fillet_point(intersection_point, end1, radius)
    point2 = calculate_fillet_point(intersection_point, end2, radius)

    # 원호의 시작 각도와 끝 각도 계산
    start_angle = calculate_angle(intersection_point, point1)
    end_angle = calculate_angle(intersection_point, point2)

    # 필렛 원호 그리기
    msp.add_arc(
        center=intersection_point,
        radius=radius,
        start_angle=start_angle,
        end_angle=end_angle
    )

    return msp

# # 사용 예시
# doc = ezdxf.new('R2010')
# # 쪽쟘상판 좌측 상단 R5 적용된 형태
# add_90_degree_fillet(doc,  (5, 0), (5, 5), (5, 0), (0, 0), 5)
# # 쪽쟘상판 우측 상단 R5 적용된 형태
# add_90_degree_fillet(doc,  (0, 0), (5, 0), (0, 0), (0, 5),  5)
# doc.saveas("90_degree_fillet_jambTop.dxf")
