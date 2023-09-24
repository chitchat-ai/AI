import sys
 
# adding Folder_2 to the system path
sys.path.insert(0, '..')

import pytest
from starlette.testclient import TestClient

from main import app
from src.schemas import RequestData, RequestUser, RequestVirtualFriend, RequestMessage

# to execute call: docker compose run ai pytest tests.py



# both method and file name must fulfill regex "test_*" or "*_test"
#  to be executed by pytest automatically

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