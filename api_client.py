import httpx

from app.schemas import MessageBase, NewConversation, UserUpdate, UserCreate


class APIClient:
    def __init__(self, base_url: str):
        self.client = httpx.Client(base_url=base_url)

    def create_user(self, user: UserCreate):
        url = f"/users"
        payload = {
            "user_id": user.user_id
        }
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_data_requested(self, category: str, query: str):
        url = f"/{category}/{query}"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

    def send_message(self, message: MessageBase):
        url = f"/chat"
        payload = {
            "prompt": message.prompt
        }
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def create_conversation(self, conversation: NewConversation):
        url = f"/conversation/"
        payload = {
            "user_id": conversation.user_id,
            "text": conversation.text
        }
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()

    def update_user_words(self, user_id: str, words: UserUpdate):
        url = f"/users/{user_id}"
        payload = {
            "words": words.words
        }
        response = self.client.put(url, json=payload)
        response.raise_for_status()
        return response.json()
