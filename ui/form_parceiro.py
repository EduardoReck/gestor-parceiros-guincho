from PySide6.QtWidgets import QMessageBox

from core.database import adicionar_parceiro
from ui.form_base import FormParceiroBase


class FormParceiro(FormParceiroBase):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Novo Parceiro")

    def _cnpj_label(self):
        return "CNPJ *"

    def salvar(self):
        if not self._validar():
            return
        adicionar_parceiro(*self._coletar_dados())
        QMessageBox.information(self, "Sucesso", "Parceiro cadastrado!")
        self.accept()
