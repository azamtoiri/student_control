import flet as ft
from flet_route import Params, Basket

from user_controls.student_app_bar import STAppBar
from views.not_registered_view import NotRegistered


def MiddleWareCheckAuthUser(page: ft.Page, params: Params, basket: Basket) -> ft.View or None:
    if page.session.get('is_auth') is not True:
        page.session.clear()
        return NotRegistered(page, params, basket)
