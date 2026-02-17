"""
ユーザー認証ロジックを提供するモジュール。
"""
import hashlib
import os
from database.database import get_db_connection
import sqlite3

def hash_password(password, salt=None):
    """
    パスワードをハッシュ化します。

    Args:
        password (str): 平文のパスワード
        salt (bytes, optional): ソルト。指定がない場合は新しく生成します。

    Returns:
        tuple: (ハッシュ化されたパスワード(hex文字列), ソルト(hex文字列))
    """
    if salt is None:
        salt = os.urandom(16)
    else:
        # saltがhex文字列の場合はbytesに変換
        if isinstance(salt, str):
            salt = bytes.fromhex(salt)

    # PBKDF2を使用してパスワードをハッシュ化
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )

    return pwd_hash.hex(), salt.hex()

def create_user(username, password):
    """
    新しいユーザーを作成します。

    Args:
        username (str): ユーザー名
        password (str): パスワード

    Returns:
        bool: 作成に成功した場合はTrue、失敗した場合（ユーザー名重複など）はFalse
    """
    password_hash, salt = hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)',
            (username, password_hash, salt)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # ユーザー名が重複している場合など
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    """
    ユーザーを認証します。

    Args:
        username (str): ユーザー名
        password (str): パスワード

    Returns:
        bool: 認証に成功した場合はTrue、失敗した場合はFalse
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT password_hash, salt FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        stored_password_hash = user['password_hash']
        stored_salt = user['salt']

        # 入力されたパスワードを同じソルトでハッシュ化して比較
        calculated_hash, _ = hash_password(password, stored_salt)

        if calculated_hash == stored_password_hash:
            return True

    return False
