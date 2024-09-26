### Inicializador dos [`Bots`](./__init__.py)

<p>

    Olá, esse é o Leia-Me do inicializador dos robôs

</p>


```python

def __init__(self, arguments_bot: dict):
    
    """
    Argumento de inicialização do bot

    """
    self.arguments_bot = arguments_bot
    self.row = 2
    self.index = 0
    self.pid = arguments_bot["pid"]

    """
    Leitura da planilha de input
    """
    self.input_file = glob.glob(os.path.join("Temp", self.pid, "*.xlsx"))[0]
    self.ws: Type[Worksheet] = openpyxl.load_workbook(self.input_file).active

    """
    Variável de output
    """

    self.output_dir_path = pathlib.Path(self.input_file).parent.resolve().__str__()

    """
    Configurador do print logs
    """
    self.prt = prt(self.pid)
    self.bot_name: str = arguments_bot.get("bot")


    """
    Setup do ChromeDriver
    """
    args = self.DriverLaunch()
    self.driver: Type[WebDriver] = args[0]
    self.wait: Type[WebDriverWait] = args[1]
    self.interact = Interact(self.driver, self.wait)
    

    """
    Gerador de planilhas de output
    """

    namefile = f"Sucessos - PID {self.pid} {datetime.now(pytz.timezone('Etc/GMT+4')).strftime('%d-%m-%y')}.xlsx"
    self.path = f"{self.output_dir_path}/{namefile}"
    MakeXlsx().make_output(f"{self.bot}_sucesso", self.path)

    namefile_erro = f"Erros - PID {self.pid} {datetime.now(pytz.timezone('Etc/GMT+4')).strftime('%d-%m-%y')}.xlsx"
    self.path_erro = f"{self.output_dir_path}/{namefile_erro}"
    MakeXlsx().make_output(f"{self.bot}_erro", self.path_erro)


    """
    Configurador do SetStatus (Responsável por informar o status da Execução)
    """
    self.set_status = SetStatus()

    status = ["usuario.executor", "id_execução", 'nome_bot', 'Status', 'Arquivo de Input']

    """
    Informa o inicio
    """
    self.set_status.botstop(status)

    """
    Informa a parada (Sucesso / Erro)
    """
    self.set_status.botstart(status)


    f"""
    
    Outras configurações

    ### Esse apenas informa a quantidade de itens na planilha

    {
    wb = openpyxl.load_workbook(filename=self.input_file)
    ws: Type[Worksheet] = wb.active
    self.rows = ws.max_row
    self.set_status.send_total_rows(self.rows, self.pid)
    }
    
    """
        


```