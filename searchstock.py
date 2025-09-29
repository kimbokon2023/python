import win32com.client

# 키움증권 OpenAPI+ 연결
kiwoom = win32com.client.Dispatch("KHOPENAPI.KHOpenAPICtrl.1")

# 종목 리스트 가져오기
def get_stock_list():
    stock_codes = kiwoom.GetCodeListByMarket("0")  # 0: 코스피, 10: 코스닥
    return stock_codes.split(';')

# 종목별 데이터 조회
def get_stock_data(stock_code):
    kiwoom.SetInputValue("종목코드", stock_code)
    kiwoom.SetInputValue("기간", "100")  # 100일 이동평균 계산
    kiwoom.CommRqData("주가데이터요청", "OPT10081", 0, "0101")

# 필터링된 종목 리스트
filtered_stocks = []

for code in get_stock_list():
    get_stock_data(code)
    
    # 이동평균선 필터링
    ma7 = kiwoom.GetCommData("OPT10081", "주가데이터요청", 0, "이동평균7")
    ma15 = kiwoom.GetCommData("OPT10081", "주가데이터요청", 0, "이동평균15")
    if float(ma7) > float(ma15):  # 골든크로스 발생
        filtered_stocks.append(code)

print("조건을 만족하는 종목 리스트:", filtered_stocks)
