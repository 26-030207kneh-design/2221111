import random
import Streamlit as st

st.set_page_config(
    Page_title="AI 판사: 균형의 법정 v13.0",
    Page_icon="⚖️",
    Layout="wide"
)

# ---------------------------------------------------------
# 판사 사법 성향 진단 로직
# ---------------------------------------------------------
Def analyze_judge_persona(humanity, law, public, trust):
    If law >= 65 and humanity < 45:
        Return {
            "title": "⚖️ 엄격한 법치주의 원칙관",
            "desc": "법조문과 객관적 증거를 철저히 존중하며 엄벌을 통해 법의 엄정함을 세우는 스타일입니다."
        }
    Elif humanity >= 65 and law < 45:
        Return {
            "title": "❤️ 온건한 인권 중심 재판관",
            "desc": "피고인의 성장 환경, 교화 가능성, 심신 상태를 깊이 참작하는 스타일입니다."
        }
    Elif public >= 65 and trust >= 65:
        Return {
            "title": "🛡️ 사회 안전 및 공익 수호관",
            "desc": "공공의 안전과 법질서 유지, 사회적 신뢰 회복을 최우선으로 고려하는 스타일입니다."
        }
    Else:
        Return {
            "title": "⚖️ 균형 잡힌 중용의 사법관",
            "desc": "법적 엄격함과 피고인의 사정, 공공의 이익을 다각도로 양립시키는 성숙한 재판 스타일입니다."
        }

# ---------------------------------------------------------
# 사건 데이터베이스 (자유 형량 선고용 메타데이터 포함)
# ---------------------------------------------------------
ALL_CASES = [
    # --- [무죄 판례 예시] ---
    {
        "id": "m_01",
        "title": "치과의사 모녀 살인 사건",
        "category": "무죄 판례 / 간접증거와 무죄추정",
        "story": "출근한 치과의사 남편이 집을 나선 후 아내와 딸이 안방 욕조에서 숨진 채 발견되었습니다.",
        "img1": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "수온 변화와 체온 감정 결과 출근 전 살해함이 명백하므로 사형에 처해야 합니다.",
        "defense": "사망시각 법의학 오차가 크며 직접증거가 없으므로 무죄입니다.",
        "ev2": "[정밀감정] 욕조 수온 식는 속도 오차로 정확한 사망 시각 특정이 불가능함이 확인됨.",
        "real_verdict": "무죄 확정 (대법원)",
        "real_reason": "간접증거만으로는 합리적 의심을 배척할 만큼 범죄가 입증되지 않아 무죄 확정.",
        "is_innocent_case": True
    },
    {
        "id": "m_02",
        "title": "낙동강 변 자갈타이어 살인 사건",
        "category": "무죄 판례 / 고문 자백과 재심 무죄",
        "story": "낙동강 변에서 발생한 살인 사건으로 체포되어 자백했으나, 21년 뒤 고문에 의한 허위 자백임이 밝혀졌습니다.",
        "img1": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80",
        "prosecution": "당시 자백 진술이 구체적이므로 기존 유죄 판결이 유지되어야 합니다.",
        "defense": "불법 체포 및 물고문으로 인한 허위 자백이므로 무죄입니다.",
        "ev2": "[재심 조사] 수사관들의 불법 감금 및 물고문 정황과 위법 수사가 공식 확인됨.",
        "real_verdict": "재심 무죄 확정 (대법원)",
        "real_reason": "고문으로 얻은 자백은 증거능력이 없으며 이를 제외하면 범행 입증 증거가 없음.",
        "is_innocent_case": True
    },

    # --- [무기징역 판례 예시] ---
    {
        "id": "l_01",
        "title": "고유정 전 남편 살인 사건",
        "category": "무기징역 판례 / 약물 계획 살인",
        "story": "피고인은 전 남편에게 졸피뎀을 투여한 후 살해하고 사체를 훼손 및 유기했습니다.",
        "img1": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "치밀하게 계획된 살인이므로 무기징역 선고가 필요합니다.",
        "defense": "성폭행 시도에 대응한 우발적 정당방위였습니다.",
        "ev2": "[국과수 감정] 계획적 졸피뎀 구입 및 사전 수색 기록 확보.",
        "real_verdict": "무기징역 확정 (대법원)",
        "real_reason": "사전 약물 준비 및 잔혹한 사체 훼손 등 치밀한 계획 살인 인정.",
        "is_innocent_case": False
    },

    # --- [유기징역 판례 예시] ---
    {
        "id": "t_01",
        "title": "음주운전 2회 적발 인명 피해 사건",
        "category": "유기징역 판례 / 윤창호법 특가법",
        "story": "음주운전 재범 상태에서 인도로 돌진하여 보행자에게 중상을 입히고 도주하려 한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "윤창호법을 적용하여 징역 8년 중형에 처해야 합니다.",
        "defense": "자백하고 피해자와 합의를 진행 중입니다.",
        "ev2": "[블랙박스] 음주 수치 0.18% 및 도주 시도 정황 확보.",
        "real_verdict": "징역 6년 선고 확정",
        "real_reason": "특가법상 위험운전치상 및 재범 가중처벌 적용.",
        "is_innocent_case": False
    }
]

