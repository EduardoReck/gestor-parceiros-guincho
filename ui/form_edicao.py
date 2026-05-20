from PySide6.QtWidgets import QMessageBox

from core.database import atualizar_parceiro, buscar_parceiro_por_id
from ui.form_base import FormParceiroBase


class FormEdicao(FormParceiroBase):

    def __init__(self, parceiro_id):
        self.parceiro_id = parceiro_id
        super().__init__()
        self.setWindowTitle(f"Editar Parceiro #{parceiro_id}")
        self._carregar_dados()

    def _botao_label(self):
        return "Salvar alterações"

    def _carregar_dados(self):
        parceiro = buscar_parceiro_por_id(self.parceiro_id)
        if not parceiro:
            return
        _, nome, nome_fantasia, cnpj, telefone, cidade, email, cep, ie, responsavel, obs = parceiro
        self.nome.setText(nome or "")
        self.nome_fantasia.setText(nome_fantasia or "")
        self.cnpj.setText(cnpj or "")
        self.telefone.setText(telefone or "")
        self.cidade.setText(cidade or "")
        self.email.setText(email or "")
        self.cep.setText(cep or "")
        self.inscricao_estadual.setText(ie or "")
        self.responsavel.setText(responsavel or "")
        self.observacoes.setText(obs or "")

    def salvar(self):
        if not self._validar():
            return
        try:
            atualizar_parceiro(self.parceiro_id, *self._coletar_dados())
            QMessageBox.information(self, "Sucesso", "Parceiro atualizado!")
            self.accept()
        except Exception:
            QMessageBox.critical(self, "Erro", "Não foi possível salvar as alterações.")
