// 준비물 마스터 데이터 및 조건 규칙 테이블
const PACKING_RULES = [
  // [공통 필수품]
  {
    name: "스마트폰 충전기 및 보조배터리",
    category: "전자기기",
    condition: () => true, // 항상 포함
  },
  {
    name: "세면도구 키트 (칫솔, 치약, 폼클렌징)",
    category: "위생용품",
    condition: (answers) => answers.stayType !== "hotel", // 호텔이면 기본 어메니티 제외 가능
  },

  // [해외/국내 분기]
  {
    name: "여권 및 여권 사본",
    category: "중요서류",
    condition: (answers) => answers.destinationType === "international",
  },
  {
    name: "현지 유심 / eSIM / 포켓와이파이",
    category: "전자기기",
    condition: (answers) => answers.destinationType === "international",
  },
  {
    name: "트래블로그/외화 체크카드 및 비상 현금",
    category: "금융",
    condition: (answers) => answers.destinationType === "international",
  },

  // [지역별 분기]
  {
    name: "소매치기 방지 스프링줄 & 복대",
    category: "보안",
    condition: (answers) => answers.region === "europe",
  },
  {
    name: "ESTA(전자여행허가) 승인증 출력본",
    category: "중요서류",
    condition: (answers) => answers.region === "usa",
  },
  {
    name: "110V 돼지코 어댑터",
    category: "전자기기",
    condition: (answers) => answers.region === "usa" || answers.country === "japan",
  },
  {
    name: "모기 기피제 및 버물리",
    category: "상비약",
    condition: (answers) => answers.region === "southeast-asia" || answers.nature === "mountain",
  },
  {
    name: "샤워기 필터",
    category: "위생용품",
    condition: (answers) => answers.region === "southeast-asia" || answers.region === "europe",
  },

  // [활동/장소 분기]
  {
    name: "수영복 및 래시가드",
    category: "의류",
    condition: (answers) => answers.hasSwimming === true,
  },
  {
    name: "방수팩 & 비치타월",
    category: "액티비티",
    condition: (answers) => answers.hasSwimming === true || answers.nature === "sea",
  },
  {
    name: "등산화 / 트레킹화",
    category: "의류",
    condition: (answers) => answers.nature === "mountain",
  },
  {
    name: "휴대용 우비 / 윈드브레이커",
    category: "의류",
    condition: (answers) => answers.nature === "mountain",
  },

  // [일정/기간 분기]
  {
    name: "속옷 및 양말 (충분한 수량)",
    category: "의류",
    condition: (answers) => answers.nights >= 1,
    quantity: (answers) => `${Math.min(answers.nights + 1, 7)}벌`,
  },
  {
    name: "여행용 압축 파우치",
    category: "수납",
    condition: (answers) => answers.nights >= 4,
  }
];