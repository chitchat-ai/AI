from typing import Any

from langchain import ConversationChain
from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory import ConversationBufferMemory, VectorStoreRetrieverMemory
from langchain.schema import (
    BaseChatMessageHistory,
    BaseMessage,
    LLMResult,
    messages_from_dict,
)
from pydantic import BaseModel, Field, root_validator
from sqlalchemy import asc

from chats.enums import MessageType
from chats.models import Message
from chats.schemas import MessageCreate
from database.local_session import session


class LongVectorStoreRetrieverMemory(VectorStoreRetrieverMemory):
    memory_key = 'long_memory'
    input_key = 'input'

    ai_prefix: str
    human_prefix: str

    def save_context(self, inputs: dict[str, Any], outputs: dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        inputs = {self.human_prefix: inputs[self.input_key]}
        outputs = {self.ai_prefix: outputs['response']}
        documents = self._form_documents(inputs, outputs)
        self.retriever.add_documents(documents)


class ShortChatMessageHistory(BaseModel, BaseChatMessageHistory):
    chat_id: int
    generation_info: dict | None = None
    new_bot_message: Message | None = None

    @property
    def messages(self) -> list[BaseMessage]:
        message_list = (
            session.query(Message).filter_by(chat_id=self.chat_id).order_by(asc(Message.created)).limit(6).all()
        )
        message_dict_list = []

        for message in message_list:
            message_dict = {
                'type': message.type,
                'data': {
                    'content': message.text,
                },
            }
            if message.type == MessageType.CHAT:
                message_dict['data']['role'] = 'System message'

            message_dict_list.append(message_dict)

        return messages_from_dict(message_dict_list)

    def add_message(self, message: BaseMessage) -> None:
        message = MessageCreate(
            chat_id=self.chat_id,
            text=message.content,
            type=message.type,
            openai_response=self.generation_info,
        )

        message = Message.from_orm(message)
        message.create()

        self.new_bot_message = message

    def clear(self) -> None:
        msg = 'is not needed'
        raise NotImplementedError(msg)


class ShortConversationBufferMemory(ConversationBufferMemory):
    memory_key = 'short_memory'
    input_key = 'input'
    chat_memory: ShortChatMessageHistory = Field(default_factory=ShortChatMessageHistory)


class CustomConversationChain(ConversationChain):
    # def create_outputs(self, response: LLMResult):
    #     """Create outputs from response."""
    #     print(response, response.generations)
    #     return [
    #         # Get the text of the top generated string.
    #         {self.output_key: generation[0].text}
    #         for generation in response.generations
    #     ]

    @root_validator()
    def validate_prompt_input_variables(cls, values: dict) -> dict:
        """Validate that prompt input variables are consistent."""
        memory_keys = values['memory'].memory_variables
        input_key = values['input_key']
        if input_key in memory_keys:
            msg = (
                f"The input key {input_key} was also found in the memory keys "
                f"({memory_keys}) - please provide keys that don't overlap."
            )
            raise ValueError(msg)

        prompt_variables = values['prompt'].input_variables
        expected_keys = [*memory_keys, input_key, 'description']
        if set(expected_keys) != set(prompt_variables):
            msg = (
                f'Got unexpected prompt input variables. The prompt expects {prompt_variables}, '
                f'but got {memory_keys} as inputs from memory, and {input_key} as the normal input key.'
            )
            raise ValueError(msg)

        return values


class CustomCallbackHandler(BaseModel, BaseCallbackHandler):
    history: ShortChatMessageHistory

    def on_chat_model_start(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        pass

    def on_llm_end(self, response: LLMResult, **_: Any) -> None:
        """Run when LLM ends running."""
        self.history.generation_info = response.llm_output
