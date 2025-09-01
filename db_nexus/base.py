# db_nexus/base.py

"""
Este módulo define a 'Base' declarativa central para a biblioteca db_nexus.

O objetivo deste arquivo é fornecer uma única instância da Base declarativa
do SQLAlchemy que possa ser importada por qualquer projeto que utilize
esta biblioteca. Funciona como um "catálogo central" para todos os modelos
(tabelas) da aplicação.
"""

# Importa a função 'declarative_base' do SQLAlchemy. Esta função é uma "fábrica"
# que cria uma classe base para os modelos do ORM (Mapeamento Objeto-Relacional).
from sqlalchemy.ext.declarative import declarative_base

# ------------------------------------------------------------------------------
#  A Base Declarativa Central
# ------------------------------------------------------------------------------
# A linha abaixo cria a classe 'Base'. Qualquer classe de modelo no projeto do
# usuário que herdar desta 'Base' será automaticamente registrada no
# catálogo de metadados do SQLAlchemy (`Base.metadata`).
#
# Exemplo de uso em um projeto que consome a biblioteca:
#
#   # Em meu_projeto/models.py
#   from db_nexus.base import Base  # <--- Importa a Base da biblioteca
#   from sqlalchemy import Column, Integer, String
#
#   class Usuario(Base):  # <--- Herda da Base para se registrar no catálogo
#       __tablename__ = 'usuarios'
#       id = Column(Integer, primary_key=True)
#       nome = Column(String)
#
# É CRUCIAL que todos os modelos do projeto herdem desta MESMA instância de 'Base'
# para que o comando `Base.metadata.create_all(engine)` consiga encontrar
# e criar todas as tabelas corretamente no banco de dados.
Base = declarative_base()