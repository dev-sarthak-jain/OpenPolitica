import requests
import os
from dotenv import load_dotenv
load_dotenv()
import time 
import json
import datetime 

def generate_policy_card(user_needs_input):
    policy_cards = []

    # Get current date in YYYY-MM-DD format
    today_date = datetime.date.today().strftime("%Y-%m-%d")

    # Determine if input is a dict (with rankings) or list (without rankings)
    if isinstance(user_needs_input, dict):
        user_needs = user_needs_input.items()
    else:
        user_needs = [(need, None) for need in user_needs_input]

    for idx, (need, ranking) in enumerate(user_needs, 1):
        if ranking is not None:
            prompt = f"Generate a policy recommendation for the following user need:\n- {need} (Ranking: {ranking})\n"
        else:
            prompt = f"Generate a policy recommendation for the following user need:\n- {need}\n"

        headers = {
            'Authorization': f'Bearer {os.getenv("apikey")}',
            'Content-Type': 'application/json'
        }

        data = {
            "model": "text-davinci-003", 
            "prompt": prompt,
            "max_tokens": 150
        }

        try:
            response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()

            policy_recommendation = response_data.get('choices', [{}])[0].get('text', '').strip()

            if not policy_recommendation:
                policy_recommendation = "No recommendation could be generated."

        except requests.RequestException as e:
            print(f"Error: {e}")
            policy_recommendation = "Error in generating recommendation."

        policy_card = {
            "content": policy_recommendation,
            "userneed_id": idx,
            "category": "Urban Development",
            "effective_date": today_date,
            "policy_makers": "N/A",
            "voting_status": False,
            "regional_info": "N/A"
        }

        policy_cards.append(policy_card)
        time.sleep(0.5)

    return policy_cards

# Example usage with and without rankings
user_needs_with_rankings = {
    "Affordability of food in local area": 5,
    "Safety of local area": 3,
    "Affordability of college": 4
}

user_needs_without_rankings = [
    "Affordability of food in local area",
    "Safety of local area",
    "Affordability of college"
]

'''
policy_cards_with_rankings = generate_policy_cards(user_needs_with_rankings, openai_api_key)
policy_cards_without_rankings = generate_policy_cards(user_needs_without_rankings, openai_api_key)

# Print policy cards
for card in policy_cards_with_rankings:
    print(json.dumps(card, indent=2))

for card in policy_cards_without_rankings:
    print(json.dumps(card, indent=2))
'''