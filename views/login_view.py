"""
ログイン画面のビューモジュール。
ユーザー名とパスワードの入力、およびログイン処理を提供します。
"""
import flet as ft

class LoginView(ft.Column):
    """
    ログイン画面のコンポーネント。
    ユーザー名とパスワードの入力を受け付け、ログイン処理を行います。
    """
    def __init__(self, on_login_success):
        """
        コンストラクタ。

        Args:
            on_login_success (function): ログイン成功時に呼び出されるコールバック関数。
        """
        super().__init__()
        self.on_login_success = on_login_success

        # UIコンポーネントの初期化
        self.username_field = ft.TextField(label="ユーザー名")
        self.password_field = ft.TextField(
            label="パスワード",
            password=True,
            can_reveal_password=True  # パスワード表示切り替え機能を有効化
        )
        self.login_button = ft.ElevatedButton(
            text="ログイン",
            on_click=self.login
        )
        self.error_text = ft.Text(color=ft.colors.RED)

        # コントロールの配置
        self.controls = [
            ft.Text("ログイン", size=30, weight=ft.FontWeight.BOLD),
            self.username_field,
            self.password_field,
            self.error_text,
            self.login_button
        ]

        # レイアウト設定
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        # 画面中央に配置するために幅を設定
        self.width = 300

    def login(self, e):
        """
        ログインボタンクリック時の処理。
        入力チェックを行い、問題なければ成功コールバックを実行します。

        Args:
            e (ft.ControlEvent): イベントオブジェクト。
        """
        if not self.username_field.value or not self.password_field.value:
            self.error_text.value = "ユーザー名とパスワードを入力してください。"
            self.update()
        else:
            # ここに実際の認証ロジックを実装する（現在はダミー）
            self.on_login_success()
