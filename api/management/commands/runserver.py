import os
import sys
import socket
from datetime import datetime
from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command as StaticfilesRunserverCommand


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.255.255.255", 1))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            try:
                return socket.gethostbyname(socket.gethostname())
            except Exception:
                return "127.0.0.1"


class Command(StaticfilesRunserverCommand):
    default_addr = "0.0.0.0"
    default_port = "8000"

    def on_bind(self, server_port):
        quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"

        if self._raw_ipv6:
            addr = f"[{self.addr}]"
        elif self.addr == "0":
            addr = "0.0.0.0"
        else:
            addr = self.addr

        now = datetime.now().strftime("%B %d, %Y - %X")
        version = self.get_version()
        local_ip = get_local_ip()

        print(
            f"{now}\n"
            f"Django version {version}, using settings {settings.SETTINGS_MODULE!r}\n\n"
            f"VayuLens Server\n"
            f"----------------------------------------\n"
            f"Local:   {self.protocol}://127.0.0.1:{server_port}/\n"
            f"Network: {self.protocol}://{local_ip}:{server_port}/\n"
            f"----------------------------------------\n\n"
            f"Starting development server at {self.protocol}://{addr}:{server_port}/\n"
            f"Quit the server with {quit_command}.",
            file=self.stdout,
        )
        if os.environ.get("DJANGO_RUNSERVER_HIDE_WARNING") != "true":
            self.stdout.write(
                self.style.WARNING(
                    "WARNING: This is a development server. Do not use it in a "
                    "production setting. Use a production WSGI or ASGI server "
                    "instead.\n"
                )
            )
