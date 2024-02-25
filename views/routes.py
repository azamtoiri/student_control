from flet_route import path

from views.index_view import IndexView
from views.default_views.login_veiw import LoginView
from views.default_views.register_view import RegisterView

all_routes = [
    path('/', clear=False, view=IndexView),
    path('/login', clear=False, view=LoginView),
    path('/register', clear=False, view=RegisterView),
]
