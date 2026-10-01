import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "service_account.json")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_PATH, scope)
gc = gspread.authorize(creds)
doc = gc.open("총자산 대시보드")

# ISA 탭의 상위 5행 데이터 확인
isa_sheet = doc.worksheet("3.ISA")
print("=== [3.ISA 탭 상위 5개 행] ===")
for i, row in enumerate(isa_sheet.get_all_values()[:5]):
    print(f"{i+1}행: {row}")

# 총자산 대시보드 상위 10개 행 확인
dash_sheet = doc.worksheet("총자산 대시보드")
print("\n=== [총자산 대시보드 탭 상위 10개 행] ===")
for i, row in enumerate(dash_sheet.get_all_values()[:10]):
    print(f"{i+1}행: {row}")