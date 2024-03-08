from flet_route import path

from views.index_view import IndexView
from views.default_views.login_veiw import LoginView
from views.default_views.register_view import RegisterView

from views.student_views import MainView, CoursesView, GradesView, HomeView, TasksView, TodoView
from views.student_views.course_view import CourseView
from views.teacher_views.main_view import TeacherMainView
from views.not_registered_view import NotRegistered

all_routes = [
    # region: base views
    path('/', clear=True, view=IndexView),
    path('/login', clear=True, view=LoginView),
    path('/register', clear=True, view=RegisterView),
    # endregion

    # region: student views
    path('/student/main', clear=True, view=MainView),
    path('/student/courses', clear=False, view=CoursesView),
    path('/student/grades', clear=False, view=GradesView),
    path('/student/home', clear=False, view=HomeView),
    path('/todo', clear=False, view=TodoView),
    path('/student/tasks', clear=False, view=TasksView),

    path(url='/course/:id', clear=False, view=CourseView),
    # endregion

    # region: teacher views
    path('/teacher/main', clear=False, view=TeacherMainView),

    # endregion

    # region: administrator views

    # endregion

    # not registred
    path('/not-registered', clear=False, view=NotRegistered),
]
