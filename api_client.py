import httpx

from app.schemas import MessageBase, ConversationCreate, UserUpdate, UserCreate


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client()

    def create_user(self, user: UserCreate):
        url = f"{self.base_url}/users"
        payload = {
            "user_id": user.user_id
        }
        response = self.client.post(url, json=payload)
        return response.json()

    def get_data_requested(self, category: str, query: str):
        url = f"{self.base_url}/{category}/{query}"
        response = self.client.get(url)
        return response.json()

    def send_message(self, message: MessageBase):
        url = f"{self.base_url}/chat"
        payload = {
            "prompt": message.prompt
        }
        response = self.client.post(url, json=payload)
        return response.json()

    def create_conversation(self, conversation: ConversationCreate):
        url = f"{self.base_url}/conversation/"
        payload = {
            "user_id": conversation.user_id,
            "text": conversation.text
        }
        response = self.client.post(url, json=payload)
        return response.json()

    def close(self):
        self.client.close()

    def update_user_words(self, user_id: str, words: UserUpdate):
        url = f"{self.base_url}/users/{user_id}"
        payload = {
            "words": words.words
        }
        response = self.client.put(url, json=payload)
        return response.json()
