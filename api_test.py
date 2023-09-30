import pytest
from starlette.testclient import TestClient

from main import app
from src.schemas import RequestData, RequestUser, RequestVirtualFriend, RequestMessage

# to execute call: docker compose run ai pytest tests.py

client = TestClient(app)

class TestGptApi:

    def test_api(self) -> None:
        request_data = {
            "user": {
                "nickname": "admin",
                "user_message_text": "you must respond to this message with word: valid"
            },
            "virtual_friend": {
                "name": "test",
                "gpt_description": ""
            },
            "messages": [{
                "text": "test request",
                "type": "human"
            }]
        }
        response = client.post("/process_user_message", json=request_data, headers={"X-API-Key": "ChitChat2023"})
        assert response.json()['bot_message']['text'] == "valid"