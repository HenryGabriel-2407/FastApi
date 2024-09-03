from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///database.db', echo=True)

with engine.connect() as con:
    sql = text("SELECT * FROM users")
    result = con.execute(sql)