from typing import Dict, List, Any
from pydantic import BaseModel

class Meta(BaseModel):
    locale: str
    timezone: str
    client_id: str
    interfaces: Dict[str, Any]

class Application(BaseModel):
    application_id: str

class Session(BaseModel):
    message_id: int
    session_id: str
    skill_id: str
    application: Application
    user_id: str
    new: bool

class Intents(BaseModel):
    slots: Dict[str, Any]

class NLU(BaseModel):
    tokens: List[str]
    entities: List[Any]
    intents: Dict[str, Intents]

class Markup(BaseModel):
    dangerous_context: bool

class Request(BaseModel):
    command: str
    original_utterance: str
    nlu: NLU
    markup: Markup
    type: str

class AliceRequest(BaseModel):
    meta: Meta
    session: Session
    request: Request
    version: str
