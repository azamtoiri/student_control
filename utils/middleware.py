import flet as ft
from flet_route import Params, Basket


async def MiddleWareCheckAuthUser(page: ft.Page, params: Params, basket: Basket) -> None:
    if page.session.get('is_auth') is not True:
        page.route = '/not-registered'

    if page.session.get('is_staff'):
        if page.route == '/home-edit' or page.route == '/todo': return
        if page.session.get('is_auth') and page.session.get('is_staff'):
            page.route = '/not-registered'


async def MiddleWareCheckIsStaff(page: ft.Page, params: Params, basket: Basket) -> None:
    if page.session.get('is_staff') is None:
        page.route = '/not-teacher'
    if page.session.get('is_staff') is not True:
        if page.session.get('is_auth') and page.session.get('is_staff'):
            page.route = '/not-teacher'
