import streamlit as st

st.set_page_config(
    page_title="REA",
    page_icon="sanctum_t_l.png",
    layout="wide"
)

st.logo("sanctum_t_l.png", size="large")

reia = st.Page("reia.py", title="REA", icon="📨")

home = st.Page("landing.py", title="Home", icon=":material/home:")


pg = st.navigation(
        {
            "🏠Home": [home],
            "✅AI Assist": [reia],
        }
    )

pg.run()
