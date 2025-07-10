# db_nexus/exceptions.py

class RepositoryError(Exception):
    """Exceção base para erros do repositório."""
    pass

class RecordNotFoundError(RepositoryError):
    """Lançada quando um registro não é encontrado."""
    def __init__(self, record_id):
        super().__init__(f"Registro com ID '{record_id}' não encontrado.")