def clamp(v):
    Return max(0, min(100, v))

# 세션 초기화
if "initialized" not in st.session_state:
    St.session_state.initialized = True
    St.session_state.judge_name = "전자고사법관"
    St.session_state.humanity = 50
    St.session_state.law = 50
    St.session_state.public = 50
    St.session_state.trust = 60
    St.session_state.case_index = 0
    St.session_state.postpone_credits = 1  # 💡 1회 제한
    St.session_state.is_postponed = False
    St.session_state.history = []

    St.session_state.cases = random.sample(ALL_CASES, min(3, len(ALL_CASES)))

St.title("⚖️ AI 판사: 균형의 법정 v13.0 (자유 형량 선고 시스템)")

# 사이드바
with st.sidebar:
    St.header(f"🏛️ {st.session_state.judge_name}")
    St.divider()
    St.subheader("📊 현재 사법 지표")
    St.progress(st.session_state.humanity / 100, text=f"❤️ 인간 중심: {st.session_state.humanity}")
    St.progress(st.session_state.law / 100, text=f"📜 법적 엄격함: {st.session_state.law}")
    St.progress(st.session_state.public / 100, text=f"🏛️ 공공 이익: {st.session_state.public}")
    St.progress(st.session_state.trust / 100, text=f"🛡️ 사회적 신뢰: {st.session_state.trust}")
    St.divider()
    St.info(f"🔍 2차 정밀 증거 요청 찬스: **{st.session_state.postpone_credits} / 1회 남음**")
    St.divider()
    If st.button("🔄 새 게임 시작"):
        St.session_state.clear()
        St.rerun()

