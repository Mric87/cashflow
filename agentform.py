import os
import streamlit as st
from openai import OpenAI
from datetime import datetime

# Load OpenAI API key (works with both st.secrets and env vars)
api_key = st.secrets.get("openai_api_key", os.getenv("OPENAI_API_KEY"))
if not api_key:
    st.error("Missing OpenAI API key in secrets.toml or environment variables.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Predefined bot personalities
BOT_PERSONALITIES = {
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
    st.session_state.selected_bot = "Startup Strategist"

# Sidebar: bot selector
st.sidebar.title("Choose a Chatbot")
selected_bot = st.sidebar.selectbox("Select a personality:", list(BOT_PERSONALITIES.keys()))
st.session_state.selected_bot = selected_bot

# Main UI
st.title(f"🤖 {selected_bot}")
st.markdown("Chat with your custom AI bot below:")

# Chat display
for entry in st.session_state.messages:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

# Input form
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call OpenAI API
    try:
        full_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": BOT_PERSONALITIES[selected_bot]},
                *st.session_state.messages
            ],
        )
        reply = full_response.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ OpenAI Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

