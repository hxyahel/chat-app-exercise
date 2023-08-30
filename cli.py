import json

from api_client import APIClient
from app.schemas import UserCreate, NewConversation, MessageBase, UserUpdate


class Chat:
    def __init__(self, user_id: str, base_url: str):
        self.user = UserCreate(user_id=user_id)
        self.api_client = APIClient(base_url=base_url)
        self.conversation = NewConversation(user_id=user_id, text="")
        self.command_handlers = {
            'exit': self._handle_exit,
            'get conversations': self._handle_query_conversations,
            'get users': self._handle_query_users
        }

    def process(self):
        self._create_user()
        try:
            while True:
                user_input = input("You: ")
                self.conversation.text += f"User {self.user.user_id}: {user_input}\n"

                if user_input.lower() in self.command_handlers:
                    self.command_handlers[user_input.lower()]()
                else:
                    self._handle_default_input(user_input)
        except KeyboardInterrupt:
            pass
        finally:
            self.api_client.create_conversation(conversation=self.conversation)
            self.api_client.update_user_words(user_id=self.user.user_id, words=UserUpdate(words=self.conversation.text))

    def _create_user(self):
        self.api_client.create_user(user=self.user)

    def _handle_default_input(self, user_input: str):
        completion = self.api_client.send_message(MessageBase(prompt=user_input))
        self.conversation.text += f"GPT: {completion}\n"
        print(f"GPT: {completion}")

    def _handle_query_conversations(self):
        self._handle_query(category='conversations', user_query="Enter a user to search for: ")

    def _handle_query_users(self):
        self._handle_query(category='users', user_query="Enter a keyword to search for: ")

    @staticmethod
    def _handle_exit():
        print("Goodbye!")
        raise SystemExit

    def _handle_query(self, category: str, user_query: str):
        user_query_input = input(user_query)
        retrieved_data = self.api_client.get_data_requested(category=category, query=user_query_input)
        self.conversation.text += f"{user_query}: {user_query_input}\n {category} found: {retrieved_data}\n"
        print(f"{category}: {json.dumps(retrieved_data, indent=4)}")


def main():
    print("Chat started.\n Type 'exit' to end the conversation. "
          "\n Type 'get conversations' to get conversations by specific use."
          "\n Type 'get users' to search for users that used a keyword in the database."
          "\n\n Lets start by telling us your name.")
    user_name = input("You: ")
    print('Thank you, lets start chatting!')

    chat = Chat(user_id=user_name, base_url="http://localhost:8000")
    chat.process()


if __name__ == "__main__":
    main()
