import flet as ft
from flet_route import Params, Basket

from views.not_registered_view import NotRegistered


def MiddleWareCheckAuthUser(page: ft.Page, params: Params, basket: Basket) -> ft.View or str:
    if page.session.get('is_auth') is not True:
        page.session.clear()
        return NotRegistered(page, params, basket)
    else:
        return page.go_async(page.route)
