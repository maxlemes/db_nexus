# db_nexus/session.py

"""
Este módulo fornece a classe `DatabaseSessionManager`, o coração da gestão
de conexões e transações com o banco de dados na biblioteca db_nexus.

O principal objetivo é usar o padrão de Gerenciador de Contexto (`with` statement)
para garantir que as sessões do SQLAlchemy sejam sempre criadas, usadas e
fechadas de forma segura e previsível, automatizando o commit em caso de sucesso
e o rollback em caso de falha.
"""

# Importações essenciais do SQLAlchemy e da biblioteca padrão do Python.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from .base import Base # Importa a Base compartilhada

class DatabaseSessionManager:
    """
    Esta classe encapsula toda a lógica de configuração e gerenciamento de sessões
    do SQLAlchemy. O objetivo é fornecer uma interface simples e segura para que
    os projetos que usarem a biblioteca 'db_nexus' possam interagir com o banco de dados
    sem se preocupar com os detalhes de abrir, fechar, cometer (commit) ou reverter (rollback) transações.
    """
    
    def __init__(self, db_url: str):
        """
        O construtor da classe. Ele é chamado uma única vez quando um projeto
        inicializa a conexão com o banco.

        :param db_url: A URL de conexão, que define qual banco de dados será usado
                       e como se conectar a ele (ex: "sqlite:///meu_banco.db" ou
                       "postgresql://usuario:senha@host/banco").
                       Tornar isso um parâmetro torna a biblioteca agnóstica ao banco de dados.
        """
        # 'create_engine' é o ponto de partida do SQLAlchemy. Ele cria um pool de conexões
        # com o banco. 'pool_pre_ping=True' é uma configuração de produção útil que
        # verifica se uma conexão do pool ainda está ativa antes de usá-la, evitando
        # erros em aplicações que ficam conectadas por muito tempo.
        self._engine = create_engine(db_url, pool_pre_ping=True, connect_args={"timeout": 15})
        
        # 'sessionmaker' cria uma "fábrica de sessões". Em vez de configurar uma sessão
        # toda vez, nós configuramos esta fábrica uma vez, e depois apenas pedimos a ela
        # para nos dar novas sessões já configuradas.
        self._session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    @contextmanager
    def get_session(self) -> Session:
        """
        Este é o método mais importante da classe. Ele usa o padrão de "Gerenciador de Contexto"
        do Python, o que permite que ele seja usado com a declaração 'with'.
        
        A mágica do '@contextmanager' está em como ele lida com o ciclo de vida da sessão
        de forma automática e à prova de falhas.

        :return: Fornece (yields) um objeto de sessão do SQLAlchemy.
        """
        
        # 1. ENTRADA: Quando o bloco 'with' começa, uma nova sessão é criada pela fábrica.
        session = self._session_factory()
        
        try:
            # 2. EXECUÇÃO: A palavra-chave 'yield' entrega a sessão para o código dentro
            # do bloco 'with'. O método pausa aqui e espera o bloco 'with' terminar.
            yield session
            
            # 3. SUCESSO: Se o bloco 'with' terminar sem nenhum erro (exceção),
            # a transação é confirmada com 'session.commit()'. Os dados são salvos no banco.
            session.commit()
            
        except Exception:
            # 4. FALHA: Se qualquer erro ocorrer DENTRO do bloco 'with', o 'try' falha.
            # 'session.rollback()' é chamado para desfazer TODAS as alterações feitas
            # nesta sessão, garantindo a integridade dos dados.
            session.rollback()
            
            # 'raise' é crucial aqui. Ele relança a exceção original. Isso impede que o
            # erro seja "engolido" silenciosamente, permitindo que o código que chamou
            # o 'with' saiba que algo deu errado e possa lidar com isso.
            raise
            
        finally:
            # 5. LIMPEZA: Este bloco é executado SEMPRE, não importa se houve sucesso ou falha.
            # 'session.close()' fecha a sessão e devolve sua conexão ao pool do engine.
            # Isso é vital para evitar vazamento de recursos (conexões abertas).
            session.close()

    def create_all_tables(self):
        """
        Cria no banco de dados todas as tabelas que foram definidas usando
        a Base da biblioteca.
        """
        if not self._engine:
            raise Exception("Banco de dados não inicializado. Chame '__init__' primeiro.")
        
        # O Base.metadata contém a definição de todas as tabelas que herdaram de Base.
        Base.metadata.create_all(bind=self._engine)
        print("Tabelas do banco de dados verificadas/criadas.")