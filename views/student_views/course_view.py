import flet as ft

from flet_route import Params, Basket


def CourseView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    return ft.View(
        route='/course/:id',
        controls=[
            ft.Text(f'course id: {params.get("id")}')
        ]
    )
