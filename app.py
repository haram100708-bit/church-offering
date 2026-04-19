import streamlit as st
import pandas as pd
import os

# 1. 설정 및 디자인
st.set_page_config(page_title="교회 헌금 관리", page_icon="⛪", layout="wide")
file_name = '교회헌금장부_USD.xlsx'
member_list = ["구하람", "구하은", "구종관", "정선임"]

# --- 사이드바: 입력 및 삭제 제어 ---
with st.sidebar:
    st.header("📝 새 내역 입력")
    date_input = st.date_input("📅 날짜 선택")
    selected_name = st.selectbox("👤 성도 이름", member_list)
    amount = st.number_input("💵 금액 ($)", min_value=0.0)
    save_btn = st.button("💾 저장하기", use_container_width=True)
    
    st.divider()
    st.header("🗑️ 데이터 관리")
    # 마지막 한 줄 삭제 버튼
    delete_last_btn = st.button("⬅️ 마지막 입력 삭제", use_container_width=True, help="가장 최근에 저장된 한 줄을 지웁니다.")

# --- 메인 화면 ---
st.title("⛪ 헌금 관리 시스템")

# 데이터 불러오기 함수
def get_data():
    if os.path.exists(file_name):
        return pd.read_excel(file_name)
    return pd.DataFrame(columns=['날짜', '이름', '금액', 'raw_amount'])

df = get_data()

# [저장 로직]
if save_btn:
    usd_amount = f"${amount:,.2f} USD"
    new_data = pd.DataFrame({'날짜': [str(date_input)], '이름': [selected_name], '금액': [usd_amount], 'raw_amount': [amount]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(file_name, index=False)
    st.toast(f"✅ {selected_name}님 저장 완료!", icon='🎉')
    st.rerun() # 화면 갱신

# [마지막 줄 삭제 로직]
if delete_last_btn:
    if len(df) > 0:
        df = df.drop(df.index[-1])
        df.to_excel(file_name, index=False)
        st.toast("🗑️ 마지막 내역이 삭제되었습니다.", icon='⚠️')
        st.rerun()
    else:
        st.sidebar.error("지울 데이터가 없습니다.")

# --- 대시보드 요약 ---
if not df.empty:
    total_usd = df['raw_amount'].sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 누적 총액", f"${total_usd:,.2f}")
    col2.metric("👥 총 입력 건수", f"{len(df)}건")
    col3.metric("📅 마지막 입력", df['날짜'].iloc[-1])

    st.divider()
    
    # [선택 삭제 기능] 메인 화면에 배치
    st.subheader("📊 전체 내역 및 선택 삭제")
    
    # 인덱스 1부터 조정
    df_display = df.copy()
    df_display.index = df_display.index + 1
    
    # 삭제하고 싶은 행 번호 선택
    delete_idx = st.number_input("삭제할 행 번호(No) 입력", min_value=1, max_value=len(df_display), step=1)
    if st.button(f"🗑️ {delete_idx}번 행 삭제하기"):
        df = df.drop(df.index[delete_idx - 1]) # 실제 인덱스는 0부터이므로 -1
        df.to_excel(file_name, index=False)
        st.success(f"✅ {delete_idx}번 내역이 삭제되었습니다.")
        st.rerun()

    st.dataframe(df_display[['날짜', '이름', '금액']], use_container_width=True)
else:
    st.info("데이터가 없습니다. 왼쪽 메뉴에서 입력을 시작해 주세요!")
