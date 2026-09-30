import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()
SHEET_TITLE = os.getenv("SHEET_TITLE", "내_구글시트_이름")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
gc = gspread.authorize(creds)
doc = gc.open(SHEET_TITLE)

print(f"📄 스프레드시트 이름: {doc.title}")
print("--- [탭 목록 및 첫 줄(헤더)] ---")
for worksheet in doc.worksheets():
    first_row = worksheet.row_values(1)
    print(f"🔹 탭 이름: [{worksheet.title}] -> 헤더: {first_row}")