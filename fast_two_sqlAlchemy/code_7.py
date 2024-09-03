from sqlalchemy import create_engine, select, MetaData, Table, delete, select
import datetime

engine = create_engine("sqlite:///database.db", echo=True)

metadata = MetaData()

t = Table('coments', metadata, autoload_with=engine)

metadata.create_all(engine)

sql  = delete(t).where(
    (t.c.name == "Henry Gabriel") & 
    (t.c.id == 2)
)
with engine.connect() as con:
    con.execute(sql)
    sql = select(t)
    result = con.execute(sql)
    print(result.fetchall())