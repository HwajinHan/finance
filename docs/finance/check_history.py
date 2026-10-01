import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(REPO_ROOT, ".env"))

KEY_PATH = os.path.join(BASE_DIR, "service_account.json")
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_PATH, scope)
gc = gspread.authorize(creds)
doc = gc.open("총자산 대시보드")

sheet = doc.worksheet("부록: 그동안의 기록")
rows = sheet.get_all_values()[:7]

print("=== [부록: 그동안의 기록 상위 7개 행] ===")
for idx, r in enumerate(rows):
    print(f"{idx+1}행: {r}")