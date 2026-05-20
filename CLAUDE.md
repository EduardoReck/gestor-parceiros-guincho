# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run in development:**
```bash
# Activate the virtual environment first
venv\Scripts\activate
python main.py
```

**Build the Windows executable:**
```bash
pyinstaller GestorParceiros.spec
# Output: dist\GestorParceiros.exe
```

There is no test suite and no linter configured.

## Architecture

**Gestor de Parceiros** is a Windows desktop app (PySide6 + SQLite) for managing business partners (seguradoras/guincho companies) with their legal data and attached documents.

### Data flow

```
main.py
  └─ inicializar_banco()       # creates data/ dir, configures logging, runs migrations
  └─ verificar_atualizacao()   # GitHub Releases API (only when sys.frozen == True)
  └─ JanelaPrincipal           # main window
       ├─ filtrar_parceiros()  # calls listar_parceiros or buscar_parceiros
       ├─ FormParceiro         # add dialog  ─┐
       ├─ FormEdicao           # edit dialog  ├─ both inherit FormParceiroBase
       └─ DocumentosParceiro   # file manager─┘
```

### Database (`database.py`)

Single SQLite file at `data/database.db`. Connection-per-call pattern (open → query → close). `inicializar_banco()` runs `ALTER TABLE` migrations on startup to add new columns non-destructively — safe to call on existing databases.

The `parceiros` table has an `ativo` column (1=active, 0=archived). All read functions accept `filtro_ativo` — `None` means all records, `1` means active only (default), `0` means archived. Errors are logged to `data/app.log` and either return empty results or re-raise depending on the function.

`_SELECT_COLS` is a module-level constant containing the shared column list used in all SELECT queries — update it whenever the schema changes.

### UI layer (`interface.py`)

`JanelaPrincipal` is the main window. The table always has 11 columns in this order: `ID, Nome, Nome Fantasia, CNPJ, Telefone, Cidade, Email, CEP, IE, Responsável, Observações`. Column 0 (ID) is the key used to open `FormEdicao` and to archive records. `_FILTRO_MAP = [1, None, 0]` maps the combo-box index to the `filtro_ativo` value.

**Two save paths exist:**
- `FormEdicao.salvar()` — saves a single record with validation (preferred)
- `salvar_alteracoes()` (F5) — bulk-saves inline table edits via `atualizar_parceiros_batch()` with no validation

### Form inheritance (`form_base.py`)

`FormParceiroBase` owns all 10 field widgets, the shared validation logic (`_validar()`), and field collection (`_coletar_dados()`). Subclasses override `_cnpj_label()` and `_botao_label()` and implement `salvar()`. The template-method pattern means `_cnpj_label()` called inside `__init__` resolves to the subclass version via Python MRO.

### Auto-update (`updater.py`)

`verificar_atualizacao()` is a no-op in dev (`sys.frozen` is False). In the compiled exe it hits the GitHub Releases API, compares semantic versions, and returns the `.exe` asset download URL if a newer release exists. `baixar_e_aplicar_update()` downloads the new exe alongside the current one, then writes and launches `_update.bat` which replaces the file and restarts the app after a 2-second delay.

**Before building a release**, update `GITHUB_API_URL` in `updater.py` to point to the real repository, and bump `VERSION` in `version.py`.

### Document storage

`DocumentosParceiro` (dialog, not used inline in the main window) stores files under `arquivos/parceiro_{id}/`. The "Documentos (F4)" button in the main window opens Windows Explorer at `documentos/parceiro_{id}/` — these are **two different directories**. This inconsistency is a known issue.

### Files to ignore

`models.py` and `ui/main_window.py` are unused leftovers from early development.

## Release workflow

1. Update `VERSION` in [version.py](version.py)
2. Update `GITHUB_API_URL` in [updater.py](updater.py) if not already pointing to the real repo
3. Build: `pyinstaller GestorParceiros.spec`
4. On GitHub: create a new Release with tag `vX.Y.Z`, attach `dist\GestorParceiros.exe` as an asset
