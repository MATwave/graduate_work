from typing import Dict, List
from pydantic import BaseModel


class Meta(BaseModel):
    locale: str
    timezone: str
    client_id: str
    interfaces: Dict[str, dict]


class User(BaseModel):
    user_id: str


class Application(BaseModel):
    application_id: str
    application_type: str | None


class Session(BaseModel):
    message_id: int
    session_id: str
    skill_id: str
    user: User
    application: Application
    user_id: str
    new: bool


class NLU(BaseModel):
    tokens: List[str]
    entities: List[dict] | None
    intents: Dict[str, dict] | None 


class Markup(BaseModel):
    dangerous_context: bool


class Request(BaseModel):
    command: str
    original_utterance: str
    nlu: NLU
    markup: Markup | None
    type: str

class State(BaseModel):
    session: dict | None = {}
    user: dict| None = {}


class MarusyaRequestModel(BaseModel):
    meta: Meta
    session: Session
    request: Request
    state: State
    version: str
