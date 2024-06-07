import streamlit as st
import random
import time
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Initialize Amazon Comprehend client
comprehend = boto3.client('comprehend', region_name='us-west-2')  # Replace with your preferred region

# Fixed questions
fixed_questions = [
    "What is your credit card number?",
    "What is your date of birth?",
    "How much amount do you want to pay?",
    "Ok. Please wait while I process your information."
]

st.title("Simple chat")

# Initialize chat history and user inputs
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0
    st.session_state.user_responses = []  # Store each user response here

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to analyze text with Amazon Comprehend
def analyze_text(text):
    try:
        response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        sentiment = response['Sentiment']
        return f"Detected sentiment: {sentiment}"
    except (BotoCoreError, ClientError) as e:
        return f"Error analyzing text: {str(e)}"


def generate_response_based_on_sentiment(sentiment):
    if sentiment == "POSITIVE":
        response = "I can sense you're feeling good about this! Let's continue."
    elif sentiment == "NEGATIVE":
        response = "I'm here to help. Please let me know how I can assist further."
    elif sentiment == "NEUTRAL":
        response = "Okay, let's proceed with the next step."
    else:  # Mixed sentiment
        response = "I noticed mixed feelings. Could you please provide more details?"
    return response

# Accept user input
if prompt := st.chat_input("Ask me anything?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Append user response to the list
    st.session_state.user_responses.append(prompt)

    # Check if all fixed questions have been answered
    if st.session_state.step < len(fixed_questions):
        # Generate next fixed question
        response = fixed_questions[st.session_state.step]
        st.session_state.step += 1

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        # Combine all user inputs into a single string for analysis
        combined_text = " ".join(st.session_state.user_responses)
        analysis_result = analyze_text(combined_text)
        final_response = generate_response_based_on_sentiment(analysis_result)

        with st.chat_message("assistant"):
            st.markdown(f"Final analysis of your responses: {analysis_result}")
            st.markdown(f"{final_response}")
        st.session_state.messages.append({"role": "assistant", "content": f"final analysis of your responses: {final_response}"})


# Streamed initial response
def response_generator():
    if st.session_state.step == 0:
        response = random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
        )
        st.session_state.step += 1  # Move to next step for fixed questions
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

# Display initial assistant response
if st.session_state.step == 0:
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    st.session_state.messages.append({"role": "assistant", "content": response})
