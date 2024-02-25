from flet_route import path

from views.index_view import IndexView
from views.default_views.login_veiw import LoginView
from views.default_views.register_view import RegisterView

from views.student_views import MainView, CoursesView, GradesView, HomeView, TasksView, ProfileView

all_routes = [
    # region: base views
    path('/', clear=False, view=IndexView),
    path('/login', clear=False, view=LoginView),
    path('/register', clear=False, view=RegisterView),
    # endregion

    # region: student views
    path('/student/main', clear=False, view=MainView),
    path('/student/courses', clear=False, view=CoursesView),
    path('/student/grades', clear=False, view=GradesView),
    path('/student/home', clear=False, view=HomeView),
    path('/student/profile', clear=False, view=ProfileView),
    path('/student/tasks', clear=False, view=TasksView),
    # endregion

    # region: teacher views

    # endregion

    # region: administrator views

    # endregion
]
