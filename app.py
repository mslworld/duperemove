import streamlit as st
import streamlit.components.v1 as components

# Page layout ko wide set karna taaki multiple columns fit aa sakein
st.set_page_config(layout="wide", page_title="Multi-Screen Browser Tool")

st.title("🌐 Dynamic Multi-Screen Browser Tool")

# Search bar / URL input
st.markdown("### 🔍 Search / Enter URL")
url = st.text_input(
    "Website ka URL enter karein (e.g., https://www.wikipedia.org):", 
    "https://www.wikipedia.org"
)

# Dynamic Rows aur Columns ke liye input
st.markdown("### 🎛️ Grid Layout Settings")
col1, col2 = st.columns(2)

with col1:
    # Aap isko apni marzi se jitna chahein badha sakte hain
    rows = st.number_input("Rows ki tadad:", min_value=1, value=2, step=1)

with col2:
    # Limit nahi hai, aap unlimited columns set kar sakte hain
    cols = st.number_input("Columns ki tadad:", min_value=1, value=5, step=1)

st.markdown("---")

# Grid generate karne ka logic
if url:
    screen_count = 1
    for r in range(int(rows)):
        # Streamlit mein dynamic columns banana
        columns_layout = st.columns(int(cols))
        
        for c in range(int(cols)):
            with columns_layout[c]:
                # Har screen ka title aur iframe
                st.markdown(f"**Screen {screen_count}**")
                
                # Streamlit components ka use karke external URL embed karna
                try:
                    components.iframe(url, height=400, scrolling=True)
                except Exception as e:
                    st.error("Website load hone mein masla hai.")
                
                screen_count += 1

# Note: Kuch badi websites (jaise Google, Facebook) security reasons (X-Frame-Options) 
# ki wajah se iframe mein open nahi hoti hain. Aise mein un sites ke search APIs use karne padte hain.
