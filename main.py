import sys
from PySide6.QtWidgets import QApplication

from database import inicializar_banco
from interface import JanelaPrincipal


def main():
    inicializar_banco()

    app = QApplication(sys.argv)

    janela = JanelaPrincipal()
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()