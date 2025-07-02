import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import urllib.parse
import time

load_dotenv()

# Set up OpenAI API key from Streamlit secrets or .env
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=api_key)

# App config
st.set_page_config(page_title="🧠 Explain Like I'm 5", layout="centered")

# Define the base URL for sharing
base_url = "https://explain-like-im-five.streamlit.app/"

# Title and subtitle
st.markdown("<h1 style='text-align: center;'>🧠 Explain Like I'm 5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Paste anything — and get it explained like you're 5 to 100 years old.</p>", unsafe_allow_html=True)

# User input
text = st.text_area("✍️ Paste something here:", placeholder="E.g. What is quantum computing?")

age = st.slider("🎂 Pick your age level:", min_value=1, max_value=100, value=5)

# Call OpenAI
if st.button("Explain It"):
    if not text.strip():
        st.warning("Please paste something first.")
    else:
        with st.spinner("Thinking really hard... 🤔"):
            prompt = f"Explain the following to someone who is {age} years old:\n\n{text}"
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                explanation = response.choices[0].message.content.strip()

                # Typing animation
                output = ""
                output_area = st.empty()
                for char in explanation:
                    output += char
                    output_area.markdown(f"🧾 **Explanation:**\n\n{output}")
                    time.sleep(0.01)

                # Shareable link
                encoded_text = urllib.parse.quote_plus(text)
                share_link = f"{base_url}?text={encoded_text}&age={age}"

                st.markdown("🔗 **Share this explanation**")
                st.code(share_link)
                st.button("📋 Copy to clipboard", on_click=st.toast, args=("Link copied!",))

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# Feedback
st.markdown("---")
st.markdown("📬 **Have feedback or want to suggest a feature?**")
st.markdown("[Submit Feedback via Tally](https://tally.so/r/nGVy4o)")

# Optional: preload from URL query params
query = st.query_params
if "text" in query and "age" in query:
    preloaded_text = query["text"]
    preloaded_age = int(query["age"])
    st.text_area("✍️ Paste something here:", value=preloaded_text, key="from_link")
    st.slider("🎂 Pick your age level:", min_value=1, max_value=100, value=preloaded_age, key="from_link_age")
