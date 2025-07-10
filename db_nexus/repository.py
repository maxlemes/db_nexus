# db_nexus/repository.py

from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from .exceptions import RecordNotFoundError

# Cria um tipo genérico 'T' que pode ser qualquer classe de modelo do SQLAlchemy
T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        """
        Inicializa o repositório com um modelo SQLAlchemy específico.
        :param model: A classe do modelo (ex: Produto, Cliente)
        """
        self.model = model

    def get_by_id(self, session: Session, record_id: any) -> Optional[T]:
        """Busca um registro pelo seu ID."""
        record = session.get(self.model, record_id)
        if not record:
            raise RecordNotFoundError(record_id)
        return record

    def list_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """Lista todos os registros, com paginação."""
        return session.query(self.model).offset(skip).limit(limit).all()

    def add(self, session: Session, record: T) -> T:
        """Adiciona um novo registro à sessão."""
        session.add(record)
        return record

    def delete(self, session: Session, record_id: any) -> None:
        """Deleta um registro pelo seu ID."""
        record = self.get_by_id(session, record_id)
        session.delete(record)