import os
import shutil

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QMessageBox,
    QFileIconProvider,
)
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt, QFileInfo


def _formatar_tamanho(n):
    for unidade in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unidade}"
        n /= 1024
    return f"{n:.1f} GB"


class DropListWidget(QListWidget):
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QPainter(self.viewport())
            painter.setPen(QColor("#9E9E9E"))
            painter.drawText(
                self.viewport().rect(),
                Qt.AlignCenter,
                "Arraste arquivos aqui\nou clique em  Adicionar",
            )


class DocumentosParceiro(QDialog):

    def __init__(self, id_parceiro, nome_parceiro=""):
        super().__init__()

        self.id_parceiro = id_parceiro
        self.pasta = os.path.join("documentos", f"parceiro_{id_parceiro}")
        os.makedirs(self.pasta, exist_ok=True)

        titulo = f"Documentos — {nome_parceiro}" if nome_parceiro else f"Documentos — Parceiro {id_parceiro}"
        self.setWindowTitle(titulo)
        self.resize(480, 420)
        self.setAcceptDrops(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.lista = DropListWidget()
        self.lista.setIconSize(self.lista.iconSize().__class__(24, 24))
        layout.addWidget(self.lista)

        layout_botoes = QHBoxLayout()

        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_abrir = QPushButton("Abrir")
        self.botao_excluir = QPushButton("Excluir")

        layout_botoes.addWidget(self.botao_adicionar)
        layout_botoes.addWidget(self.botao_abrir)
        layout_botoes.addStretch()
        layout_botoes.addWidget(self.botao_excluir)

        layout.addLayout(layout_botoes)
        self.setLayout(layout)

        self.botao_adicionar.clicked.connect(self.adicionar_arquivo)
        self.botao_abrir.clicked.connect(self.abrir_arquivo)
        self.botao_excluir.clicked.connect(self.excluir_arquivo)

        self.carregar_arquivos()

    # --- drag and drop ---

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            caminho = url.toLocalFile()
            if os.path.isfile(caminho):
                shutil.copy(caminho, os.path.join(self.pasta, os.path.basename(caminho)))
        self.carregar_arquivos()
        event.acceptProposedAction()

    # --- file list ---

    def carregar_arquivos(self):
        self.lista.clear()
        provider = QFileIconProvider()
        for arquivo in sorted(os.listdir(self.pasta)):
            caminho = os.path.join(self.pasta, arquivo)
            tamanho = _formatar_tamanho(os.path.getsize(caminho))
            item = QListWidgetItem(
                provider.icon(QFileInfo(caminho)),
                f"{arquivo}  ({tamanho})"
            )
            item.setData(Qt.UserRole, arquivo)
            self.lista.addItem(item)

    def _arquivo_selecionado(self):
        item = self.lista.currentItem()
        if not item:
            return None
        return item.data(Qt.UserRole)

    def adicionar_arquivo(self):
        caminhos, _ = QFileDialog.getOpenFileNames(self, "Selecionar arquivos")
        for caminho in caminhos:
            if caminho:
                shutil.copy(caminho, os.path.join(self.pasta, os.path.basename(caminho)))
        if caminhos:
            self.carregar_arquivos()

    def abrir_arquivo(self):
        nome = self._arquivo_selecionado()
        if not nome:
            return
        os.startfile(os.path.join(self.pasta, nome))

    def excluir_arquivo(self):
        nome = self._arquivo_selecionado()
        if not nome:
            return
        resp = QMessageBox.question(
            self,
            "Excluir arquivo",
            f"Excluir '{nome}'?"
        )
        if resp == QMessageBox.Yes:
            os.remove(os.path.join(self.pasta, nome))
            self.carregar_arquivos()
