import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime

from werkzeug.security import generate_password_hash

from config import ADMIN_PASSWORD, ADMIN_USER, DB_PATH


@contextmanager
def connect():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with connect() as conn:
        conn.execute("PRAGMA auto_vacuum = INCREMENTAL")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contratos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                dados TEXT NOT NULL,
                imagem TEXT,
                pdf TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute("UPDATE contratos SET pdf = NULL WHERE pdf IS NOT NULL")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS imagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                content_type TEXT NOT NULL,
                conteudo BLOB NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login_at TEXT
            )
            """
        )
        if ADMIN_PASSWORD and not _has_users(conn):
            _create_user(conn, ADMIN_USER, ADMIN_PASSWORD)


def _has_users(conn):
    row = conn.execute("SELECT 1 FROM usuarios LIMIT 1").fetchone()
    return row is not None


def _create_user(conn, username, password):
    now = datetime.now().isoformat(timespec="seconds")
    cursor = conn.execute(
        """
        INSERT INTO usuarios (username, password_hash, created_at)
        VALUES (?, ?, ?)
        """,
        (username, generate_password_hash(password), now),
    )
    return cursor.lastrowid


def has_users():
    with connect() as conn:
        return _has_users(conn)


def create_user(username, password):
    with connect() as conn:
        return _create_user(conn, username, password)


def get_user_by_username(username):
    with connect() as conn:
        return conn.execute("SELECT * FROM usuarios WHERE username = ?", (username,)).fetchone()


def get_user(user_id):
    with connect() as conn:
        return conn.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()


def mark_user_login(user_id):
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as conn:
        conn.execute("UPDATE usuarios SET last_login_at = ? WHERE id = ?", (now, user_id))


def list_contracts():
    with connect() as conn:
        return conn.execute(
            "SELECT id, titulo, imagem, created_at, updated_at FROM contratos ORDER BY updated_at DESC"
        ).fetchall()


def list_contract_rows():
    with connect() as conn:
        return conn.execute("SELECT * FROM contratos ORDER BY updated_at DESC").fetchall()


def get_contract(contract_id):
    with connect() as conn:
        return conn.execute("SELECT * FROM contratos WHERE id = ?", (contract_id,)).fetchone()


def delete_contract(contract_id):
    with connect() as conn:
        conn.execute("DELETE FROM contratos WHERE id = ?", (contract_id,))


def save_contract(values, image_ref, contract_id=None):
    now = datetime.now().isoformat(timespec="seconds")
    title = values.get("nomeContratante") or "Contrato sem nome"
    payload = json.dumps(values, ensure_ascii=False, separators=(",", ":"))

    with connect() as conn:
        if contract_id:
            conn.execute(
                """
                UPDATE contratos
                SET titulo = ?, dados = ?, imagem = ?, pdf = NULL, updated_at = ?
                WHERE id = ?
                """,
                (title, payload, image_ref, now, contract_id),
            )
            return int(contract_id)

        cursor = conn.execute(
            """
            INSERT INTO contratos (titulo, dados, imagem, pdf, created_at, updated_at)
            VALUES (?, ?, ?, NULL, ?, ?)
            """,
            (title, payload, image_ref, now, now),
        )
        return cursor.lastrowid


def update_contract_values(contract_id, values):
    now = datetime.now().isoformat(timespec="seconds")
    title = values.get("nomeContratante") or "Contrato sem nome"
    payload = json.dumps(values, ensure_ascii=False, separators=(",", ":"))
    with connect() as conn:
        conn.execute(
            """
            UPDATE contratos
            SET titulo = ?, dados = ?, updated_at = ?
            WHERE id = ?
            """,
            (title, payload, now, contract_id),
        )


def insert_image(name, content_type, content):
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO imagens (nome, content_type, conteudo, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (name, content_type, content, now),
        )
        return cursor.lastrowid


def get_image(image_id):
    with connect() as conn:
        return conn.execute("SELECT * FROM imagens WHERE id = ?", (image_id,)).fetchone()


def list_uploaded_images():
    with connect() as conn:
        return conn.execute(
            "SELECT id, nome, content_type, created_at FROM imagens ORDER BY created_at DESC"
        ).fetchall()
