####################################################################################################################################################################################
# 천장 자동작도
####################################################################################################################################################################################
def execute_lc():     

    Abs_Xpos = 0
    Abs_Ypos = 0

    global CD
    global CW
    global workplace
    global secondord

    # LC 크기 지정
    LCCD = CD-50
    LCCW = CW-50


    # 도면틀 넣기
    BasicXscale = 2560
    BasicYscale = 1550
    TargetXscale = 800 
    TargetYscale = 300 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale

# print("현장명: " + workplace)
# print("작성일: " + drawdate_str)  # 수정된 부분
# print("lctype: " + lctype)
# print("발주처: " + secondord)
# print("CD: " + str(CD))  # CD가 숫자 타입일 경우 문자열로 변환
# print("CW: " + str(CW))  # CW가 숫자 타입일 경우 문자열로 변환        

    frame_scale = 1    
    # print (f'스케일 : {frame_scale}')
    #  insert_frame(Abs_Xpos , Abs_Ypos , frame_scale, "title_frame", workplace)    
    # 현장명
    Textstr = workplace       
    x = Abs_Xpos + 80
    y = Abs_Ypos + 1000 + 218
    draw_Text(doc, x, y , 7, str(Textstr), layer='0')
    # 발주처
    Textstr = secondord
    x = Abs_Xpos + 80
    y = Abs_Ypos + 1000 + 218 - 30
    draw_Text(doc, x, y , 7, str(Textstr), layer='0')
    # 타입
    Textstr = lctype
    x = Abs_Xpos + 260
    y = Abs_Ypos + 1000 + 214 + 10
    draw_Text(doc, x, y , 7, str(Textstr), layer='0')
    # 수량
    Textstr = su
    x = Abs_Xpos + 260
    y = Abs_Ypos + 1000 + 214 + 10 - 18
    draw_Text(doc, x, y , 7, str(Textstr), layer='0')
    # 카사이즈
    Textstr = f"W{CW} x D{CD}"
    x = Abs_Xpos + 260
    y = Abs_Ypos + 1000 + 214 + 10 - 18 - 18
    draw_Text(doc, x, y , 7, str(Textstr), layer='0')
    # 색상
    Textstr = f"L / C : 흑색무광"
    x = Abs_Xpos + 260
    y = Abs_Ypos + 1000 + 214 + 10 - 18 - 18 - 18
    draw_Text(doc, x, y , 7, str(Textstr), layer='0')
    # (등기구업체 : 덴크리)    
    Textstr = f"(등기구업체 : 덴크리)"
    x = Abs_Xpos + 120
    y = Abs_Ypos + 1000 + 90
    draw_Text(doc, x, y , 12, str(Textstr), layer='0')    
    # (아답터용량 : 60W )
    Textstr = f"(아답터용량 : 60W )"
    x = Abs_Xpos + 120
    y = Abs_Ypos + 1000 + 90 - 20
    draw_Text(doc, x, y , 12, str(Textstr), layer='0')
    # 납품일자 :
    Textstr = f"*. 납품일자 : {drawdate_str}"
    x = Abs_Xpos + 230
    y = Abs_Ypos + 1000 + 30 
    draw_Text(doc, x, y , 8, str(Textstr), layer='0')
    # 출도일자 :
    Textstr = f"*. 출도일자 : {deadlinedate_str}"
    x = Abs_Xpos + 230
    y = Abs_Ypos + 1000 + 30 - 15
    draw_Text(doc, x, y , 8, str(Textstr), layer='0')

    # led바에 대한 내용 기술
    # LED BAR :
    Textstr = f"LED BAR - {CD-100}=2(EA)"
    x = Abs_Xpos + 711
    y = Abs_Ypos + 600
    draw_Text(doc, x, y , 20, str(Textstr), layer='0')    
    # SMPS-1(EA)
    Textstr = f"SMPS-1(EA)"
    x = Abs_Xpos + 711 + 60
    y = Abs_Ypos + 600 - 35
    draw_Text(doc, x, y , 20, str(Textstr), layer='0')    
    # Type
    Textstr = f"{lctype}타입"
    x = Abs_Xpos + 711 + 100
    y = Abs_Ypos + 600 - 35 - 85 
    draw_Text(doc, x, y , 20, str(Textstr), layer='0')    
    # 현장명
    Textstr = f"*.현장명 : {secondord}-{workplace} - {su}(set)"
    x = Abs_Xpos + 30
    y = Abs_Ypos + 600 
    draw_Text(doc, x, y , 18, str(Textstr), layer='0')    
    # (등기구업체 : 덴크리)
    Textstr = f"(등기구업체 : 덴크리)"
    x = Abs_Xpos + 30 + 200
    y = Abs_Ypos + 600 - 50
    draw_Text(doc, x, y , 18, str(Textstr), layer='0')    
    # LED BAR-(누드&클립&잭타입)10000K-1400L
    Textstr = f"LED BAR-(누드&클립&잭타입)10000K-{CD-100}L"
    x = Abs_Xpos + 30 + 60
    y = Abs_Ypos + 600 - 50 - 80
    draw_Text(doc, x, y , 14, str(Textstr), layer='0')    
    # (하단) LED BAR-(누드&클립&잭타입)10000K-1400L
    Textstr = f"LED BAR-(누드&클립&잭타입)10000K-{CD-100}L"
    x = Abs_Xpos + 30 + 60
    y = Abs_Ypos + 600 - 50 - 80 - 360
    draw_Text(doc, x, y , 14, str(Textstr), layer='0')    

    # LC ASSY 상부 형상
    Abs_Xpos = Abs_Xpos + 2500
    Abs_Ypos = Abs_Ypos + CD + 450
    insert_block(Abs_Xpos , Abs_Ypos , "lc026_top_left")    

    x = Abs_Xpos + CW 
    y = Abs_Ypos 
    insert_block(x , y , "lc026_top_right")  

    x1 = Abs_Xpos + 375 - 40
    y1 = Abs_Ypos + 19.6    
    x2 = x1 + (CW - 375*2 + 80)
    y2 = y1
    line(doc, x1, y1, x2, y2, layer='4')     # 4는 하늘색
    lineto(doc, x2, y1+10, layer='4')     # 4는 하늘색
    lineto(doc, x1, y1+10, layer='4')     # 4는 하늘색
    lineto(doc, x1, y1, layer='4')     # 4는 하늘색
    Textstr =  f"LMW(CW-670)"
    dim_string(doc, x1, y2, x2, y2, 45,  Textstr, text_height=0.20, text_gap=0.07, direction="up")    

    # 상부선 2mm 간격
    X1 = Abs_Xpos - 25
    Y1 = Abs_Ypos + 150
    X2 = X1 + CW + 50
    Y2 = Y1
    line(doc, X1, Y1, X2, Y2, layer='2')     # 회색
    lineto(doc, X2, Y1+2, layer='2')    
    lineto(doc, X1, Y1+2, layer='2')    
    lineto(doc, X1, Y1, layer='2')     

    # Assy 상부 치수
    x1 = Abs_Xpos + 300
    y1 = Abs_Ypos + 150
    x2 = Abs_Xpos + CW - 300
    y2 = y1    
    Textstr =  f"CW-600={CW-600}"
    dim_string(doc, x1, y1, x2, y2, 155,  Textstr, text_height=0.20, text_gap=0.07, direction="up")
    # Assy 중심 치수
    x1 = Abs_Xpos + 375
    y1 = Abs_Ypos 
    x2 = Abs_Xpos + CW - 375
    y2 = y1    
    Textstr =  f"CW-750={CW-750}"
    dim_string(doc, x1, y1, x2, y2, 105,  Textstr, text_height=0.20, text_gap=0.07, direction="down")
    # Assy 상단 하부 치수
    x1 = Abs_Xpos 
    y1 = Abs_Ypos 
    x2 = Abs_Xpos + CW
    y2 = y1    
    Textstr =  f"CW(AA) {CW}"
    dim_string(doc, x1, y1, x2, y2, 160,  Textstr, text_height=0.20, text_gap=0.07, direction="down")

    # Assy Car case    
    insideGap = 25
    Abs_Ypos = Abs_Ypos - 450 - CD
    x1 = Abs_Xpos 
    y1 = Abs_Ypos 
    x2 = Abs_Xpos + CW
    y2 = CD    
    rectangle(doc, x1, y1, x2, y2, layer='0')    
    x1 = Abs_Xpos + insideGap
    y1 = Abs_Ypos + insideGap
    x2 = Abs_Xpos + CW - insideGap
    y2 = Abs_Ypos + CD - insideGap
    line(doc, x1, y1, x1+2, y1, layer='0')     # 회색
    line(doc, x2, y1, x2-2, y1, layer='0')     # 회색
    line(doc, x1, y2, x1+2, y2, layer='0')     # 회색
    line(doc, x2, y2, x2-2, y2, layer='0')     # 회색
    line(doc, x1, y1, x1,   y2, layer='0')     # 회색
    line(doc, x2, y1, x2,   y2, layer='0')     # 회색
    

    # 좌측 fan assy
    insert_block(Abs_Xpos + 15 , Abs_Ypos  + CD - 70 , "lc026_fan")    
    insert_block(Abs_Xpos + insideGap + 2 , Abs_Ypos  + CD - insideGap , "lc026_rib_top_left")    
    insert_block(Abs_Xpos + CW - insideGap - 2 , Abs_Ypos  + CD - insideGap , "lc026_rib_top_right")    
    insert_block(Abs_Xpos + insideGap + 2 , Abs_Ypos  + insideGap , "lc026_rib_bottom_left")    
    insert_block(Abs_Xpos + CW - insideGap - 2 , Abs_Ypos  + insideGap , "lc026_rib_bottom_right")    
    # adaptor
    insert_block(Abs_Xpos + insideGap + 245 , Abs_Ypos  + 50 , "lc026_adptor")    
    # 장공/단공 70
    insert_block(Abs_Xpos + 150 , Abs_Ypos  + 275 , "circle70")    
    insert_block(Abs_Xpos + CW - 150 , Abs_Ypos  + 275 , "circle70")    
    insert_block(Abs_Xpos + CW - 150 , Abs_Ypos  + CD - 275 , "circle70")    
    insert_block(Abs_Xpos + 150 , Abs_Ypos  + CD - 275 , "circle70")    
    # 장공/단공 20
    insert_block(Abs_Xpos + 200 , Abs_Ypos  + 200 , "circle20")    
    insert_block(Abs_Xpos + CW - 200 , Abs_Ypos  + 200 , "circle20")    
    insert_block(Abs_Xpos + CW - 200 , Abs_Ypos  + CD - 200, "circle20")    
    insert_block(Abs_Xpos + 200 , Abs_Ypos  + CD - 200 , "circle20")    
    # 장공/단공 11 and 10 장공
    insert_block(Abs_Xpos + 100 , Abs_Ypos + CD/2  , "circle11plus")    
    insert_block(Abs_Xpos + CW - 100 , Abs_Ypos + CD/2 , "circle11plus")    
    insert_block(Abs_Xpos + CW + 1200 , Abs_Ypos + 650 , "lc026assy")    

    # 내부 폴리갈 자리 하늘색    
    x1 = Abs_Xpos + 335
    y1 = Abs_Ypos + 29
    x2 = Abs_Xpos + CW - 335
    y2 = Abs_Ypos + CD - 29
    rectangle(doc, x1, y1, x2, y2, layer='4')   # 하늘색   
    line(doc, x1, Abs_Ypos + CD/2 , x2, Abs_Ypos + CD/2 , layer='4')     # 4는 하늘색
    dim_vertical_left(doc,  Abs_Xpos + CW /1.6 , y1, Abs_Xpos + CW /1.7 , y2, 150, "JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_left(doc,  Abs_Xpos + CW /1.6 , y1, Abs_Xpos + CW /1.7 , (y1+y2)/2, 70, "JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_left(doc,  Abs_Xpos + CW /1.6 , y2, Abs_Xpos + CW /1.7 , (y1+y2)/2, 70, "JKW", text_height=0.20,  text_gap=0.07)

    # 인발 파란색(왼쪽)
    side_gap = 275
    top_gap = 27
    x1 = Abs_Xpos + side_gap
    y1 = Abs_Ypos + top_gap
    x2 = Abs_Xpos + side_gap + 100
    y2 = Abs_Ypos + CD - top_gap
    rectangle(doc, x1, y1, x2, y2, layer='5')   # 파란색
    line(doc, x1+12.5, y1, x1+12.5, y2, layer='55')
    line(doc, x1+12.5+11.5, y1, x1+12.5+11.5, y2, layer='55')
    line(doc, x1+12.5+11.5+2, y1, x1+12.5+11.5+2, y2, layer='55')
    line(doc, x1+12.5+11.5+2+11.5, y1, x1+12.5+11.5+2+11.5, y2, layer='55')
    line(doc, x1+12.5+11.5+2+11.5+25, y1, x1+12.5+11.5+2+11.5+25, y2, layer='55')
    line(doc, x1+12.5+11.5+2+11.5+25+11.5, y1, x1+12.5+11.5+2+11.5+25+11.5, y2, layer='55')
    line(doc, x1+12.5+11.5+2+11.5+25+11.5+2, y1, x1+12.5+11.5+2+11.5+25+11.5+2, y2, layer='55')
    line(doc, x1+12.5+11.5+2+11.5+25+11.5+2+11.5, y1, x1+12.5+11.5+2+11.5+25+11.5+2+11.5, y2, layer='55')

    # 인발 파란색 (오른쪽)
    side_gap = CW - 275 - 100
    top_gap = 27
    x1 = Abs_Xpos + side_gap
    y1 = Abs_Ypos + top_gap
    x2 = Abs_Xpos + side_gap + 100
    y2 = Abs_Ypos + CD - top_gap
    rectangle(doc, x1, y1, x2, y2, layer='5')   # 파란색
    line(doc, x1+12.5, y1, x1+12.5, y2, layer='55')
    line(doc, x1+12.5+11.5, y1, x1+12.5+11.5, y2, layer='55')
    line(doc, x1+12.5+11.5+2, y1, x1+12.5+11.5+2, y2, layer='55')
    line(doc, x1+12.5+11.5+2+11.5, y1, x1+12.5+11.5+2+11.5, y2, layer='55')
    line(doc, x1+12.5+11.5+2+11.5+25, y1, x1+12.5+11.5+2+11.5+25, y2, layer='55')
    line(doc, x1+12.5+11.5+2+11.5+25+11.5, y1, x1+12.5+11.5+2+11.5+25+11.5, y2, layer='55')
    line(doc, x1+12.5+11.5+2+11.5+25+11.5+2, y1, x1+12.5+11.5+2+11.5+25+11.5+2, y2, layer='55')
    line(doc, x1+12.5+11.5+2+11.5+25+11.5+2+11.5, y1, x1+12.5+11.5+2+11.5+25+11.5+2+11.5, y2, layer='55')   

    # LC 좌우 사각형 (왼쪽)
    side_gap = 85
    top_gap = 25
    x1 = Abs_Xpos + side_gap
    y1 = Abs_Ypos + top_gap
    x2 = Abs_Xpos + side_gap + 25
    y2 = Abs_Ypos + CD - top_gap
    rectangle(doc, x1, y1, x2, y2, layer='0')   # 흰색     

    # LC 좌우 사각형 (오른쪽)
    side_gap = CW - 85 - 25
    top_gap = 25
    x1 = Abs_Xpos + side_gap
    y1 = Abs_Ypos + top_gap
    x2 = Abs_Xpos + side_gap + 25
    y2 = Abs_Ypos + CD - top_gap
    rectangle(doc, x1, y1, x2, y2, layer='0')   # 흰색    

    # 본천장 및 LC 상단 
    x1 = Abs_Xpos 
    y1 = Abs_Ypos + CD
    x2 = Abs_Xpos + CW
    y2 = y1    
    Textstr =  f"L/C {CW-50}"
    dim_string(doc, x1 + 25 , y1 - 25, x2 - 25 , y2 - 25, 100,  Textstr, text_height=0.20, text_gap=0.07, direction="up")    
    x1 = Abs_Xpos 
    y1 = Abs_Ypos + CD
    x2 = Abs_Xpos + CW
    y2 = y1    
    Textstr =  f"CAR INSIDE - {CW}"
    dim_string(doc, x1 , y1 , x2  , y2, 140,  Textstr, text_height=0.20, text_gap=0.07, direction="up")    

    # 우측 치수선
    x1 = Abs_Xpos + CW 
    y1 = Abs_Ypos + CD - 25
    x2 = Abs_Xpos + CW - 140
    y2 = y1 - 15      
    dim_vertical_right(doc, x1, y1, x2, y2, 265-140, "JKW", text_height=0.20,  text_gap=0.07)
    x1 = Abs_Xpos + CW - 140 
    y1 = Abs_Ypos + CD - 40
    x2 = x1
    y2 = Abs_Ypos + CD/2
    dim_vertical_right(doc, x1, y1, x2, y2, 265, "JKW", text_height=0.20,  text_gap=0.07)
    x1 = Abs_Xpos + CW - 140 
    y1 = Abs_Ypos + 40
    x2 = x1
    y2 = Abs_Ypos + CD/2
    dim_vertical_right(doc, x1, y1, x2, y2, 265, "JKW", text_height=0.20,  text_gap=0.07)
    x1 = Abs_Xpos + CW 
    y1 = Abs_Ypos + 25
    x2 = Abs_Xpos + CW - 140
    y2 = y1 + 15      
    dim_vertical_right(doc, x1, y1, x2, y2, 265-140, "JKW", text_height=0.20,  text_gap=0.07)    
    x1 = Abs_Xpos + CW - 25
    y1 = Abs_Ypos + CD - 25
    x2 = x1
    y2 = Abs_Ypos + CD/2
    dim_vertical_right(doc, x1, y1, x2, y2, 225, "JKW", text_height=0.20,  text_gap=0.07)    
    x1 = Abs_Xpos + CW - 25
    y1 = Abs_Ypos + 25
    x2 = x1
    y2 = Abs_Ypos + CD/2
    dim_vertical_right(doc, x1, y1, x2, y2, 225, "JKW", text_height=0.20,  text_gap=0.07)    
    x1 = Abs_Xpos + CW - 25
    y1 = Abs_Ypos + CD - 25
    x2 = x1
    y2 = Abs_Ypos + 25        
    Textstr =  f"L/C {CD-panel_thickness*2}"
    # dim_vertical_right_string(doc, x1, y1, x2, y2, 308, Textstr , text_height=0.20,  text_gap=0.07)        
    dim_string(doc,  x2, y2, x1, y1, 308, Textstr , text_height=0.20,  text_gap=0.07, direction="aligned_reverse")     # aligned로 나오지 않을때 역방향 개발
    x1 = Abs_Xpos + CW
    y1 = Abs_Ypos + CD
    x2 = x1
    y2 = Abs_Ypos         
    Textstr =  f"CAR INSIDE {CD}"    
    dim_string(doc,  x2, y2, x1, y1, 364, Textstr , text_height=0.20,  text_gap=0.07, direction="aligned_reverse")     # aligned로 나오지 않을때 역방향 개발

    # 도면틀 넣기
    BasicXscale = 2560
    BasicYscale = 1550
    TargetXscale = CW + 2500
    TargetYscale = CD + 1000
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
    print("스케일 비율 : " + str(frame_scale))    
    insert_frame(Abs_Xpos  - 500 * frame_scale ,Abs_Ypos - 450 * frame_scale , frame_scale, "transom_frame", workplace)   

    # 1page 상단에 car inside 표기
    x = Abs_Xpos + CW/4
    y = Abs_Ypos + frame_scale*BasicYscale + 300
    Textstr = f"W{CW} x D{CD}"    
    draw_Text(doc, x, y , 300, str(Textstr), layer='0')    


    # 2page LC frame 삽입
    rx1 = Abs_Xpos + math.ceil(math.ceil(frame_scale * BasicXscale) / 100) * 100 + 1500 
    ry1 = Abs_Ypos + 630
    insert_block(rx1 , ry1 , "lc026_frame_section")    
    # 도면틀 넣기
    BasicXscale = 2813
    BasicYscale = 1765
    TargetXscale = 3780 + (CD - 1500)  # 기본 모형이 1450
    TargetYscale = 1715
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
    print("스케일 비율 : " + str(frame_scale))   
    x1 = Abs_Xpos + math.ceil(math.ceil(frame_scale * BasicXscale) / 100) * 100 + 1000 
    y1 = Abs_Ypos - 450 * frame_scale
    insert_frame(  x1 , y1 - 245 , frame_scale, "transom_frame", workplace)   
    
    Textstr = f"Part Name : Frame"    
    draw_Text(doc, x1 + LCCD + 830 + (CD-1500), y1 + 1445 , 30, str(Textstr), layer='0')    
    Textstr = f"Mat.Spec : SPCC1.6t"    
    draw_Text(doc, x1 + LCCD + 830 + (CD-1500), y1 + 1385 , 30, str(Textstr), layer='0')    
    Textstr = f"Size : {LCCD} x 524"    
    draw_Text(doc, x1 + LCCD + 830 + (CD-1500), y1 + 1325 , 30, str(Textstr), layer='0')        
    Textstr = f"Quantity : {su*2} EA"    
    draw_Text(doc, x1 + LCCD + 830 + (CD-1500), y1 + 1265 , 30, str(Textstr), layer='0')    

    #################################################################################################
    # 2page
    #################################################################################################    
    ry1 = ry1 - 245

    x1 = rx1 + 2
    y1 = ry1
    x2 = rx1+LCCW-2
    y2 = y1    
    x3 = x2
    y3 = y2 + 18.5
    x4 = x3
    y4 = y3 + 48.6
    x5 = x4
    y5 = y4 + 12.5
    x6 = x5 + 2
    y6 = y5
    x7 = x6 
    y7 = y6 + 6.1
    x8 = x7 
    y8 = y7 + 246
    x9 = x8 
    y9 = y8 + 48
    x10 = x9 
    y10 = y9 + 115.3
    x11 = x10 
    y11 = y10 + 29
    x12 = rx1
    y12 = y11
    x13 = x12 
    y13 = y12 - 29
    x14 = x13 
    y14 = y13 - 115.3
    x15 = x14 
    y15 = y14 - 48
    x16 = x15 
    y16 = y15 - 246
    x17 = x16 
    y17 = y16 - 6.1
    x18 = x17 + 2
    y18 = y17 
    x19 = x18
    y19 = y18 - 12.5  
    x20 = x19
    y20 = y19 - 48.6
    x21 = x1
    y21 = y1

    prev_x, prev_y = x1, y1  # 첫 번째 점으로 초기화
    lastNum = 21
    for i in range(1, lastNum + 1):
        curr_x, curr_y = eval(f'x{i}'), eval(f'y{i}')
        line(doc, prev_x, prev_y, curr_x, curr_y, layer="레이져")
        prev_x, prev_y = curr_x, curr_y

    #절곡라인        
    line(doc, x20, y20, x3, y3,  layer='hidden')    # 절곡선  
    line(doc, x16, y16, x7, y7,  layer='hidden')    # 절곡선  
    line(doc, x15, y15, x8, y8,  layer='hidden')    # 절곡선  
    line(doc, x14, y14, x9, y9,  layer='hidden')    # 절곡선  
    line(doc, x13, y13, x10, y10,  layer='hidden')    # 절곡선  
    #반대 절곡라인
    line(doc, x19, y19, x4, y4,  layer='22')    # 절곡선  
    # line(doc, x1, y1, x2, y2, layer='레이져')   
    # draw_circle(doc, x1 + 248, y1 + 208.7 , 70 , layer='레이져', color='5')   
    circle70x1 =  rx1 + 250
    circle70y1 =  ry1 + 208.7
    circle_cross(doc, circle70x1 , circle70y1 , 70 , layer='레이져', color='2')    
    circle70x2 =  rx1 +  (LCCW-250) 
    circle70y2 =  circle70y1
    circle_cross(doc, circle70x2 , circle70y2 , 70 , layer='레이져', color='2')        
    dim_diameter(doc, (circle70x1, circle70y1), 70, angle=225, dimstyle="JKW", override=None) # 70은 지름 기록
    circle15x1 =  rx1 + 15
    circle15y1 =  ry1 + 29
    circle_cross(doc, circle15x1 , circle15y1 , 15 , layer='레이져', color='2')    
    circle15x2 =  rx1 +  LCCW - 15
    circle15y2 =  circle15y1
    circle_cross(doc, circle15x2 , circle15y2 , 15 , layer='레이져', color='2')        
    dim_diameter(doc, (circle15x1, circle15y1), 15, angle=225, dimstyle="JKW", override=None) # 70은 지름 기록
    dim_diameter(doc, (circle15x2, circle15y2), 15, angle=225, dimstyle="JKW", override=None) # 70은 지름 기록
    circle20x1 =  rx1 + 100
    circle20y1 =  ry1 + 439
    circle_cross(doc, circle20x1 , circle20y1 , 20 , layer='레이져', color='2')    
    circle20x2 =  rx1 +  LCCW - 100
    circle20y2 =  circle20y1
    circle_cross(doc, circle20x2 , circle20y2 , 20 , layer='레이져', color='2')        
    dim_diameter(doc, (circle20x1, circle20y1), 20, angle=225, dimstyle="JKW", override=None) 
    dim_diameter(doc, (circle20x2, circle20y2), 20, angle=315, dimstyle="JKW", override=None) 
    # 중앙 11파이 단공
    circle11x1 =  rx1 + LCCW/2
    circle11y1 =  ry1 + 509
    circle_cross(doc, circle11x1 , circle11y1 , 11 , layer='레이져', color='2')            
    dim_diameter(doc, (circle11x1, circle11y1), 11, angle=225, dimstyle="JKW", override=None) 

    # 하부 치수선
    dim(doc, x17, y17, x6, y6, 262, text_height=0.22, text_gap=0.07, direction="down")
    dim(doc, x17, y17, x1, y1, 196, text_height=0.22, text_gap=0.07, direction="down")
    dim(doc, x2, y2, x6, y6, 116, text_height=0.22, text_gap=0.07, direction="down")

    # 상부 치수선
    dim(doc, x12, y12, circle70x1 , circle70y1 , 98, text_height=0.22, text_gap=0.07, direction="up")
    dim(doc, circle70x1 , circle70y1 , circle70x2 , circle70y2 ,  412, text_height=0.22, text_gap=0.07, direction="up")
    dim(doc,  circle70x2 , circle70y2, x11, y11 , 412, text_height=0.22, text_gap=0.07, direction="up")
    dim(doc,  x12, y12, circle11x1, circle11y1, 176, text_height=0.22, text_gap=0.07, direction="up")
    dim(doc,  circle11x1, circle11y1, x11, y11, 190, text_height=0.22, text_gap=0.07, direction="up")
    dim(doc,  x12, y12, circle20x1, circle20y1, 240, text_height=0.22, text_gap=0.07, direction="up")
    dim(doc,  circle20x1, circle20y1, circle20x2, circle20y2, 325, text_height=0.22, text_gap=0.07, direction="up")
    dim(doc,  circle20x2, circle20y2, x11, y11, 325, text_height=0.22, text_gap=0.07, direction="up")
    dim(doc,  x12, y12, x11, y11, 308, text_height=0.22, text_gap=0.07, direction="up")

    # 좌측 치수
    dim_vertical_left(doc, x12, y12, circle20x1, circle20y1,  60 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_left(doc, circle15x1, circle15y1,  x1, y1, 107 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_left(doc, x17, y17,  x1, y1, 147 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_left(doc, x12, y12, x17, y17,   147 ,"JKW", text_height=0.20,  text_gap=0.07)

    #70파이 치수선 좌측
    dim_vertical_left(doc, circle70x2, circle70y2, circle70x2 - 150, y1, 150 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_left(doc, circle70x2, circle70y2, circle70x2 - 150, y12, 150 ,"JKW", text_height=0.20,  text_gap=0.07)

    # 우측 치수선
    dim_vertical_right(doc, x11, y11, x10, y10,  200 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_right(doc, x10, y10, x9, y9,  200 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_right(doc,  x9, y9, x8, y8,  270 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_right(doc,  x8, y8, x7, y7,  200 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_right(doc,  x7, y7, x4, y4, 270 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_right(doc,  x4, y4, x3, y3, 200 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_right(doc,  x3, y3, x2, y2, 130 ,"JKW", text_height=0.20,  text_gap=0.07)
    dim_vertical_right(doc,  x11, y11, x2, y2, 342 ,"JKW", text_height=0.20,  text_gap=0.07)

    # 2page LC frame 삽입
    rx1 = Abs_Xpos + math.ceil(math.ceil(frame_scale * BasicXscale) / 100) * 100 + 1500 + TargetXscale + 300
    ry1 = Abs_Ypos + 412 - 1043
    insert_block(rx1 , ry1 , "lc026_framecover")    
    # 도면틀 넣기
    BasicXscale = 2813
    BasicYscale = 1765
    TargetXscale = 1217
    TargetYscale = 670
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
    print("3page 스케일 비율 : " + str(frame_scale))  
    insert_frame(  rx1 - 330 , ry1 - 370  , frame_scale, "transom_frame", workplace)           
    Textstr = f" : {su*2} EA"    
    draw_Text(doc, rx1+780 , ry1 + 35 , 10, str(Textstr), layer='0')    
    draw_Text(doc, rx1+780 , ry1 + 35 - 25 , 10, str(Textstr), layer='0')    

    #############################################################################################
    # 4page
    #############################################################################################
    Abs_Xpos = rx1 - 330 + 1670
    Abs_Ypos = ry1 - 370  

    # 폴리갈 크기 산출
    polygal_width = LCCW - 620
    polygal_height = LCCD/2 - 8
    
    # 도면틀 넣기
    BasicXscale = 2813
    BasicYscale = 1765
    TargetXscale = 2100 + (polygal_width - 930)
    TargetYscale = 1280 + (polygal_height - 710)
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
    print("4page 스케일 비율 : " + str(frame_scale))  
    insert_frame(  Abs_Xpos , Abs_Ypos , frame_scale, "transom_frame", workplace)           
    Textstr = f" : {su*2} EA"    
    draw_Text(doc, rx1+780 , ry1 + 35 , 10, str(Textstr), layer='0')    
    draw_Text(doc, rx1+780 , ry1 + 35 - 25 , 10, str(Textstr), layer='0')    

    # 폴리갈 전개도 기준점 위치
    rx1 = Abs_Xpos + 220
    ry1 = Abs_Ypos + 470

    insideGap = 17    
    x1 = rx1 
    y1 = ry1
    x2 = rx1 + polygal_width 
    y2 = y1 + insideGap    
    rectangle(doc, x1, y1, x2, y2, layer='0')      
    insideGap = 17    
    x1 = rx1 
    y1 = ry1 + polygal_height - 7
    x2 = rx1 + polygal_width 
    y2 = y1 + insideGap    
    rectangle(doc, x1, y1, x2, y2, layer='0')    

    insideGap = polygal_height   
    x1 = rx1 
    y1 = ry1 + 5
    x2 = rx1 + polygal_width 
    y2 = y1 + insideGap    
    rectangle(doc, x1, y1, x2, y2, layer='6')            
    # 폴리갈 해치    
    hatch = msp.add_hatch(dxfattribs={'layer': '55'})  # 5는 파란색 코드입니다.

    # "CORK" 패턴으로 해치 패턴 설정
    hatch.set_pattern_fill("CORK", scale=10.0, color='5')  # 여기서 scale은 패턴의 크기를 조정합니다. 색상지정은 여기서 해야 된다.

    # 경계선 추가 (여기서는 사각형을 예로 듭니다)
    hatch.paths.add_polyline_path(
        [(x1, y1), (x2, y1), (x2, y2), (x1, y2)], 
        is_closed=True
    )

    Textstr =  f"폴리갈 몰딩 절단 칫수 - {polygal_width}"
    dim_string(doc, x1, y2+5, x2, y2+5, 140,  Textstr, text_height=0.33, text_gap=0.07, direction="up")    # 글자키움
    Textstr =  f"폴리갈  - {polygal_width}"
    dim_string(doc, x1, y2+5, x2, y2+5, 65,  Textstr, text_height=0.33, text_gap=0.07, direction="up")    

    # 우측 치수선    
    dim_vertical_right(doc, x2, y2, x2, y2+5, 80, "JKW", text_height=0.20,  text_gap=0.07)    
    dim_vertical_right(doc, x2, y1, x2, y1-5, 80, "JKW", text_height=0.20,  text_gap=0.07)    
    Textstr =  f"폴리갈  - {math.ceil(polygal_height)}"    
    dim_string(doc, x2, y1, x2, y2, 80,  Textstr , text_height=0.20,  text_gap=0.07, direction="aligned_reverse")     # aligned로 나오지 않을때 역방향 개발    
    
    Textstr =  f"폴리갈 몰딩 외경 - {math.ceil(polygal_height+10)}"
    dim_string(doc, x2, y1-5, x2, y2+5, 140,  Textstr , text_height=0.20,  text_gap=0.07, direction="aligned_reverse")     # aligned로 나오지 않을때 역방향 개발    

    # 우측 단면도 
    insideGap = polygal_height   
    rx1 = x2 + 380
    ry1 = ry1 + 5
    x1 = rx1 
    y1 = ry1 
    x2 = rx1 + 6
    y2 = y1 + insideGap    
    rectangle(doc, x1, y1, x2, y2, layer='22')     

    insert_block(x1 , y1 , "polygal_rib_bottom")  
    insert_block(x1 , y2 , "polygal_rib")  

    # 단면도 치수선
    dim_vertical_right(doc, x2, y2, x2, y2 + 5, 36, "JKW", text_height=0.20,  text_gap=0.07)  
    dim_vertical_left(doc, x1, y1-5, x1, y2 + 5, 140, "JKW", text_height=0.24,  text_gap=0.07)  
    dim(doc,  x1, y2, x2, y2, 72, text_height=0.22, text_gap=0.07, direction="up")
    dim(doc,  x1-1.2, y2+5, x2+1.2, y2+5, 112, text_height=0.22, text_gap=0.07, direction="up")
    
    # description
    insideGap = polygal_height   
    rx1 = x2 + 100
    ry1 = ry1 + LCCD/4 + 100
    x1 = rx1 
    y1 = ry1 

    Textstr = f"Part Name : 중판"    
    draw_Text(doc, x1 , y1 , 30 , str(Textstr), layer='0')    
    Textstr = f"Mat.Spec : 폴리갈 6T"    
    draw_Text(doc, x1 , y1 -60 , 30, str(Textstr), layer='0')    
    Textstr = f"Size : {polygal_width} x {polygal_height}"    
    draw_Text(doc, x1 , y1 - 120 , 30, str(Textstr), layer='0')        
    Textstr = f"Quantity : {su*2} EA"    
    draw_Text(doc, x1 , y1 - 180 , 30, str(Textstr), layer='0')    


    #############################################################################################
    # page 5
    #############################################################################################
    Abs_Xpos = rx1 - 330 + 1670

    # 폴리갈 크기 산출
    polygal_width = LCCW - 620
    polygal_height = LCCD/2 - 8
    
    # 도면틀 넣기
    BasicXscale = 2813
    BasicYscale = 1765
    TargetXscale = 2100 + (LCCD - 1450)
    TargetYscale = 1280 
    if(TargetXscale/BasicXscale > TargetYscale/BasicYscale ):
        frame_scale = TargetXscale/BasicXscale
    else:
        frame_scale = TargetYscale/BasicYscale    
    print("5page 스케일 비율 : " + str(frame_scale))  
    insert_frame(  Abs_Xpos , Abs_Ypos , frame_scale, "transom_frame", workplace)           

    # 그리드 14개 1.5 간격 12.5 시작 2.75 시작 후 1.5 간격 13개 확장
    # 프로파일 전개도 기준점 위치
    rx1 = Abs_Xpos + 180
    ry1 = Abs_Ypos + 800
    insideGap = 100   
    x1 = rx1 
    y1 = ry1 
    x2 = rx1 + LCCD - 4
    y2 = y1 + insideGap    
    rectangle(doc, x1, y1, x2, y2, layer='0')  
    line(doc, x1, y1+12.5, x2, y1+12.5,  layer='0')    # 0 선  
    line(doc, x1, y2-12.5, x2, y2-12.5,  layer='0')    # 0 선      
    # 회색선 다량생성    
    line(doc, x1, y1+12.5+2.75, x2, y1+12.5+2.75,  layer='22')    # 0 선  
    line(doc, x1, y1+37.5, x2, y1+37.5,  layer='22')    # 0 선  
    line(doc, x1, y1+12.5+2.75+50, x2, y1+12.5+2.75+50,  layer='22')    # 0 선      
    for i in range(1, 13 + 1):
        line(doc, x1, y1+12.5+2.75+i*1.5, x2, y1+12.5+2.75+i*1.5,  layer='22')    # 0 선  
        line(doc, x1, y1+50+12.5+2.75+i*1.5, x2, y1+50+12.5+2.75+i*1.5,  layer='22')    # 0 선  

    rx1 = Abs_Xpos + 180
    ry1 = Abs_Ypos + 800 + 400
    insideGap = 100   
    x1 = rx1 
    y1 = ry1 
    x2 = rx1 + LCCD - 4
    y2 = y1 + insideGap    
    rectangle(doc, x1, y1, x2, y2, layer='0')  
    line(doc, x1, y1+12.5, x2, y1+12.5,  layer='0')    # 0 선  
    line(doc, x1, y2-12.5, x2, y2-12.5,  layer='0')    # 0 선  
    # 회색선 다량생성    
    line(doc, x1, y1+12.5+2.75, x2, y1+12.5+2.75,  layer='22')    # 0 선  
    line(doc, x1, y1+37.5, x2, y1+37.5,  layer='22')    # 0 선  
    line(doc, x1, y1+12.5+2.75+50, x2, y1+12.5+2.75+50,  layer='22')    # 0 선      
    for i in range(1, 13 + 1):
        line(doc, x1, y1+12.5+2.75+i*1.5, x2, y1+12.5+2.75+i*1.5,  layer='22')    # 0 선  
        line(doc, x1, y1+50+12.5+2.75+i*1.5, x2, y1+50+12.5+2.75+i*1.5,  layer='22')    # 0 선  

    # 선홍색
    rx1 = Abs_Xpos + 180 + 23
    ry1 = Abs_Ypos + 800 + 50 - 2.5
    insideGap = 5   
    x1 = rx1 
    y1 = ry1 
    x2 = rx1 + LCCD - 4 - 23*2
    y2 = y1 + insideGap    
    rectangle(doc, x1, y1, x2, y2, layer='6')  

    rx1 = Abs_Xpos + 180 + 23
    ry1 = Abs_Ypos + 800 + 400 + 50 - 2.5
    insideGap = 5 
    x1 = rx1 
    y1 = ry1 
    x2 = rx1 + LCCD -4 - 23*2
    y2 = y1 + insideGap    
    rectangle(doc, x1, y1, x2, y2, layer='6')  
    insert_block(x2  , y2 - 2.5 , "lc026_profile_wire")  # smps    

    # 단공 3.2파이 6개
    rx1 = Abs_Xpos + 180 + 173
    ry1 = Abs_Ypos + 800 + 50 
    x1 = rx1 
    y1 = ry1 
    circle_cross(doc, x1 , y1 , 3.2 , layer='0', color='4')  
    rx1 = Abs_Xpos + 180 + (LCCD-4)/2 
    ry1 = Abs_Ypos + 800 + 50 
    x1 = rx1 
    y1 = ry1 
    circle_cross(doc, x1 , y1 , 3.2 , layer='0', color='4')  
    rx1 = Abs_Xpos + 180 + LCCD-4 - 173 
    ry1 = Abs_Ypos + 800 + 50 
    x1 = rx1 
    y1 = ry1 
    circle_cross(doc, x1 , y1 , 3.2 , layer='0', color='4')  
    rx1 = Abs_Xpos + 180 + 173
    ry1 = Abs_Ypos + 800 + 400 + 50 
    x1 = rx1 
    y1 = ry1 
    circle_cross(doc, x1 , y1 , 3.2 , layer='0', color='4')  
    rx1 = Abs_Xpos + 180 + (LCCD-4)/2 
    ry1 = Abs_Ypos + 800 + 400 + 50 
    x1 = rx1 
    y1 = ry1 
    circle_cross(doc, x1 , y1 , 3.2 , layer='0', color='4')  
    rx1 = Abs_Xpos + 180 + LCCD-4 - 173 
    ry1 = Abs_Ypos + 800 + 400 + 50 
    x1 = rx1 
    y1 = ry1 
    circle_cross(doc, x1 , y1 , 3.2 , layer='0', color='4')  

    # 블럭삽입 단면도, SMPS 위치
    insert_block(rx1 + 400 , ry1 , "lc026_profile_section")  

    # 치수선
    rx1 = Abs_Xpos + 180  
    ry1 = Abs_Ypos + 800 + 500
    x1 = rx1 
    y1 = ry1 
    x2 = rx1 + LCCD - 4
    y2 = ry1        
    dim(doc,  rx1, ry1, x2, y2, 76, text_height=0.22, text_gap=0.07, direction="up")
    rx1 = Abs_Xpos + 180 + 23
    ry1 = Abs_Ypos + 800 + 400 + 50 - 2.5
    x1 = rx1 
    y1 = ry1 
    x2 = rx1 + LCCD - 4 - 23*2
    y2 = ry1            
    Textstr =  f"LED BAR - 10000K - 1400L (누드&클립&잭타입)"
    dim_string(doc, rx1, ry1, x2, y2, 140,  Textstr, text_height=0.20, text_gap=0.07, direction="down")    

    # description
    insideGap = polygal_height   
    rx1 = Abs_Xpos + 1100
    ry1 = 480 - 900
    x1 = rx1 
    y1 = ry1 

    Textstr = f"Part Name : Frame 용 AL Profile"    
    draw_Text(doc, x1 , y1 , 30 , str(Textstr), layer='0')    
    Textstr = f"Mat.Spec : AL"    
    draw_Text(doc, x1 , y1 -60 , 30, str(Textstr), layer='0')    
    Textstr = f"Size : 100 x 34.6 x {LCCD-4} "    
    draw_Text(doc, x1 , y1 - 120 , 30, str(Textstr), layer='0')        
    Textstr = f"Quantity : {su*2} EA"    
    draw_Text(doc, x1 , y1 - 180 , 30, str(Textstr), layer='0')    

    # 레이져 도면틀 생성 (공통) 레이져에 배열할때 편리한 기능
    # 1219*1950 철판크기 샘플
    rectangle(doc, 10000, 5000,10000+3400 , 5000+ 2340, layer='0')  
    rectangle(doc, 10000+850, 5000+130,10000+850+1950 , 5000+130+1219, layer='레이져')  
    dim(doc, 10000+850, 5000+130+1219, 10000+850+1950, 5000+130+1219, 100, text_height=0.22, text_gap=0.07, direction="up")
    dim_vertical_left(doc,  10000+850, 5000+130, 10000+850 , 5000+130+1219, 150, "JKW", text_height=0.22,  text_gap=0.07)  

    Textstr = f"{secondord} - {workplace} - {drawdate_str_short} 출도, {deadlinedate_str_short} 납기"    
    draw_Text(doc, 10000+300 , 5000+ 2340 - 200 ,  80, str(Textstr), layer='0')        
    Textstr = f"SPCC 1.6Tx1219x1950=1장"        
    draw_Text(doc, 10000+1000 , 5000+ 2340 - 200 - 200 ,  90, str(Textstr), layer='0')        
    
