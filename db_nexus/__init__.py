# db_nexus/__init__.py

from .session import DatabaseSessionManager
from .repository import BaseRepository
from .exceptions import RepositoryError, RecordNotFoundError

# Define o que será publicamente acessível quando alguém importar 'db_nexus'
__all__ = [
    "DatabaseSessionManager",
    "BaseRepository",
    "RepositoryError",
    "RecordNotFoundError"
]