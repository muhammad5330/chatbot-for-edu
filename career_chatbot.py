import streamlit as st
import requests

# ==== CONFIGURATION ====
GROQ_API_KEY = "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"  # <-- Paste your key here
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

# ==== HELPER FUNCTION ====
def get_career_advice(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

# ==== UI ====
st.set_page_config(page_title="Career Path Chatbot", page_icon="🎓", layout="centered")
st.title("🎓 Career Path Chatbot")
st.write("Hi there! I'm here to help you figure out the best career options based on your interests and goals. Let's get started!")

# ==== FORM ====
with st.form("user_form"):
    name = st.text_input("Your Name")
    academic_interest = st.text_area("Your Academic Interests")
    career_goals = st.text_area("Your Career Goals")
    skills = st.text_area("Skills You Have (technical, communication, creative etc.)")
    submitted = st.form_submit_button("Submit and Start Chatting")

# ==== INITIAL SYSTEM PROMPT ====
if submitted:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                f"You are a friendly and supportive career guidance bot. Only provide helpful suggestions about career paths. "
                f"Never discuss anything outside of career guidance. "
                f"Your tone should be positive, empathetic, and easy to understand. "
                f"Start the conversation by greeting the student and providing them personalized guidance based on their background below:\n\n"
                f"Name: {name}\n"
                f"Academic Interests: {academic_interest}\n"
                f"Career Goals: {career_goals}\n"
                f"Skills: {skills}\n\n"
                f"Now, give a warm welcome and offer career suggestions accordingly."
            )
        }
    ]
    bot_response = get_career_advice(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.chat_message("assistant").markdown(bot_response)

# ==== CHAT INTERFACE ====
if "messages" in st.session_state:
    for msg in st.session_state.messages[1:]:  # Skip system prompt
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User sends a message
    if prompt := st.chat_input("Ask more about your career options..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_career_advice(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("user").markdown(prompt)
        st.chat_message("assistant").markdown(response)