# db_nexus/repository.py

"""
Este módulo define o 'BaseRepository', uma implementação genérica do
padrão de projeto "Repository".

O Padrão de Repositório serve como uma camada de abstração entre a lógica de
negócio e a fonte de dados. Ele esconde a complexidade do acesso a dados
(queries do SQLAlchemy) por trás de uma interface simples e orientada a objetos
(ex: get_by_id, add, list_all). O uso de Generics (`TypeVar`) torna esta
implementação reutilizável para qualquer modelo de dados.
"""

# Importações avançadas de 'typing' para criar componentes genéricos e type-safe (seguros em tipo).
from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
# Importa a exceção customizada, uma boa prática para erros específicos da camada de dados.
from .exceptions import RecordNotFoundError

# 'TypeVar' cria uma variável de tipo genérico, que chamamos de 'T'.
# Pense em 'T' como um espaço reservado que pode ser preenchido por qualquer
# tipo de modelo (ex: Usuario, Produto, Transacao) no futuro.
T = TypeVar('T')

# A classe 'BaseRepository' usa 'Generic[T]' para se tornar uma classe genérica.
# Isso significa que podemos criar um repositório de Usuários, um repositório de Produtos, etc.,
# todos baseados neste mesmo molde, sem reescrever o código. É o ápice da reutilização!
class BaseRepository(Generic[T]):
    
    def __init__(self, model: Type[T]):
        """
        O construtor do repositório. Cada repositório específico (ex: UserRepository)
        será inicializado com a classe do modelo que ele gerencia.

        :param model: A classe do modelo SQLAlchemy que este repositório irá manipular.
        """
        self.model = model

    def get_by_id(self, session: Session, record_id: any) -> Optional[T]:
        """
        Busca um único registro pela sua chave primária.
        Note que o método recebe a 'session' como parâmetro. Isso é chamado de
        Injeção de Dependência e é uma prática excelente, pois o repositório não
        se preocupa em como a sessão foi criada ou como ela será fechada. Ele apenas a usa.
        """
        # 'session.get()' é a forma moderna e otimizada do SQLAlchemy para buscar por chave primária.
        record = session.get(self.model, record_id)
        if not record:
            # Lançar uma exceção customizada é mais claro do que retornar 'None' e forçar
            # o código que chama a sempre checar se o resultado é nulo.
            raise RecordNotFoundError(record_id)
        return record

    def list_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Retorna uma lista de registros, implementando paginação básica para
        evitar carregar milhares de registros do banco de uma só vez.
        """
        return session.query(self.model).offset(skip).limit(limit).all()

    def add(self, session: Session, record: T) -> T:
        """
        Adiciona uma nova instância do modelo à sessão.
        É importante notar que este método *não* chama 'session.commit()'.
        O repositório é responsável apenas por preparar as operações na sessão.
        A responsabilidade de 'commitar' a transação é do gerenciador de sessão
        (o nosso 'DatabaseSessionManager' com o bloco 'with'). Isso mantém as
        responsabilidades bem separadas.
        """
        session.add(record)
        return record

    def delete(self, session: Session, record_id: any) -> None:
        """
        Deleta um registro.
        Este método demonstra uma boa prática: ele reutiliza 'get_by_id' para
        primeiro encontrar o registro (e garantir que ele existe). Isso evita
        escrever a mesma lógica de busca duas vezes.
        """
        record = self.get_by_id(session, record_id)
        session.delete(record)