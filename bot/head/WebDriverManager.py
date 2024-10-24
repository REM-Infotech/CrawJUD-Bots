



import os
import shutil
import signal
import zipfile
import requests
import platform
import subprocess


from clear import clear
from pathlib import Path
from typing import Iterable
from threading import Event
from functools import partial
import chrome_version as v_chrome
from urllib.request import urlopen

from rich.live import Live
from rich.console import Group
from rich.panel import Panel
from rich.progress import (
    TimeElapsedColumn, Progress, TaskID,
    TextColumn, BarColumn, DownloadColumn, 
    TransferSpeedColumn, TimeRemainingColumn)


from concurrent.futures import ThreadPoolExecutor

class GetDriver:
    
    code_ver = '.'.join(v_chrome.get_chrome_version().split('.')[:-1])
    progress = Progress(
    TimeElapsedColumn(),
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
    )
    
    current_app_progress = Progress(
        TimeElapsedColumn(),
        TextColumn("{task.description}"),
    )

    progress_group = Group(
        Panel(
            Group(current_app_progress, progress)))
    
    def __init__(self, destination: str = os.path.join(os.getcwd()), **kwargs):
        
        self.file_path: str = os.path.join(os.getcwd(), "webdriver", "chromedriver")
        self.file_path += self.code_ver
        
        self.fileN = os.path.basename(self.file_path)
        if not self.code_ver in self.fileN:
            self.fileN += self.code_ver
        
        for key, value in list(kwargs.items()):
            setattr(self, key, value)
        
        self.destination = destination
        
    def __call__(self) -> str:
        
        clear()
        with Live(self.progress_group):
            with ThreadPoolExecutor() as pool:
                self.ConfigBar(pool)
        
        shutil.copy(self.file_path, self.destination)     
        return os.path.basename(self.destination)
    
    def ConfigBar(self, pool: ThreadPoolExecutor):
        self.current_task_id = self.current_app_progress.add_task("[bold blue] Baixando Chromedriver")
        task_id = self.progress.add_task("download", filename=self.fileN.upper(), start=False)
        
        if platform.system() == "Windows":
            self.fileN += ".exe" 
            self.file_path += ".exe"
        
        self.destination = os.path.join(self.destination, self.fileN)
        
        root_path = str(Path(self.file_path).parent.resolve())
        if not os.path.exists(root_path):
            
            os.makedirs(root_path)
            pool.submit(self.copy_url, task_id, self.getUrl(), self.file_path)
            
        elif os.path.exists(root_path):
            if os.path.exists(self.file_path):
                self.current_app_progress.update(
                self.current_task_id, 
                description="[bold green] Carregado webdriver salvo em cache!")
                shutil.copy(self.file_path, self.destination)
     
    def getUrl(self) -> str:
        
        ## Verifica no endpoint qual a versão disponivel do WebDriver 
        url_chromegit = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{self.code_ver}"
        results = requests.get(url_chromegit)
        chrome_version = results.text

        ## Baixa o WebDriver conforme disponivel no repositório 
        return f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/linux64/chromedriver-linux64.zip"
    
    
    def copy_url(self, task_id: TaskID, url: str, path: str) -> None:
        
        """Copy data from a url to a local file."""

        response = urlopen(url)
        
        # This will break if the response doesn't contain content length
        self.progress.update(task_id, total=int(response.info()["Content-length"]))
        
        with open(path, "wb") as dest_file:
            
            self.progress.start_task(task_id)
            for data in iter(partial(response.read, 32768), b""):
                
                dest_file.write(data)
                self.progress.update(task_id, advance=len(data))
                
        self.current_app_progress.update(
            self.current_task_id, description="[bold green] ChromeDriver Baixado!")
