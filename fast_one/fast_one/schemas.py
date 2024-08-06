from pydantic import BaseModel, EmailStr

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):  # schemas é um contrato de o que devemos retornar
    nome: str
    email: EmailStr
    senha: str

class UserPublic(BaseModel):
    nome: str
    email: EmailStr