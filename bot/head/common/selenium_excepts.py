from selenium.common.exceptions import (TimeoutException, StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException,
                                        ElementClickInterceptedException)


def webdriver_exepts() -> list[TimeoutException | StaleElementReferenceException |  
                               NoSuchElementException | ElementNotInteractableException | 
                               ElementClickInterceptedException]:

    return [TimeoutException, StaleElementReferenceException, NoSuchElementException,
            ElementNotInteractableException, ElementClickInterceptedException, ValueError, Exception]


def exeption_message() -> dict[str, str]:

    return {
        TimeoutException: "Falha ao encontrar elemento",
        StaleElementReferenceException: "Erro ao encontrar referencia do elemento",
        NoSuchElementException: "Elemento não encontrado",
        ElementNotInteractableException: "Não foi possível interagir com o elemento",
        ElementClickInterceptedException: "Click interceptado",
        ValueError: "Erro de informação",
        Exception: "Erros diversos"

    }
