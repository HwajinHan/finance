import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# 키 파일 로드
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# 내 시트 열기 (실제 구글 시트 제목 입력)
SHEET_TITLE = "총자산 대시보드" 

try:
    doc = client.open(SHEET_TITLE)
    sheet = doc.sheet1
    print("✅ 구글 시트 연결 성공!")
    print(f"첫 번째 시트 탭 이름: {sheet.title}")
    
    # 1행 1열 셀 값 읽어보기
    first_val = sheet.cell(1, 1).value
    print(f"A1 셀 값: {first_val}")
except Exception as e:
    print(f"❌ 연결 실패: {e}")