import os, requests, streamlit as st

API_URL = os.getenv("API_URL", "http://translator-api:8000/translate")

st.title("German ➜ French translator")
text = st.text_area("Enter German text")

if st.button("Translate") and text.strip():
    with st.spinner("Calling API …"):
        res = requests.post(API_URL, json={"text": text})
    if res.ok:
        st.success(res.json()["translation"])
    else:
        st.error(f"API error: {res.text}")
