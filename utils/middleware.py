import flet as ft
from flet_route import Params, Basket


def MiddleWareCheckAuthUser(page: ft.Page, params: Params, basket: Basket) -> None:
    if page.session.get('is_auth') is not True:
        page.route = '/not-registered'

    if page.session.get('is_staff'):
        if page.route == '/home-edit': return
        if page.session.get('is_auth') and page.session.get('is_staff'):
            page.route = '/not-registered'


def MiddleWareCheckIsStaff(page: ft.Page, params: Params, basket: Basket) -> None:
    if page.session.get('is_staff') is None:
        page.route = '/not-teacher'
    if page.session.get('is_staff') is not True:
        if page.session.get('is_auth') and page.session.get('is_staff'):
            page.route = '/not-teacher'
