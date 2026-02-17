"""
データベース接続と初期化を行うモジュール。
"""
import sqlite3
import os

DB_FILE = "app.db"

def get_db_connection():
    """
    データベースへの接続を取得します。

    Returns:
        sqlite3.Connection: データベース接続オブジェクト
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    データベースを初期化し、必要なテーブルを作成します。
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # ユーザーテーブルの作成
    # id: 自動インクリメントの主キー
    # username: ユーザー名（ユニーク）
    # password_hash: ハッシュ化されたパスワード
    # salt: パスワードハッシュ化に使用したソルト
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
