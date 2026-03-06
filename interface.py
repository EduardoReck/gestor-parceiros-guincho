from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QInputDialog,
    QMessageBox,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)
import os
import subprocess

from form_parceiro import FormParceiro
from database import adicionar_parceiro, listar_parceiros, buscar_parceiros, excluir_parceiro, conectar
from documentos_parceiro import DocumentosParceiro

class JanelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestor de Parceiros")
        self.resize(800, 500)

        layout = QVBoxLayout()

        # Layout dos botões
        layout_botoes = QHBoxLayout()

        # Campo de busca
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar parceiro...")
        self.campo_busca.textChanged.connect(self.filtrar_parceiros)

        layout_botoes.addWidget(self.campo_busca)

        # Botão adicionar
        self.botao_novo = QPushButton("Adicionar parceiro (F1)")
        self.botao_novo.clicked.connect(self.abrir_form)
        self.botao_novo.setShortcut("F1")

        layout_botoes.addWidget(self.botao_novo)

        # Botão atualizar
        self.botao_atualizar = QPushButton("Atualizar lista (F2)")
        self.botao_atualizar.clicked.connect(self.carregar_parceiros)
        self.botao_atualizar.setShortcut("F2")

        layout_botoes.addWidget(self.botao_atualizar)

        # Botão excluir
        self.botao_excluir = QPushButton("Excluir parceiro (F3)")
        self.botao_excluir.clicked.connect(self.excluir_parceiro)
        self.botao_excluir.setShortcut("F3")

        layout_botoes.addWidget(self.botao_excluir)

        # Botão documentos
        self.botao_docs = QPushButton("Documentos do parceiro (F4)")
        self.botao_docs.clicked.connect(self.abrir_documentos)
        self.botao_docs.setShortcut("F4")

        layout_botoes.addWidget(self.botao_docs)

        # Botão salvar
        self.botao_salvar = QPushButton("Salvar alterações (F5)")
        self.botao_salvar.clicked.connect(self.salvar_alteracoes)
        self.botao_salvar.setShortcut("F5")

        layout_botoes.addWidget(self.botao_salvar)

        # adiciona linha de botões ao layout principal
        layout.addLayout(layout_botoes)

        # =====================
        # TABELA
        # =====================

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(8)
        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Nome",
            "Nome Fantasia",
            "CNPJ",
            "Telefone",
            "Cidade",
            "Email",
            "CEP"
        ])

        self.tabela.resizeColumnsToContents()
        self.tabela.setSortingEnabled(True)
        layout.addWidget(self.tabela)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.carregar_parceiros()

    def carregar_parceiros(self):

        parceiros = listar_parceiros()

        self.tabela.setRowCount(len(parceiros))

        for linha, parceiro in enumerate(parceiros):

            for coluna, valor in enumerate(parceiro):

                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(str(valor))
                )

    def abrir_form(self):

        form = FormParceiro()
    
        if form.exec():

            self.carregar_parceiros()
        

    def filtrar_parceiros(self):

        texto = self.campo_busca.text()

        if texto == "":
            parceiros = listar_parceiros()
        else:
            parceiros = buscar_parceiros(texto)

        self.tabela.setRowCount(len(parceiros))

        for linha, parceiro in enumerate(parceiros):
            for coluna, valor in enumerate(parceiro):
                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(str(valor))
                )   

    def excluir_parceiro(self):

        id_parceiro, ok = QInputDialog.getInt(
            self,
            "Excluir parceiro",
            "Digite o ID do parceiro que deseja excluir:"
        )

        if not ok:
            return

        confirmacao = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Tem certeza que deseja excluir o parceiro ID {id_parceiro}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmacao == QMessageBox.Yes:

            excluir_parceiro(id_parceiro)

            QMessageBox.information(
                self,
                "Sucesso",
                "Parceiro excluído."
            )

            self.carregar_parceiros()

    def abrir_documentos(self):

        linha = self.tabela.currentRow()

        if linha == -1:
            return

        parceiro_id = self.tabela.item(linha, 0).text()

        pasta = os.path.join("documentos", f"parceiro_{parceiro_id}")

        os.makedirs(pasta, exist_ok=True)

        subprocess.Popen(f'explorer "{pasta}"')

    def salvar_alteracoes(self):

        conn = conectar()
        cursor = conn.cursor()

        linhas = self.tabela.rowCount()

        for linha in range(linhas):

            id_parceiro = int(self.tabela.item(linha, 0).text())
            nome = self.tabela.item(linha, 1).text()
            nome_fantasia = self.tabela.item(linha, 2).text()
            cnpj = self.tabela.item(linha, 3).text()
            telefone = self.tabela.item(linha, 4).text()
            cidade = self.tabela.item(linha, 5).text()
            email = self.tabela.item(linha, 6).text()
            cep = self.tabela.item(linha, 7).text()

            cursor.execute("""
            UPDATE parceiros
            SET nome=?, nome_fantasia=?, cnpj=?, telefone=?, cidade=?, email=?, cep=?
            WHERE id=?
            """, (nome, nome_fantasia, cnpj, telefone, cidade, email, cep, id_parceiro))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "Sucesso", "Alterações salvas no banco.")
 