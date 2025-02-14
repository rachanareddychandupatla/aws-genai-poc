import time
import random
import boto3
import streamlit as st
from botocore.exceptions import BotoCoreError, ClientError

# Initialize session state for storing messages and responses
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_responses" not in st.session_state:
    st.session_state.user_responses = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "flag" not in st.session_state:
    st.session_state.flag = False

# Initialize AWS clients
comprehend = boto3.client("comprehend", region_name="us-east-1")  # Change region if needed
bot_client = boto3.client("lexv2-runtime", region_name="us-east-1")  # Change region if needed

# Define Lex bot parameters (Replace with actual values)
botId = "your-bot-id"
botAliasId = "your-bot-alias-id"
localeId = "en_US"
sessionId = "unique-session-id"

st.title("Agent Ultron")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to analyze sentiment using Amazon Comprehend
def analyze_text(text):
    try:
        response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
        sentiment = response["Sentiment"]
        return f"Detected Sentiment: {sentiment}"
    except (BotoCoreError, ClientError) as e:
        return f"Error analyzing text: {str(e)}"

# Function to generate responses based on sentiment
def generate_response_based_on_sentiment(sentiment):
    if sentiment == "POSITIVE":
        return "That's great to hear!"
    elif sentiment == "NEGATIVE":
        return "I'm sorry to hear that. How can I help?"
    elif sentiment == "NEUTRAL":
        return "Got it. Let me know how I can assist you."
    else:
        return "Interesting. Tell me more!"

# Function to simulate streaming response
def sleep_bt_response(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Accept user input
prompt = st.chat_input("Type your message here...")
if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_responses.append(prompt)

    # Call Amazon Lex for response
    if st.session_state.flag:
        backend.momo(st.session_state.sock, prompt)  # Placeholder for backend function
    else:
        lex_response = bot_client.recognize_text(
            botId=botId,
            botAliasId=botAliasId,
            localeId=localeId,
            sessionId=sessionId,
            text=prompt
        )
        bot_reply = lex_response.get("messages", [{"content": "I'm not sure how to respond."}])[0]["content"]

    # Analyze sentiment
    sentiment_analysis = analyze_text(prompt)

    # Generate response based on sentiment
    final_response = generate_response_based_on_sentiment(sentiment_analysis.split(": ")[1])

    # Display chatbot response
    with st.chat_message("assistant"):
        response_generator = sleep_bt_response(final_response)
        full_response = "".join(response_generator)
        st.markdown(full_response)

    # Store chatbot response
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Print sentiment analysis in sidebar
with st.sidebar:
    st.write(sentiment_analysis)
