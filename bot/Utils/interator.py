from bot.common.exceptions import ItemNaoEcontrado


from time import sleep
from ..CrawJUD import CrawJUD
from contextlib import suppress

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class Interact(CrawJUD):

    def __getattr__(self, nome):
        return super().__getattr__(nome)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def send_key(self, element: WebElement, word: any) -> None:

        send = None
        for key in dir(Keys):
            if getattr(Keys, key) == word:
                send = ""
                element.send_keys(word)
                break

        if send is None:
            element.click()
            sleep(0.05)
            for c in str(word):
                sleep(0.001)
                element.send_keys(c)

    def click(self, element: WebElement) -> None:

        sleep(0.05)
        element.click()
        sleep(0.05)

    def double_click(self, element: WebDriver) -> None:

        Action = ActionChains(self.driver)
        Action.double_click(element).perform()

    def select_item(self, elemento: str, text: str) -> bool | Exception:

        itens: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, elemento))
        )

        self.diplay_none(itens)
        sleep(0.5)

        if not text.isupper():
            itens = list(
                filter(
                    lambda item: not item.text.isupper(),
                    itens.find_element(By.CSS_SELECTOR, "ul").find_elements(
                        By.TAG_NAME, "li"
                    ),
                )
            )

        elif text.isupper():
            itens = itens.find_element(By.TAG_NAME, "ul").find_elements(
                By.TAG_NAME, "li"
            )

        item = next(filter(lambda item: text == item.text, itens), None)

        if not item:
            raise ItemNaoEcontrado(message=f'Item "{text}" não encontrado!')

        Action = ActionChains(self.driver)
        Action.double_click(item).perform()

        return True

    def clear(self, element: WebElement) -> None:

        element.click()
        sleep(0.5)
        element.clear()
        sleep(1)

    def sleep_load(self, element: str = 'div[id="j_id_3x"]') -> None:

        while True:
            sleep(0.5)
            load = None
            aria_value = None
            with suppress(TimeoutException):
                load: WebElement = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, element))
                )

            if load:

                for attributes in ["aria-live", "aria-hidden", "class"]:
                    aria_value = load.get_attribute(attributes)

                    if not aria_value:
                        continue

                    break

                if aria_value is None or any(
                    value == aria_value
                    for value in [
                        "off",
                        "true",
                        "spinner--fullpage spinner--fullpage--show",
                    ]
                ):
                    break

            if not load:
                break

    def diplay_none(self, elemento: WebElement):

        while True:

            style = elemento.get_attribute("style")

            if "display: none;" not in style:
                sleep(0.01)
                break

    def wait_caixa(self) -> None:

        while True:

            check_wait = None
            with suppress(NoSuchElementException):
                check_wait = self.driver.find_element(
                    By.CSS_SELECTOR,
                    'div[id="modal:waitContainer"][style="position: absolute; z-index: 100; background-color: inherit; display: none;"]',
                )

            if check_wait:
                break

    def wait_fileupload(self) -> None:

        while True:

            sleep(0.05)
            div1 = 'div[class="ui-fileupload-files"]'
            div2 = 'div[class="ui-fileupload-row"]'
            div0 = 'div[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_2_1_9_g_1:uploadGedEFile"]'
            progress_bar = None

            div0progress_bar = self.driver.find_element(By.CSS_SELECTOR, div0)
            div1progress_bar = div0progress_bar.find_element(By.CSS_SELECTOR, div1)

            with suppress(NoSuchElementException):
                progress_bar = div1progress_bar.find_element(By.CSS_SELECTOR, div2)

            if progress_bar is None:
                break

    def scroll_to(self, element: WebElement):

        Action = ActionChains(self.driver)
        Action.scroll_to_element(element)
        sleep(0.5)
