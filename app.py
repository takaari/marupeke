import streamlit as st
import random

st.set_page_config(page_title="✖️⭕MARUPEKE✖️⭕", page_icon="⭕")

st.title("✖️⭕MARUPEKE✖️⭕")

# ===== 初期化 =====
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.game_over = False

# ===== 勝敗判定 =====
def check_winner(board):
    lines = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in lines:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Draw"
    return None

# ===== CPUの手 =====
def cpu_move():
    empty = [i for i,v in enumerate(st.session_state.board) if v == ""]
    if empty:
        choice = random.choice(empty)
        st.session_state.board[choice] = "✖️"

# ===== マス表示 =====
cols = st.columns(3)

for i in range(9):
    col = cols[i % 3]
    if col.button(
        st.session_state.board[i] if st.session_state.board[i] else " ",
        key=i,
        use_container_width=True
    ):
        if not st.session_state.game_over and st.session_state.board[i] == "":
            st.session_state.board[i] = "⭕"

            winner = check_winner(st.session_state.board)
            if winner:
                st.session_state.game_over = True
            else:
                cpu_move()
                winner = check_winner(st.session_state.board)
                if winner:
                    st.session_state.game_over = True

# ===== 結果表示 =====
winner = check_winner(st.session_state.board)

if winner == "⭕":
    st.success("あなたの勝ち！ 🎉")
elif winner == "✖️":
    st.error("コンピュータの勝ち 🤖")
elif winner == "Draw":
    st.info("引き分け！")

# ===== リセット =====
if st.button("もう一回あそぶ"):
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.rerun()
