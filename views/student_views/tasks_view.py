import flet as ft
from flet_route import Params, Basket

from utils.routes_url import StudentRoutes


def TasksView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    return ft.View(
        route=StudentRoutes.TASKS_URL,
        controls=[]
    )
