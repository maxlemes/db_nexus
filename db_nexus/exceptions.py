# db_nexus/exceptions.py

"""
Este módulo define a hierarquia de exceções personalizadas para a biblioteca db_nexus.

Criar exceções específicas, como 'RecordNotFoundError', em vez de usar as genéricas
do Python (como ValueError ou Exception), é uma prática recomendada por várias razões:
1.  **Clareza**: O código que utiliza a biblioteca pode capturar erros específicos
    (ex: `except RecordNotFoundError:`), tornando a intenção do tratamento de erro
    explícita e legível.
2.  **Robustez**: Evita a captura acidental de outros erros não relacionados. Se você
    captura a exceção genérica `Exception`, pode acabar mascarando bugs inesperados.
3.  **API Contratual**: A biblioteca estabelece um "contrato" claro sobre quais
    erros ela pode lançar, facilitando a vida de quem a utiliza.
"""

class RepositoryError(Exception):
    """
    Exceção base para todos os erros gerados pela camada de repositório.

    Esta classe serve como um "guarda-chuva". Ao herdar dela, todas as nossas
    exceções de repositório (como RecordNotFoundError) podem ser capturadas
    de forma genérica, se necessário. Por exemplo, um bloco de log poderia ter
    um `except RepositoryError:` para registrar qualquer falha relacionada ao
    banco de dados, sem se preocupar com os detalhes específicos.
    """
    pass

class RecordNotFoundError(RepositoryError):
    """
    Lançada especificamente quando uma operação de busca por um registro
    (geralmente por ID ou outra chave única) não encontra resultados.

    Herda de 'RepositoryError', estabelecendo a hierarquia de exceções.
    """
    def __init__(self, record_id):
        """
        O construtor da exceção.

        :param record_id: O identificador do registro que não foi encontrado.
                          Isso é usado para criar uma mensagem de erro informativa.
        """
        # A mensagem de erro é formatada para ser clara e útil para depuração.
        message = f"Registro com ID '{record_id}' não encontrado."
        
        # 'super().__init__(message)' chama o construtor da classe pai ('RepositoryError')
        # para registrar a mensagem de erro.
        super().__init__(message)