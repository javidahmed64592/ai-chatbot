import json
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from chatbot.chatbot import Chatbot
from helpers.general_helpers import system_msg

PERSONALITIES_FOLDER = Path("./personalities")
CHAT_HISTORY_FOLDER = Path("./history")

app = Flask(__name__)
chatbot = Chatbot(
    personality_config_filepath=PERSONALITIES_FOLDER / "piper.json",
    chat_history_directory=CHAT_HISTORY_FOLDER,
)


@app.route("/api/chat/load", methods=["GET"])
def load_chat():
    if request.method == "GET":
        reply = chatbot.load_chat()
        print(reply)
        return jsonify(success=True)


@app.route("/api/chat/end", methods=["GET"])
def end_chat():
    if request.method == "GET":
        reply = chatbot.end_chat()
        print(reply)
        return jsonify(success=True)


@app.route("/api/messages", methods=["GET"])
def messages():
    if request.method == "GET":
        return jsonify({"messages": chatbot._messages})


@app.route("/api/chat/send", methods=["POST"])
def send_message():
    if request.method == "POST":
        data = json.loads(request.data)
        message = data["message"]
        reply = chatbot.send_message(message)
        print(reply)
        return jsonify({"reply": reply})


@app.route("/api/chat/reply", methods=["GET"])
def get_reply():
    if request.method == "GET":
        reply = chatbot.generate_response()
        print(reply)
        return jsonify({"reply": reply})


@app.route("/api/chatbot/personality", methods=["GET", "POST"])
def personality():
    if request.method == "GET":
        return jsonify({"personality_config": chatbot.personality_config})
    elif request.method == "POST":
        data = json.loads(request.data)
        chatbot.personality_config = data


if __name__ == "__main__":
    print(system_msg("Loading environment variables..."))
    load_dotenv()

    try:
        print(system_msg("Running app..."))
        app.run(host="0.0.0.0")
    except (KeyboardInterrupt, SystemExit):
        print(system_msg("Shutting down program..."))
