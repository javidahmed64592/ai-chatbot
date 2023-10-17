import json
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from chatbot.chatbot import Chatbot
from helpers.general_helpers import load_config

PERSONALITIES_FOLDER = Path("./personalities")
CHAT_HISTORY_FOLDER = Path("./history")

app = Flask(__name__)
chatbot = Chatbot(load_config(PERSONALITIES_FOLDER / "piper.json"), chat_history_directory=CHAT_HISTORY_FOLDER)


@app.route("/api/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        return jsonify({"messages": chatbot.chat_history})
    elif request.method == "POST":
        data = json.loads(request.data)
        message = data["message"]
        reply = chatbot.chat(message)
        return jsonify({"reply": reply})


if __name__ == "__main__":
    load_dotenv()

    try:
        chatbot.load_chat()
    except FileNotFoundError:
        print("Chat history not found!")

    try:
        app.run()
    except (KeyboardInterrupt, SystemExit):
        chatbot.save_chat()
