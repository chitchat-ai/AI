import pytest
from starlette.testclient import TestClient

from main import app
from src.schemas import RequestData, RequestUser, RequestVirtualFriend, RequestMessage

# to execute call: docker compose run ai pytest tests.py

client = TestClient(app)

class TestGptApi:

    def test_code_execution(self) -> None:
        question = "you must respond to this message with word HEHEHEHA"
        user = RequestUser(
            nickname="admin",
            user_message_text=""
        )
        virtual_friend = RequestVirtualFriend(
            name="test",
            gpt_description=""
        )
        message = RequestMessage(
            text=question,
            type=""
        )
        request_data = RequestData(
            user=user,
            virtual_friend=virtual_friend,
            messages=[message]
        )
        data = {}
        response = client.post("/process_user_message", json=data, headers={"X-API-Key": "ChitChat2023"})
        print(response.json())
        assert response.status_code == 200


# def test_client_execution(self) -> None:
#     pass