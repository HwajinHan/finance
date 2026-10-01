import os

# 1. 윈도우 기본 Git 경로 지정 (본인 컴퓨터의 git.exe 경로로 확인)
git_path = r"C:\Program Files\Git\bin\git.exe"

# 만약 위 경로에 없다면 cmd 폴더 확인
if not os.path.exists(git_path):
    git_path = r"C:\Program Files\Git\cmd\git.exe"

import git
import os
from datetime import datetime

# 현재 폴더를 Git 저장소로 인식
repo = git.Repo(".")

# 1. 간단한 HTML 파일 생성 (대시보드 웹페이지)
html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>내 자산 대시보드</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #f8fafc; padding: 24px; margin: 0; }}
        .card {{ max-width: 500px; margin: 0 auto; background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        h1 {{ font-size: 20px; color: #1e293b; margin-top: 0; }}
        .time {{ color: #64748b; font-size: 14px; margin-bottom: 20px; }}
        .success {{ color: #059669; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>📊 내 자산 대시보드 (테스트)</h1>
        <p class="time">최근 갱신: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p class="success">✅ GitHub Pages 자동 배포 파이프라인이 정상 작동 중입니다!</p>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("1. index.html 파일 생성 완료")

# 2. Git 스테이징, 커밋 및 푸시
try:
    repo.git.add("index.html")
    repo.index.commit(f"Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    origin = repo.remote(name="origin")
    origin.push()
    print("2. 🚀 GitHub에 Push 성공!")
except Exception as e:
    print(f"❌ Git 푸시 실패: {e}")