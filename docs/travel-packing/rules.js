// docs/travel-packing/rules.js
const PACKING_RULES = [
  // ==========================================
  // [1. 만국공통 필수품 (모든 여행)]
  // ==========================================
  {
    name: "자외선 차단제 (선크림 / 바디용 선스틱·선스프레이)",
    category: "스킨케어/위생",
    tip: "팔다리 탈색 방지용으로는 슥슥 바르는 선스틱이 필수",
    condition: () => true,
  },
  {
    name: "보조배터리 & 충전 케이블",
    category: "전자기기",
    tip: "이동 중 지도 검색 및 카메라 배터리 방전 대비 (기내 휴대 필수)",
    condition: () => true,
  },
  {
    name: "비상약 & 피로회복제 (간 영양제, 종합감기약, 진통제)",
    category: "상비약/건강",
    tip: "강행군 여행 시 간 영양제/비타민으로 피로 회복",
    condition: () => true,
  },
  {
    name: "잠옷 (편한 실내복)",
    category: "의류",
    tip: "짐 쌀 때 가장 자주 빼먹는 항목 1위",
    condition: () => true,
  },
  {
    name: "휴지, 휴대용 물티슈, 비닐봉지(쓰레기/빨랫감용)",
    category: "위생/편의",
    condition: () => true,
  },
  {
    name: "인생샷용 경량 삼각대 / 셀카봉",
    category: "전자기기",
    condition: () => true,
  },

  // ==========================================
  // [2. 해외여행 특화 필수템]
  // ==========================================
  {
    name: "여권 및 여권 사본",
    category: "중요서류",
    condition: (ans) => ans.destinationType === "international",
  },
  {
    name: "해외결제 카드 2종류 이상 (Visa, Master, Amex 교차 준비)",
    category: "금융/결제",
    tip: "단일 브랜드는 현지 카드망 오류로 결제 거부될 수 있음",
    condition: (ans) => ans.destinationType === "international",
  },
  {
    name: "만능 멀티 어댑터 (국가별 변환 플러그)",
    category: "전자기기",
    condition: (ans) => ans.destinationType === "international",
  },
  {
    name: "3구 휴대용 멀티탭",
    category: "전자기기",
    tip: "콘센트가 적은 숙소에서 스마트폰, 보조배터리, 카메라 동시 충전용",
    condition: (ans) => ans.destinationType === "international",
  },
  {
    name: "비상용 컵라면 / 매운 라면(불닭 등)",
    category: "식품/간식",
    tip: "현지 음식 물릴 때 구원투수 (서양권 갈 때 필수)",
    condition: (ans) => ans.destinationType === "international",
  },
  {
    name: "수면/휴식용 목베개 & 안대",
    category: "비행/이동",
    tip: "장시간 비행기/기차 탑승 시 목 디스크 방지",
    condition: (ans) => ans.destinationType === "international",
  },

  // ==========================================
  // [3. 유럽 / 석회수 / 도보 여행 특화]
  // ==========================================
  {
    name: "고영양 헤어팩 & 고보습 린스",
    category: "스킨케어/위생",
    tip: "유럽 특유의 석회수물 머릿결 뻣뻣해짐 방지",
    condition: (ans) => ans.region === "europe",
  },
  {
    name: "고보습 핸드크림",
    category: "스킨케어/위생",
    tip: "사계절 불문 석회수 손 뻑뻑함 방지",
    condition: (ans) => ans.region === "europe",
  },
  {
    name: "소매치기 방지 스프링줄 & 복대",
    category: "안전/보안",
    condition: (ans) => ans.region === "europe",
  },
  {
    name: "샤워기 헤드 필터",
    category: "스킨케어/위생",
    condition: (ans) => ans.region === "europe" || ans.region === "southeast-asia",
  },

  // ==========================================
  // [4. 일정/도보량/체류 기간 분기]
  // ==========================================
  {
    name: "휴족시간 (발바닥 쿨링 패치) 또는 입욕제",
    category: "피로회복",
    tip: "하루 20,000보 이상 걸은 날 다리 붓기 완화용",
    condition: (ans) => ans.nature === "city" || ans.nature === "mountain" || ans.nights >= 3,
  },
  {
    name: "1일 1팩 마스크팩",
    category: "스킨케어/위생",
    tip: "강한 햇빛에 지친 피부 진정 및 수분 보충",
    condition: (ans) => ans.nights >= 2,
    quantity: (ans) => `${ans.nights}장`,
  },
  {
    name: "휴대용 소포장 세탁세제",
    category: "위생/편의",
    tip: "폼클렌징으로 빨래하는 대참사 방지",
    condition: (ans) => ans.nights >= 4,
  },
  {
    name: "블루투스 키보드",
    category: "전자기기",
    tip: "스마트폰으로 당일 여행 일기 및 블로그 기록 시 편리",
    condition: (ans) => ans.nights >= 4,
  },

  // ==========================================
  // [5. 자연/등산/벌레 특화]
  // ==========================================
  {
    name: "모기 기피제 & 물린 뒤 바르는 약(버물리)",
    category: "상비약/건강",
    tip: "휴양지, 숲길, 동남아 및 유럽 남부 필수",
    condition: (ans) => ans.region === "southeast-asia" || ans.nature === "mountain" || ans.nature === "sea",
  },
  {
    name: "등산화 & 등산양말 (발목 지지용)",
    category: "등산/활동",
    condition: (ans) => ans.nature === "mountain",
  },
  {
    name: "등산스틱 (무릎 충격 완화)",
    category: "등산/활동",
    condition: (ans) => ans.nature === "mountain",
  },
  {
    name: "체온 조절용 여벌옷 (등산조끼/바람막이)",
    category: "등산/활동",
    condition: (ans) => ans.nature === "mountain",
  },
  {
    name: "등산 장갑 & 모자",
    category: "등산/활동",
    condition: (ans) => ans.nature === "mountain",
  },
  {
    name: "휴대용 접이식 방석",
    category: "등산/활동",
    tip: "바위 쉼터에서 휴식할 때 엉덩이 보호",
    condition: (ans) => ans.nature === "mountain",
  },
  {
    name: "당충전 간식 (초콜릿, 에너지바, 식염포도당)",
    category: "음식/간식",
    condition: (ans) => ans.nature === "mountain",
  },
  {
    name: "스포츠 타월 / 땀 닦는 손수건",
    category: "등산/활동",
    condition: (ans) => ans.nature === "mountain" || ans.nature === "sea",
  },

  // ==========================================
  // [6. 물놀이 / 바다 특화]
  // ==========================================
  {
    name: "수영복 및 래시가드",
    category: "물놀이/비치",
    condition: (ans) => ans.hasSwimming === true || ans.nature === "sea",
  },
  {
    name: "스마트폰 방수팩 & 대형 비치타월",
    category: "물놀이/비치",
    condition: (ans) => ans.hasSwimming === true || ans.nature === "sea",
  },
  {
    name: "아쿠아슈즈 또는 방수 슬리퍼",
    category: "물놀이/비치",
    condition: (ans) => ans.hasSwimming === true || ans.nature === "sea",
  }
];