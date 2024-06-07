import streamlit as st
import random
import time

fixed_questions = [
    "What is your credit card number ?",
    "What is your data of birth ?",
    "How much amount do you want to pay ?",
    "Ok. Please wait while I process your information."
]

st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything ?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Streamed response emulator
def response_generator():
    if st.session_state.step == 0:
        response = random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
        )
    else:
        response = fixed_questions[st.session_state.step - 1]
    st.session_state.step += 1
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

#Display assistant response in chat message container
with st.chat_message("assistant"):
    response = st.write_stream(response_generator())
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})