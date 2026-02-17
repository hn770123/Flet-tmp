"""
メインアプリケーションモジュール。
アプリケーションのエントリーポイントです。
"""
import flet as ft
from views.login_view import LoginView
from views.home_view import HomeView
from database.database import init_db
from database.auth import create_user

def main(page: ft.Page):
    """
    アプリケーションのメイン関数。
    初期画面としてログイン画面を表示し、ログイン成功後にホーム画面に遷移します。
    """
    # データベースの初期化
    init_db()

    # デフォルトユーザーの作成（存在しない場合）
    create_user("admin", "password")

    page.title = "Flet App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_login_success():
        """
        ログイン成功時の処理。
        ホーム画面に遷移します。
        """
        page.clean()
        page.add(HomeView())
        page.update()

    # 初期画面（ログイン画面）の表示
    login_view = LoginView(on_login_success)
    page.add(login_view)

if __name__ == "__main__":
    ft.run(main)
