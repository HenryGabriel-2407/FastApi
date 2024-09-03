from sqlalchemy import Column, DateTime, Integer, String, func, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session

engine = create_engine("sqlite:///database_avaliacao.db", echo=True)

class Base(DeclarativeBase):
    ...

class Avaliacoes(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    avaliacao = Column(String, nullable=False)
    nota = Column(Integer, nullable=False)
    date_creat = Column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"{self.id} = Nome: {self.name} / Avaliação: {self.avaliacao} / Nota: {self.nota}"

Base.metadata.create_all(engine)

#tabela = Avaliacoes(name="Giovanna", avaliacao = "Simples e aconchegante", nota=8)

with Session(engine) as s:
    #s.add(tabela)
    result = s.scalars(select(Avaliacoes))
    print()
    for linha in result.fetchall():
        print(linha)
    print()
    s.commit()
    s.close()