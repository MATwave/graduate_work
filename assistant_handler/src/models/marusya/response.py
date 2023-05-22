from pydantic import BaseModel


class Buttons(BaseModel):
    title: str
    url: str | None
    payload: dict | None


class ResponseMarusya(BaseModel):
    text: str
    end_session: bool = False


class Session(BaseModel):
    session_id: str
    user_id: str
    message_id: int


class MarusyaResponseModel(BaseModel):
    response: ResponseMarusya
    session: Session
    session_state: dict = {}
    version: str = '1.0'
