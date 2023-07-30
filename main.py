import textbase
from textbase.message import Message
from textbase import models
from typing import List
import os
import datetime

# Load your OpenAI API key
models.OpenAI.api_key = "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"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!

"""
# Language Learning Tips
LANGUAGE_TIPS = {
    "english": "Tip: Practice speaking with native English speakers to improve your fluency.",
    "spanish": "Tip: Watch Spanish movies with subtitles to pick up common phrases.",
    # Add more language tips here
}


# Function to get the current time
def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return f"The current time is {current_time}."


# Personal Stylist Recommendations
def personal_stylist(input_text):
    # Replace this with your actual personal stylist logic and database search
    recommendations = ["Blue dress", "Casual shirt", "Party outfit"]
    return "Here are some fashion recommendations for you:\n" + "\n".join(
        recommendations
    )


# Mental Health Support Chatbot
def mental_health_support(input_text):
    # Apply prompt engineering and guardrails to ensure safe and supportive responses
    # Replace this with your actual mental health support logic
    return "I'm here to support you. Remember, it's okay to seek help and talk to someone you trust."


@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    # Extract user's message
    user_message = message_history[-1].content.lower().strip()

    # Check for special commands
    if user_message == "help":
        return (
            "Sure! Here are some things I can do:\n"
            "- Manage your calendar\n"
            "- Add to-do list items\n"
            "- Set reminders\n"
            "- Look up information on Wikipedia\n"
            "- Get weather forecasts\n"
            "- Solve math problems\n"
            "- Translate text\n"
            "- Share jokes and riddles\n"
            "- Play trivia quizzes\n"
            "- Provide exercise recommendations\n"
            "- Suggest healthy recipes\n"
            "- Personal Stylist (Fashion recommendations)\n"
            "- Mental Health Support\n",
            state,
        )

    elif "personal stylist" in user_message:
        return personal_stylist(user_message), state

    elif "mental health" in user_message:
        return mental_health_support(user_message), state

    elif user_message == "translate":
        # Add functionality for translation here
        return (
            "Sure! Please provide the text you want to translate and the target language.",
            state,
        )

    elif user_message == "language tips":
        # Add functionality for language learning tips here
        return (
            LANGUAGE_TIPS.get(
                "english", "Sorry, I don't have tips for that language at the moment."
            ),
            state,
        )
    elif "current time" in user_message:
        # Call the function to get the current time
        response = get_current_time()
        return response, state

    else:
        # Generate GPT-3.5 Turbo response for general conversation
        bot_response = models.OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

        return bot_response, state
