from enum import Enum


class MessageType(str, Enum):
    SYSTEM = 'system'
    AI = 'ai'
    HUMAN = 'human'
    CHAT = 'chat'