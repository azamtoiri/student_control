import flet as ft


def create_container(content, col=None) -> ft.Container:
    box_shadow = ft.BoxShadow(
        color=ft.colors.SURFACE_TINT,
        offset=ft.Offset(1, 2),
        blur_radius=10,
    )

    container = ft.Container(
        bgcolor=ft.colors.SURFACE_VARIANT, border_radius=8, padding=ft.padding.all(10),
        alignment=ft.alignment.center
    )
    container.shadow = box_shadow
    container.content = content
    if col:
        container.col = col

    return container


def create_expand_container(content, col=None):
    box_shadow = ft.BoxShadow(
        color=ft.colors.SURFACE_TINT,
        offset=ft.Offset(1, 2),
        blur_radius=8,
    )

    container = ft.Container(
        bgcolor=ft.colors.SURFACE_VARIANT, border_radius=8, padding=ft.padding.all(10),
        alignment=ft.alignment.top_left, expand=1, height=200
    )
    container.shadow = box_shadow
    container.content = ft.Column(
        [
            content
        ]
    )
    if col:
        container.col = col

    return container
