from typing import List

from app.database.models import Conversation


def format_conversations(conversations: List[Conversation]):
    formatted_conversations = []
    for conv in conversations:
        try:
            formatted_conv = {
                'user_id': conv['user_id'],
                'text': conv['text'].replace('\n', '<br>'),
                'created_at': conv['created_at'],
                'id': conv['id']
            }
            formatted_conversations.append(formatted_conv)
        except KeyError as e:
            pass
            # print(f"Error processing conversation: {e}")
    return formatted_conversations
