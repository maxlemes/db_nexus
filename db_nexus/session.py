# db_nexus/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

class DatabaseSessionManager:
    def __init__(self, db_url: str):
        """
        Inicializa o gerenciador de sessão.
        :param db_url: A URL de conexão do banco de dados (ex: "postgresql://user:pass@host/db")
        """
        self._engine = create_engine(db_url, pool_pre_ping=True)
        self._session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    @contextmanager
    def get_session(self) -> Session:
        """
        Fornece uma sessão de banco de dados transacional.
        Garante que a sessão seja sempre fechada e que as transações
        sejam confirmadas (commit) ou revertidas (rollback).
        """
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()