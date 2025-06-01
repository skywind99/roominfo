import streamlit as st
import pandas as pd
import hashlib

# 구글시트 CSV 불러오기
SHEET_URL = "https://docs.google.com/spreadsheets/d/1tg6FyQ8rKjS63xur6lncTT1bpGDei0CLadcrtZ2nSTo/export?format=csv"
@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    # 컬럼명 자동감지 (혹시 헤더가 두줄이면 수정 필요)
    df.columns = [c.strip() for c in df.columns]
    return df

df = load_data()

st.title("학생 정보 암호화 열람 시스템")

# 사용자 입력
name = st.text_input("이름을 입력하세요")
birth = st.text_input("생년월일 8자리 (예: 20130824)")

def hash_key(name, birth):
    # 이름+생년월일(공백없음)을 sha256으로 암호화
    base = (name.strip() + birth.strip()).encode("utf-8")
    return hashlib.sha256(base).hexdigest()

if st.button("방호수 조회하기"):
    if not name or not birth:
        st.warning("이름과 생년월일을 모두 입력하세요.")
    else:
        # 사용자 입력 암호화
        input_hash = hash_key(name, birth)
        # 시트에 있는 각각의 row도 똑같이 암호화해서 비교
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
st.caption("※ 모든 정보는 입력값을 sha256으로 변환하여 검색하며, 시트의 원본 정보는 외부에 노출되지 않습니다.")
