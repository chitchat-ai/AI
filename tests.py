import pytest
from src.schemas import RequestData, RequestUser, RequestVirtualFriend, RequestMessage
import main

# to execute call: docker compose run ai pytest tests.py


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
        respond = main.process_user_message(request_data).bot_message.text
        print(respond)
        assert respond == "HEHEHEHA"


def test_client_execution(self) -> None:
    pass