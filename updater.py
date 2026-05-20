import urllib.request
import json
import os
import sys
import subprocess

GITHUB_API_URL = "https://api.github.com/repos/EduardoReck/gestor-parceiros-guincho/releases/latest"


def verificar_atualizacao(versao_atual):
    # Só verifica quando rodando como exe compilado (não em dev)
    if not getattr(sys, 'frozen', False):
        return False, versao_atual, ""

    try:
        req = urllib.request.Request(
            GITHUB_API_URL,
            headers={"User-Agent": "GestorParceiros"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())

        tag = data["tag_name"].lstrip("v")

        if _versao_maior(tag, versao_atual):
            for asset in data.get("assets", []):
                if asset["name"].endswith(".exe"):
                    return True, tag, asset["browser_download_url"]

        return False, versao_atual, ""
    except Exception:
        return False, versao_atual, ""


def _versao_maior(nova, atual):
    try:
        return tuple(int(x) for x in nova.split(".")) > tuple(int(x) for x in atual.split("."))
    except (ValueError, AttributeError):
        return False


def baixar_e_aplicar_update(url_download, janela_pai=None):
    from PySide6.QtWidgets import QProgressDialog, QApplication
    from PySide6.QtCore import Qt

    caminho_atual = sys.executable
    caminho_novo = caminho_atual + ".new"

    progress = QProgressDialog("Baixando atualização...", None, 0, 100, janela_pai)
    progress.setWindowModality(Qt.WindowModal)
    progress.setWindowTitle("Atualizando")
    progress.show()
    QApplication.processEvents()

    def reporthook(block_num, block_size, total_size):
        if total_size > 0:
            percent = min(int(block_num * block_size * 100 / total_size), 100)
            progress.setValue(percent)
            QApplication.processEvents()

    try:
        urllib.request.urlretrieve(url_download, caminho_novo, reporthook)
    except Exception as e:
        progress.close()
        raise RuntimeError(f"Falha no download: {e}")

    progress.close()

    # Script batch substitui o exe após o app fechar e relança
    script = (
        "@echo off\r\n"
        "timeout /t 2 /nobreak > nul\r\n"
        f'move /y "{caminho_novo}" "{caminho_atual}"\r\n'
        f'start "" "{caminho_atual}"\r\n'
        'del "%~f0"\r\n'
    )
    script_path = os.path.join(os.path.dirname(caminho_atual), "_update.bat")
    with open(script_path, "w") as f:
        f.write(script)

    subprocess.Popen(script_path, shell=True)
    sys.exit(0)
