import flet as ft

from constants import LOGO_PATH

# help classes
button_style: dict = {
    "expand": True,
    "height": 50,
    "bgcolor": "blue",
    "style": ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)}),
    "color": "white"
}


class Button(ft.ElevatedButton):
    def __init__(self, text: str, on_click):
        super().__init__(**button_style, text=text, on_click=on_click)


body_style: dict = {
    "width": 400,
    "padding": 15,
    "bgcolor": ft.colors.with_opacity(0.045, "white"),
    "border_radius": 10,
    "shadow": ft.BoxShadow(
        spread_radius=20,
        blur_radius=45,
        color=ft.colors.with_opacity(0.45, "black"),
    )
}


class Body(ft.Container):
    def __init__(self):
        super().__init__(**body_style)
        self.logo = ft.Image(
            width=100,
            height=100,
            expand=True,
            src=LOGO_PATH,
        )
        self.logo_text = ft.Text(
            value="FoxHub",
            weight=ft.FontWeight.BOLD,
            color=ft.colors.with_opacity(1, "White"),
            size=30,
            expand=1,
            text_align="center"
        )

        self.welcome_text = ft.Text(
            value='Добро пожаловать',
            size=34,
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
            expand=1
        )

        self.content = ft.Column(
            controls=[
                ft.Row([self.logo], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.logo_text], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Row([self.welcome_text], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([Button('Вход', on_click=lambda e: self.login_click(e))]),
                ft.Row([Button('Регистрация', on_click=lambda e: self.register_click(e))]),
            ]
        )

    @staticmethod
    def register_click(e: ft.ControlEvent) -> None:
        e.page.route = '/register'
        e.page.update()

    @staticmethod
    def login_click(e: ft.ControlEvent) -> None:
        e.page.route = '/login'
        e.page.update()


stack = ft.Stack(
    expand=True,
    controls=[
        ft.Column(
            alignment="center",
            horizontal_alignment="center",
            controls=[
                ft.Row(alignment='center', controls=[Body()])
            ]
        )
    ]
)
