import sqlite3
import os
import logging

DB_PATH = os.path.join("data", "database.db")

_SELECT_COLS = """
    id, nome, nome_fantasia, cnpj, telefone, cidade, email, cep,
    inscricao_estadual, responsavel, observacoes
"""

_logger = logging.getLogger(__name__)


def conectar():
    return sqlite3.connect(DB_PATH)


def inicializar_banco():
    os.makedirs("data", exist_ok=True)
    logging.basicConfig(
        filename=os.path.join("data", "app.log"),
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parceiros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        nome_fantasia TEXT,
        cnpj TEXT,
        telefone TEXT,
        cidade TEXT,
        email TEXT,
        cep TEXT,
        inscricao_estadual TEXT DEFAULT '',
        responsavel TEXT DEFAULT '',
        observacoes TEXT DEFAULT '',
        ativo INTEGER DEFAULT 1
    )
    """)

    for col, tipo in [
        ("inscricao_estadual", "TEXT DEFAULT ''"),
        ("responsavel", "TEXT DEFAULT ''"),
        ("observacoes", "TEXT DEFAULT ''"),
        ("ativo", "INTEGER DEFAULT 1"),
    ]:
        try:
            cursor.execute(f"ALTER TABLE parceiros ADD COLUMN {col} {tipo}")
        except Exception:
            pass

    conn.commit()
    conn.close()


def listar_parceiros(filtro_ativo=1):
    try:
        conn = conectar()
        cursor = conn.cursor()

        if filtro_ativo is None:
            cursor.execute(f"SELECT {_SELECT_COLS} FROM parceiros")
        else:
            cursor.execute(
                f"SELECT {_SELECT_COLS} FROM parceiros WHERE ativo = ?",
                (filtro_ativo,),
            )

        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception as e:
        _logger.error(f"listar_parceiros: {e}")
        return []


def buscar_parceiros(texto, filtro_ativo=1):
    try:
        conn = conectar()
        cursor = conn.cursor()

        texto_like = f"%{texto}%"
        query = f"""
        SELECT {_SELECT_COLS} FROM parceiros
        WHERE (
            nome LIKE ? OR nome_fantasia LIKE ? OR cnpj LIKE ?
            OR telefone LIKE ? OR cidade LIKE ? OR email LIKE ?
            OR cep LIKE ? OR inscricao_estadual LIKE ? OR responsavel LIKE ?
        )
        """
        params = [texto_like] * 9

        if filtro_ativo is not None:
            query += " AND ativo = ?"
            params.append(filtro_ativo)

        cursor.execute(query, params)
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception as e:
        _logger.error(f"buscar_parceiros: {e}")
        return []


def buscar_parceiro_por_id(id_parceiro):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT {_SELECT_COLS} FROM parceiros WHERE id = ?",
            (id_parceiro,),
        )
        row = cursor.fetchone()
        conn.close()
        return row
    except Exception as e:
        _logger.error(f"buscar_parceiro_por_id: {e}")
        return None


def adicionar_parceiro(nome, nome_fantasia, cnpj, telefone, cidade, email, cep,
                       inscricao_estadual='', responsavel='', observacoes=''):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO parceiros
            (nome, nome_fantasia, cnpj, telefone, cidade, email, cep,
             inscricao_estadual, responsavel, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, nome_fantasia, cnpj, telefone, cidade, email, cep,
              inscricao_estadual, responsavel, observacoes))
        parceiro_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return parceiro_id
    except Exception as e:
        _logger.error(f"adicionar_parceiro: {e}")
        return None


def atualizar_parceiro(id_parceiro, nome, nome_fantasia, cnpj, telefone, cidade, email, cep,
                       inscricao_estadual='', responsavel='', observacoes=''):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE parceiros
        SET nome=?, nome_fantasia=?, cnpj=?, telefone=?, cidade=?, email=?, cep=?,
            inscricao_estadual=?, responsavel=?, observacoes=?
        WHERE id=?
        """, (nome, nome_fantasia, cnpj, telefone, cidade, email, cep,
              inscricao_estadual, responsavel, observacoes, id_parceiro))
        conn.commit()
        conn.close()
    except Exception as e:
        _logger.error(f"atualizar_parceiro: {e}")
        raise


def atualizar_parceiros_batch(atualizacoes):
    """atualizacoes: list of tuples (nome, …, observacoes, id) para executemany."""
    if not atualizacoes:
        return
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.executemany("""
        UPDATE parceiros
        SET nome=?, nome_fantasia=?, cnpj=?, telefone=?, cidade=?, email=?, cep=?,
            inscricao_estadual=?, responsavel=?, observacoes=?
        WHERE id=?
        """, atualizacoes)
        conn.commit()
        conn.close()
    except Exception as e:
        _logger.error(f"atualizar_parceiros_batch: {e}")
        raise


def arquivar_parceiro(id_parceiro):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE parceiros SET ativo=0 WHERE id=?", (id_parceiro,))
        conn.commit()
        conn.close()
    except Exception as e:
        _logger.error(f"arquivar_parceiro: {e}")
        raise


def excluir_parceiro(id_parceiro):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM parceiros WHERE id = ?", (id_parceiro,))
        conn.commit()
        conn.close()
    except Exception as e:
        _logger.error(f"excluir_parceiro: {e}")
        raise
