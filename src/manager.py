from functools import cached_property
from typing import Any

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import CombinedMemory
from pydantic import BaseModel

from .admin.models import Config
from .classes import (
    CustomCallbackHandler,
    CustomConversationChain,
    ShortChatMessageHistory,
    ShortConversationBufferMemory,
)
from .schemas import RequestData, ResponseMessage

# DESCRIPTION_TEMPLATE = '{description}\n\n'

# LONG_MEMORY_TEMPLATE = "Relevant memorized messages:\n\n{long_memory}\n\n"

# SHORT_MEMORY_TEMPLATE = 'Current conversation:\n\n{short_memory}\n{human_prefix}: {input}\n{ai_prefix}: '

# SYSTEM_TEMPLATE = DESCRIPTION_TEMPLATE + SHORT_MEMORY_TEMPLATE


class AIManager(BaseModel):
    openai_api_key: str
    request_data: RequestData
    db: Any
    config: Config

    async def get_bot_message(self) -> ResponseMessage:
        handler = CustomCallbackHandler(history=self.short_memory.chat_memory, db=self.db)
        llm = ChatOpenAI(temperature=self.config.temperature, openai_api_key=self.openai_api_key)

        conversation = CustomConversationChain(
            llm=llm,
            memory=self.memory,
            verbose=True,
            prompt=self.prompt,
        )
        await conversation.arun(
            description=self.description,
            input=self.user_message_text,
            callbacks=[handler],
        )
        return self.short_memory.chat_memory.response_message


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

    # @cached_property
    # def long_memory(self) -> LongVectorStoreRetrieverMemory:
    #     vector_store = CustomLanceDB(
    #         chat_id=self.chat_id, embeddings=OpenAIEmbeddings(openai_api_key=self.openai_api_key)
    #     )
    #     retriever = vector_store.as_retriever(search_kwargs=dict(k=2))
    #
    #     return LongVectorStoreRetrieverMemory(
    #         retriever=retriever,
    #         human_prefix=self.human_prefix,
    #         ai_prefix=self.ai_prefix,
    #     )

    @cached_property
    def short_memory(self) -> ShortConversationBufferMemory:
        return ShortConversationBufferMemory(
            chat_memory=ShortChatMessageHistory(request_messages=self.request_data.messages[:-1]),
            human_prefix=self.human_prefix,
            ai_prefix=self.ai_prefix,
        )

    @cached_property
    def memory(self) -> CombinedMemory:
        return CombinedMemory(memories=[self.short_memory])


    @cached_property
    def prompt(self) -> PromptTemplate:
        prompt = PromptTemplate(
            input_variables=[
                'description',
                # 'long_memory',
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
