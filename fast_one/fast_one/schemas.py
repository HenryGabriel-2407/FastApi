from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):  # schemas é um contrato de o que devemos retornar
    nome: str
    email: EmailStr
    senha: str


class UserDb(UserSchema):
    id: int


class UserPublic(BaseModel):  # após inserir dados, o FastApi retornará isso
    id: int
    nome: str
    email: EmailStr


class UserList(BaseModel):
    users: list[UserPublic]
