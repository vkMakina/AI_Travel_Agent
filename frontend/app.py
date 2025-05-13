# frontend/app.py – Streamlit Frontend for Travel Planner

import streamlit as st
import requests

st.set_page_config(page_title="AI Travel Planner", layout="centered")
st.title("✈️ AI Travel Planner")
st.caption("Ask anything about your next trip!")

prompt = st.text_area("What do you want to know?", placeholder="e.g., What's the best time to visit Italy and what should I pack?")

if st.button("Get Travel Plan") and prompt:
    with st.spinner("Thinking like a travel expert..."):
        try:
            response = requests.post(
                url="http://localhost:8000/travel-plan",
                json={"prompt": prompt}
            )
            if response.status_code == 200:
                st.success("Here's your travel guide!")
                st.markdown(response.json()["response"])
            else:
                st.error("Failed to fetch travel plan. Try again.")
        except Exception as e:
            st.error(f"Error: {e}")
