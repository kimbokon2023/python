import pandas as pd

# 엑셀 파일 읽기
original_df = pd.read_excel('c:/python/이전품목코드.xlsx')
modified_df = pd.read_excel('c:/python/이후품목코드.xlsx')

# 열 이름의 공백 제거
original_df.columns = original_df.columns.str.strip()
modified_df.columns = modified_df.columns.str.strip()

# 코드 열에서 공백 제거 및 대소문자 통일 (필요 시)
original_df['품목코드'] = original_df['품목코드'].str.strip().str.upper()
modified_df['품목코드'] = modified_df['품목코드'].str.strip().str.upper()

# 거래처 코드를 기준으로 추가된 행 추출
new_rows = modified_df[~modified_df['품목코드'].isin(original_df['품목코드'])]

# 결과 확인
print("추출된 추가 자료:\n", new_rows)

# 추가된 자료를 새로운 엑셀 파일로 저장
new_rows.to_excel('c:/python/추가품목코드.xlsx', index=False, header=True)

print("추가된 자료가 파일에 저장되었습니다.")

# # 엑셀 파일 읽기
# original_df = pd.read_excel('c:/python/이전거래처코드.xlsx')
# modified_df = pd.read_excel('c:/python/이후거래처코드.xlsx')

# # 열 이름의 공백 제거
# original_df.columns = original_df.columns.str.strip()
# modified_df.columns = modified_df.columns.str.strip()

# # 코드 열에서 공백 제거 및 대소문자 통일 (필요 시)
# original_df['거래처명'] = original_df['거래처명'].str.strip().str.upper()
# modified_df['거래처명'] = modified_df['거래처명'].str.strip().str.upper()

# # 거래처 코드를 기준으로 추가된 행 추출
# new_rows = modified_df[~modified_df['거래처명'].isin(original_df['거래처명'])]

# # 결과 확인
# print("추출된 추가 자료:\n", new_rows)

# # 추가된 자료를 새로운 엑셀 파일로 저장
# new_rows.to_excel('c:/python/추가거래처.xlsx', index=False, header=True)

# print("추가된 자료가 파일에 저장되었습니다.")
