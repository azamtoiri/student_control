import flet as ft
from flet_route import Params, Basket


def TasksView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    return ft.View(
        route='/student/tasks',
        controls=[]
    )