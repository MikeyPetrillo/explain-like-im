import streamlit as st
import os
import random
import time
import urllib.parse
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Streamlit config
st.set_page_config(page_title="Explain Like I'm...", page_icon="🧠")

# Sidebar
with st.sidebar:
    st.title("🧠 Explain Like I'm...")
    st.markdown("""
This tiny tool helps you reframe any concept for any age — from 1 to 100.

- Great for simplifying complex ideas
- Built in one night with GPT

[💬 Give feedback](https://tally.so/r/nGVy4o)
""")

# Hero
st.markdown("""
## 🧠 Explain Like I'm...
Explain any concept in a way a **1 to 100-year-old** could understand.

Just paste your text. Pick an age. Boom — explained.

🤯 🧒 👩‍🎓 👨‍💼 👵  
---
""")

# Query param handling
query_params = st.query_params
if "q" in query_params:
    st.session_state.input_text = urllib.parse.unquote(query_params["q"])
if "a" in query_params:
    st.session_state.age = int(query_params["a"])

# Example buttons
example_1 = "What is blockchain?"
example_2 = "Why do we pay taxes?"

col1, col2 = st.columns(2)
with col1:
    if st.button("💡 Try Example: Blockchain"):
        st.session_state.input_text = example_1
with col2:
    if st.button("💡 Try Example: Taxes"):
        st.session_state.input_text = example_2

# Text input
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

input_text = st.text_area("🔍 What do you want explained?", st.session_state.input_text, height=200)
st.session_state.input_text = input_text

# Tone selection
tone = st.selectbox("🗣️ Choose a tone (optional)", ["Default", "Funny", "Poetic", "Sarcastic"])

# Age slider
if "age" not in st.session_state:
    st.session_state.age = 5

col3, col4 = st.columns([3, 1])
with col3:
    age = st.slider("🎂 Explain like I'm...", 1, 100, st.session_state.age)
    st.session_state.age = age
with col4:
    if st.button("🎲 Surprise Me"):
        st.session_state.age = random.randint(1, 100)
        st.rerun()

emoji = "🍼" if age < 10 else "🎓" if age < 25 else "💼" if age < 65 else "🧓"
st.caption(f"You're explaining this to someone who is **{age} years old** — {emoji}")
st.markdown("---")

# Explanation generator
if st.button("🧠 Explain it!"):
    if not input_text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Thinking like a 5-year-old... or a 100-year-old..."):
            style_prompt = f" Use a {tone.lower()} tone." if tone != "Default" else ""
            prompt = f"""
You are a world-class communicator. Your task is to explain the following text to someone who is {age} years old.{style_prompt}

Use vocabulary, tone, and examples appropriate for someone that age. Be empathetic, concise, and funny if appropriate.

Text to explain:
\"\"\"{input_text}\"\"\"
"""
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                explanation = response.choices[0].message.content

                st.markdown("### ✍️ Here's the explanation (typing...):")

                # Typing animation
                placeholder = st.empty()
                typed = ""
                for char in explanation:
                    typed += char
                    placeholder.markdown(f"```\n{typed}\n```")
                    time.sleep(0.01)

                # Share link
                base_url = "https://your-app-name.streamlit.app"  # Replace with your deployed app URL
                share_url = f"{base_url}?q={urllib.parse.quote(input_text)}&a={age}"
                st.markdown(f"🔗 [Share this explanation](<{share_url}>)")

                st.button("🔁 Try another age or input", on_click=st.rerun)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
