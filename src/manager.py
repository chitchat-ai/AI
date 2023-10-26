from functools import cached_property

from langchain.chat_models import ChatOpenAI
from langchain.memory import CombinedMemory
from pydantic import BaseModel
from langchain.prompts import PromptTemplate

from .chroma import MemoryChroma
from .classes import (
    CustomCallbackHandler,
    CustomConversationChain, ChromaVectorStoreRetriever, ChromaLongMemory,
    ChromaShortMemory,
)
from .schemas import RequestData, ResponseMessage

DESCRIPTION_TEMPLATE = '{description}\n\n'

LONG_MEMORY_TEMPLATE = "Relevant memorized messages:\n\n{long_memory}\n\n"

SHORT_MEMORY_TEMPLATE = 'Current conversation:\n\n{short_memory}\n{human_prefix}: {input}\n{ai_prefix}: '

SYSTEM_TEMPLATE = DESCRIPTION_TEMPLATE + LONG_MEMORY_TEMPLATE + SHORT_MEMORY_TEMPLATE


class AIManager(BaseModel):
    openai_api_key: str
    request_data: RequestData

    def get_bot_message(self) -> ResponseMessage:
        handler = CustomCallbackHandler()
        llm = ChatOpenAI(temperature=0.8, openai_api_key=self.openai_api_key)

        conversation = CustomConversationChain(
            llm=llm,
            memory=self.memory,
            verbose=True,
            prompt=self.prompt,
        )
        message_from_ai = conversation.run(
            description=self.description,
            input=self.user_message_text,
            callbacks=[handler],
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
    def chroma(self):
        return MemoryChroma(chat_id=self.request_data.chat.id)

    @cached_property
    def long_memory(self) -> ChromaLongMemory:
        retriever = ChromaVectorStoreRetriever(
            vectorstore=self.chroma,
            search_kwargs=dict(k=3, filter=self.chroma.exclude_last_msg_blocks_filter)
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
            template=SYSTEM_TEMPLATE,
        )
        return prompt.partial(human_prefix=self.human_prefix, ai_prefix=self.ai_prefix)


    class Config:
        keep_untouched = (cached_property,)
        arbitrary_types_allowed = True
