import streamlit as st
import streamlit.components.v1 as components

# Page layout ko wide set karna
st.set_page_config(layout="wide", page_title="MSL SEARCH TOOL")

# Top Header Layout (Title aur Row/Col Inputs)
header_col1, header_col2, header_col3 = st.columns([2, 1, 1])

with header_col1:
    st.markdown("### MSL SEARCH TOOL")
with header_col2:
    rows = st.number_input("Rows", min_value=1, value=2, step=1)
with header_col3:
    cols = st.number_input("Column", min_value=1, value=5, step=1)

st.markdown("---")

# Dynamic Grid Generation
screen_count = 1

# Rows create karna
for r in range(int(rows)):
    # Columns create karna
    grid_cols = st.columns(int(cols))
    
    for c in range(int(cols)):
        with grid_cols[c]:
            # Har screen ke liye individual search bar
            search_query = st.text_input(
                "Google Search Here", 
                placeholder="Google Search Here",
                key=f"search_{screen_count}",
                label_visibility="collapsed" # Label hide kar ke sirf placeholder dikhane ke liye
            )
            
            # Container for the screen content
            with st.container():
                if search_query:
                    # Agar user direct URL type nahi karta, toh usko search query bana dein
                    if not search_query.startswith("http"):
                        # Note: Google iframe mein block hota hai, isliye hum Bing search embed kar rahe hain 
                        # jo iframes mein achi tarah kaam karta hai. Aap custom iframe-friendly URLs use kar sakte hain.
                        url = f"https://www.bing.com/search?q={search_query}"
                    else:
                        url = search_query
                    
                    try:
                        components.iframe(url, height=350, scrolling=True)
                    except Exception as e:
                        st.error("Error loading page")
                else:
                    # Agar search bar khali hai toh default "screen X" text dikhaye
                    st.markdown(
                        f"""
                        <div style="height: 350px; display: flex; align-items: center; justify-content: center; border: 1px solid #ddd; border-radius: 5px;">
                            <h3>screen {screen_count}</h3>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
            
            screen_count += 1
