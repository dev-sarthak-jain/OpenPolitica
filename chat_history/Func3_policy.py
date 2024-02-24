import requests
import os
from dotenv import load_dotenv
import time
import json
import datetime

load_dotenv()

def generate_policy_card(user_needs_input):
    policy_cards = []

    # Get current date in YYYY-MM-DD format
    today_date = datetime.date.today().strftime("%Y-%m-%d")

    for idx, (need, ranking) in enumerate(user_needs_input.items() if isinstance(user_needs_input, dict) else [(need, None) for need in user_needs_input], 1):
        # Constructing the system message to instruct the model to output JSON
        system_message = "You are a helpful assistant of humanity designed to see a user/human need or desired outcome and output a potentially intelligent policy recommendation in JSON format."
        
        user_message_content = f"Generate a policy recommendation in JSON format for the following user need: {need}" + (f" (Ranking: {ranking})" if ranking is not None else "")
        
        data = {
            "model": "gpt-3.5-turbo-0125",  # Specify the model
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message_content}
            ],
            "response_format": {"type": "json_object"}  # Enable JSON mode
        }

        headers = {
            'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
            response.raise_for_status()  # This will raise an exception for HTTP error codes
            response_data = response.json()
            
            # Extracting the JSON content from the message
            policy_recommendation_json = json.loads(response_data['choices'][0]['message']['content'])

            # Assuming policy_recommendation_json contains the fields you need
            policy_card = {
                "content": policy_recommendation_json.get("recommendation", "No recommendation could be generated."),
                "userneed_id": idx,
                "category": "Urban Development",
                "effective_date": today_date,
                "policy_makers": policy_recommendation_json.get("policy_makers", "N/A"),
                "voting_status": policy_recommendation_json.get("voting_status", False),
                "regional_info": policy_recommendation_json.get("regional_info", "N/A")
            }

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            policy_card = {
                "content": "Error in generating recommendation.",
                "userneed_id": idx,
                "category": "Urban Development",
                "effective_date": today_date,
                "policy_makers": "N/A",
                "voting_status": False,
                "regional_info": "N/A"
            }

        policy_cards.append(policy_card)
        time.sleep(0.5)  # Be mindful of the rate limits

    return policy_cards
