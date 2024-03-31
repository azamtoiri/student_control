import re

from utils.routes_url import StudentRoutes, TeacherRoutes, BaseRoutes

subject_url = re.compile(r'^/subject/\d+$')
subject_theory_url = re.compile(r'^/subject/theory/\d+$')

routes_names = {
    StudentRoutes.HOME_URL: 'Домашняя страница',
    StudentRoutes.GRADES_URL: 'Оценки',
    StudentRoutes.SUBJECTS_URL: 'Предметы',
    StudentRoutes.TODO_URL: 'Todo',
    BaseRoutes.HOME_EDIT_URL: 'Настройки',
    StudentRoutes.TASKS_URL: 'Задания',
    TeacherRoutes.HOME_URL: 'Домашняя страница',
    subject_url: 'Предмет',
    subject_theory_url: 'Теория предмета',
    TeacherRoutes.SUBJECTS_URL: 'Мои предметы',
    TeacherRoutes.GRADES_URL: 'Оценки',
    TeacherRoutes.TASKS_URL: 'Задания',
    TeacherRoutes.SUBJECT_ADD_URL: 'Добавить предмет',
    TeacherRoutes.SUBJECT_URL: 'Предмет'
}
