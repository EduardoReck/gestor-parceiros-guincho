from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QMessageBox
)

from database import adicionar_parceiro


class FormParceiro(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Novo Parceiro")

        layout = QVBoxLayout()

        self.nome = QLineEdit()
        self.nome_fantasia = QLineEdit()
        self.cnpj = QLineEdit()
        self.telefone = QLineEdit()
        self.cidade = QLineEdit()
        self.email = QLineEdit()
        self.cep = QLineEdit()

        layout.addWidget(QLabel("Nome"))
        layout.addWidget(self.nome)

        layout.addWidget(QLabel("Nome Fantasia"))
        layout.addWidget(self.nome_fantasia)

        layout.addWidget(QLabel("CNPJ"))
        layout.addWidget(self.cnpj)

        layout.addWidget(QLabel("Telefone"))
        layout.addWidget(self.telefone)

        layout.addWidget(QLabel("Cidade"))
        layout.addWidget(self.cidade)

        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email)

        layout.addWidget(QLabel("CEP"))
        layout.addWidget(self.cep)

        botao_salvar = QPushButton("Salvar")
        botao_salvar.clicked.connect(self.salvar)

        layout.addWidget(botao_salvar)

        self.setLayout(layout)

    def salvar(self):

        adicionar_parceiro(
            self.nome.text(),
            self.nome_fantasia.text(),
            self.cnpj.text(),
            self.telefone.text(),
            self.cidade.text(),
            self.email.text(),
            self.cep.text()
        )

        QMessageBox.information(self, "Sucesso", "Parceiro cadastrado!")

        self.accept()