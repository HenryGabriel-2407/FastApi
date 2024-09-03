import sqlalchemy as sa
from sqlalchemy import create_engine, text, select, MetaData, Table

engine = create_engine("sqlite:///database.db", echo=True)

metadata = MetaData()

t = Table('coments', metadata, autoload_with=engine)

metadata.create_all(engine)

sql = select(t)

with engine.connect() as con:
    with con.begin():
        resultado = con.execute(sql)
        print(resultado.fetchall())
        print("\n\n")
        sql = (select(t.c.id, t.c.name, t.c.comment)
               .where(t.c.name == 'Giovanna')
               # .limit(10)  --> limite de quantas linhas de deseja
               # .offset(2) --> qual indice começa das linhas selecionadas
               # .order_by(t.c.comment)  --> odernar por 
               )
        resultado = con.execute(sql)
        print(resultado.fetchall())