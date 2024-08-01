from pydantic import BaseModel

class Message(BaseModel): # schemas é um contrato de o que devemos retornar
    message: str
    batata: int
