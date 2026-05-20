from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QMessageBox,
)

from validators import validar_cnpj, validar_email, validar_telefone


class FormParceiroBase(QDialog):

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        self.nome = QLineEdit()
        self.nome_fantasia = QLineEdit()
        self.cnpj = QLineEdit()
        self.cnpj.setPlaceholderText("00.000.000/0000-00")
        self.telefone = QLineEdit()
        self.telefone.setPlaceholderText("(00) 00000-0000")
        self.cidade = QLineEdit()
        self.email = QLineEdit()
        self.cep = QLineEdit()
        self.cep.setPlaceholderText("00000-000")
        self.inscricao_estadual = QLineEdit()
        self.responsavel = QLineEdit()
        self.observacoes = QLineEdit()

        campos = [
            ("Nome *", self.nome),
            ("Nome Fantasia", self.nome_fantasia),
            (self._cnpj_label(), self.cnpj),
            ("Telefone", self.telefone),
            ("Cidade", self.cidade),
            ("Email", self.email),
            ("CEP", self.cep),
            ("Inscrição Estadual", self.inscricao_estadual),
            ("Responsável", self.responsavel),
            ("Observações", self.observacoes),
        ]

        for label_text, widget in campos:
            layout.addWidget(QLabel(label_text))
            layout.addWidget(widget)

        botao = QPushButton(self._botao_label())
        botao.clicked.connect(self.salvar)
        layout.addWidget(botao)

        self.setLayout(layout)

    def _cnpj_label(self):
        return "CNPJ"

    def _botao_label(self):
        return "Salvar"

    def _validar(self):
        nome = self.nome.text().strip()
        cnpj = self.cnpj.text().strip()
        email = self.email.text().strip()
        telefone = self.telefone.text().strip()

        if not nome:
            QMessageBox.warning(self, "Campo obrigatório", "O campo Nome é obrigatório.")
            self.nome.setFocus()
            return False

        if cnpj and not validar_cnpj(cnpj):
            QMessageBox.warning(self, "CNPJ inválido", "O CNPJ informado não é válido.")
            self.cnpj.setFocus()
            return False

        if not validar_email(email):
            QMessageBox.warning(self, "Email inválido", "O email informado não é válido.")
            self.email.setFocus()
            return False

        if not validar_telefone(telefone):
            QMessageBox.warning(self, "Telefone inválido", "O telefone deve ter 10 ou 11 dígitos.")
            self.telefone.setFocus()
            return False

        return True

    def _coletar_dados(self):
        return (
            self.nome.text().strip(),
            self.nome_fantasia.text().strip(),
            self.cnpj.text().strip(),
            self.telefone.text().strip(),
            self.cidade.text().strip(),
            self.email.text().strip(),
            self.cep.text().strip(),
            self.inscricao_estadual.text().strip(),
            self.responsavel.text().strip(),
            self.observacoes.text().strip(),
        )

    def salvar(self):
        raise NotImplementedError
