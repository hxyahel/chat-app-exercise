import json

import httpx
import requests

from app.schemas import UserCreate, ConversationCreate, MessageBase, UserUpdate
from cli_utils import format_conversations


class Chat:
    def __init__(self, user_id: str):
        self.user = UserCreate(user_id=user_id)
        self._create_user()
        self.conversation = ConversationCreate(user_id=user_id, text="")

    def process(self):
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            self.conversation.text += f"User {self.user.user_id}: {user_input}\n"

            if user_input.lower() == 'get conversations':
                self._handle_query(category='conversations', user_query="Enter a user to search for: ")

            elif user_input.lower() == 'get users':
                self._handle_query(category='users', user_query="Enter a keyword to search for: ")

            else:
                completion = self._send_message(MessageBase(prompt=user_input))
                self.conversation.text += f"GPT: {completion}\n"
                print(f"GPT: {completion}")

        self._create_conversation()
        _update_user_words(UserUpdate(user_id=self.user.user_id, text=self.conversation.text))

    def _handle_query(self, category: str, user_query: str):
        value = input(user_query)
        retrieved_data = self._get_data_requested(category=category, query=value)
        self.conversation.text += f"{user_query}: {value}\n {category} found: {retrieved_data}\n"
        if category == 'conversations':
            retrieved_data = json.dumps(format_conversations(retrieved_data), indent=4)

        print(f"{category}: {retrieved_data}")

    def _create_user(self):
        url = "http://localhost:8000/users"
        payload = {
            "user_id": self.user.user_id
        }
        response = requests.post(url, json=payload)
        return response.content

    @staticmethod
    def _get_data_requested(category: str, query: str):
        url = f"http://localhost:8000/{category}/{query}"

        with httpx.Client() as client:
            response = client.get(url)
            return response.content

    @staticmethod
    def _send_message(message: MessageBase):
        url = "http://localhost:8000/chat"
        payload = {
            "prompt": message.prompt
        }
        response = requests.get(url, json=payload)
        return response.content

    def _create_conversation(self):
        url = "http://localhost:8000/conversation/"
        payload = {
            "user_id": self.conversation.user_id,
            "text": self.conversation.text
        }
        response = requests.post(url, json=payload)
        return response.content


def _update_user_words(user: UserUpdate):
    url = "http://localhost:8000/users_words"
    payload = {
        "user_id": user.user_id,
        "text": user.text
    }
    response = requests.put(url, json=payload)
    return response.content


def main():
    print("Chat started.\n Type 'exit' to end the conversation. "
          "\n Type 'get conversations' to get conversations by specific use."
          "\n Type 'get users' to search for users that used a keyword in the database."
          "\n\n Lets start by telling us your name.")
    user_name = input("You: ")
    print('Thank you, lets start chatting!')
    chat = Chat(user_name)
    chat.process()


if __name__ == "__main__":
    main()
