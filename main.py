import sys
import os

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon

from core.database import inicializar_banco
from ui.interface import JanelaPrincipal
from ui.theme import THEMES, load_theme
from version import VERSION
from core.updater import verificar_atualizacao, baixar_e_aplicar_update


def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("documentos", exist_ok=True)
    os.makedirs("lixeira", exist_ok=True)
    inicializar_banco()

    app = QApplication(sys.argv)
    app.setStyleSheet(THEMES[load_theme()])
    if os.path.exists("assets/icon.ico"):
        app.setWindowIcon(QIcon("assets/icon.ico"))

    tem_update, nova_versao, url = verificar_atualizacao(VERSION)
    if tem_update:
        resp = QMessageBox.question(
            None,
            "Atualização Disponível",
            f"Nova versão {nova_versao} disponível!\n"
            f"Deseja atualizar agora?\n"
            f"(O aplicativo será reiniciado automaticamente)",
            QMessageBox.Yes | QMessageBox.No
        )
        if resp == QMessageBox.Yes:
            try:
                baixar_e_aplicar_update(url)
            except Exception as e:
                QMessageBox.warning(
                    None,
                    "Erro na atualização",
                    f"Não foi possível atualizar:\n{e}"
                )

    janela = JanelaPrincipal()
    janela.setWindowTitle(f"Gestor de Parceiros v{VERSION}")
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
