import pandas as pd

# 엑셀 파일 읽기
original_df = pd.read_excel('c:/python/원본.xlsx')
modified_df = pd.read_excel('c:/python/수정파일.xlsx')

# 열 이름의 공백 제거
original_df.columns = original_df.columns.str.strip()
modified_df.columns = modified_df.columns.str.strip()

# 거래처 코드를 기준으로 추가된 행 추출
new_rows = modified_df[~modified_df['code'].isin(original_df['code'])]

# 추가된 자료를 새로운 엑셀 파일로 저장
new_rows.to_excel('c:/python/추가자료.xlsx', index=False)

print("추가된 자료가 '추가자료.xlsx' 파일에 저장되었습니다.")