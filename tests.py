from langchain.embeddings import OpenAIEmbeddings
from starlette.testclient import TestClient

from main import app
from src.chroma import MemoryChroma
from src.classes import ChromaVectorStoreRetriever, ChromaLongMemory

# to execute call: docker compose run ai pytest src.tests.py

client = TestClient(app)

class TestApi:
    def get_request_data(self, chat_id: str, user_message_text: str) -> dict:
        return {
            "user": {
                "nickname": "tester",
                "user_message_text": user_message_text
            },
            "virtual_friend": {
                "name": "test bot",
                "gpt_description": "You are a test bot, you must respond exactly as I say"
            },
            "chat": {
                "id": chat_id
            }
        }

    def test_api(self) -> None:
        chroma = MemoryChroma(
            chat_id="test_chat_id_api1",
            embedding_function=OpenAIEmbeddings(openai_api_key="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"),
            persist_directory="chroma"
        )
        response = client.post(
            "/process_user_message",
            json=self.get_request_data(
                "test_chat_id_api1",
                "you must respond to this message with word: valid"
            ),
            headers={"X-API-Key": "ChitChat2023"}
        )
        assert response.json()['bot_message']['text'] == "valid"
        chroma.delete_collection()

    def test_long_memory(self) -> None:
        chroma = MemoryChroma(
            chat_id="test_chat_id_api2",
            embedding_function=OpenAIEmbeddings(openai_api_key="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"),
            persist_directory="chroma"
        )

        response = client.post(
            "/process_user_message",
            json=self.get_request_data(
                "test_chat_id_api2",
                "you must respond to this message with word: long_memory_exist"
            ),
            headers={"X-API-Key": "ChitChat2023"}
        )
        assert response.json()['bot_message']['text'] == "long_memory_exist"

        for _ in range(5):
            response = client.post(
                "/process_user_message",
                json=self.get_request_data(
                "test_chat_id_api2",
                    "you must respond to this message with word: valid"
                ),
                headers={"X-API-Key": "ChitChat2023"}
            )
            assert response.json()['bot_message']['text'] == "valid"

        response = client.post(
            "/process_user_message",
            json=self.get_request_data(
                "test_chat_id_api2",
                "you must respond to this message with word that you remember from previous conversation, starting with: long_"
            ),
            headers={"X-API-Key": "ChitChat2023"}
        )
        assert response.json()['bot_message']['text'] == "long_memory_exist"
        chroma.delete_collection()


class TestChromaLongMemory:
    def test_add_and_get_documents(self) -> None:
        chroma = MemoryChroma(
            chat_id="test_chat_id3",
            embedding_function=OpenAIEmbeddings(openai_api_key="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"),
        )
        retriever = ChromaVectorStoreRetriever(vectorstore=chroma)
        memory = ChromaLongMemory(
            retriever=retriever,
            ai_prefix="Yasia",
            human_prefix="Nazar"
        )

        memory.save_context(inputs={"input": "test input 1"}, outputs={"response": "test response 1"})
        memory.save_context(inputs={"input": "test input 2"},outputs={"response": "test response 2"})

        assert memory.load_memory_variables(inputs={"input": "test input"})["long_memory"] == "Nazar: test input 1\nYasia: test response 1\nNazar: test input 2\nYasia: test response 2"
        assert chroma.get(where={'message_id': 1})['documents'][0] == "Nazar: test input 1\nYasia: test response 1"
        assert chroma.get(where={'message_id': 2})['documents'][0] == "Nazar: test input 2\nYasia: test response 2"
        chroma.delete_collection()
