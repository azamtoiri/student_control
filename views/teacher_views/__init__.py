"""
Здесь хранятся все представления для учителя
Что за что отвечает:
    my_tasks_view - представление для просмотра заданий для каждого предмета, создавать новые задания и другие
    my_subject_view - представление для просмотра предмета и его заданий, также для создания новых заданий для предмета
    my_subjects_view - представление для просмотра всех предметов, у преподавателя
    set_grades_view - представление для выставления оценок, просмотра оценок студентов
    home_view - представление для домашней страницы, где можно отредактировать профиль. Посмотреть кол-во предметов
    main_view - представление для главной страницы (после авторизации) (навигационная панель)
"""
from .home_view import TeacherHomeView
from .main_view import TeacherMainView
from .my_subject_view import MySubjectView
from .my_subjects_view import MySubjectsView
from .my_tasks_view import MyTasksView
from .set_grades_view import SetGradesView
