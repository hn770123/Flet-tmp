"""
メインアプリケーションモジュール。
Fletを使用したHello Worldアプリケーションのエントリーポイントです。
"""
import flet as ft

def main(page: ft.Page):
    """
    アプリケーションのメイン関数。
    ページに"Hello World"のテキストを追加します。
    """
    page.title = "Flet Hello World"
    page.add(ft.Text(value="Hello, world!"))

if __name__ == "__main__":
    ft.run(main)
