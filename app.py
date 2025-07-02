import streamlit as st
from openai import OpenAI
from datetime import datetime
import random
import time

# Streamlit page config
st.set_page_config(page_title="Explain Like I'm...", layout="centered")

# OpenAI client from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# ---- App Title ----
st.markdown("""
    <h1 style='text-align: center;'>🧠 Explain Like I'm...</h1>
""", unsafe_allow_html=True)

# ---- Counter ----
if "counter" not in st.session_state:
    st.session_state.counter = 0

# ---- Prompt Input ----
st.markdown("### 💬 What do you want explained?")
prompt = st.text_input("Enter a concept (e.g. blockchain, ROI, Kubernetes)", key="main_prompt")

# ---- Example Buttons ----
st.markdown("#### 🔍 Try an example:")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📦 Blockchain"):
        prompt = "blockchain"
with col2:
    if st.button("📈 Customer Lifetime Value"):
        prompt = "customer lifetime value"
with col3:
    if st.button("🧩 Microservices"):
        prompt = "microservices"

# ---- Age Slider ----
age = st.slider("Select the age level to explain at", 1, 100, 5)

# ---- Style Option ----
style = st.selectbox("Add a tone or style?", ["Default", "Poetic", "Sarcastic", "Funny"])

# ---- Explanation Output ----
if st.button("✨ Explain it!") and prompt:
    with st.spinner("Thinking really hard... 🧠"):
        instruction = f"Explain '{prompt}' to a {age}-year-old in a {style.lower()} tone." if style != "Default" else f"Explain '{prompt}' to a {age}-year-old."

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": instruction}],
                temperature=0.7
            )

            explanation = response.choices[0].message.content

            # Typing animation
            with st.container():
                placeholder = st.empty()
                displayed_text = ""
                for char in explanation:
                    displayed_text += char
                    placeholder.markdown(f"🧾 **Explanation:**\n\n{displayed_text}")
                    time.sleep(0.005)

            # Save to file
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("explanations.txt", "a", encoding="utf-8") as file:
                file.write(f"[{timestamp}] Age {age}, Prompt: {prompt}\n{explanation}\n\n")

            st.session_state.counter += 1

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---- Counter ----
st.markdown(f"✅ Total explanations generated: **{st.session_state.counter}**")

# ---- Feedback ----
st.markdown("""
---
📢 **Feedback?** [Click here](https://tally.so/r/nGVy4o) to tell me what you think!
""")

# ---- Creator Info ----
st.markdown("""
---
Created with ❤️ by [Mike Petrillo](https://www.linkedin.com/in/mikelovesdata) · [GitHub](https://github.com/MikeyPetrillo/explain-like-im)
""")
