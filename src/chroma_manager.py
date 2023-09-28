from functools import cached_property

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import chromadb


openai_api_key = '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'

class ChatManager:

    def __init__(self, openai_api_key:str, client_id:str, character_name:str) -> None:
        self.openai_api_key = openai_api_key
        self.client_id = client_id
        self.character_name = character_name
        self.embedding_function = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.db = Chroma(
            collection_name=client_id,
            embedding_function=self.embedding_function,
            persist_directory=character_name
        )

    def add_message(self, message) -> None:
        id = self.length
        self.db.add_texts([message], id=[id])


    def get_last_messages(self, number_of_messages:int = 1) -> list[{"chat":str}]:
        if number_of_messages > self.length:
            print("ERROR: number_of_messages exceeds length of database. Returning all messages instead")
            number_of_messages = self.length

        result = []

        for i in range(number_of_messages):
            result.append({"chat": self.db.get(str((-1)*(i+1)))["documents"][0]})

        return result


    def search_relevant(self, query:str, number_of_messages:int = 1) -> list[{"chat":str}]:
        if self.length == 0:
            return []
        if number_of_messages > self.length:
            print("ERROR: number_of_messages exceeds length of database. Returning all messages instead")
            number_of_messages = self.length

        search_result = self.db.similarity_search(
            query,
            k=number_of_messages
        )

        result = []

        for document in search_result:
            result.append({"chat":document.page_content})

        return result


    def get_memory(self, query:str, short_term_memory_depth:int=1, long_term_memory_depth:int=1) -> list[{"chat": str}]:
        return self.get_last_messages(short_term_memory_depth) + self.search_relevant(query, long_term_memory_depth)


    @cached_property
    def length(self) -> int:
        return len(self.db.get()["ids"])