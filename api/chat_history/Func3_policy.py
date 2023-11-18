import requests
import os
from dotenv import load_dotenv
load_dotenv()
import time 

def generate_policy_card(user_needs_rankings):
    openai_api_key= os.getenv("apikey")
    policy_cards = []

    for idx, (need, ranking) in enumerate(user_needs_rankings.items(), 1):
        prompt = f"Generate a policy recommendation for the following user need:\n- {need} (Ranking: {ranking})\n"

        headers = {
            'Authorization': f'Bearer {openai_api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            "model": "text-davinci-003", 
            "prompt": prompt,
            "max_tokens": 150
        }

        try:
            response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad status codes
            response_data = response.json()

            policy_recommendation = response_data.get('choices', [{}])[0].get('text', '').strip()

            if not policy_recommendation:  # Check if the recommendation is empty
                policy_recommendation = "No recommendation could be generated."

        except requests.RequestException as e:
            print(f"Error: {e}")
            policy_recommendation = "Error in generating recommendation."

        policy_card = {
            "content": policy_recommendation,
            "userneed_id": idx,
            "category": "Urban Development",
            "effective_date": "2023-11-13",
            "policy_makers": "N/A",
            "voting_status": False,
            "regional_info": "N/A"
        }

        policy_cards.append(policy_card)
        time.sleep(0.5)  # Add a small delay to avoid hitting rate limits

    return policy_cards

'''
user_needs = {
    "Affordability of food in local area": 5,
    "Safety of local area": 3,
    "Affordability of college": 4
}

openai_api_key = apikey
policy_cards = generate_policy_cards(user_needs, openai_api_key)
for card in policy_cards:
    print(json.dumps(card, indent=2))
'''
# Policy Card Generation Documentation

# Overview

# The Policy Card Generation feature in our application is designed to create policy recommendations based on user needs. These policy cards are generated using OpenAI's GPT model, leveraging natural language processing to produce insightful, relevant, and actionable policy suggestions. This feature is crucial for decision-makers, policy analysts, and stakeholders who require quick, AI-driven insights into public needs and preferences.

# Components

# generate_policy_card Function: The core function that interfaces with the OpenAI API to generate policy recommendations.
# User Needs Input: User needs and their rankings are taken as input, reflecting the priorities and concerns of the user base.
# Policy Card Output: The output is a structured policy card containing the policy recommendation and relevant metadata.

# Arguments
# user_needs_rankings (dict): A dictionary where keys are user needs (as strings) and values are their rankings (as integers).
# openai_api_key (str): The API key for accessing OpenAI's GPT model.
# Return Value
# Returns a dictionary representing a policy card, including the policy recommendations and related information.

# Output Structure

# The generated policy card is a dictionary with the following keys:

# content: The textual content of the policy recommendation.
# userneed_id: The identifier of the user need.
# category: The category of the policy (e.g., "Urban Development").
# effective_date: The date when the policy is to be considered effective.
# policy_makers: Information about the policymakers involved (if available).
# voting_status: The current voting status of the policy.
# regional_info: Regional information relevant to the policy (if applicable).
# Error Handling

# The function includes error handling for unauthorized access (incorrect API key) and network issues.
# In case of an error, the function returns a policy card with an "Error in generating recommendation" message.
# Security Considerations

# API keys should be stored securely and never hard-coded into the application.
# Access to the API key should be limited to authorized personnel only.
# Integration Guidelines

# Ensure the function is integrated with a secure backend service.
# User needs and rankings should be collected and processed securely, adhering to data privacy laws.
# The output policy cards should be presented in a user-friendly format, suitable for the target audience.
# Further Development

# The policy card generation feature can be enhanced to include more detailed analytics, regional customization, and support for multiple languages.
# Continuous testing and updating are recommended to keep the feature aligned with the latest OpenAI API developments.


