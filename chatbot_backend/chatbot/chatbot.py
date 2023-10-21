import os

import openai
from openai.error import RateLimitError

from helpers.general_helpers import read_txt_file, write_to_txt_file


class Chatbot:
    def __init__(self, personality_config, chat_history_directory):
        self.name = personality_config["name"]
        self.personality = personality_config["personality"]
        self.rules = personality_config["rules"]

        self.api_key = os.getenv("API_KEY")
        openai.api_key = self.api_key

        self.model = personality_config["model"]
        self.temperature = personality_config["temperature"]
        self.max_tokens = personality_config["max_tokens"]
        self.n = personality_config["n"]
        self.stop = personality_config["stop"]
        self.max_messages = personality_config["max_messages"]

        self.chat_history_directory = chat_history_directory
        self._messages = []
        self._msg_system(
            f"Your name is {self.name}. {self.personality}. You follow these rules: \n{Chatbot.create_numbered_list(self.rules)}"
        )
        self.num_messages_at_start = 1

    @staticmethod
    def create_numbered_list(lst):
        numbered_list = [f"{i}) {item}" for i, item in enumerate(lst, start=1)]
        numbered_string = "\n".join(numbered_list)
        return numbered_string

    def _add_msg(self, role, msg):
        if len(self._messages) >= self.max_messages:
            del self._messages[self.num_messages_at_start : self.num_messages_at_start + 2]

        self._messages.append({"role": role, "content": msg})

    def _msg_system(self, msg):
        self._add_msg("system", msg)

    def _msg_assistant(self, msg):
        self._add_msg("assistant", msg)

    def _msg_user(self, msg):
        self._add_msg("user", msg)

    def _generate_response(self):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self._messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                n=self.n,
                stop=self.stop,
            )

            reply = response.choices[0]["message"]["content"]
            self._msg_assistant(reply)

        except RateLimitError:
            reply = "Too many requests! Please try again shortly..."
            del self._messages[-1]
        except Exception as err:
            reply = f"Something has gone wrong: {err}"
            del self._messages[-1]
        finally:
            return reply

    @property
    def chat_history(self):
        return self._messages

    @property
    def chat_history_filename(self):
        return self.chat_history_directory / f"{self.name}.txt"

    def load_chat(self):
        if os.path.exists(self.chat_history_filename):
            self._messages += eval(read_txt_file(self.chat_history_filename))[1:]
        else:
            raise FileNotFoundError("Chat history does not exist.")

        self.num_messages_at_start = len(self._messages)

    def save_chat(self):
        summary = self._generate_response()
        del self._messages[self.num_messages_at_start :]
        self._msg_system(summary)
        write_to_txt_file(self.chat_history_filename, str(self._messages))

    def start_chat(self, load_chat=False):
        response = ""

        if load_chat:
            try:
                self.load_chat()
            except FileNotFoundError:
                response += "Error loading chat history. Starting from scratch... "

        self._msg_user(f"Hi, {self.name}!")

        response += self._generate_response()
        return response

    def end_chat(self, save_chat=False):
        self._msg_user(f"Goodbye, {self.name}!")
        response = self._generate_response()

        num_messages = len(self._messages) - self.num_messages_at_start

        if save_chat and num_messages > 4:
            self._msg_user(f"Can you summarise the last {num_messages} messages? Keep your response concise.")
            self.save_chat()

        return response

    def chat(self, msg):
        if len(msg) == 0:
            return "Can't send empty message!"

        self._msg_user(msg)
        return self._generate_response()
