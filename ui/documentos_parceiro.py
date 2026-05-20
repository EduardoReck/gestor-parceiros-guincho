import os
import shutil

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QFileDialog,
    QMessageBox
)


class DocumentosParceiro(QDialog):

    def __init__(self, id_parceiro):
        super().__init__()

        self.id_parceiro = id_parceiro

        self.setWindowTitle(f"Documentos do parceiro {id_parceiro}")

        layout = QVBoxLayout()

        self.lista = QListWidget()

        self.botao_adicionar = QPushButton("Adicionar arquivo")
        self.botao_abrir = QPushButton("Abrir arquivo")
        self.botao_excluir = QPushButton("Excluir arquivo")

        layout.addWidget(self.lista)
        layout.addWidget(self.botao_adicionar)
        layout.addWidget(self.botao_abrir)
        layout.addWidget(self.botao_excluir)

        self.setLayout(layout)

        self.botao_adicionar.clicked.connect(self.adicionar_arquivo)
        self.botao_abrir.clicked.connect(self.abrir_arquivo)
        self.botao_excluir.clicked.connect(self.excluir_arquivo)

        self.pasta = os.path.join("arquivos", f"parceiro_{id_parceiro}")

        os.makedirs(self.pasta, exist_ok=True)

        self.carregar_arquivos()

    def carregar_arquivos(self):

        self.lista.clear()

        arquivos = os.listdir(self.pasta)

        for arquivo in arquivos:
            self.lista.addItem(arquivo)

    def adicionar_arquivo(self):

        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo")

        if caminho:

            nome = os.path.basename(caminho)

            destino = os.path.join(self.pasta, nome)

            shutil.copy(caminho, destino)

            self.carregar_arquivos()

    def abrir_arquivo(self):

        item = self.lista.currentItem()

        if not item:
            return

        caminho = os.path.join(self.pasta, item.text())

        os.startfile(caminho)

    def excluir_arquivo(self):

        item = self.lista.currentItem()

        if not item:
            return

        resposta = QMessageBox.question(
            self,
            "Excluir arquivo",
            "Tem certeza que deseja excluir este arquivo?"
        )

        if resposta == QMessageBox.Yes:

            caminho = os.path.join(self.pasta, item.text())

            os.remove(caminho)

            self.carregar_arquivos()