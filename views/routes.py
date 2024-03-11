from flet_route import path

from utils.routes_url import BaseRoutes, StudentRoutes, TeacherRoutes
from views.default_views import LoginView, RegisterView
from views.index_view import IndexView
from views.not_registered_view import NotRegistered
from views.student_views import (
    HomeView,
    MainView,
    SubjectsView,
    GradesView,
    TasksView,
    TodoView,
    SubjectView
)
from views.teacher_views import (
    TeacherMainView,
    TeacherHomeView,
    MySubjectsView,
    MySubjectView,
    MyTasksView,
    SetGradesView
)

all_routes = [
    # region: base views
    path(BaseRoutes.INDEX_URL, clear=True, view=IndexView),
    path(BaseRoutes.LOGIN_URL, clear=True, view=LoginView),
    path(BaseRoutes.REGISTER_URL, clear=True, view=RegisterView),
    # endregion

    # region: student views
    path(url=StudentRoutes.MAIN_URL, clear=True, view=MainView),
    path(url=StudentRoutes.HOME_URL, clear=False, view=HomeView),
    path(url=StudentRoutes.SUBJECTS_URL, clear=False, view=SubjectsView),
    path(url=StudentRoutes.SUBJECT_URL, clear=False, view=SubjectView),
    path(url=StudentRoutes.GRADES_URL, clear=False, view=GradesView),
    path(url=StudentRoutes.TASKS_URL, clear=False, view=TasksView),
    path(url=BaseRoutes.TODO_URL, clear=False, view=TodoView),

    # endregion

    # region: teacher views
    path(url=TeacherRoutes.MAIN_URL, clear=False, view=TeacherMainView),
    path(url=TeacherRoutes.HOME_URL, clear=False, view=TeacherHomeView),
    path(url=TeacherRoutes.SUBJECTS_URL, clear=False, view=MySubjectsView),
    path(url=TeacherRoutes.SUBJECT_URL, clear=False, view=MySubjectView),
    path(url=TeacherRoutes.TASKS_URL, clear=False, view=MyTasksView),
    path(url=TeacherRoutes.GRADES_URL, clear=False, view=SetGradesView),

    # endregion

    # region: administrator views

    # endregion

    # not registred
    path('/not-registered', clear=False, view=NotRegistered),
]
