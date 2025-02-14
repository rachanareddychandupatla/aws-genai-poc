import streamlit as st
import random
import time
import boto3
import json
import os
from botocore.exceptions import BotoCoreError, ClientError

# Initialize Amazon Comprehend client
comprehend = boto3.client('comprehend', region_name='us-east-1')

# Secret configurations
botId = "BIDQLLPAMN"
botAliasId = "MNCI7OVVPR"
localeId = "en_US"
sessionId = "100"

st.title("Chat with Bedrock Knowledge Base")

# Initialize AWS clients
session = boto3.session.Session()
region_name = session.region_name

bedrock_client = boto3.client('bedrock-agent-runtime')
bot_client = boto3.client('lexv2-runtime')

# Fixed questions
fixed_questions = [
    "What is your credit card number?",
    "What is your date of birth?",
    "How much amount do you want to pay?",
    "Ok. Please wait while I process your information."
]

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "user_responses" not in st.session_state:
    st.session_state.user_responses = []

if "flag" not in st.session_state:
    st.session_state.flag = False

if "sock" not in st.session_state:
    st.session_state.sock = ""

# Display chat history
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

# Function to handle responses
def lambda_handler(user_input):
    response = bedrock_client.retrieve_and_generate(
        input={"text": user_input},
        retrieveAndGenerateConfiguration={
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": "ZB2KOJNF6C"
            },
            "modelArn": f"arn:aws:bedrock:{region_name}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
            "type": "KNOWLEDGE_BASE"
        }
    )
    return response['output']['text']

# Function to generate responses based on sentiment
def generate_response_based_on_sentiment(sentiment):
    response_text = "Recommend three credit cards for me and I travel a lot"
    return lambda_handler(response_text)

# Function to simulate typewriter effect
def sleep_bt_response(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Accept user input
if prompt := st.chat_input("Ask me anything?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_responses.append(prompt)

    if st.session_state.flag:
        pass
    else:
    #    backend.momo(st.session_state.sock, prompt)
        lex_response = bot_client.recognize_text(
            botId=botId,
            botAliasId=botAliasId,
            localeId=localeId,
            sessionId=sessionId,
            text=prompt
        )

        if 'messages' in lex_response:
            for message in lex_response['messages']:
                bot_response = message['content']
                with st.chat_message("assistant"):
                    st.write_stream(sleep_bt_response(bot_response))

                st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Streamed initial response
def response_generator():
    if st.session_state.step == 0:
        response = random.choice([
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Hello there! What do you need help with?"
        ])
        st.session_state.step += 1
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

# Display initial assistant response
if st.session_state.step == 0:
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    st.session_state.messages.append({"role": "assistant", "content": response})

# Connect button
connect_button = st.button("Connect to agent", type="primary")
if connect_button:
    with st.spinner("Please wait while I connect to an agent..."):
        # sock = backend.main()
        st.session_state.flag = True
        st.session_state.sock = sock
