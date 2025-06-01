import streamlit as st
import pandas as pd
import hashlib

ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
SHEET_URL = st.secrets["sheet"]
# ADMIN_PASSWORD = "admin1234"   # 실제 서비스에서는 환경변수나 secrets.toml 사용 권장

@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = [c.strip() for c in df.columns]
    return df

df = load_data()

st.title("학생 정보 열람 시스템")

# --- 어드민 로그인 ---
with st.sidebar:
    st.subheader("🔒 어드민 로그인")
    admin_input = st.text_input("어드민 비밀번호(테스트용:1234)", type="password")
    admin_login = st.button("어드민 로그인")
    admin_mode = False

    if admin_login:
        if admin_input == ADMIN_PASSWORD:
            st.success("어드민 인증 성공!")
            admin_mode = True
        else:
            st.error("비밀번호가 틀렸습니다.")

# --- 어드민 모드: 구글시트 전체 보기 ---
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

if admin_login and admin_input == ADMIN_PASSWORD:
    st.session_state.admin_mode = True

if st.session_state.admin_mode:
    st.subheader("전체 학생 정보 테이블")
    st.dataframe(df)
    st.stop()

# --- 일반 사용자: 방호수 조회 ---
name = st.text_input("이름을 입력하세요")
birth = st.text_input("생년월일 8자리 (예: 20130824)")

def hash_key(name, birth):
    base = (name.strip() + birth.strip()).encode("utf-8")
    return hashlib.sha256(base).hexdigest()

if st.button("방호수 조회하기"):
    if not name or not birth:
        st.warning("이름과 생년월일을 모두 입력하세요.")
    else:
        input_hash = hash_key(name, birth)
        matched_row = None
        for idx, row in df.iterrows():
            row_hash = hash_key(str(row["이름"]), str(row["생년월일"]))
            if row_hash == input_hash:
                matched_row = row
                break
        if matched_row is not None:
            st.success(f"방호수: {matched_row['호실배정']}")
        else:
            st.error("해당 정보를 찾을 수 없습니다.")

st.markdown("---")
st.caption("※ 어드민만 전체 데이터 열람 가능. 일반 사용자는 이름/생년월일로 방호수만 조회됩니다.")
