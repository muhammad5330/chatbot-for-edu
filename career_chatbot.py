import os
import streamlit as st
import requests
import logging

# ==== CONFIGURATION ====
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set this in environment instead of hardcoding
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

# ==== HELPER FUNCTION ====
def get_career_advice(messages):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set in environment variables.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
        # If non-2xx, raise with context
        if not response.ok:
            # Log full response for internal diagnostics
            logging.error("GROQ API error: status=%s body=%s", response.status_code, response.text)
            # Surface a truncated, safe message to user
            truncated = response.text[:1000].replace(GROQ_API_KEY, "[REDACTED]")
            raise requests.exceptions.HTTPError(
                f"Request failed with status {response.status_code}. "
                f"Response snippet: {truncated}"
            )
        data = response.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        # Re-raise so caller can handle; include message
        raise RuntimeError(f"Error calling career advice API: {e}") from e

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
    try:
        bot_response = get_career_advice(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.chat_message("assistant").markdown(bot_response)
    except Exception as e:
        st.error(f"Failed to get career advice: {e}")

# ==== CHAT INTERFACE ====
if "messages" in st.session_state:
    for msg in st.session_state.messages[1:]:  # Skip system prompt
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask more about your career options..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        try:
            response = get_career_advice(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("user").markdown(prompt)
            st.chat_message("assistant").markdown(response)
        except Exception as e:
            st.chat_message("user").markdown(prompt)
            st.error(f"Error getting follow-up advice: {e}")
