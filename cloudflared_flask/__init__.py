import atexit
import requests
import subprocess
import tarfile
import tempfile
import shutil
import os
import platform
import time
import re
import yaml
from random import randint
from threading import Timer
from pathlib import Path
from flask import Flask

CLOUDFLARED_CONFIG = {
    ('Windows', 'AMD64'): {
        'command': 'cloudflared-windows-amd64.exe',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe'
    },
    ('Windows', 'x86'): {
        'command': 'cloudflared-windows-386.exe',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-386.exe'
    },
    ('Linux', 'x86_64'): {
        'command': 'cloudflared-linux-amd64',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64'
    },
    ('Linux', 'i386'): {
        'command': 'cloudflared-linux-386',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386'
    },
    ('Linux', 'arm'): {
        'command': 'cloudflared-linux-arm',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm'
    },
    ('Linux', 'arm64'): {
        'command': 'cloudflared-linux-arm64',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64'
    },
    ('Linux', 'aarch64'): {
        'command': 'cloudflared-linux-arm64',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64'
    },
    ('Darwin', 'x86_64'): {
        'command': 'cloudflared',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz'
    },
    ('Darwin', 'arm64'): {
        'command': 'cloudflared',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz'
    }
}


class CloudFlared:
    
    def __init__(self, app: Flask):
        
        self.old_run = app.run
        self.app = app
        
    def recreate_run(self) -> Flask:
        
        self.app.run = self.new_run
        return self.app
     
    def new_run(self, metrics_port: int = randint(8100, 9000), 
                tunnel_id: str = None, config_path: str = None,
                port: int = 5000, *args, **kwargs):

        # Starting the Cloudflared tunnel in a separate thread.
        tunnel_args = (port, metrics_port, tunnel_id, config_path)
        thread = Timer(2, self.start_cloudflared, args=tunnel_args)
        thread.daemon = True
        thread.start()

        # Running the Flask app.
        self.old_run(*args, **kwargs)
   
    def _get_command(self, system: str, machine: str):
        try:
            return CLOUDFLARED_CONFIG[(system, machine)]['command']
        except KeyError:
            raise Exception(f"{machine} is not supported on {system}")

    def _get_url(self, system: str , machine: str):
        try:
            return CLOUDFLARED_CONFIG[(system, machine)]['url']
        except KeyError:
            raise Exception(f"{machine} is not supported on {system}")

    def read_one_block_of_yaml_data(self, filename):
        with open(f'{filename}.yaml','r') as f:
            output = yaml.safe_load(f)

    def _download_cloudflared(self, cloudflared_path, command):
        system, machine = platform.system(), platform.machine()
        if Path(cloudflared_path, command).exists():
            executable = (cloudflared_path+'/'+'cloudflared') if (system == "Darwin" and machine in ["x86_64", "arm64"]) else (cloudflared_path+'/'+command)
            update_cloudflared = subprocess.Popen([executable, 'update'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            return
        print(f" * Downloading cloudflared for {system} {machine}...")
        url = self._get_url(system, machine)
        self._download_file(url)

    def _download_file(self, url):
        local_filename = url.split('/')[-1]
        r = requests.get(url, stream=True)
        download_path = str(Path(tempfile.gettempdir(), local_filename))
        with open(download_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return download_path

    def _run_cloudflared(self, port, metrics_port, tunnel_id=None, config_path=None):
        system, machine = platform.system(), platform.machine()
        command = self._get_command(system, machine)
        cloudflared_path = str(Path(tempfile.gettempdir()))
        
        self._download_cloudflared(cloudflared_path, command)

        executable = str(Path(cloudflared_path, command))
        os.chmod(executable, 0o777)

        cloudflared_command = [executable, 'tunnel', '--metrics', f'127.0.0.1:{metrics_port}']
        if config_path:
            cloudflared_command.extend(['--config', config_path, 'run'])
        elif tunnel_id:
            cloudflared_command.extend(['--url', f'http://127.0.0.1:{port}', 'run', tunnel_id])
        elif not config_path and not tunnel_id:
            cloudflared_command.extend(['--url', f'http://127.0.0.1:{port}'])


        cloudflared = subprocess.Popen(cloudflared_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        atexit.register(cloudflared.terminate)
        localhost_url = f"http://127.0.0.1:{metrics_port}/metrics"

        for _ in range(10):
            try:
                metrics = requests.get(localhost_url).text
                if tunnel_id or config_path:
                    # If tunnel_id or config_path is provided, we check for cloudflared_tunnel_ha_connections, as no tunnel URL is available in the metrics
                    if re.search("cloudflared_tunnel_ha_connections\s\d", metrics):
                        # No tunnel URL is available in the metrics, so we return a generic text
                        tunnel_url = "preconfigured tunnel URL"
                        break
                else:
                    # If neither tunnel_id nor config_path is provided, we check for the tunnel URL in the metrics
                    tunnel_url = (re.search("(?P<url>https?:\/\/[^\s]+.trycloudflare.com)", metrics).group("url"))
                    break
            except:
                time.sleep(3)
        else:
            raise Exception(f"! Can't connect to Cloudflare Edge")

        return tunnel_url

    def start_cloudflared(self, port, metrics_port, tunnel_id=None, config_path=None):
        cloudflared_address = self._run_cloudflared(port, metrics_port, tunnel_id, config_path)
        print(f" * Running on {cloudflared_address}")
        print(f" * Traffic stats available on http://127.0.0.1:{metrics_port}/metrics")
