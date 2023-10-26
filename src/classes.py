from typing import Any

from langchain.chains import ConversationChain
from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory import VectorStoreRetrieverMemory
from langchain.schema import BaseMemory
from langchain.vectorstores.base import VectorStoreRetriever
from pydantic import Field, root_validator

from src.chroma import MemoryChroma


class ChromaVectorStoreRetriever(VectorStoreRetriever):
    vectorstore: MemoryChroma


class ChromaLongMemory(VectorStoreRetrieverMemory):
    retriever: ChromaVectorStoreRetriever = Field(exclude=True)

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


class ChromaShortMemory(BaseMemory):
    memory_key: str = 'short_memory'

    vectorstore: MemoryChroma

    @property
    def memory_variables(self) -> list[str]:
        return [self.memory_key]

    def load_memory_variables(self, inputs: dict[str, Any]) -> dict[str, str]:
        last_msg_blocks = self.vectorstore.get_last_message_blocks()

        return {self.memory_key: '\n'.join([block for block in last_msg_blocks])}

    def save_context(self, *_, **__) -> None:
        """This memory is read-only."""

    def clear(self) -> None:
        """This memory is read-only."""


class CustomConversationChain(ConversationChain):
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


class CustomCallbackHandler(BaseCallbackHandler):

    def on_chat_model_start(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        pass

    # def on_llm_end(self, response: LLMResult, **_: Any) -> None:
    #     """Run when LLM ends running."""
    #     self.history.openai_response = response.llm_output
