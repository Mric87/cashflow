import streamlit as st
import openai
from datetime import datetime
from typing import Dict

# Set your OpenAI API key securely
openai.api_key = st.secrets["openai_api_key"]

# Predefined bot personalities
BOT_PERSONALITIES = {
    "Helper Bot": "You are a helpful assistant.",
    "Startup Strategist": "You specialize in helping new businesses with planning and execution.",
    "Hip-Hop Guru": (
        "Welcome to Hip-Hop Guru, the chatbot that knows the beats, rhymes, and stories of the hip-hop world! "
        "Whether you're curious about the origins of the genre, looking for the latest news on your favorite artists, "
        "or searching for song lyrics and meanings, Hip-Hop Guru has got you covered."
    ),
    "Generational Copy": (
        "At Generational Copy, LLC, we specialize in helping each generation write and share their unique stories. "
        "Whether you're a first-time writer or a seasoned author, our tailored services guide you through the writing process."
    ),
    "Jasmine Renee": (
        "I am a motivational speaker with a message sharing God’s love that inspires others to align with their Divine Connection. "
        "My goal is to inspire hope, connection, and mindful living."
    ),
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_bot" not in st.session_state:
    st.session_state.selected_bot = "Helper Bot"

st.title("🤖 Multi-Bot Chat Assistant")

# Sidebar bot selection
st.sidebar.header("🧠 Choose Your Bot")
bot_choice = st.sidebar.selectbox("Select a chatbot personality:", list(BOT_PERSONALITIES.keys()))
st.session_state.selected_bot = bot_choice
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Current Bot:** `{bot_choice}`")

def send_message_to_openai(message: str, bot_personality: str) -> Dict:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": bot_personality},
                {"role": "user", "content": message},
            ],
        )
        return {"response": response["choices"][0]["message"]["content"]}
    except Exception as e:
        st.error(f"OpenAI API Error: {str(e)}")
        return {"response": f"Error: {str(e)}"}

# Chat display
for chat in st.session_state.messages:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# User input
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    bot_personality = BOT_PERSONALITIES.get(st.session_state.selected_bot, "You are a helpful assistant.")
    result = send_message_to_openai(user_input, bot_personality)
    assistant_reply = result["response"]

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
