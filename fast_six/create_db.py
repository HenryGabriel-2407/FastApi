from sqlalchemy import create_engine

from fast_six.models import table_registry  # Importa o registro das tabelas

# Define o caminho do banco de dados
DATABASE_URL = 'sqlite:///database.db'  # Substitua pelo caminho que desejar

# Cria o engine para conectar ao SQLite
engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` exibe os logs das operações no console

# Cria todas as tabelas registradas
table_registry.metadata.create_all(engine)

print('Tabelas criadas com sucesso no arquivo database.db!')
