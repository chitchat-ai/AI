from functools import cached_property
from typing import Any

import chromadb
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import CombinedMemory
from pydantic import BaseModel
from langchain.prompts import PromptTemplate

from settings import settings
from .chroma import MemoryChroma
from .admin.models import Config
from .classes import (
    CustomCallbackHandler,
    CustomConversationChain, ChromaVectorStoreRetriever, ChromaLongMemory,
    ChromaShortMemory,
)
from .schemas import RequestData, ResponseMessage


class AIManager(BaseModel):
    openai_api_key: str
    request_data: RequestData
    db: Any
    config: Config

    async def get_bot_message(self) -> ResponseMessage:

        conversation = CustomConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True,
            prompt=self.prompt,
        )

        message_from_ai = await conversation.arun(
            description=self.description,
            input=self.user_message_text,
            callbacks=[self.handler],
        )

        return ResponseMessage(text=message_from_ai)

    @cached_property
    def human_prefix(self) -> str:
        return self.request_data.user.nickname

    @cached_property
    def ai_prefix(self) -> str:
        return self.request_data.virtual_friend.name

    @cached_property
    def description(self) -> str:
        return self.request_data.virtual_friend.gpt_description

    @cached_property
    def user_message_text(self) -> str:
        return self.request_data.user.user_message_text

    @cached_property
    def long_memory(self) -> ChromaLongMemory:
        retriever = ChromaVectorStoreRetriever(
            vectorstore=self.chroma,
            search_kwargs=dict(k=self.config.long_memory_length, filter=self.chroma.exclude_last_msg_blocks_filter)
        )

        return ChromaLongMemory(
            retriever=retriever,
            ai_prefix=self.ai_prefix,
            human_prefix=self.human_prefix,
        )

    @cached_property
    def short_memory(self) -> ChromaShortMemory:
        return ChromaShortMemory(
            vectorstore=self.chroma,
            ai_prefix=self.ai_prefix,
            human_prefix=self.human_prefix
        )

    @cached_property
    def memory(self) -> CombinedMemory:
        return CombinedMemory(memories=[self.short_memory, self.long_memory])

    @cached_property
    def handler(self) -> CustomCallbackHandler:
        return CustomCallbackHandler(db=self.db)

    @cached_property
    def llm(self) -> ChatOpenAI:
        return ChatOpenAI(temperature=self.config.temperature, openai_api_key=self.openai_api_key)

    @cached_property
    def embedding_function(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

    @cached_property
    def chroma(self) -> MemoryChroma:
        return MemoryChroma(
            chat_id=self.request_data.chat.id,
            last_message_block_count=self.config.short_memory_length,
            client=self.chroma_client,
            embedding_function=self.embedding_function
        )

    @cached_property
    def chroma_client(self) -> chromadb.HttpClient:
        return chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)

    @cached_property
    def prompt(self) -> PromptTemplate:
        prompt = PromptTemplate(
            input_variables=[
                'description',
                'long_memory',
                'short_memory',
                'input',
                'human_prefix',
                'ai_prefix',
            ],
            template=self.config.prompt_template,
        )
        return prompt.partial(human_prefix=self.human_prefix, ai_prefix=self.ai_prefix)


    class Config:
        keep_untouched = (cached_property,)
        arbitrary_types_allowed = True
