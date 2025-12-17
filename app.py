import streamlit as st
import time
from backend import BonusChecker

# --- Configuration ---
st.set_page_config(page_title="Operator A Bonus Bot", page_icon="🤖")

# --- Initialize Backend ---
@st.cache_resource
def get_checker():
    return BonusChecker("bonus_data.csv", "terms.txt")

bot_engine = get_checker()

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am the Operator A Assistant. I can help you check your bonus eligibility. How can I help you today?"}
    ]

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle User Input ---
if prompt := st.chat_input("Type your message here..."):
    
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Bot Logic
    response = ""
    
    # Check if the input is an Account ID (Digits only)
    if prompt.strip().isdigit():
        account_id = prompt.strip()
        
        # Simulate "thinking" time for realism
        with st.chat_message("assistant"):
            with st.spinner(f"Checking eligibility for Account {account_id}..."):
                time.sleep(1) 
                result = bot_engine.check_status(account_id)
        
        # Format the response based on the backend result
        if result["status"] == "success":
            response = f"🎉 **Good news!** {result['message']}\n\n**Terms:**\n{result['details']}"
        elif result["status"] == "failed":
            response = f"⚠️ **Bonus Unavailable.**\n\n{result['details']}"
        else:
            response = f"❌ **Error:** {result['message']}\n{result['details']}"

    # Check if user is asking for a bonus (Keyword search)
    elif "bonus" in prompt.lower() or "check" in prompt.lower() or "promotion" in prompt.lower():
        response = "Sure, I can check that for you. Please provide your **Account ID**."
    
    # Greeting / Fallback
    elif "hello" in prompt.lower() or "hi" in prompt.lower():
        response = "Hi there! If you want to check your bonus status, just let me know."
        
    else:
        response = "I'm just a demo bot, but I can help with bonuses! Try asking 'Do I have a bonus?' or enter your Account ID."

    # 3. Display Bot Response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})