# バックエンド分離とサーバー稼働の手順

このドキュメントでは、現在のFletアプリケーション（スタンドアロン構成）から、バックエンド（データベース処理）を分離してサーバー上で動作させるクライアント・サーバー構成への移行手順をまとめます。

## 構成の変更点

*   **変更前**: クライアントアプリが直接SQLiteデータベースファイル(`app.db`)を読み書きする。
*   **変更後**:
    *   **サーバー**: データベース操作を行うWeb API (FastAPI) を提供する。
    *   **クライアント**: API経由でデータの取得・更新を行う。データベースファイルには直接アクセスしない。

---

## 1. 必要なライブラリのインストール

サーバー機能（FastAPI）とHTTP通信（requests）のために、以下のライブラリを追加します。

```bash
pip install fastapi uvicorn requests
```

`requirements.txt` にも以下を追加してください。

```txt
fastapi
uvicorn
requests
```

---

## 2. サーバー側の実装 (`server.py`)

プロジェクトのルートディレクトリに `server.py` を作成します。
このファイルがAPIサーバーのエントリーポイントとなり、既存の `database` モジュールを利用してデータベース操作を行います。

```python
# server.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database.database import init_db
from database.auth import authenticate_user, create_user
import uvicorn

app = FastAPI()

# リクエストボディの定義
class UserAuth(BaseModel):
    username: str
    password: str

@app.on_event("startup")
def on_startup():
    """サーバー起動時にデータベースを初期化"""
    init_db()
    # 初期ユーザーの作成（必要に応じて）
    create_user("admin", "password")

@app.post("/login")
def login(auth: UserAuth):
    """ログインAPI"""
    if authenticate_user(auth.username, auth.password):
        return {"status": "success", "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/register")
def register(auth: UserAuth):
    """ユーザー登録API（必要に応じて実装）"""
    if create_user(auth.username, auth.password):
        return {"status": "success", "message": "User created"}
    else:
        raise HTTPException(status_code=400, detail="User already exists")

if __name__ == "__main__":
    # 開発用サーバー起動設定
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 3. クライアント側の修正

### 3.1. `views/login_view.py` の修正

直接 `database.auth` をインポートするのをやめ、APIサーバーへリクエストを送るように変更します。

**修正前:**
```python
from database.auth import authenticate_user
# ...
            if authenticate_user(username, password):
                self.on_login_success()
            else:
                self.error_text.value = "ユーザー名またはパスワードが間違っています。"
```

**修正後:**
```python
import requests
# database.auth のインポートは削除

# ... (中略) ...

    def login(self, e):
        # ... (入力チェックなどはそのまま) ...

            username = self.username_field.value
            password = self.password_field.value

            # APIサーバーのURL (環境に合わせて変更してください)
            API_URL = "http://localhost:8000/login"

            try:
                response = requests.post(
                    API_URL,
                    json={"username": username, "password": password},
                    timeout=5
                )

                if response.status_code == 200:
                    self.on_login_success()
                elif response.status_code == 401:
                    self.error_text.value = "ユーザー名またはパスワードが間違っています。"
                    self.update()
                else:
                    self.error_text.value = f"エラーが発生しました: {response.status_code}"
                    self.update()

            except requests.exceptions.RequestException as ex:
                self.error_text.value = "サーバーに接続できませんでした。"
                self.update()
                print(ex)
```

### 3.2. `main.py` の修正

`main.py` で行っていたデータベースの初期化処理はサーバー側に移譲したため、削除します。

**修正箇所:**
1. `from database.database import init_db` を削除
2. `from database.auth import create_user` を削除
3. `init_db()` の呼び出しを削除
4. `create_user(...)` の呼び出しを削除

---

## 4. 実行手順

### 手順1: サーバーの起動

まず、APIサーバーを起動します。

```bash
python server.py
# または
uvicorn server:app --reload
```

これによって `http://localhost:8000` でAPIが待ち受け状態になります。

### 手順2: クライアントの起動

別のターミナルでクライアントアプリを起動します。

```bash
flet run main.py
# または
python main.py
```

クライアントからログイン操作を行うと、サーバー側のログにリクエストが表示され、認証が行われます。

## 注意事項

*   **セキュリティ**: 本番環境で運用する場合は、パスワードの平文送信を避けるため、HTTPS化（SSL/TLS）が必須です。
*   **エラーハンドリング**: ネットワークエラー時の再試行処理などを適宜追加してください。
*   **構成管理**: サーバーとクライアントを別のマシンで動かす場合は、`API_URL` をサーバーのIPアドレスまたはドメインに変更してください。
