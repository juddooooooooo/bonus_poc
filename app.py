import streamlit as st
import time
from backend import BonusChecker

# Page Configuration
st.set_page_config(page_title="Betway Bonus Bot", page_icon="🤖")

@st.cache_resource
def get_checker():
    # Ensure "bonus_data.csv" and "terms.txt" exist in your directory
    return BonusChecker("bonus_data.csv", "terms.txt")

bot_engine = get_checker()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Enter your Account ID to check for bonuses."}
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Type your message here..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = ""
    
    # Check ID Logic (if input is a number)
    if prompt.strip().isdigit():
        account_id = prompt.strip()
        
        with st.chat_message("assistant"):
            with st.spinner(f"Checking Account {account_id}..."):
                time.sleep(0.5)  # Simulate network delay
                result = bot_engine.check_status(account_id)
        
            # --- DISPLAY LOGIC ---
            status = result["status"]
            
            # 1. VIP HOSTED
            # Logic: User is directed to their specific host
            if status == "vip_redirect":
                st.info(f"💎 **{result['message']}**")
                st.write(result['details'])
                # Direct link to contact host (e.g., WhatsApp or Email link from CSV)
                st.link_button("Contact Host", result.get("action_url")) 
                response = "I have located your VIP status."

            # 2. STANDARD ELIGIBLE
            # Logic: Offer bonus -> Save to session -> Redirect to Game Lobby
            elif status == "success":
                st.success(f"🎉 **{result['message']}**")
                
                # --- BONUS TRANSFER LOGIC ---
                # Store the bonus in memory so the Game Lobby page can read it
                st.session_state['pending_bonus'] = 500  # Grant 500 credits
                st.session_state['bonus_message'] = result['message']
                # ----------------------------

                with st.expander("Terms & Conditions"):
                    st.write(result['details'])
                
                # Link to the local Streamlit Page (pages/game_lobby.py)
                st.page_link("pages/game_lobby.py", label="💰 Claim & Play Now", icon="🎮", use_container_width=True)
                
                response = "You are eligible! Click the button above to play."

            # 3. STANDARD NOT ELIGIBLE
            # Logic: No bonus -> Redirect to Game Lobby anyway
            elif status == "failed":
                st.warning(f"⚠️ **{result['message']}**")
                st.write(result['details'])
                
                # Link to the local Streamlit Page
                st.page_link("pages/game_lobby.py", label="🎮 Go to Game Lobby", icon="🎲", use_container_width=True)
                
                response = "No bonus currently, but you can still head to the lobby."

            # 4. ERROR (ID not found)
            else:
                st.error(f"❌ {result['message']}")
                st.write(result['details'])
                response = "I couldn't find that account."

    else:
        # Simple conversational fallback if input is not a number
        if "bonus" in prompt.lower():
            response = "Please provide your **Account ID**."
        else:
            response = "I can help check bonuses. Just enter your Account ID."
            
        with st.chat_message("assistant"):
            st.markdown(response)

    
    st.session_state.messages.append({"role": "assistant", "content": response})
