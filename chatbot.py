import json
import random

with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def get_response(message):

    message = message.lower().strip()

    for intent in data["intents"]:

        for pattern in intent["patterns"]:

            if pattern.lower() in message:

                return random.choice(intent["responses"])

    return "Sorry! I couldn't understand your question. Please try asking something else."