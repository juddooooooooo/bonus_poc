import streamlit as st
import time
import random

# 1. Page Config
st.set_page_config(page_title="Game Lobby", page_icon="🎰", layout="centered", initial_sidebar_state="collapsed")

# 2. Custom CSS (Dark Theme + Gold)
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; color: white; }
        .title-text {
            font-size: 4rem; text-align: center; font-weight: 800;
            color: #FFD700; text-shadow: 0 0 10px #FFD700, 0 0 20px #ff00de;
            margin-bottom: 20px; font-family: 'Arial Black', sans-serif;
            text-transform: uppercase;
        }
        .slot-container {
            background-color: #222; border: 4px solid #FFD700; border-radius: 15px;
            padding: 20px; text-align: center; box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        }
        .slot-symbol { font-size: 80px; text-align: center; }
        [data-testid="stSidebarNav"] {display: none;}
        footer {visibility: hidden;} header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Credits
if 'credits' not in st.session_state:
    st.session_state.credits = 1000

# --- NEW LOGIC: CHECK FOR BONUS FROM CHATBOT ---
if 'pending_bonus' in st.session_state:
    # Get the data
    bonus_amount = st.session_state['pending_bonus']
    bonus_msg = st.session_state['bonus_message']
    
    # 1. Apply credits
    st.session_state.credits += bonus_amount
    
    # 2. Show Popup Notification (Toast)
    st.toast(f"Congratulations! {bonus_msg}", icon="🎉")
    st.toast(f"+{bonus_amount} Credits added to your balance!", icon="💰")
    
    # 3. Celebrate
    st.balloons()
    
    # 4. Remove the pending bonus so it doesn't trigger again on refresh
    del st.session_state['pending_bonus']
    del st.session_state['bonus_message']
# ------------------------------------------------

# 4. The Header
st.markdown('<div class="title-text">GAME LOBBY</div>', unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.write(f"### 💳 Your Credits: **{st.session_state.credits}**")
    
    # Slot Container
    slot_container = st.container()
    with slot_container:
        reel1, reel2, reel3 = st.columns(3)
        place1 = reel1.empty()
        place2 = reel2.empty()
        place3 = reel3.empty()

    # Spin Button
    spin_btn = st.button("🎰 SPIN (Bet 50)", use_container_width=True, type="primary")

    symbols = ["🍒", "🍋", "🍇", "🍊", "💎", "7️⃣"]

    if spin_btn:
        if st.session_state.credits < 50:
            st.error("Not enough credits! Refresh page to reset.")
        else:
            st.session_state.credits -= 50
            
            # Animation
            for i in range(15):
                place1.markdown(f"<div class='slot-symbol'>{random.choice(symbols)}</div>", unsafe_allow_html=True)
                place2.markdown(f"<div class='slot-symbol'>{random.choice(symbols)}</div>", unsafe_allow_html=True)
                place3.markdown(f"<div class='slot-symbol'>{random.choice(symbols)}</div>", unsafe_allow_html=True)
                time.sleep(0.1)

            # Result
            final_s1 = random.choice(symbols)
            final_s2 = random.choice(symbols)
            final_s3 = random.choice(symbols)

            place1.markdown(f"<div class='slot-symbol'>{final_s1}</div>", unsafe_allow_html=True)
            place2.markdown(f"<div class='slot-symbol'>{final_s2}</div>", unsafe_allow_html=True)
            place3.markdown(f"<div class='slot-symbol'>{final_s3}</div>", unsafe_allow_html=True)

            # Win Logic
            if final_s1 == final_s2 == final_s3:
                win_amount = 500
                if final_s1 == "7️⃣": win_amount = 1000
                elif final_s1 == "💎": win_amount = 800
                st.session_state.credits += win_amount
                st.balloons()
                st.success(f"JACKPOT! You won {win_amount} credits!")
            elif final_s1 == final_s2 or final_s2 == final_s3 or final_s1 == final_s3:
                st.session_state.credits += 100
                st.success("Nice! You won 100 credits!")
            
            time.sleep(1)
            st.rerun()

    else:
        # Default view
        place1.markdown(f"<div class='slot-symbol'>7️⃣</div>", unsafe_allow_html=True)
        place2.markdown(f"<div class='slot-symbol'>💎</div>", unsafe_allow_html=True)
        place3.markdown(f"<div class='slot-symbol'>🍒</div>", unsafe_allow_html=True)
