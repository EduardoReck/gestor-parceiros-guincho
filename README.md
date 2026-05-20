# Gestor de Parceiros

Aplicativo desktop Windows para gerenciar parceiros comerciais — seguradoras e empresas de guincho — com dados jurídicos, documentos e atualização automática via GitHub.

---

## Funcionalidades

- **Cadastro completo** de parceiros com Razão Social, Nome Fantasia, CNPJ, Telefone, Cidade, Email, CEP, Inscrição Estadual, Responsável e Observações
- **Preenchimento automático via Receita Federal** — digite o CNPJ e os campos são preenchidos automaticamente consultando a base pública da Receita Federal
- **Máscara inteligente** — CNPJ e telefone formatam sozinhos enquanto você digita
- **Busca em tempo real** com filtros Ativos / Inativos / Todos
- **Edição inline** diretamente na tabela com salvamento em lote
- **Arquivamento** de parceiros inativos (sem exclusão permanente)
- **Exportação CSV** para o Desktop com um clique
- **Atualização automática** — ao abrir, o app verifica se há nova versão no GitHub e atualiza sem intervenção manual

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Interface | [PySide6](https://doc.qt.io/qtforpython/) (Qt6 para Python) |
| Banco de dados | SQLite (via `sqlite3` da stdlib) |
| Empacotamento | [PyInstaller](https://pyinstaller.org/) — gera `.exe` standalone |
| Auto-update | GitHub Releases API + `urllib` |
| Dados de CNPJ | [BrasilAPI](https://brasilapi.com.br/) |

---

## Instalação

Não requer Python nem nenhuma dependência — basta baixar e executar.

1. Acesse a [página de releases](https://github.com/EduardoReck/gestor-parceiros-guincho/releases/latest)
2. Baixe `GestorParceiros.exe`
3. Execute — na primeira abertura, a pasta `data/` é criada automaticamente

---

## Estrutura do projeto

```
main.py          ← entry point
version.py       ← controle de versão

core/
  database.py    ← operações SQLite
  validators.py  ← validação e formatação de CNPJ, email, telefone
  updater.py     ← verificação e aplicação de atualizações via GitHub

ui/
  interface.py          ← janela principal com tabela e filtros
  form_base.py          ← base compartilhada dos formulários
  form_parceiro.py      ← formulário de novo parceiro
  form_edicao.py        ← formulário de edição
  documentos_parceiro.py ← gerenciador de arquivos por parceiro
```

---

## Desenvolvimento local

**Pré-requisitos:** Python 3.11+

```bash
# Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar
python main.py
```

**Gerar o executável:**

```bash
pyinstaller GestorParceiros.spec
# Saída: dist\GestorParceiros.exe
```

---

## Fluxo de atualização

Ao abrir o `.exe`, o app consulta a GitHub Releases API comparando a versão atual com a mais recente. Se houver atualização disponível, o usuário é perguntado e o download + substituição acontecem automaticamente, reiniciando o app na nova versão.

```
Abre o .exe
    └─ Consulta GitHub API
        └─ Nova versão disponível?
            ├─ Não → abre normalmente
            └─ Sim → pergunta ao usuário → baixa → substitui → reinicia
```

---

## Licença

MIT
