from dataclasses import dataclass


@dataclass
class SendMessageCommand:
    chat_id: int
    sender_id: int
    content: str


@dataclass
class CreateChatCommand:
    title: str
    creator_id: int


@dataclass
class JoinChatCommand:
    invite_code: str
    user_id: int


@dataclass
class EditMessageCommand:
    message_id: int
    user_id: int
    new_content: str

@dataclass
class DeleteMessageCommand:
    message_id: int
    user_id: int
    chat_id: int
