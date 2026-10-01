import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import git
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(REPO_ROOT, ".env"))

SHEET_TITLE = os.getenv("SHEET_TITLE", "총자산 대시보드")
KEY_PATH = os.path.join(BASE_DIR, "service_account.json")

# 1. 구글 시트 연결
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_PATH, scope)
gc = gspread.authorize(creds)
doc = gc.open(SHEET_TITLE)
dash_sheet = doc.worksheet("총자산 대시보드")
rows = dash_sheet.get_all_values()

# 2. 데이터 추출
# 2행: 총 순자산 및 시장 지수
total_net_worth = rows[1][1] if len(rows) > 1 else "0"
kospi_val = rows[1][8] if len(rows[1]) > 8 and rows[1][8] else "-"
nasdaq_val = rows[1][9] if len(rows[1]) > 9 and rows[1][9] else "-"

# 3행부터 10행: 개별 자산 항목
asset_cards_html = ""
for r in rows[2:10]:
    if not r or not r[0]:
        continue
    category = r[0]
    amount = r[1]
    curr_weight = r[2] if len(r) > 2 else "0%"
    target_weight = r[3] if len(r) > 3 and r[3] else "-"
    note = r[6] if len(r) > 6 else ""

    asset_cards_html += f"""
    <div class="asset-card">
        <div class="card-main">
            <span class="category-name">{category}</span>
            <span class="category-amount">{amount} 원</span>
        </div>
        <div class="card-sub">
            <span class="weight-badge">비중 {curr_weight}</span>
            <span class="target-text">목표: {target_weight}</span>
            <span class="note-text">{note}</span>
        </div>
    </div>
    """

# 3. 모바일 최적화 반응형 HTML 템플릿
html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>내 자산 포트폴리오</title>
    <style>
        :root {{
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --primary: #2563eb;
            --border: #e2e8f0;
        }}
        * {{ box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", Roboto, sans-serif; }}
        body {{ background-color: var(--bg); color: var(--text-primary); margin: 0; padding: 16px; display: flex; justify-content: center; }}
        .container {{ width: 100%; max-width: 520px; }}
        
        .hero-card {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: #ffffff;
            border-radius: 20px;
            padding: 24px 20px;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
            margin-bottom: 20px;
        }}
        .hero-label {{ font-size: 13px; opacity: 0.85; margin-bottom: 6px; font-weight: 500; }}
        .hero-total {{ font-size: 30px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 16px; }}
        
        .market-pills {{ display: flex; gap: 8px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 14px; font-size: 12px; }}
        .market-pill {{ background: rgba(255,255,255,0.15); padding: 4px 10px; border-radius: 12px; }}

        .section-header {{ display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 12px; padding: 0 4px; }}
        .section-title {{ font-size: 16px; font-weight: 700; color: var(--text-primary); }}
        .sync-time {{ font-size: 11px; color: var(--text-secondary); }}

        .asset-list {{ display: flex; flex-direction: column; gap: 10px; }}
        .asset-card {{
            background: var(--card-bg);
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
            border: 1px solid var(--border);
        }}
        .card-main {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
        .category-name {{ font-size: 15px; font-weight: 600; color: var(--text-primary); }}
        .category-amount {{ font-size: 16px; font-weight: 700; color: var(--text-primary); }}
        
        .card-sub {{ display: flex; align-items: center; gap: 8px; font-size: 12px; }}
        .weight-badge {{ background: #eff6ff; color: var(--primary); font-weight: 700; padding: 2px 8px; border-radius: 6px; }}
        .target-text {{ color: var(--text-secondary); }}
        .note-text {{ color: #94a3b8; margin-left: auto; font-size: 11px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; max-width: 140px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="hero-card">
            <div class="hero-label">총 순자산</div>
            <div class="hero-total">{total_net_worth} 원</div>
            <div class="market-pills">
                <span class="market-pill">KOSPI <strong>{kospi_val}</strong></span>
                <span class="market-pill">NASDAQ <strong>{nasdaq_val}</strong></span>
            </div>
        </div>

        <div class="section-header">
            <span class="section-title">자산별 구성</span>
            <span class="sync-time">동기화: {datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
        </div>

        <div class="asset-list">
            {asset_cards_html}
        </div>
    </div>
</body>
</html>
"""

# 4. docs/index.html 저장
index_path = os.path.join(BASE_DIR, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print("1. docs/index.html 생성 완료")

# 5. Git Push (GitHub Pages 자동 반영)
try:
    repo = git.Repo(REPO_ROOT)
    repo.git.add("docs/index.html")
    repo.index.commit(f"Update dashboard: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    repo.remote(name="origin").push()
    print("2. GitHub 배포 푸시 완료!")
except Exception as e:
    print(f"2. Git 푸시 실패: {e}")