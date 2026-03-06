from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Parceiros - Guinchos")
        self.resize(900, 500)

        layout = QVBoxLayout()

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels([
            "Nome",
            "Nome Fantasia",
            "CNPJ",
            "Telefone",
            "Cidade"
        ])

        btn_adicionar = QPushButton("Adicionar parceiro")

        layout.addWidget(self.tabela)
        layout.addWidget(btn_adicionar)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)