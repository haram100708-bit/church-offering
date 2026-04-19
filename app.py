import streamlit as st
import pandas as pd
import os

# 1. 설정 및 디자인
st.set_page_config(page_title="교회 헌금 관리", page_icon="⛪", layout="wide")
file_name = '교회헌금장부_USD.xlsx'
member_list = ["구하람", "구하은", "구종관", "정선임"]

# --- 사이드바 (입력 창을 왼쪽으로!) ---
with st.sidebar:
    st.header("📝 새 내역 입력")
    date_input = st.date_input("📅 날짜 선택")
    selected_name = st.selectbox("👤 성도 이름", member_list)
    amount = st.number_input("💵 금액 ($)", min_value=0.0)
    save_btn = st.button("💾 저장하기", use_container_width=True)

# --- 메인 화면 (결과 대시보드) ---
st.title("⛪ 헌금 관리 시스템")
st.caption("데이터를 실시간으로 분석하고 기록합니다.")

if save_btn:
    usd_amount = f"${amount:,.2f} USD"
    new_data = {'날짜': [str(date_input)], '이름': [selected_name], '금액': [usd_amount], 'raw_amount': [amount]}
    df_new = pd.DataFrame(new_data)

    if os.path.exists(file_name):
        df_old = pd.read_excel(file_name)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new
    df_final.to_excel(file_name, index=False)
    st.toast(f"✅ {selected_name}님 저장 완료!", icon='🎉')

# --- 요약 통계 보여주기 ---
if os.path.exists(file_name):
    df_all = pd.read_excel(file_name)
    
    # 총 합계 계산 (간단한 분석 추가)
    total_usd = df_all['raw_amount'].sum() if 'raw_amount' in df_all.columns else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 누적 총액", f"${total_usd:,.2f}")
    col2.metric("👥 총 입력 건수", f"{len(df_all)}건")
    col3.metric("📅 마지막 입력", df_all['날짜'].iloc[-1] if len(df_all) > 0 else "-")

    st.divider()
    st.subheader("📊 전체 내역 확인")
    df_show = df_all.copy()
    df_show.index = df_show.index + 1
    # 필요한 열만 보여주기
    st.dataframe(df_show[['날짜', '이름', '금액']], use_container_width=True)
else:
    st.info("아직 입력된 데이터가 없습니다. 왼쪽 메뉴에서 입력을 시작해 주세요!")
