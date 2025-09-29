import pandas as pd

# 엑셀 파일 불러오기
file_path = 'test.xlsx'
df = pd.read_excel(file_path)

# 데이터 출력
print(df)
