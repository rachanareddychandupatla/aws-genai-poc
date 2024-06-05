import json

import boto3

client = boto3.client('bedrock-agent-runtime')

def lambda_handler(prompt):
    user_prompt = prompt
    response = client.retrieve_and_generate(
        input={
            'text': user_prompt
        },
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'C1YEQO6PYG',
                'modelArn': 'anthropic.claude-v2:1'
            },
            'type': 'KNOWLEDGE_BASE'
        },
    )

prompt ="Recommend three credit cards for my customer who is a frequent traveller"
lambda_handler(prompt)