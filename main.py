import flet as ft
from flet_route import Routing
from views.routes import all_routes


def main(page: ft.Page):
    page.title = 'test'

    route = Routing(page=page, app_routes=all_routes)
    page.on_route_change = route.change_route
    page.go('/')


ft.app(target=main)
