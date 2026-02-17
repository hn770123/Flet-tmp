"""
ホーム画面のビューモジュール。
ログイン後に表示されるメイン画面です。
"""
import flet as ft

class HomeView(ft.Column):
    """
    ホーム画面のコンポーネント。
    """
    def __init__(self):
        super().__init__()
        self.controls = [
            ft.Text(value="Hello, world!", size=30),
            ft.Text("ログインに成功しました。", size=20)
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