# 게임 진행 화면
if st.session_state.case_index < len(st.session_state.cases):
    Case = st.session_state.cases[st.session_state.case_index]
    
    St.caption(f"📍 재판 진행도: {st.session_state.case_index + 1} / 3")
    St.subheader(f"⚖️ 사건 {st.session_state.case_index + 1}: {case['title']}")
    St.caption(f"분야: {case['category']}")

    Col_img, col_info = st.columns([1, 1.2])
    With col_img:
        If not st.session_state.is_postponed:
            St.image(case["img1"], caption="📸 1차 제출 현장 증거 사진", use_container_width=True)
        Else:
            St.image(case["img2"], caption="🔍 2차 정밀 포렌식/부검 증거 사진", use_container_width=True)

    With col_info:
        St.info(f"**사건 개요:**\n\n{case['story']}")
        T1, t2 = st.tabs(["⚖️ 검찰 구형", "🛡️ 변호인 변론"])
        With t1:
            St.write(case["prosecution"])
        With t2:
            St.write(case["defense"])

    If st.session_state.is_postponed:
        St.success(f"🔍 **2차 추가 증거 개시:**\n\n{case['ev2']}")

    St.divider()
    
    # --- 판결 유예 버튼 로직 ---
    If not st.session_state.is_postponed:
        If st.session_state.postpone_credits > 0:
            If st.button("🔍 판결 유예 및 2차 정밀 증거 요청 (게임 당 1회 제한)", key=f"postpone_{st.session_state.case_index}"):
                St.session_state.postpone_credits -= 1
                St.session_state.is_postponed = True
                St.rerun()
        Else:
            St.caption("⚠️ *이번 게임의 2차 정밀 증거 요청 찬스를 이미 사용하셨습니다.*")

    # --- ✍️ 주도적 자유 형량 입력 법정 폼 ---
    St.subheader("✍️ 재판관 직접 판결문 작성 및 선고")
    
    With st.form(key=f"judgment_form_{st.session_state.case_index}"):
        Penalty_type = st.radio(
            "선고할 형벌 종류를 선택하세요:",
            ["무죄", "유기징역", "무기징역", "사형"],
            Horizontal=True
        )

        Col_years, col_months = st.columns(2)
        With col_years:
            Years = st.number_input("징역 (년)", min_value=0, max_value=50, value=1, disabled=(penalty_type != "유기징역"))
        With col_months:
            Months = st.number_input("징역 (개월)", min_value=0, max_value=11, value=0, disabled=(penalty_type != "유기징역"))

        Reasoning = st.text_area("판결 이유 및 양형 조건 입력 (선택사항)", placeholder="피고인의 성행, 환경, 범행 동기 및 합리적 의심 유무를 작성하세요.")

        Submitted = st.form_submit_button("⚖️ 이 판결 확정 선고하기", type="primary", use_container_width=True)

    If submitted:
        # 선고 문구 정리
        If penalty_type == "무죄":
            Verdict_str = "무죄"
        Elif penalty_type == "유기징역":
            Verdict_str = f"징역 {years}년 {months}개월" if months > 0 else f"징역 {years}년"
        Else:
            Verdict_str = penalty_type

        # 지표 변화 자동 계산 알고리즘
        If penalty_type == "무죄":
            If case["is_innocent_case"]:
                St.session_state.law += 15
                St.session_state.trust += 15
                St.session_state.humanity += 10
            Else:
                St.session_state.law -= 15
                St.session_state.public -= 15
                St.session_state.trust -= 10
        Elif penalty_type in ["사형", "무기징역"]:
            St.session_state.law += 15
            St.session_state.public += 15
            St.session_state.humanity -= 15
        Else: # 유기징역
            If years >= 10:
                St.session_state.law += 10
                St.session_state.public += 10
                St.session_state.humanity -= 5
            Else:
                St.session_state.humanity += 10
                St.session_state.law += 5

        # 값 보정
        St.session_state.humanity = clamp(st.session_state.humanity)
        St.session_state.law = clamp(st.session_state.law)
        St.session_state.public = clamp(st.session_state.public)
        St.session_state.trust = clamp(st.session_state.trust)

        St.session_state.history.append({
            "case": f"{case['title']} (2차 증거 개시)" if st.session_state.is_postponed else case['title'],
            "my_decision": verdict_str,
            "my_reasoning": reasoning if reasoning else "작성 안 함",
            "real_verdict": case["real_verdict"],
            "real_reason": case["real_reason"]
        })

        St.session_state.case_index += 1
        St.session_state.is_postponed = False
        St.rerun()

# 재판 종결 리포트 화면
else:
    St.balloons()
    St.title("🏛️ 재판 종결: 판사 성향 및 판례 비교 리포트")
    
    Persona = analyze_judge_persona(
        St.session_state.humanity,
        St.session_state.law,
        St.session_state.public,
        St.session_state.trust
    )
    
    St.container(border=True).markdown(f"""
    ## 🧐 {st.session_state.judge_name}님의 사법 성향 진단
    ### **{persona['title']}**
    
    {persona['desc']}
    """)

    St.divider()
    St.subheader("📜 내 직접 작성 판결 VS 실제 대법원 판례 비교")
    For idx, item in enumerate(st.session_state.history):
        With st.expander(f"사건 {idx+1}: {item['case']}", expanded=True):
            Col_a, col_b = st.columns(2)
            With col_a:
                St.warning(f"**내가 직접 작성한 선고:**\n{item['my_decision']}\n\n*작성 이유:* {item['my_reasoning']}")
            With col_b:
                St.success(f"**실제 대법원 최종 확정:**\n{item['real_verdict']}")
            St.caption(f"**실제 대법원 판단 이유:** {item['real_reason']}")

    If st.button("🔄 새 게임 시작", type="primary", use_container_width=True):
        St.session_state.clear()
        St.rerun()
