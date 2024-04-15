from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory  # Or adjust based on available memory management
import os
from dotenv import load_dotenv
import datetime
import json

load_dotenv(override=True)

def initialize_openai_model():
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(openai_api_key=openai_api_key)

# Assuming necessary imports are done

def generate_policy_card(user_needs_input):
    model = initialize_openai_model()
    policy_cards = []
    today_date = datetime.date.today().strftime("%Y-%m-%d")

    for idx, (need, ranking) in enumerate(user_needs_input.items(), 1):
        prompt_messages = [
            SystemMessagePromptTemplate.from_template("You are a helpful assistant of humanity designed to see a user/human need or desired outcome and output a potentially intelligent policy recommendation."),
            HumanMessagePromptTemplate.from_template(f"Need: {need}" + (f" (Ranking: {ranking})" if ranking else ""))
        ]

        prompt = ChatPromptTemplate(messages=prompt_messages)
        llmchain = LLMChain(llm=model, prompt=prompt)
        try:
            # .invoke({"question": user_input})
            response = llmchain.invoke({}, temperature=0.7)
            recommendation = response['text'].split('\n')[-1].strip("AI: ")
        except Exception as e:
            print(f"Error during recommendation generation: {e}")
            recommendation = "Error in generating recommendation."

        policy_card = {
            "content": recommendation,
            "userneed_id": idx,
            "category": "Urban Development",
            "effective_date": today_date,
            "policy_makers": "N/A",
            "voting_status": False,
            "regional_info": "N/A"
        }

        policy_cards.append(policy_card)

    return policy_cards




# # Example usage, adjust as necessary
# user_needs_with_rankings = {
#     "Affordability of food in local area": 5,
#     "Safety of local area": 3,
#     "Affordability of college": 4
# }

# policy_cards_with_rankings = generate_policy_card(user_needs_with_rankings)

# # Print policy cards
# for card in policy_cards_with_rankings:
#     print(json.dumps(card, indent=2))
