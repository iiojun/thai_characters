import streamlit as st
import pandas as pd

st.title("タイ文字暗記帳（子音）")

# 1. 同じディレクトリの Excel ファイルを読み込む
df = pd.read_excel("thai_char.xlsx")

import random

# 出題をセッション状態に固定
if "row_index" not in st.session_state:
    st.session_state.row_index = random.randint(0, len(df) - 1)

row_index = st.session_state.row_index

# 選択された行
target_row = df.iloc[row_index]

# 2. A の文字を 300px × 300px で表示
st.markdown(
    f"<div style='font-size: 160px; text-align: center; border: 1px solid #ccc; width:300px; height:300px; display:flex; align-items:center; justify-content:center;'>"
    f"{target_row['A']}"
    f"</div>",
    unsafe_allow_html=True,
)

st.write("### これ，なんて文字？")

# 3. C,D の選択肢を全データからプルダウン化
DEFAULT_OPTION = '選択してください'

# session_state に初期値を設定
if "selected1" not in st.session_state:
    st.session_state.selected1 = DEFAULT_OPTION
if "selected2" not in st.session_state:
    st.session_state.selected2 = DEFAULT_OPTION

choice_C = st.selectbox("読み方", 
                options=[DEFAULT_OPTION] + list(df["C"].unique()),
                key="selected1")
choice_D = st.selectbox("意味",
                options=[DEFAULT_OPTION] + list(df["D"].unique()),
                key="selected2")

# 4. サブミットボタン
if st.button("判定"):
    correct = (
        choice_C == target_row["C"]
        and choice_D == target_row["D"]
    )

    # 5. 判定結果
    if correct:
        st.success("正解！")
        st.write("### 読み方と意味")
        st.write(f"### {target_row['B']}")
        st.write(f"読み方: 　 {target_row['C']}")
        st.write(f"意　味: 　 {target_row['D']}")
    else:
        st.error("不正解です" + (" …… 惜しい" \
                if choice_C == target_row["C"] or
                   choice_D == target_row["D"] else ""))
        st.write("### 正しい読み方と意味はこちら")
        st.write(f"### {target_row['B']}")
        st.write(f"読み方: 　 {target_row['C']}")
        st.write(f"意　味: 　 {target_row['D']}")

# 次の問題ボタン
if st.button("次の問題"):
    del st.session_state.selected1
    del st.session_state.selected2
    st.session_state.row_index = random.randint(0, len(df) - 1)
    st.rerun()
