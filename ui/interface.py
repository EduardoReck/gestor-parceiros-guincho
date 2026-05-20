from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLineEdit,
    QHBoxLayout,
    QComboBox,
    QLabel,
    QApplication,
)
import os
import csv
import re
from datetime import date

from ui.form_parceiro import FormParceiro
from ui.form_edicao import FormEdicao
from ui.documentos_parceiro import DocumentosParceiro
from ui.theme import THEMES, load_theme, save_theme
from core.database import (
    listar_parceiros, buscar_parceiros,
    arquivar_parceiro, desarquivar_parceiro, excluir_parceiro,
    atualizar_parceiros_batch,
)
from core.validators import formatar_cnpj

COLUNAS = [
    "ID",  # col 0, oculta
    "Nome Fantasia", "Nome", "CNPJ", "Telefone",
    "Cidade", "Email", "CEP", "Rua", "Número", "Bairro", "Complemento",
    "Observações"
]

_FILTRO_MAP = [1, None, 0]


class JanelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestor de Parceiros")
        self.resize(1200, 550)

        layout = QVBoxLayout()

        layout_busca = QHBoxLayout()
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar parceiro...")
        self.campo_busca.textChanged.connect(self.filtrar_parceiros)
        layout_busca.addWidget(self.campo_busca)
        layout_busca.addWidget(QLabel("Mostrar:"))
        self.combo_filtro = QComboBox()
        self.combo_filtro.addItems(["Ativos", "Todos", "Inativos"])
        self.combo_filtro.currentIndexChanged.connect(self.filtrar_parceiros)
        self.combo_filtro.currentIndexChanged.connect(self._atualizar_botoes_filtro)
        layout_busca.addWidget(self.combo_filtro)
        self._tema_atual = load_theme()
        self.botao_tema = QPushButton("☀️ Claro" if self._tema_atual == "dark" else "🌙 Escuro")
        self.botao_tema.setObjectName("botao_tema")
        self.botao_tema.setFixedWidth(110)
        self.botao_tema.clicked.connect(self._alternar_tema)
        layout_busca.addWidget(self.botao_tema)
        layout.addLayout(layout_busca)

        layout_botoes = QHBoxLayout()

        self.botao_novo = QPushButton("Adicionar (F1)")
        self.botao_novo.setObjectName("botao_novo")
        self.botao_novo.clicked.connect(self.abrir_form)
        self.botao_novo.setShortcut("F1")
        layout_botoes.addWidget(self.botao_novo)

        self.botao_editar = QPushButton("Editar (F2)")
        self.botao_editar.clicked.connect(self.editar_parceiro)
        self.botao_editar.setShortcut("F2")
        layout_botoes.addWidget(self.botao_editar)

        self.botao_atualizar = QPushButton("Atualizar (F3)")
        self.botao_atualizar.clicked.connect(self.filtrar_parceiros)
        self.botao_atualizar.setShortcut("F3")
        layout_botoes.addWidget(self.botao_atualizar)

        self.botao_arquivar = QPushButton("Arquivar (F4)")
        self.botao_arquivar.setObjectName("botao_arquivar")
        self.botao_arquivar.clicked.connect(self._arquivar_ou_desarquivar)
        self.botao_arquivar.setShortcut("F4")
        layout_botoes.addWidget(self.botao_arquivar)

        self.botao_excluir = QPushButton("Excluir (Del)")
        self.botao_excluir.setObjectName("botao_excluir")
        self.botao_excluir.clicked.connect(self.excluir_parceiro_ui)
        self.botao_excluir.setShortcut("Delete")
        self.botao_excluir.setEnabled(False)
        layout_botoes.addWidget(self.botao_excluir)

        self.botao_docs = QPushButton("Documentos (F5)")
        self.botao_docs.clicked.connect(self.abrir_documentos)
        self.botao_docs.setShortcut("F5")
        layout_botoes.addWidget(self.botao_docs)

        self.botao_salvar = QPushButton("Salvar (F6)")
        self.botao_salvar.clicked.connect(self.salvar_alteracoes)
        self.botao_salvar.setShortcut("F6")
        layout_botoes.addWidget(self.botao_salvar)

        self.botao_exportar = QPushButton("Exportar CSV (F7)")
        self.botao_exportar.setObjectName("botao_exportar")
        self.botao_exportar.clicked.connect(self.exportar_csv)
        self.botao_exportar.setShortcut("F7")
        layout_botoes.addWidget(self.botao_exportar)

        layout.addLayout(layout_botoes)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(len(COLUNAS))
        self.tabela.setHorizontalHeaderLabels(COLUNAS)
        self.tabela.resizeColumnsToContents()
        self.tabela.setSortingEnabled(True)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.doubleClicked.connect(self.editar_parceiro)
        layout.addWidget(self.tabela)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.filtrar_parceiros()
        self.tabela.setColumnHidden(0, True)

    def _get_filtro_ativo(self):
        return _FILTRO_MAP[self.combo_filtro.currentIndex()]

    def _alternar_tema(self):
        self._tema_atual = "dark" if self._tema_atual == "light" else "light"
        QApplication.instance().setStyleSheet(THEMES[self._tema_atual])
        self.botao_tema.setText("☀️ Claro" if self._tema_atual == "dark" else "🌙 Escuro")
        save_theme(self._tema_atual)

    def _preencher_tabela(self, parceiros):
        self.tabela.setSortingEnabled(False)
        self.tabela.setRowCount(len(parceiros))
        for linha, parceiro in enumerate(parceiros):
            for coluna, valor in enumerate(parceiro):
                self.tabela.setItem(
                    linha, coluna,
                    QTableWidgetItem(str(valor) if valor is not None else "")
                )
        self.tabela.setSortingEnabled(True)

    def filtrar_parceiros(self):
        texto = self.campo_busca.text()
        digits = re.sub(r'\D', '', texto)
        if len(digits) == 14 and not any(c in texto for c in './-'):
            texto = formatar_cnpj(texto)
        filtro_ativo = self._get_filtro_ativo()
        if texto:
            parceiros = buscar_parceiros(texto, filtro_ativo)
        else:
            parceiros = listar_parceiros(filtro_ativo)
        self._preencher_tabela(parceiros)

    def abrir_form(self):
        if FormParceiro().exec():
            self.filtrar_parceiros()

    def editar_parceiro(self):
        linha = self.tabela.currentRow()
        if linha == -1:
            QMessageBox.information(self, "Selecione um parceiro", "Clique em uma linha da tabela para selecionar.")
            return
        item = self.tabela.item(linha, 0)
        if item is None:
            return
        if FormEdicao(int(item.text())).exec():
            self.filtrar_parceiros()

    def _atualizar_botoes_filtro(self):
        eh_inativos = self.combo_filtro.currentIndex() == 2
        self.botao_arquivar.setText("Desarquivar (F4)" if eh_inativos else "Arquivar (F4)")
        self.botao_excluir.setEnabled(eh_inativos)

    def _arquivar_ou_desarquivar(self):
        linha = self.tabela.currentRow()
        if linha == -1:
            QMessageBox.information(self, "Selecione um parceiro", "Clique em uma linha da tabela para selecionar.")
            return
        item_id = self.tabela.item(linha, 0)
        item_nome = self.tabela.item(linha, 1)
        if item_id is None:
            return
        parceiro_id = int(item_id.text())
        nome = item_nome.text() if item_nome else str(parceiro_id)
        eh_inativos = self.combo_filtro.currentIndex() == 2
        if eh_inativos:
            resp = QMessageBox.question(
                self, "Desarquivar parceiro",
                f"Desarquivar '{nome}'?\nEle voltará a aparecer em 'Ativos'.",
                QMessageBox.Yes | QMessageBox.No
            )
            if resp == QMessageBox.Yes:
                try:
                    desarquivar_parceiro(parceiro_id)
                    self.filtrar_parceiros()
                except Exception:
                    QMessageBox.critical(self, "Erro", "Não foi possível desarquivar o parceiro.")
        else:
            resp = QMessageBox.question(
                self, "Arquivar parceiro",
                f"Arquivar '{nome}'?\nEle ficará visível em 'Inativos'.",
                QMessageBox.Yes | QMessageBox.No
            )
            if resp == QMessageBox.Yes:
                try:
                    arquivar_parceiro(parceiro_id)
                    self.filtrar_parceiros()
                except Exception:
                    QMessageBox.critical(self, "Erro", "Não foi possível arquivar o parceiro.")

    def excluir_parceiro_ui(self):
        linha = self.tabela.currentRow()
        if linha == -1:
            QMessageBox.information(self, "Selecione um parceiro", "Clique em uma linha da tabela para selecionar.")
            return
        item_id = self.tabela.item(linha, 0)
        item_nome = self.tabela.item(linha, 1)
        if item_id is None:
            return
        parceiro_id = int(item_id.text())
        nome = item_nome.text() if item_nome else str(parceiro_id)
        resp = QMessageBox.question(
            self,
            "Excluir parceiro permanentemente",
            f"Excluir '{nome}' permanentemente?\n\n"
            f"Os dados serão salvos em 'lixeira/' antes de serem removidos.\n"
            f"Esta ação não pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No
        )
        if resp == QMessageBox.Yes:
            try:
                excluir_parceiro(parceiro_id)
                self.filtrar_parceiros()
            except Exception:
                QMessageBox.critical(self, "Erro", "Não foi possível excluir o parceiro.")

    def abrir_documentos(self):
        linha = self.tabela.currentRow()
        if linha == -1:
            return
        parceiro_id = int(self.tabela.item(linha, 0).text())
        item_nome = self.tabela.item(linha, 1)
        nome = item_nome.text() if item_nome else str(parceiro_id)
        DocumentosParceiro(parceiro_id, nome).exec()

    def salvar_alteracoes(self):
        def cel(linha, col):
            item = self.tabela.item(linha, col)
            return item.text() if item else ""

        atualizacoes = []
        for linha in range(self.tabela.rowCount()):
            try:
                id_parceiro = int(cel(linha, 0))
                atualizacoes.append((
                    cel(linha, 1), cel(linha, 2), cel(linha, 3), cel(linha, 4),
                    cel(linha, 5), cel(linha, 6), cel(linha, 7),
                    cel(linha, 8), cel(linha, 9), cel(linha, 10), cel(linha, 11),
                    cel(linha, 12), id_parceiro,
                ))
            except ValueError:
                pass

        try:
            atualizar_parceiros_batch(atualizacoes)
            QMessageBox.information(self, "Sucesso", "Alterações salvas no banco.")
        except Exception:
            QMessageBox.warning(self, "Erro", "Não foi possível salvar as alterações.")

    def exportar_csv(self):
        filtro_ativo = self._get_filtro_ativo()
        parceiros = listar_parceiros(filtro_ativo)
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        nome_arquivo = f"parceiros_{date.today().isoformat()}.csv"
        caminho = os.path.join(desktop, nome_arquivo)
        try:
            with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(COLUNAS)
                writer.writerows(parceiros)
            QMessageBox.information(self, "Exportação concluída", f"Arquivo salvo em:\n{caminho}")
        except Exception as e:
            QMessageBox.critical(self, "Erro na exportação", f"Não foi possível exportar:\n{e}")
