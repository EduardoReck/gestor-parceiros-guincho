import sqlite3
import os

DB_PATH = os.path.join("data", "database.db")


def conectar():
    return sqlite3.connect(DB_PATH)


def inicializar_banco():
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
    cep TEXT
    )
    """)

    conn.commit()
    conn.close()


def listar_parceiros():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nome, nome_fantasia, cnpj, telefone, cidade, email, cep
    FROM parceiros
    """)

    dados = cursor.fetchall()

    conn.close()
    return dados

def buscar_parceiros(texto):

    conn = conectar()
    cursor = conn.cursor()

    texto = f"%{texto}%"

    cursor.execute("""
    SELECT id, nome, nome_fantasia, cnpj, telefone, cidade, email, cep
    FROM parceiros
    WHERE
        nome LIKE ?
        OR nome_fantasia LIKE ?
        OR cnpj LIKE ?
        OR telefone LIKE ?
        OR cidade LIKE ?
        OR email LIKE ?
        OR cep LIKE ?
    """, (texto, texto, texto, texto, texto, texto, texto))

    dados = cursor.fetchall()

    conn.close()
    return dados


def adicionar_parceiro(nome, nome_fantasia, cnpj, telefone, cidade, email, cep):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO parceiros 
        (nome, nome_fantasia, cnpj, telefone, cidade, email, cep)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nome, nome_fantasia, cnpj, telefone, cidade, email, cep))

    parceiro_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return parceiro_id

def excluir_parceiro(id_parceiro):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM parceiros WHERE id = ?", (id_parceiro,))

    conn.commit()
    conn.close()