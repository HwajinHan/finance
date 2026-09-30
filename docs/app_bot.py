import os
import io
import json
import discord
from dotenv import load_dotenv
from PIL import Image
from google import genai
from google.genai import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import git
from datetime import datetime

# 1. 환경변수 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))  # Git 루트 폴더
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(REPO_ROOT, ".env"))

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SHEET_TITLE = os.getenv("SHEET_TITLE", "총자산 대시보드")
KEY_PATH = os.path.join(BASE_DIR, "service_account.json")

# 2. 구글 Gemini 클라이언트 초기화
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# 3. 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# 4. 구글 시트 연결
def get_spreadsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_PATH, scope)
    gc = gspread.authorize(creds)
    return gc.open(SHEET_TITLE)

# 5. Gemini를 통한 스크린샷 분석
def parse_asset_screenshot(image_bytes: bytes) -> dict:
    prompt = """
    당신은 자산 관리 전문 데이터 추출 AI입니다.
    제공된 주식/계좌 잔고 스크린샷을 분석하여 다음 JSON 규격으로만 응답하세요. 마크다운 따옴표(```json) 없이 순수 JSON만 반환하세요.
    
    규칙:
    1. target_tab: 다음 목록 중 화면의 계좌와 가장 일치하는 탭 이름을 정확히 고르세요.
       ["1.유동현금", "2-1.국내주식", "2-2.해외주식", "3.ISA", "4.연금&보험", "5.퇴직연금(IRP)"]
    2. items: 화면에 표시된 모든 보유 종목과 보유 수량을 추출하세요.
       - name: 종목명 (예: KODEX 미국S&P500, TIGER 미국배당다우존스 등)
       - quantity: 보유 수량 (반드시 숫자 정수 또는 소수)
    
    반환 JSON 예시:
    {
        "target_tab": "3.ISA",
        "items": [
            {"name": "1Q 미국S&P500", "quantity": 1150},
            {"name": "KODEX 미국S&P500", "quantity": 190}
        ]
    }
    """
    image = Image.open(io.BytesIO(image_bytes))
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[image, prompt]
    )
    
    text = response.text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])
    return json.loads(text)

# 6. 구글 시트 수량 갱신 함수 (C열=종목명, E열=수량)
def update_sheet_quantities(target_tab: str, items: list) -> list:
    doc = get_spreadsheet()
    sheet = doc.worksheet(target_tab)
    
    # C열(종목명) 전체 읽기
    stock_names = sheet.col_values(3)
    results = []
    
    for item in items:
        name = item["name"]
        qty = item["quantity"]
        matched_row = None
        
        # 종목명 매칭 (부분 일치 지원)
        for idx, s_name in enumerate(stock_names, start=1):
            if idx <= 2:  # 1~2행은 헤더이므로 스킵
                continue
            if name.replace(" ", "") in s_name.replace(" ", "") or s_name.replace(" ", "") in name.replace(" ", ""):
                matched_row = idx
                break
        
        if matched_row:
            # 5번째 열(E열: 보유수량) 업데이트
            sheet.update_cell(matched_row, 5, qty)
            results.append(f"✅ [{stock_names[matched_row-1]}] ➔ {qty:,}주 갱신")
        else:
            results.append(f"⚠️ [{name}] 시트에서 종목을 찾지 못함 (수동 확인 필요)")
            
    return results

# 7. 대시보드 탭 읽어서 HTML 생성 및 GitHub Pages 푸시
def build_and_deploy_web():
    doc = get_spreadsheet()
    dash = doc.worksheet("총자산 대시보드")
    data = dash.get_all_values()
    
    # 2행: 총 순자산
    total_net_worth = data[1][1] if len(data) > 1 else "0"
    
    # 3행부터 10행까지의 자산 분류 테이블
    rows_html = ""
    for r in data[2:10]:
        cat_name = r[0]
        amount = r[1]
        weight = r[2] if len(r) > 2 else ""
        note = r[6] if len(r) > 6 else ""
        rows_html += f"""
        <tr>
            <td><strong>{cat_name}</strong></td>
            <td style="text-align:right; font-weight:600;">{amount} 원</td>
            <td style="text-align:center;"><span class="badge">{weight}</span></td>
            <td style="color:#64748b; font-size:13px;">{note}</td>
        </tr>
        """
        
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Portfolio Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; margin: 0; padding: 20px; color: #1e293b; }}
        .container {{ max-width: 680px; margin: 0 auto; background: white; border-radius: 16px; padding: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .header {{ border-bottom: 2px solid #f1f5f9; padding-bottom: 16px; margin-bottom: 20px; }}
        .title {{ font-size: 14px; color: #64748b; margin-bottom: 4px; }}
        .total {{ font-size: 32px; font-weight: 800; color: #2563eb; }}
        .updated {{ font-size: 12px; color: #94a3b8; margin-top: 8px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
        th, td {{ padding: 12px 10px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }}
        th {{ background: #f8fafc; color: #475569; text-align: left; }}
        .badge {{ background: #eff6ff; color: #1d4ed8; padding: 4px 8px; border-radius: 6px; font-weight: 600; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">총 순자산</div>
            <div class="total">{total_net_worth} 원</div>
            <div class="updated">마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>자산 분류</th>
                    <th style="text-align:right;">금액</th>
                    <th style="text-align:center;">비중</th>
                    <th>비고</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    # docs/index.html 저장
    index_path = os.path.join(BASE_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    # Git Push
    repo = git.Repo(REPO_ROOT)
    repo.git.add("docs/index.html")
    repo.index.commit(f"Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    repo.remote(name="origin").push()
    return "GitHub 배포 완료"

# 8. 디스코드 이벤트 핸들러
@bot.event
async def on_ready():
    print(f"🚀 자산 관리 자동화 봇 가동 시작: {bot.user.name}")
    print("디스코드에 계좌 잔고 스크린샷을 올려보세요!")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
        
    # 이미지가 업로드되었을 때
    if message.attachments:
        for att in message.attachments:
            if any(att.filename.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]):
                status_msg = await message.reply("🔍 Gemini AI가 스크린샷을 분석 중입니다...")
                
                try:
                    img_bytes = await att.read()
                    parsed = parse_asset_screenshot(img_bytes)
                    
                    target_tab = parsed.get("target_tab")
                    items = parsed.get("items", [])
                    
                    await status_msg.edit(content=f"📊 **[{target_tab}]** 계좌 감지 완료! 시트 수량을 갱신 중입니다...")
                    
                    # 시트 갱신
                    update_logs = update_sheet_quantities(target_tab, items)
                    log_text = "\n".join(update_logs)
                    
                    # 웹사이트 배포
                    await status_msg.edit(content=f"🌐 웹사이트(GitHub Pages) 대시보드 갱신 중...")
                    build_and_deploy_web()
                    
                    await status_msg.edit(content=(
                        f"✨ **업데이트 완료!**\n\n"
                        f"📁 **대상 탭**: `{target_tab}`\n"
                        f"{log_text}\n\n"
                        f"👉 [내 웹 대시보드 확인하기](https://hwajinhan.github.io/finance/)"
                    ))
                except Exception as e:
                    await status_msg.edit(content=f"❌ 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)