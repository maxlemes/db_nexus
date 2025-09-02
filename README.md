# db_nexus: Um Wrapper Python para SQLAlchemy

`db_nexus` é uma pequena biblioteca Python projetada para simplificar e padronizar o uso do SQLAlchemy em diversos projetos. Ela encapsula a complexidade do gerenciamento de sessões e implementa o Padrão de Repositório de forma genérica, permitindo que você escreva um código de acesso a dados mais limpo, seguro e reutilizável.

## Principais Recursos

* **Gerenciamento de Sessão Seguro**: Utiliza um gerenciador de contexto (`with` statement) para garantir que as sessões sejam sempre fechadas e que as transações sejam automaticamente commitadas ou revertidas (rollback), prevenindo vazamento de recursos e inconsistência de dados.
* **Padrão de Repositório Genérico**: Oferece uma `BaseRepository` que implementa operações CRUD (Create, Read, Update, Delete) comuns, eliminando a necessidade de reescrever código repetitivo para cada modelo do seu banco de dados.
* **Hierarquia de Exceções Claras**: Define exceções personalizadas como `RecordNotFoundError`, tornando o tratamento de erros na sua aplicação mais explícito e robusto.
* **Fácil Configuração**: A inicialização é feita com uma única linha, passando a URL do seu banco de dados, tornando a biblioteca agnóstica ao SGBD (funciona com SQLite, PostgreSQL, MySQL, etc.).

## Instalação

Você pode instalá-la diretamente do repositório do GitHub:

```bash
pip install git+https://github.com/maxlemes/db_nexus.git
```

Isso tornará o pacote `db_nexus` importável em outros projetos no mesmo ambiente. Se um dia a biblioteca for publicada no PyPI, a instalação seria `pip install db-nexus`.

## Guia Rápido de Uso

Veja como integrar o `db_nexus` em seu projeto em 4 passos simples.

### Passo 1: Defina seus Modelos de Dados

No seu projeto, crie um arquivo `models.py` e defina suas tabelas como classes Python, herdando da `Base` fornecida pelo `db_nexus`.

**`meu_projeto/models.py`**
```python
from sqlalchemy import Column, Integer, String
from db_nexus.base import Base  # Importe a Base da biblioteca!

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome}')>"
```

### Passo 2: Crie um Repositório Específico

Crie um repositório para o seu modelo herdando da `BaseRepository`. Você pode adicionar métodos customizados aqui se precisar.

**`meu_projeto/repositories.py`**
```python
from db_nexus.repository import BaseRepository
from .models import Usuario

class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self):
        super().__init__(Usuario)

    # Exemplo de método customizado
    def find_by_email(self, session, email: str):
        return session.query(self.model).filter(self.model.email == email).first()
```

### Passo 3: Inicialize a Biblioteca na sua Aplicação

No seu arquivo principal, inicialize o `DatabaseSessionManager` e os seus repositórios.

**`meu_projeto/main.py`**
```python
from db_nexus.session import DatabaseSessionManager
from db_nexus.exceptions import RecordNotFoundError
from .repositories import UsuarioRepository
from .models import Usuario

# 1. Inicialize o gerenciador de sessão com a URL do seu banco
db_manager = DatabaseSessionManager("sqlite:///meu_app.db")

# 2. Crie as tabelas no banco de dados (se não existirem)
# O db_nexus encontrará todos os modelos que herdaram de sua 'Base'.
db_manager.create_all_tables()

# 3. Instancie seus repositórios
usuario_repo = UsuarioRepository()
```

### Passo 4: Use o Repositório e a Sessão para Manipular Dados

Agora, use o bloco `with` para obter uma sessão segura e passe-a para os métodos do seu repositório.

**`meu_projeto/main.py` (continuação)**
```python
def executar_crud():
    # --- Adicionar um usuário ---
    print("Adicionando novo usuário...")
    with db_manager.get_session() as session:
        novo_usuario = Usuario(nome="Ana", email="ana@example.com")
        usuario_repo.add(session, novo_usuario)
    print("Usuário adicionado com sucesso.")

    # --- Buscar um usuário ---
    print("\nBuscando usuário com ID 1...")
    try:
        with db_manager.get_session() as session:
            usuario_encontrado = usuario_repo.get_by_id(session, 1)
            print(f"Encontrado: {usuario_encontrado}")
    except RecordNotFoundError as e:
        print(e)
    
    # --- Usar um método customizado ---
    print("\nBuscando usuário pelo email 'ana@example.com'...")
    with db_manager.get_session() as session:
        usuario_por_email = usuario_repo.find_by_email(session, "ana@example.com")
        print(f"Encontrado por email: {usuario_por_email}")


    # --- Deletar um usuário ---
    print("\nDeletando usuário com ID 1...")
    try:
        with db_manager.get_session() as session:
            usuario_repo.delete(session, 1)
        print("Usuário deletado com sucesso.")
    except RecordNotFoundError as e:
        print(e)

if __name__ == "__main__":
    executar_crud()
```

## Licença

Este projeto está licenciado sob a Licença MIT.
