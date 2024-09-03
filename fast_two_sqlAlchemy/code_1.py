from sqlalchemy import create_engine

# Criando o BD
engine = create_engine('sqlite:///database.db', echo=True)

print(engine)
print(engine.dialect)
print()

print(engine.pool)
print(engine.pool.status())
print()

# Realizando a conexão com BD
con = engine.connect()
print(engine.pool.status())
print(con.connection.dbapi_connection)
con.close()