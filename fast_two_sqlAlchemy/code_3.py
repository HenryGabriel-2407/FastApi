import sqlalchemy as sa
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///database.db", echo=True)

metadata = sa.MetaData()

t = sa.Table('coments', metadata,
             sa.Column('id', sa.Integer(), nullable=False),
             sa.Column('name', sa.String(), nullable=False),
             sa.Column('comment', sa.String(), nullable=False),
             sa.Column('date_creat', sa.DateTime, nullable=False),
             sa.PrimaryKeyConstraint('id'))

metadata.create_all(engine)

inspect = sa.inspect(engine)
print(inspect.get_table_names())
print(inspect.get_columns('coments'))
print()
print(t.columns)

with engine.connect() as con:
    with con.begin():
        con.execute(text('insert into coments("name", "comment", "date_creat") values ("Henry Gabriel", "Olá mundo!", "2024-07-24 15:50:54.25140")'))
    with con.begin():
        resultado = con.execute(text("select * from coments"))
        print(resultado.fetchall())