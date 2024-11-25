DESCRIPTION_TEMPLATE = '{description}\n\n'

LONG_MEMORY_TEMPLATE = "Relevant memorized messages:\n\n{long_memory}\n\n"

SHORT_MEMORY_TEMPLATE = 'Current conversation:\n\n{short_memory}\n{human_prefix}: {input}\n{ai_prefix}: '

EXAMPLE_PROMPT_TEMPLATE = DESCRIPTION_TEMPLATE + LONG_MEMORY_TEMPLATE + SHORT_MEMORY_TEMPLATE