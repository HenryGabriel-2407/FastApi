from sqlalchemy import create_engine, select, MetaData, Table, insert
import datetime

engine = create_engine("sqlite:///database.db", echo=True)

metadata = MetaData()

t = Table('coments', metadata, autoload_with=engine)

metadata.create_all(engine)

for col in t.columns:
    print(col)

sql = insert(t).values(
    name= 'Edu',
    comment= 'SQLAlchemy',
    date_creat= datetime.datetime.now())

print(sql)