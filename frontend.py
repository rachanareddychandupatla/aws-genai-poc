import streamlit as st
import Backend as backend

# Page configuration
st.set_page_config(page_title="Credit Card Recommendation With Amazon Bedrock")

# Custom CSS
st.markdown("""
    <style>
        .title {
            font-family: sans-serif;
            color: Green;
            font-size: 42px;
        }
        .response {
            font-family: sans-serif;
            color: Black;
            font-size: 20px;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .stButton button {
            font-family: sans-serif;
            font-size: 16px;
        }
        .stTextArea textarea {
            font-family: sans-serif;
            font-size: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

# Title
new_title = '<p class="title">Credit Card Recommendation With Amazon Bedrock</p>'
st.markdown(new_title, unsafe_allow_html=True)

# Input text area
input_text = st.text_area("Input text", label_visibility="collapsed")

# Button
go_button = st.button("Get Credit Card Recommendations", type="primary")

if go_button:
    with st.spinner("Please wait while I get the best cards for you"):
        response_content = backend.lambda_handler(prompt=input_text)
        response_html = f'<div class="response">{response_content}</div>'
        st.markdown(response_html, unsafe_allow_html=True)
