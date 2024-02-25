from flet_route import path

from views.index_view import IndexView

all_routes = [
    path('/', clear=False, view=IndexView)
]
