import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time

# === CONFIG ===
st.set_page_config(
    page_title="Career Buddy", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

def load_lottie_url(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        else:
            return None
    except:
        return None

# Load animations
hero_animation = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_xlky4kvh.json")
bot_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_e3jNDe.json")

# === ENHANCED CSS ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Animated Background */
.stApp {
    background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Glass Morphism Effects */
.glass-container {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    margin: 1rem 0;
    animation: slideInUp 0.8s ease-out;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Enhanced Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 15px;
    padding: 15px 30px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    width: 100%;
}

div.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* Form Styling */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    padding: 15px;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border: 2px solid #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    transform: translateY(-2px);
}

/* Title Styling */
.main-title {
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.5rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 2rem;
    animation: titlePulse 3s ease-in-out infinite;
}

@keyframes titlePulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}

/* Chat Messages */
.stChatMessage {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(15px);
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    animation: messageSlide 0.5s ease-out;
}

@keyframes messageSlide {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Feature Cards */
.feature-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

/* Section Headers */
.section-header {
    color: white;
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Success Message */
.success-message {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    color: white;
    padding: 1rem 2rem;
    border-radius: 15px;
    text-align: center;
    font-weight: 600;
    animation: successBounce 0.6s ease-out;
    margin: 1rem 0;
}

@keyframes successBounce {
    0% { transform: scale(0.8); opacity: 0; }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); opacity: 1; }
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Responsive */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.5rem;
    }
    .glass-container {
        padding: 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# === UI LAYOUT ===
st.markdown('<h1 class="main-title">🚀 Career Buddy – Your Future Starts Here</h1>', unsafe_allow_html=True)

# Feature highlights
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: white; margin-bottom: 1rem;">🎯 Personalized Guidance</h3>
        <p style="color: rgba(255,255,255,0.8);">Get tailored career advice based on your unique skills and interests</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: white; margin-bottom: 1rem;">🤖 AI-Powered Insights</h3>
        <p style="color: rgba(255,255,255,0.8);">Leverage advanced AI to discover hidden career opportunities</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: white; margin-bottom: 1rem;">📈 Future-Ready Skills</h3>
        <p style="color: rgba(255,255,255,0.8);">Learn about emerging skills and future job market trends</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Content Area
main_col1, main_col2 = st.columns([1, 1.5])

with main_col1:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    if hero_animation:
        st_lottie(hero_animation, height=350, key="hero")
    else:
        st.markdown("""
        <div style="height: 350px; display: flex; align-items: center; justify-content: center; 
                    background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 20px; 
                    color: white; font-size: 4rem;">
            🚀
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with main_col2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🌟 Let\'s Build Your Career Path</h2>', unsafe_allow_html=True)
    
    with st.form("career_form"):
        name = st.text_input("👤 Your Name", placeholder="Enter your full name...")
        academic_interest = st.text_area("📚 Your Academic Interests", 
                                       placeholder="What subjects fascinate you?",
                                       height=80)
        career_goals = st.text_area("🎯 Your Career Goals", 
                                  placeholder="Where do you see yourself in 5-10 years?",
                                  height=80)
        skills = st.text_area("🧠 Your Skills", 
                            placeholder="List your technical, creative, and soft skills",
                            height=80)
        
        submitted = st.form_submit_button("✨ Generate My Career Path")
    
    st.markdown('</div>', unsafe_allow_html=True)

# === API FUNCTION ===
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
    try:
        res = requests.post(GROQ_API_URL, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"I apologize, but I'm having trouble connecting right now. Please try again in a moment."

# === CHAT FUNCTIONALITY ===
if submitted and name and academic_interest and career_goals and skills:
    with st.spinner('🤖 Analyzing your profile and generating personalized career insights...'):
        time.sleep(1)
        
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    f"You are Career Buddy, an enthusiastic and knowledgeable career guidance AI. "
                    f"Provide comprehensive, actionable career advice with specific recommendations. "
                    f"Use emojis appropriately and maintain a warm, encouraging tone.\n\n"
                    f"User Profile:\n"
                    f"Name: {name}\n"
                    f"Academic Interests: {academic_interest}\n"
                    f"Career Goals: {career_goals}\n"
                    f"Current Skills: {skills}"
                )
            }
        ]
        
        bot_response = get_career_advice(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        st.markdown("""
        <div class="success-message">
            🎉 Your personalized career roadmap is ready!
        </div>
        """, unsafe_allow_html=True)

elif submitted:
    st.error("🚨 Please fill in all fields to get your personalized career guidance!")

# === CHAT INTERFACE ===
if "messages" in st.session_state:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💬 Your Career Consultation</h2>', unsafe_allow_html=True)
    
    # Display chat messages
    for msg in st.session_state.messages[1:]:  # Skip system message
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    if user_msg := st.chat_input("💭 Ask me anything about your career journey..."):
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_msg)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Thinking..."):
                response = get_career_advice(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.markdown(response)
                
                if bot_animation:
                    st_lottie(bot_animation, height=100, key="bot_response")

# === FOOTER ===
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="glass-container" style="text-align: center;">
    <h3 style="color: white; margin-bottom: 1rem;">🌟 Ready to Transform Your Career?</h3>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">
        Join thousands of professionals who've discovered their perfect career path with Career Buddy!
    </p>
    <div style="margin-top: 1.5rem;">
        <span style="font-size: 2rem;">🚀</span>
        <span style="font-size: 2rem; margin: 0 1rem;">✨</span>
        <span style="font-size: 2rem;">🎯</span>
    </div>
</div>
""", unsafe_allow_html=True)