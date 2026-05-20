import json
import os

_SETTINGS_PATH = os.path.join("data", "settings.json")


def load_theme():
    try:
        with open(_SETTINGS_PATH) as f:
            return json.load(f).get("theme", "light")
    except Exception:
        return "light"


def save_theme(name):
    os.makedirs("data", exist_ok=True)
    data = {}
    try:
        with open(_SETTINGS_PATH) as f:
            data = json.load(f)
    except Exception:
        pass
    data["theme"] = name
    with open(_SETTINGS_PATH, "w") as f:
        json.dump(data, f)


LIGHT = """
QMainWindow, QDialog { background-color: #F5F7FA; }
QWidget { background-color: #F5F7FA; }
QLabel { color: #212529; font-size: 13px; }
QLineEdit, QComboBox {
    background-color: #FFFFFF; border: 1px solid #CED4DA;
    border-radius: 4px; padding: 6px 10px; font-size: 13px;
    color: #212529; min-height: 20px;
}
QLineEdit:focus, QComboBox:focus { border-color: #5C7A9B; }
QComboBox QAbstractItemView {
    background-color: #FFFFFF; color: #212529;
    selection-background-color: #5C7A9B; selection-color: #FFFFFF;
    border: 1px solid #CED4DA;
}
QPushButton {
    background-color: #5C7A9B; color: #FFFFFF; border: none;
    border-radius: 4px; padding: 7px 16px; font-size: 13px;
    font-weight: bold; min-height: 32px;
}
QPushButton:hover   { background-color: #4A6585; }
QPushButton:pressed { background-color: #3A5272; }
QPushButton#botao_novo         { background-color: #5C8A6A; }
QPushButton#botao_novo:hover   { background-color: #4A7258; }
QPushButton#botao_arquivar     { background-color: #A06040; }
QPushButton#botao_arquivar:hover { background-color: #8A5035; }
QPushButton#botao_exportar     { background-color: #5C7A8A; }
QPushButton#botao_exportar:hover { background-color: #4A6575; }
QPushButton#botao_tema         { background-color: #6B7B8A; }
QPushButton#botao_tema:hover   { background-color: #5A6A78; }
QTableWidget {
    background-color: #FFFFFF; alternate-background-color: #EEF4FC;
    color: #212529; gridline-color: #E9ECEF;
    border: 1px solid #DEE2E6; border-radius: 4px;
    selection-background-color: #C8D8E8; selection-color: #212529;
    font-size: 13px;
}
QTableWidget::item { color: #212529; }
QHeaderView::section {
    background-color: #5C7A9B; color: #FFFFFF;
    padding: 8px 10px; border: none; font-weight: bold;
}
QListWidget {
    background-color: #FFFFFF; color: #212529;
    border: 1px solid #DEE2E6; border-radius: 4px; font-size: 13px;
}
QListWidget::item:selected { background-color: #C8D8E8; color: #212529; }
QListWidget::item:hover    { background-color: #E8F0F8; }
QScrollBar:vertical {
    background: #F0F0F0; width: 8px; border-radius: 4px;
}
QScrollBar::handle:vertical { background: #B0B8C8; border-radius: 4px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
"""

DARK = """
QMainWindow, QDialog { background-color: #1F1F1F; }
QWidget { background-color: #1F1F1F; }
QLabel { color: #E0E0E0; font-size: 13px; }
QLineEdit, QComboBox {
    background-color: #2B2B2B; border: 1px solid #555555;
    border-radius: 4px; padding: 6px 10px; font-size: 13px;
    color: #E0E0E0; min-height: 20px;
}
QLineEdit:focus, QComboBox:focus { border-color: #6B8FAD; }
QComboBox QAbstractItemView {
    background-color: #2B2B2B; color: #E0E0E0;
    selection-background-color: #6B8FAD; selection-color: #FFFFFF;
    border: 1px solid #555555;
}
QPushButton {
    background-color: #6B8FAD; color: #FFFFFF; border: none;
    border-radius: 4px; padding: 7px 16px; font-size: 13px;
    font-weight: bold; min-height: 32px;
}
QPushButton:hover   { background-color: #5A7A99; }
QPushButton:pressed { background-color: #4A6585; }
QPushButton#botao_novo         { background-color: #6B9E7A; }
QPushButton#botao_novo:hover   { background-color: #5A8A68; }
QPushButton#botao_arquivar     { background-color: #B87050; }
QPushButton#botao_arquivar:hover { background-color: #9A5E40; }
QPushButton#botao_exportar     { background-color: #6B8A9A; }
QPushButton#botao_exportar:hover { background-color: #5A7888; }
QPushButton#botao_tema         { background-color: #7A8B9A; }
QPushButton#botao_tema:hover   { background-color: #697888; }
QTableWidget {
    background-color: #2B2B2B; alternate-background-color: #262626;
    color: #E0E0E0; gridline-color: #3A3A3A;
    border: 1px solid #3A3A3A; border-radius: 4px;
    selection-background-color: #3D5A75; selection-color: #FFFFFF;
    font-size: 13px;
}
QTableWidget::item { color: #E0E0E0; }
QHeaderView::section {
    background-color: #263238; color: #ECEFF1;
    padding: 8px 10px; border: none; font-weight: bold;
}
QListWidget {
    background-color: #2B2B2B; color: #E0E0E0;
    border: 1px solid #3A3A3A; border-radius: 4px; font-size: 13px;
}
QListWidget::item:selected { background-color: #3D5A75; color: #FFFFFF; }
QListWidget::item:hover    { background-color: #323A42; }
QScrollBar:vertical {
    background: #2B2B2B; width: 8px; border-radius: 4px;
}
QScrollBar::handle:vertical { background: #555555; border-radius: 4px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
"""

THEMES = {"light": LIGHT, "dark": DARK}
