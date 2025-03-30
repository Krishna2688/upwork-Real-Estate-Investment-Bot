import streamlit as st
from streamlit_extras.bottom_container import bottom


# Streamlit Landing Page

def main():
    # Header Section with Logo
    st.text("")
    st.text("")
    col1, col2 = st.columns([1, 12])
    with col1:
        st.image("logo_t.png", width=250)  # Replace 'logo_t.png' with your logo image path
    with col2:
        st.title("I am REA!!!")
        st.markdown("### Your Personal AI-Powered Real Estate Investment Assistant 🏡💼")

    # Main Description with Bordered Box
    st.markdown(
        """        
        <div style="border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; background-color: #000000;">
            <p style="font-size: 26px; ">Leverage the power of AI to analyze and assess your real estate investments with ease. 📈 🚀</p>
            <p style="font-size: 18px; ">With REIA, you can streamline your investment decisions by analyzing key financial metrics, market data, and property details—automatically!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("👈 Explore Features")
    st.markdown(
        "🔍 **Analyze Property Deals** \n📊 **Financial Modeling** \n🌍 **Market Data Insights** \n💬 **AI Recommendations**")

    with bottom():
        st.write("**&copy; 2025 Sanctum Digital Solutions**")


# Run the main function to render the landing page
main()