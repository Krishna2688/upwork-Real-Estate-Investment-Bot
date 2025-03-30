import streamlit as st
import pandas as pd
from docx import Document
import time

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role":"system", "content":"You are a real estate investment expert."}]

if "API_KEY" not in st.session_state:
    st.session_state["API_KEY"] = None

if "logon" not in st.session_state:
    st.session_state["logon"] = None

if "ai_insights" not in st.session_state:
    st.session_state["ai_insights"] = None

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True

def stream_data(data):
    for w in data.split(" "):
        yield w + " "
        time.sleep(0.1)

def query_gemini(messages, api_key):

    from openai import OpenAI
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    response = client.chat.completions.create(
        model="gemini-1.5-flash-latest",
        n=1,
        messages=messages
    )

    return response.choices[0].message.content

# Streamlit UI
# st.set_page_config(page_title="Real Estate AI Assistant", layout="wide")
# st.title("🏡 Real Estate AI Assistant")
# Header Section with Logo
col1, col2 = st.columns([1, 16])
with col1:
    st.image("logo_t.png", width=250)  # Replace 'path_to_logo.png' with the actual path to your logo image
with col2:
    st.title(":orange[REA] - Real Estate AI Assistant")

st.session_state["API_KEY"] = st.sidebar.text_input("Enter Your Key To Unlock (Press Enter)", type="password")
# logon = st.sidebar.button("Login", key="logon_button")

# with st.echo():
#     st.write(str(st.session_state["API_KEY"]))
#     # st.write(str(st.session_state.logon_button))

if st.session_state["API_KEY"]:
    st.sidebar.write("Upload underwriting models, analyze market data, and receive AI-driven deal insights.")
    # Upload Underwriting Model
    underwriting_file = st.sidebar.file_uploader("Upload Underwriting Model (Excel)", type=["xlsx"])
    property_file = st.sidebar.file_uploader("Upload Property Data (PDF)", type=["pdf"])
    market_file = st.sidebar.file_uploader("Upload Market Data (Word)", type=["docx"])

    if underwriting_file:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(underwriting_file)
        # Convert the DataFrame to a string
        df_string = df.to_string()
        underwriting_data = df_string
    else:
        df = pd.DataFrame()
        underwriting_data = "Not Given"

    with st.expander("Underwriting Model", icon="📄"):
        st.dataframe(df)

    if property_file:
        import PyPDF2
        # Open the PDF file
        reader = PyPDF2.PdfReader(property_file)

        # Extract text from each page
        property_data = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            property_data += page.extract_text()
    else:
        property_data = "Not Given"

    with st.expander("Property Packet", icon="🏠"):
        st.write(property_data)

    if market_file:
        doc = Document(market_file)
        market_data = ""
        for para in doc.paragraphs:
            market_data += para.text + "\n"
    else:
        market_data = "Not Given"
    with st.expander("Market Data", icon = "📊"):
        st.write(market_data)

    generate_insights = st.sidebar.button("Generate AI Insights")

    if generate_insights:
        # AI Analysis
        # st.write("### AI Deal Evaluation")
        prompt = f"""
        Given the following real estate underwriting details: {underwriting_data}    
        Additionally, considering the market data: {market_data},
        and the details extracted from the property information packet: {property_data},
        
        Provide an evaluation of this deal, potential risks, and recommendations.
        """
        st.session_state["messages"].append([{"role":"user", "content": prompt}])
        with st.spinner("Generating Deal Insights.."):
            response = query_gemini(st.session_state["messages"],st.session_state["API_KEY"])
            st.session_state["messages"].append({"role": "assistant", "content": response})
            st.write("#### AI Insights & Recommendations")
            st.write_stream(stream_data(response))
            st.session_state["ai_insights"] = response

        st.button('Chat', on_click=click_button)

    if st.session_state.clicked:
        with st.expander("AI Insights & Recommendations"):
            st.write(st.session_state["ai_insights"])
        user_input = st.chat_input("Ask me about your deal")

        if user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})
            for m in st.session_state["messages"][3:]:
                print(f"ch {m}")
                for r, c in m.items():
                    if r == "role":
                        role = c
                    elif r == "content":
                        if role == "user":
                            if isinstance(c, str) and not c.startswith("CONTEXT:"):
                                user_message = st.chat_message("user", avatar="ra_avatar.png")
                                user_message.write(c)
                        elif role == "assistant":
                            assistant_message = st.chat_message("assistant", avatar="logo_t.png")
                            assistant_message.write(c)

            response = query_gemini(st.session_state["messages"], st.session_state["API_KEY"])
            st.session_state["messages"].append({"role": "assistant", "content": response})
            assistant_message = st.chat_message("assistant", avatar="logo_t.png")
            assistant_message.write_stream(stream_data(response))
else:
    st.subheader("👈 Log on by entering your secret key")