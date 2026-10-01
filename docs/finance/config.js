// docs/config.js
// ⚙️ 여기에서 스프레드시트 ID와 탭 이름만 편하게 수정하세요!

const APP_CONFIG = {
  // 1. 내 구글 스프레드시트 ID (URL 중간의 긴 영문/숫자 조합)
  // 예: https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
  // 이라면 "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms" 만 입력
  SPREADSHEET_ID: "1zPULW7071jJjzatXoFnNy9bvL_0v2q3343YruyN-6rM",

  // 2. 탭 이름 매핑 (시트에 적힌 탭 이름 그대로 입력)
  TABS: {
    DASHBOARD: "총자산 대시보드",
    HISTORY: "부록: 그동안의 기록",
    ISA: "3.ISA",
    DOMESTIC: "2-1.국내주식",
    OVERSEAS: "2-2.해외주식",
    CASH: "1.유동현금",
    PENSION: "4.연금&보험",        // 추가
    IRP: "5.퇴직연금(IRP)"        // 추가
  }
};