from flet_route import path

from utils.routes_url import BaseRoutes, StudentRoutes, TeacherRoutes
from views.default_views import LoginView, RegisterView, HomeEditView
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
from utils.middleware import MiddleWareCheckAuthUser

all_routes = [
    # region: base views
    path(BaseRoutes.INDEX_URL, clear=True, view=IndexView),
    path(BaseRoutes.LOGIN_URL, clear=True, view=LoginView),
    path(BaseRoutes.REGISTER_URL, clear=True, view=RegisterView),
    # endregion

    # region: student views
    path(url=StudentRoutes.MAIN_URL, clear=True, view=MainView, middleware=MiddleWareCheckAuthUser),
    path(url=StudentRoutes.HOME_URL, clear=False, view=HomeView, middleware=MiddleWareCheckAuthUser),
    path(url=StudentRoutes.SUBJECTS_URL, clear=False, view=SubjectsView, middleware=MiddleWareCheckAuthUser),
    path(url=StudentRoutes.SUBJECT_URL, clear=False, view=SubjectView, middleware=MiddleWareCheckAuthUser),
    path(url=StudentRoutes.GRADES_URL, clear=False, view=GradesView, middleware=MiddleWareCheckAuthUser),
    path(url=StudentRoutes.TASKS_URL, clear=False, view=TasksView, middleware=MiddleWareCheckAuthUser),
    path(url=BaseRoutes.TODO_URL, clear=False, view=TodoView, middleware=MiddleWareCheckAuthUser),

    # endregion

    # region: teacher views
    path(url=TeacherRoutes.MAIN_URL, clear=False, view=TeacherMainView, middleware=MiddleWareCheckAuthUser),
    path(url=TeacherRoutes.HOME_URL, clear=False, view=TeacherHomeView, middleware=MiddleWareCheckAuthUser),
    path(url=TeacherRoutes.SUBJECTS_URL, clear=False, view=MySubjectsView, middleware=MiddleWareCheckAuthUser),
    path(url=TeacherRoutes.SUBJECT_URL, clear=False, view=MySubjectView, middleware=MiddleWareCheckAuthUser),
    path(url=TeacherRoutes.TASKS_URL, clear=False, view=MyTasksView, middleware=MiddleWareCheckAuthUser),
    path(url=TeacherRoutes.GRADES_URL, clear=False, view=SetGradesView, middleware=MiddleWareCheckAuthUser),

    # endregion

    # region: administrator views

    # endregion

    # not registred
    path(BaseRoutes.NOT_REGISTERED_URL, clear=False, view=NotRegistered),
    path(BaseRoutes.HOME_EDIT_URL, clear=True, view=HomeEditView, middleware=MiddleWareCheckAuthUser)
]
