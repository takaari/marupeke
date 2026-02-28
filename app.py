import streamlit as st
import random

st.set_page_config(page_title="✖️⭕MARUPEKE✖️⭕", page_icon="⭕")

st.title("✖️⭕MARUPEKE✖️⭕")

# ===== 正方形CSS =====
st.markdown("""
<style>

/* ボタンを正方形に */
button[kind="secondary"] {
    width: 100%;
    aspect-ratio: 1 / 1;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

/* 中の文字を巨大化 */
button[kind="secondary"] * {
    font-size: min(22vw, 150px) !important;
}

</style>
""", unsafe_allow_html=True)

# ===== 初期化 =====
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.cpu_pending = False
if "cpu_thinking" not in st.session_state:
    st.session_state.cpu_thinking = False

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
    
def smart_cpu_move():
    board = st.session_state.board

    lines = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    # ① 勝てるなら勝つ（これは残す）
    for a,b,c in lines:
        line = [board[a], board[b], board[c]]
        if line.count("✖️") == 2 and line.count("") == 1:
            move = [a,b,c][line.index("")]
            board[move] = "✖️"
            return

    # ② 相手を止める（70%の確率だけ止める）
    import random
    if random.random() < 0.7:   # ← ここで弱体化
        for a,b,c in lines:
            line = [board[a], board[b], board[c]]
            if line.count("⭕") == 2 and line.count("") == 1:
                move = [a,b,c][line.index("")]
                board[move] = "✖️"
                return

    # ③ 真ん中（50%の確率）
    if board[4] == "" and random.random() < 0.5:
        board[4] = "✖️"
        return

    # ④ ランダム
    empty = [i for i,v in enumerate(board) if v == ""]
    if empty:
        board[random.choice(empty)] = "✖️"

# ===== プレイヤー入力 =====
cols = st.columns(3)

for i in range(9):
    col = cols[i % 3]
    if col.button(
        st.session_state.board[i] if st.session_state.board[i] else " ",
        key=i,
        use_container_width=True
    ):
        if (
            not st.session_state.game_over
            and not st.session_state.cpu_thinking
            and st.session_state.board[i] == ""
        ):
            st.session_state.board[i] = "⭕"
            st.session_state.cpu_thinking = True
            st.rerun()

# ===== CPUターン（別フェーズ）=====
if st.session_state.cpu_thinking and not st.session_state.game_over:

    st.info("🤖 コンピュータが考え中…")

    import time
    time.sleep(2)

    # CPUが打つ
    smart_cpu_move()

    st.session_state.cpu_thinking = False
    st.rerun()

# ===== 勝敗チェック =====
winner = check_winner(st.session_state.board)

if winner:
    st.session_state.game_over = True
    if winner == "⭕":
        st.success("あなたの勝ち！ 🎉")
    elif winner == "✖️":
        st.error("コンピュータの勝ち 🤖")
    else:
        st.info("引き分け！")

# ===== リセット =====
if st.button("もう一回あそぶ"):
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.cpu_pending = False
    st.rerun()
