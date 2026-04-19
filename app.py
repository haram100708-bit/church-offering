import streamlit as st
import pandas as pd
import os

# 파일 설정
file_name = '교회헌금장부_USD.xlsx'
member_list = ["구하람", "구하은", "구종관", "정선임","홍길동"]

st.title("⛪ 교회 헌금 관리 시스템")

# 웹 화면 구성
date_input = st.date_input("📅 날짜를 선택하세요")
selected_name = st.selectbox("👤 성도 이름을 선택하세요", member_list)
amount = st.number_input("💵 헌금액 ($)", min_value=0.0)

if st.button("💾 저장하기"):
    usd_amount = f"${amount:,.2f} USD"
    new_data = {'날짜': [str(date_input)], '이름': [selected_name], '금액': [usd_amount]}
    df_new = pd.DataFrame(new_data)

    if os.path.exists(file_name):
        df_old = pd.read_excel(file_name)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_excel(file_name, index=False)
    st.success(f"✅ {selected_name}님 저장 완료!")
    st.dataframe(df_final.tail()) # 화면에 최근 내역 보여주기
