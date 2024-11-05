import os
import re
import shutil
import requests
import platform
import zipfile

from clear import clear
from pathlib import Path
from functools import partial
from urllib.request import urlopen

from rich.live import Live
from rich.console import Group
from rich.panel import Panel
from rich.progress import (
    TimeElapsedColumn,
    Progress,
    TaskID,
    TextColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)


from concurrent.futures import ThreadPoolExecutor


class GetDriver:

    @property
    def code_ver(self):
        return ".".join(get_chrome_version().split(".")[:-1])

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

    progress_group = Group(Panel(Group(current_app_progress, progress)))

    def __init__(self, destination: str = os.path.join(os.getcwd()), **kwrgs):

        self.file_path: str = os.path.join(os.getcwd(), "webdriver", "chromedriver")
        self.file_path += self.code_ver

        self.fileN = os.path.basename(self.file_path)
        if self.code_ver not in self.fileN:
            self.fileN += self.code_ver

        for key, value in list(kwrgs.items()):
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
        self.current_task_id = self.current_app_progress.add_task(
            "[bold blue] Baixando Chromedriver"
        )
        task_id = self.progress.add_task(
            "download", filename=self.fileN.upper(), start=False
        )

        if platform.system() == "Windows":
            self.fileN += ".exe"
            self.file_path += ".exe"

        self.destination = os.path.join(self.destination, self.fileN)
        root_path = str(Path(self.file_path).parent.resolve())
        if not os.path.exists(self.file_path):

            if not os.path.exists(root_path):
                os.makedirs(root_path)

            pool.submit(self.copy_url, task_id, self.getUrl(), self.file_path)

        elif os.path.exists(root_path):
            if os.path.exists(self.file_path):
                self.current_app_progress.update(
                    self.current_task_id,
                    description="[bold green] Carregado webdriver salvo em cache!",
                )
                shutil.copy(self.file_path, self.destination)

    def getUrl(self) -> str:

        # Verifica no endpoint qual a versão disponivel do WebDriver
        url_chromegit = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{self.code_ver}"
        results = requests.get(url_chromegit)
        chrome_version = results.text

        system = platform.system().replace("dows", "").lower()
        arch = platform.architecture()
        if type(arch) is tuple:
            arch = arch[0].replace("bit", "")

        os_sys = f"{system}{arch}"
        # Baixa o WebDriver conforme disponivel no repositório
        url_driver = "https://storage.googleapis.com/chrome-for-testing-public/"

        set_URL = [chrome_version, os_sys, os_sys]
        for pos, item in enumerate(set_URL):

            if pos == len(set_URL) - 1:
                url_driver += f"chromedriver-{item}.zip"
                continue

            url_driver += f"{item}/"

        return url_driver

    def copy_url(self, task_id: TaskID, url: str, path: str) -> None:
        """Copy data from a url to a local file."""

        response = urlopen(url)

        # This will break if the response doesn't contain content length
        self.progress.update(task_id, total=int(response.info()["Content-length"]))

        with open(path.replace(".exe", ".zip"), "wb") as dest_file:

            self.progress.start_task(task_id)
            for data in iter(partial(response.read, 32768), b""):

                dest_file.write(data)
                self.progress.update(task_id, advance=len(data))

        # Extract the zip file
        with zipfile.ZipFile(path.replace(".exe", ".zip"), "r") as zip_ref:

            # Extract each file directly into the subfolder
            for member in zip_ref.namelist():

                not_Cr1 = member.split("/")[1].lower() == "chromedriver.exe"
                not_Cr2 = member.split("/")[1].lower() == "chromedriver"

                if not_Cr1 or not_Cr2:

                    # Get the original file name without any directory structure
                    extracted_path = zip_ref.extract(member, os.path.dirname(path))

                    # If the extracted path has directories, move the file directly into the subfolder
                    if os.path.basename(extracted_path) and os.path.isdir(
                        extracted_path
                    ):
                        continue

                    shutil.move(
                        extracted_path, os.path.join(os.path.dirname(path), self.fileN)
                    )

        os.remove(path.replace(".exe", ".zip"))
        self.current_app_progress.update(
            self.current_task_id, description="[bold green] ChromeDriver Baixado!"
        )


def get_chrome_version():
    """Gets the Chrome version."""
    version = None
    install_path = None

    try:
        system = platform.system().lower()
        if system == "linux" or system == "linux2":
            # linux
            install_path = "/usr/bin/google-chrome"
        elif platform == "darwin":
            # OS X
            install_path = (
                r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
            )
        elif system == "windows":
            # Windows...
            try:
                # Try registry key.
                stream = os.popen(
                    r'reg query "HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome"'
                )
                output = stream.read()
                version = extract_version_registry(output)
            except Exception:
                # Try folder path.
                version = extract_version_folder()
    except Exception as ex:
        print(ex)

    version = (
        os.popen(f"{install_path} --version").read().strip("Google Chrome ").strip()
        if install_path
        else version
    )

    return version


def extract_version_registry(output):
    """Extracts the Chrome version from the registry output."""
    try:
        google_version = ""
        for letter in output[output.rindex("DisplayVersion    REG_SZ") + 24:]:
            if letter != "\n":
                google_version += letter
            else:
                break
        return google_version.strip()
    except TypeError:
        return


def extract_version_folder():
    """Extracts the Chrome version from the folder name.

    Check if the Chrome folder exists in the x32 or x64 Program Files folders.
    """
    for i in range(2):
        path = (
            r"C:\Program Files"
            + (" (x86)" if i else "")
            + r"\Google\Chrome\Application"
        )
        if os.path.isdir(path):
            paths = [f.path for f in os.scandir(path) if f.is_dir()]
            for path in paths:
                filename = os.path.basename(path)
                pattern = r"\d+\.\d+\.\d+\.\d+"
                match = re.search(pattern, filename)
                if match and match.group():
                    # Found a Chrome version.
                    return match.group(0)

    return None
