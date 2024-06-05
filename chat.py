import streamlit as st
import RecommendationSystemBackend as backend

st.set_page_config(page_title="Credit Card Recommendation With Amazon Bedrock")

new_title = '<p style="font-family:sans-serif; color:Green; font-size:42px;">Credit Card Recommendation With Amazon Bedrock</p>'
st.markdown(new_title, unsafe_allow_html=True)

if 'vector_index' not in st.session_state:
    with st.spinner("Wait for magic...All beautiful things in life take time :-"):
        st.session_state.vector_index = backend.data_ingension_flow()

input_text = st.text_area("Input text", label_visibility="collapsed")
go_button = st.button("Get Credit Card Recommendations", type="primary")

if go_button:
    with st.spinner("I can do more"):
        response_content = backend.userRecommendations(index=st.session_state.vector_index, question=input_text)
        st.write(response_content)