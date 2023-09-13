import pytest
from starlette.testclient import TestClient

from main import app
from src.schemas import RequestData, RequestUser, RequestVirtualFriend, RequestMessage

# to execute call: docker compose run ai pytest tests.py

client = TestClient(app)

class TestGptApi:

    def test_code_execution(self) -> None:
        request_data = {
            "user": {
                "nickname": "admin",
                "user_message_text": ""
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
        print(response.json())
        assert response.status_code == 200