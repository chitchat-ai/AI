from functools import cached_property

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


openai_api_key = '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'

class ChatDB:

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


    def get_last_messages(self, number_of_messages:int = 1) -> list[str]:
        if number_of_messages > self.length:
            print("ERROR: number_of_messages exceeds length of database. Returning all messages instead")
            number_of_messages = self.length

        result = []

        for i in range(number_of_messages):
            result.append(self.db.get(str((-1)*(i+1))).documents[0])

        return result


    def search_relevant(self, query:str, number_of_messages:int = 1) -> {int:str}:
        if number_of_messages > self.length:
            print("ERROR: number_of_messages exceeds length of database. Returning all messages instead")
            number_of_messages = self.length

        search_result = self.db.similarity_search_with_score(
            query,
            k=number_of_messages
        )

        result = [i[0].page_content for i in search_result]

        return result



    @cached_property
    def length(self) -> int:
        return len(self.db.get()["ids"])



my_chat = ChatDB(openai_api_key, "001", "user")

my_chat.add_message("cat")
my_chat.add_message("car")

print("db contains 2 words: cat and car")
print(f"searches word similar by meaning to 'dog', result is {my_chat.search_relevant('dog')[0]}")  # expects words cat
print(f"searches word similar by meaning to 'machine', result is {my_chat.search_relevant('machine')[0]}")  # expects words car
