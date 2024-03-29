# Func4_titleGeneration.py
import openai # Ensure you have the OpenAI library installed
import os
from dotenv import load_dotenv
load_dotenv()


def generate_chat_title(question):
    openai_api_key = os.getenv("apikey")
    """
    Generate a concise title for a chat based on the initial question.

    Args:
        question (str): The initial question of the chat.
        openai_api_key (str): Your OpenAI API key.

    Returns:
        str: A concise title for the chat, 5-6 words long.
    """
    # Initialize the OpenAI client
    client = openai.OpenAI()

    # Setup the chat completion API call
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Updated to use a non-deprecated model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
                {"role": "assistant", "content": "Generate a concise, engaging title of 5-6 words from the question above."}
            ]
        )
        # Assuming the response format aligns with your example, adjust as necessary
        title = response['choices'][0]['message']['content'].strip()
        return title
    except Exception as e:
        print(f"Error in generating title: {e}")
        return "Chat Title Generation Error"

'''
initial_question = "How can I improve my time management skills?"
chat_title = generate_chat_title(initial_question)
print(chat_title)
'''