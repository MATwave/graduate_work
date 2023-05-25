from typing import Any

from pydantic import BaseModel


class Meta(BaseModel):
    locale: str
    timezone: str
    client_id: str
    interfaces: dict[str, Any]


class User(BaseModel):
    user_id: str


class Application(BaseModel):
    application_id: str


class Session(BaseModel):
    message_id: int
    session_id: str
    skill_id: str
    user: User
    application: Application
    user_id: str
    new: bool


class Slots(BaseModel):
    type: str
    tokens: dict[str, int]
    value: str


class Intents(BaseModel):
    slots: dict[str, Slots]


class NLU(BaseModel):
    tokens: list[str]
    entities: list[Any]
    intents: dict[str, Intents]


class Markup(BaseModel):
    dangerous_context: bool


class Request(BaseModel):
    command: str
    original_utterance: str
    nlu: NLU
    markup: Markup
    type: str


class AliceRequestModel(BaseModel):
    meta: Meta
    session: Session
    request: Request
    version: str
    state: dict[str, Any]
