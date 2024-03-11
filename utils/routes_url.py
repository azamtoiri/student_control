from dataclasses import dataclass


@dataclass
class BaseRoutes:
    INDEX_URL = '/'
    LOGIN_URL = '/login'
    REGISTER_URL = '/register'
    TODO_URL = '/todo'
    NOT_REGISTERED_URL = '/not-registered'
    STUDENT_MAIN_URL = '/student/main'
    TEACHER_MAIN_URL = '/teacher/main'


@dataclass
class StudentRoutes:
    MAIN_URL = '/student/main'
    SUBJECTS_URL = '/student/subjects'
    GRADES_URL = '/student/grades'
    HOME_URL = '/student/home'
    TASKS_URL = '/student/tasks'
    TODO_URL = '/todo'
    SUBJECT_URL = '/subject/:id'
    SIMPLE_SUBJECT_URL = '/subject'  # without id for adding new subject


@dataclass
class TeacherRoutes:
    MAIN_URL = '/teacher/main'
    HOME_URL = '/teacher/home'
    SUBJECTS_URL = '/teacher/my-subjects'
    SUBJECT_URL = '/teacher/my-subject/:id'
    GRADES_URL = '/teacher/set-grades'
    TASKS_URL = '/teacher/subjects-tasks'
