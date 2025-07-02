import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import urllib.parse

# Load .env
load_dotenv()

# Set OpenAI key
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=api_key)

# Config
st.set_page_config(page_title="🧠 Explain Like I'm 5", layout="centered")
base_url = "https://explain-like-im-five.streamlit.app/"

# Title
st.markdown("<h1 style='text-align: center;'>🧠 Explain Like I'm 5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Paste anything — and get it explained like you're 5 to 100 years old, with a bit of flair.</p>", unsafe_allow_html=True)

# Query params
query = st.query_params
preloaded_text = query.get("text", "")
preloaded_age = int(query.get("age", 5))
preloaded_tone = query.get("tone", "Default")

# Sidebar presets
with st.sidebar:
    st.header("📘 Try an example")
    preset = st.selectbox(
        "Choose a topic:",
        ["", "What is quantum physics?", "How do mortgages work?", "What is blockchain?", "Explain climate change"]
    )
    if preset:
        preloaded_text = preset

# Input
text = st.text_area("📋 Paste something here:", value=preloaded_text)
age = st.slider("🎂 Pick your age level:", min_value=1, max_value=100, value=preloaded_age)
tone = st.selectbox("🎭 Add a tone (optional):", ["Default", "Funny", "Sarcastic", "Poetic"], index=["Default", "Funny", "Sarcastic", "Poetic"].index(preloaded_tone))

# Button
if st.button("💡 Explain It"):
    if not text.strip():
        st.warning("Please paste something first.")
    else:
        with st.spinner("Thinking really hard... 🤯"):
            tone_instruction = "" if tone == "Default" else f"Use a {tone.lower()} tone."
            prompt = f"Explain the following to someone who is {age} years old. {tone_instruction}\n\n{text}"

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )
                explanation = response.choices[0].message.content.strip()

                st.success("Done! Here's your explanation:")
                st.markdown("🧾 **Your Explanation:**")
                st.markdown(f"{explanation}")
                st.balloons()

                # Download
                st.download_button("⬇️ Save as Text", explanation, file_name="explanation.txt")

                # Share link
                encoded_text = urllib.parse.quote_plus(text)
                encoded_tone = urllib.parse.quote_plus(tone)
                share_link = f"{base_url}?text={encoded_text}&age={age}&tone={encoded_tone}"

                st.markdown("🔗 **Share this explanation**")
                st.code(share_link)
                st.button("📋 Copy to clipboard", on_click=st.toast, args=("Link copied!",))

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# Feedback
st.markdown("---")
st.markdown("📬 **Have feedback or want to suggest a feature?**")
st.markdown("[Submit Feedback via Tally](https://tally.so/r/nGVy4o)")

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; font-size: 0.9em;'>
  🛠️ Created by <a href='https://www.linkedin.com/in/mikelovesdata' target='_blank'>Mike Petrillo</a> · 
  <a href='https://github.com/MikeyPetrillo/explain-like-im' target='_blank'>GitHub Repo</a>
</p>
""", unsafe_allow_html=True)

# Retro visitor counter
st.markdown(
    "<p style='text-align: center;'><img src='https://visitor-badge.laobi.icu/badge?page_id=explain-like-im-five' alt='visitor badge'></p>",
    unsafe_allow_html=True
)
