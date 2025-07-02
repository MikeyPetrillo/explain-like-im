import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import urllib.parse

# Load environment
load_dotenv()

# OpenAI API Key
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=api_key)

# Page config
st.set_page_config(page_title="🧠 Explain Like I'm 5", layout="centered")
base_url = "https://explain-like-im-five.streamlit.app/"

# Set defaults in session
if "text" not in st.session_state:
    st.session_state["text"] = ""
if "output" not in st.session_state:
    st.session_state["output"] = ""
if "history" not in st.session_state:
    st.session_state["history"] = []

# Title
st.markdown("<h1 style='text-align: center;'>🧠 Explain Like I'm 5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Paste anything — and get it explained like you're 5 to 100 years old, with a bit of flair.</p>", unsafe_allow_html=True)

# Examples
st.markdown("📘 **Try an example:**")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔗 What is blockchain?"):
        st.session_state["text"] = "What is blockchain?"
with col2:
    if st.button("📈 What is customer lifetime value?"):
        st.session_state["text"] = "What is customer lifetime value?"
with col3:
    if st.button("🏗️ What is a microservice?"):
        st.session_state["text"] = "What is a microservice?"

# Inputs
text = st.text_area("📋 Paste something here:", value=st.session_state["text"])
age = st.slider("🎂 Pick your age level:", 1, 100, 5)
tone = st.selectbox("🎭 Add a tone (optional):", ["Default", "Funny", "Sarcastic", "Poetic"])

# Explain button
if st.button("💡 Explain It"):
    if not text.strip():
        st.warning("Please paste something first.")
    else:
        with st.spinner("Thinking really hard... 🧯"):
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
                st.session_state["text"] = text
                st.session_state["output"] = explanation
                st.session_state["history"].insert(0, {
                    "text": text,
                    "age": age,
                    "tone": tone,
                    "output": explanation
                })
                st.session_state["history"] = st.session_state["history"][:3]
                st.balloons()
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# Display explanation
if st.session_state["output"]:
    explanation = st.session_state["output"]
    st.success("Done! Here's your explanation:")
    st.markdown("🗾️ **Your Explanation:**")
    st.markdown(explanation)

    # Save/share
    save_text = f"""📋 Original Prompt:
{text.strip()}

🎂 Age Level:
{age}

🎭 Tone:
{tone}

🗾️ Explanation:
{explanation}
"""
    st.download_button("⬇️ Save as Text", save_text, file_name="explanation.txt")

    encoded_text = urllib.parse.quote_plus(text)
    encoded_tone = urllib.parse.quote_plus(tone)
    share_link = f"{base_url}?text={encoded_text}&age={age}&tone={encoded_tone}"
    st.markdown("🔗 **Share this explanation**")
    st.code(share_link)
    st.button("📋 Copy to clipboard", on_click=st.toast, args=("Link copied!",))

# History
if st.session_state["history"]:
    st.markdown("---")
    st.markdown("🔄 **Previous Explanations:**")
    for i, h in enumerate(st.session_state["history"]):
        with st.expander(f"#{i+1}: {h['text'][:50]}..."):
            st.markdown(f"**🎂 Age:** {h['age']} | **🎭 Tone:** {h['tone']}")
            st.markdown(h["output"])

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

# Retro Counter
st.markdown(
    "<p style='text-align: center;'><img src='https://visitor-badge.laobi.icu/badge?page_id=explain-like-im-five' alt='visitor badge'></p>",
    unsafe_allow_html=True
)
