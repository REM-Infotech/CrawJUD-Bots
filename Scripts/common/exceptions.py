class CrawJUDExceptions(Exception):
    """Exceção base personalizada."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class ItemNaoEcontrado(CrawJUDExceptions):
    """Exceção para quando um recurso não é encontrado."""
    def __init__(self, message = "Item não encontrado"):
        super().__init__(message)
        
class ErroDeExecucao(CrawJUDExceptions):
    """Exceção para quando um recurso não é encontrado."""
    def __init__(self, message = "Erro ao executar operação"):
        super().__init__(message)    
        