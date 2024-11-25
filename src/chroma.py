from typing import Iterable, Any

import chromadb
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

class MemoryChroma(Chroma):

    COLLECTION_NAME_PREFIX: str = 'memory'

    last_message_block_count: int

    def __init__(
        self,
        chat_id: str,
        last_message_block_count: int,
        embedding_function: OpenAIEmbeddings,
        client: chromadb.HttpClient
    ) -> None:
        collection_name = f"{self.COLLECTION_NAME_PREFIX}_{chat_id}"

        super().__init__(
            collection_name=collection_name,
            embedding_function=embedding_function,
            client=client,
        )

        if last_message_block_count > self.length:
            self.last_message_block_count = self.length
        else:
            self.last_message_block_count = last_message_block_count

    @property
    def length(self) -> int:
        return self._collection.count()

    def add_texts(self, texts: Iterable[str], *_, **__) -> list[str]:
        message_id = self.length + 1
        return super().add_texts(texts, metadatas=[{'message_id': message_id}])

    def get_last_message_blocks(self) -> list[str]:
        result = []

        for i in reversed(range(self.last_message_block_count)):
            msg_block = self.get(where={"message_id": self.length - i})["documents"][0]
            result.append(msg_block)

        return result

    @property
    def exclude_last_msg_blocks_filter(self):
        if not self.last_message_block_count:
            return None

        return {'message_id': {'$nin': [self.length - i for i in range(self.last_message_block_count)]}}



