from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QMessageBox,
)
import json
import re
import urllib.request

from core.validators import validar_cnpj, validar_email, validar_telefone, formatar_cnpj, formatar_telefone, formatar_cep
from core.database import buscar_parceiro_por_cnpj


class FormParceiroBase(QDialog):

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(640)

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
        self.rua = QLineEdit()
        self.numero = QLineEdit()
        self.numero.setPlaceholderText("Nº")
        self.bairro = QLineEdit()
        self.complemento = QLineEdit()
        self.complemento.setPlaceholderText("Apto, sala…")
        self.inscricao_estadual = QLineEdit()
        self.responsavel = QLineEdit()
        self.observacoes = QLineEdit()

        pares = [
            ("Nome *",                self.nome),
            ("Nome Fantasia",         self.nome_fantasia),
            (self._cnpj_label(),      self.cnpj),
            ("Telefone",              self.telefone),
            ("CEP",                   self.cep),
            ("Cidade",                self.cidade),
            ("Rua",                   self.rua),
            ("Número",                self.numero),
            ("Bairro",                self.bairro),
            ("Complemento",           self.complemento),
            ("Email",                 self.email),
            ("Inscrição Estadual",    self.inscricao_estadual),
            ("Responsável",           self.responsavel),
            ("Observações",           self.observacoes),
        ]

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(8)
        grid.setContentsMargins(20, 20, 20, 20)

        for i, (label, widget) in enumerate(pares):
            row, base_col = divmod(i, 2)
            col = base_col * 2
            grid.addWidget(QLabel(label), row, col)
            grid.addWidget(widget, row, col + 1)

        botao = QPushButton(self._botao_label())
        botao.clicked.connect(self.salvar)
        grid.addWidget(botao, len(pares) // 2, 0, 1, 4)

        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        self.setLayout(grid)

        self.cnpj.textEdited.connect(self._on_cnpj_edited)
        self.telefone.textEdited.connect(self._on_telefone_edited)
        self.cep.textEdited.connect(self._on_cep_edited)
        self.cnpj.editingFinished.connect(self._buscar_dados_cnpj)

    def _cnpj_label(self):
        return "CNPJ"

    def _botao_label(self):
        return "Salvar"

    def _on_cnpj_edited(self, texto):
        formatado = formatar_cnpj(texto)
        self.cnpj.blockSignals(True)
        self.cnpj.setText(formatado)
        self.cnpj.setCursorPosition(len(formatado))
        self.cnpj.blockSignals(False)

    def _on_telefone_edited(self, texto):
        formatado = formatar_telefone(texto)
        self.telefone.blockSignals(True)
        self.telefone.setText(formatado)
        self.telefone.setCursorPosition(len(formatado))
        self.telefone.blockSignals(False)

    def _on_cep_edited(self, texto):
        formatado = formatar_cep(texto)
        self.cep.blockSignals(True)
        self.cep.setText(formatado)
        self.cep.setCursorPosition(len(formatado))
        self.cep.blockSignals(False)

    def _buscar_dados_cnpj(self):
        digits = re.sub(r'\D', '', self.cnpj.text())
        if len(digits) != 14:
            return

        existente = buscar_parceiro_por_cnpj(digits)
        if existente and existente[0] != getattr(self, 'parceiro_id', None):
            QMessageBox.warning(
                self, "CNPJ já cadastrado",
                f"Este CNPJ já está registrado para:\n{existente[1]}"
            )
            return

        try:
            url = f"https://brasilapi.com.br/api/cnpj/v1/{digits}"
            req = urllib.request.Request(url, headers={"User-Agent": "GestorParceiros"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                dados = json.loads(resp.read())
        except Exception:
            return

        self.nome.setText(dados.get("razao_social") or "")
        self.nome_fantasia.setText(dados.get("nome_fantasia") or "")
        self.cidade.setText(dados.get("municipio") or "")
        self.email.setText(dados.get("email") or "")
        self.cep.setText(formatar_cep(dados.get("cep") or ""))
        self.telefone.setText(formatar_telefone(dados.get("ddd_telefone_1") or ""))
        self.rua.setText(dados.get("logradouro") or "")
        self.numero.setText(dados.get("numero") or "")
        self.bairro.setText(dados.get("bairro") or "")
        self.complemento.setText(dados.get("complemento") or "")
        qsa = dados.get("qsa") or []
        if qsa:
            self.responsavel.setText(qsa[0].get("nome_socio") or "")

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

        if cnpj:
            existente = buscar_parceiro_por_cnpj(re.sub(r'\D', '', cnpj))
            if existente and existente[0] != getattr(self, 'parceiro_id', None):
                QMessageBox.warning(
                    self, "CNPJ já cadastrado",
                    f"Este CNPJ já está registrado para:\n{existente[1]}"
                )
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
            self.rua.text().strip(),
            self.numero.text().strip(),
            self.bairro.text().strip(),
            self.complemento.text().strip(),
            self.inscricao_estadual.text().strip(),
            self.responsavel.text().strip(),
            self.observacoes.text().strip(),
        )

    def salvar(self):
        raise NotImplementedError
