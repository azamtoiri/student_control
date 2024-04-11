import flet as ft


def display_success_banner(page: ft.Page, message: str, icons: ft.icons = ft.icons.SUNNY, duration=300) -> None:
    banner = ft.SnackBar(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(message, color=ft.colors.WHITE), ft.Icon(icons, color=ft.colors.WHITE)
            ]
        ),
        bgcolor=ft.colors.SURFACE_TINT, duration=duration,
    )
    page.snack_bar = banner
    page.show_snack_bar(banner)
    page.update()
