import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


# Imports
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load Env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in .env")
    st.stop()

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


# Page Config
st.set_page_config(
    page_title="AI Chatbot Mentor",
    page_icon="🤖",
    layout="centered"
)


# Custom Styling

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.header-box {
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
}
.sub-text {
    color: #d1d5db;
}

</style>
""", unsafe_allow_html=True)

# Header

st.markdown("""
<div class="header-box">
    <h1>🤖 AI Chatbot Mentor</h1>
    <p class="sub-text">Personalized learning assistant powered by Gemini</p>
</div>
""", unsafe_allow_html=True)

# Module Navigation

st.markdown("<div class='card'>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📚 Learning Modules")

    module = st.selectbox(
        "Choose a module",
        [
            "Python",
            "SQL",
            "Power BI",
            "EDA",
            "Machine Learning",
            "Deep Learning",
            "Generative AI",
            "Agentic AI"
        ]
    )


experience = st.selectbox(
    "🧑‍💻 Select Your Experience (Years)",
    list(range(1, 11))
)

st.markdown("</div>", unsafe_allow_html=True)

# Run Button
if "run" not in st.session_state:
    st.session_state.run = False

if st.button("🚀 Run Mentor"):
    st.session_state.run = True
    st.session_state.conv = []
    st.session_state.memory = []
    st.session_state.model = None


# Chat Section
if st.session_state.run:

    st.markdown(f"""
    <div class="card">
        <h3 style="text-align:center;">
            {module} Mentor • {experience}+ Years Experience
        </h3>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.memory:

        system_prompt = f"""
        You are an AI mentor specialized ONLY in {module}.
        The learner has {experience} years of experience.

        Rules:
        - Answer ONLY {module} related questions
        - Adjust explanation depth based on experience
        - If irrelevant, reply EXACTLY:
        "Sorry, I don’t know about this question. Please ask something related to the selected module."
        """

        st.session_state.memory.append(("system", system_prompt))
        st.session_state.conv.append({
            "role": "ai",
            "content": f"Welcome to {module} Mentor! Ask your first question."
        })

        st.session_state.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.3
        )

    for msg in st.session_state.conv:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your question here...")

    if user_input:
        st.session_state.conv.append({"role": "user", "content": user_input})
        st.session_state.memory.append(("user", user_input))

        response = st.session_state.model.invoke(st.session_state.memory)

        st.session_state.conv.append({"role": "ai", "content": response.content})
        st.session_state.memory.append(("ai", response.content))

        st.rerun()

   
    # Download Chat
    def build_chat_text():
        return "\n\n".join(
            [f"{m['role'].upper()}:\n{m['content']}" for m in st.session_state.conv]
        )

    if st.session_state.conv:
        st.download_button(
            "⬇️ Download Conversation",
            data=build_chat_text(),
            file_name=f"{module}_mentor_chat.txt",
            mime="text/plain"
        )
