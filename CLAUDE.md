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

**Publish a new release (requires `gh` CLI authenticated):**
```bash
gh release create vX.Y.Z "dist/GestorParceiros.exe" --title "Versão X.Y.Z" --notes "..."
```

There is no test suite and no linter configured.

## Architecture

**Gestor de Parceiros** is a Windows desktop app (PySide6 + SQLite) for managing business partners (seguradoras/guincho companies) with their legal data and attached documents.

### Structure

```
main.py          ← entry point
version.py       ← VERSION constant

core/
  database.py    ← all SQLite operations
  validators.py  ← CNPJ, email, phone validation
  updater.py     ← GitHub Releases auto-update

ui/
  interface.py        ← JanelaPrincipal (main window)
  form_base.py        ← FormParceiroBase (shared base class)
  form_parceiro.py    ← add partner dialog
  form_edicao.py      ← edit partner dialog
  documentos_parceiro.py ← file manager dialog
```

### Data flow

```
main.py
  └─ core.database.inicializar_banco()  # creates data/ dir, runs migrations
  └─ core.updater.verificar_atualizacao()  # GitHub API (only when sys.frozen)
  └─ ui.interface.JanelaPrincipal       # main window
       ├─ filtrar_parceiros()           # calls listar_parceiros or buscar_parceiros
       ├─ ui.form_parceiro.FormParceiro    ─┐
       ├─ ui.form_edicao.FormEdicao        ├─ both inherit ui.form_base.FormParceiroBase
       └─ ui.documentos_parceiro.DocumentosParceiro
```

### Database (`core/database.py`)

Single SQLite file at `data/database.db`. Connection-per-call pattern (open → query → close). `inicializar_banco()` runs `ALTER TABLE` migrations on startup to add new columns non-destructively — safe to call on existing databases.

The `parceiros` table has an `ativo` column (1=active, 0=archived). All read functions accept `filtro_ativo` — `None` means all records, `1` means active only (default), `0` means archived. Errors are logged to `data/app.log` and either return empty results or re-raise depending on the function.

`_SELECT_COLS` is a module-level constant containing the shared column list used in all SELECT queries — update it whenever the schema changes.

### UI layer (`ui/interface.py`)

`JanelaPrincipal` is the main window. The table has 15 columns in this order: `ID, Nome, Nome Fantasia, CNPJ, Telefone, Cidade, Email, CEP, Rua, Número, Bairro, Complemento, IE, Responsável, Observações`. Column 0 (ID) is the key used to open `FormEdicao` and to archive records. `_FILTRO_MAP = [1, None, 0]` maps the combo-box index to the `filtro_ativo` value.

**Two save paths exist:**
- `FormEdicao.salvar()` — saves a single record with validation (preferred)
- `salvar_alteracoes()` (F6) — bulk-saves inline table edits via `atualizar_parceiros_batch()` with no validation

### Form inheritance (`ui/form_base.py`)

`FormParceiroBase` owns all 14 field widgets, the shared validation logic (`_validar()`), and field collection (`_coletar_dados()`). Subclasses override `_cnpj_label()` and `_botao_label()` and implement `salvar()`. The template-method pattern means `_cnpj_label()` called inside `__init__` resolves to the subclass version via Python MRO.

Fields: nome, nome_fantasia, cnpj, telefone, cidade, email, cep, rua, numero, bairro, complemento, inscricao_estadual, responsavel, observacoes. Live formatting via `textEdited` + `blockSignals` applies to cnpj, telefone, and cep. `editingFinished` on cnpj triggers BrasilAPI lookup which fills all address fields automatically.

### Auto-update (`core/updater.py`)

`verificar_atualizacao()` is a no-op in dev (`sys.frozen` is False). In the compiled exe it hits the GitHub Releases API at `https://api.github.com/repos/EduardoReck/gestor-parceiros-guincho/releases/latest`, compares semantic versions, and returns the `.exe` asset download URL if a newer release exists. `baixar_e_aplicar_update()` downloads the new exe alongside the current one, then writes and launches `_update.bat` which replaces the file and restarts the app after a 2-second delay.

### Document storage

`ui/documentos_parceiro.py` (dialog) and the "Documentos (F4)" button in the main window both store and open files under `documentos/parceiro_{id}/`. This directory is created at startup by `main.py`.

### Files to ignore

`ui/main_window.py` was an unused leftover — it has been deleted.

## Release workflow

**GitHub repository:** https://github.com/EduardoReck/gestor-parceiros-guincho

**Current version:** `1.2.0` — release `v1.2.0` already published.

To ship a new version:

1. Update `VERSION` in [version.py](version.py) (e.g. `"1.1.0"`)
2. Commit and push:
   ```bash
   git add .
   git commit -m "..."
   git push
   ```
3. Build the exe:
   ```bash
   pyinstaller GestorParceiros.spec
   ```
4. Publish the release (`gh` CLI must be authenticated via `gh auth login`):
   ```bash
   gh release create v1.2.0 "dist/GestorParceiros.exe" --title "Versão 1.2.0" --notes "..."
   ```

Users running the previous `.exe` will be prompted to update automatically on next launch.

**Installing on a new machine:** download `GestorParceiros.exe` from the latest release — no Python or dependencies needed.
