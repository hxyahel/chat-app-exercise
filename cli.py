import json

from api_client import APIClient
from app.schemas import UserCreate, ConversationCreate, MessageBase, UserUpdate, UserResponse
from cli_utils import format_conversations


class Chat:
    def __init__(self, user_id: str, base_url: str, block_toxic_prompts: bool = False):
        self.user = UserCreate(user_id=user_id)
        self.api_client = APIClient(base_url=base_url)
        self.conversation = ConversationCreate(user_id=user_id, text="")
        self.block_toxic_prompts = block_toxic_prompts

    def process(self):
        self._create_user()
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
                completion = self.api_client.send_message(MessageBase(prompt=user_input),
                                                          block_toxic_prompts=self.block_toxic_prompts)
                self.conversation.text += f"GPT: {completion}\n"
                print(f"GPT: {completion}")

        self.api_client.create_conversation(conversation=self.conversation)
        self.api_client.update_user_words(user_id=self.user.user_id, words=UserUpdate(words=self.conversation.text))

    def _handle_query(self, category: str, user_query: str):
        value = input(user_query)
        retrieved_data = self.api_client.get_data_requested(category=category, query=value)
        self.conversation.text += f"{user_query}: {value}\n {category} found: {retrieved_data}\n"
        if category == 'conversations':
            retrieved_data = json.dumps(format_conversations(retrieved_data), indent=4)

        print(f"{category}: {retrieved_data}")

    def _create_user(self):
        self.api_client.create_user(user=self.user)


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
