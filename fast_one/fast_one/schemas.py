from pydantic import BaseModel


class Message(BaseModel):
    message: str
    batata: int
