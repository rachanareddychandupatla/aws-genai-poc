import json

import boto3

#code to handle incoming req using knowledgebase
client = boto3.client('bedrock-agent-runtime')

def lambda_handler(prompt):
    user_prompt = prompt
    response = client.retrieve_and_generate(
        input={
            'text': user_prompt
        },
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'DHRTEPLCTQ',
                'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2'
            },
            'type': 'KNOWLEDGE_BASE'
        },
    )

    return response["output"]["text"]

# prompt ="Recommend three credit cards for my customer who is a frequent traveller"
# lambda_handler(prompt)