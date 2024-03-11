from flet_route import path

from utils.routes_url import BaseRoutes, StudentRoutes, TeacherRoutes

from views.index_view import IndexView
from views.default_views.login_veiw import LoginView
from views.default_views.register_view import RegisterView

from views.student_views import MainView, SubjectsView, GradesView, HomeView, TasksView, TodoView
from views.student_views.subject_view import SubjectView
from views.teacher_views.main_view import TeacherMainView
from views.not_registered_view import NotRegistered

all_routes = [
    # region: base views
    path(BaseRoutes.INDEX_URL, clear=True, view=IndexView),
    path(BaseRoutes.LOGIN_URL, clear=True, view=LoginView),
    path(BaseRoutes.REGISTER_URL, clear=True, view=RegisterView),
    # endregion

    # region: student views
    path(url=StudentRoutes.MAIN_URL, clear=True, view=MainView),
    path(url=StudentRoutes.SUBJECTS_URL, clear=False, view=SubjectsView),
    path(url=StudentRoutes.GRADES_URL, clear=False, view=GradesView),
    path(url=StudentRoutes.HOME_URL, clear=False, view=HomeView),
    path(url=BaseRoutes.TODO_URL, clear=False, view=TodoView),
    path(url=StudentRoutes.TASKS_URL, clear=False, view=TasksView),
    path(url=StudentRoutes.SUBJECT_URL, clear=False, view=SubjectView),

    # endregion

    # region: teacher views
    path(url=TeacherRoutes.MAIN_URL, clear=False, view=TeacherMainView),

    # endregion

    # region: administrator views

    # endregion

    # not registred
    path('/not-registered', clear=False, view=NotRegistered),
]
