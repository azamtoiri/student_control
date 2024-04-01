import flet as ft
from flet_route import Params, Basket

from database.database import StudentDatabase
from user_controls.grades_card import create_subject_grade_card, create_task_grade_card
from utils.exceptions import DontHaveGrades, UserDontHaveGrade
from utils.lazy_db import LazyDatabase
from utils.routes_url import StudentRoutes

sub_db = LazyDatabase(StudentDatabase)


def GradesView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # constants
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')

    def add_final_grades():
        """Добавления итоговых оценок на страницу"""
        try:
            for grade in sub_db.database.get_student_grades(user_id=USER_ID):
                create_subject_grade_card(
                    f'Предмет: {grade[1]}', f"{grade[2]}",
                    f"Дата оценки: {grade[3].strftime('%d-%m-%Y')}",
                    grades
                )
        except DontHaveGrades as err:
            no_grades.value = 'У вас нет оценок'
            no_grades.visible = True
            page.update()

    def add_tasks_grade():
        """Добавления оценок по заданиям на страницу"""
        try:
            _grades = sub_db.database.get_student_tasks_grades_v2(user_id=USER_ID)
            for grade in _grades:
                create_task_grade_card(
                    subject_title=f'Предмет: {grade.subject_task.subject.subject_name}',
                    grade_value=f"{grade.grade_value}",
                    grade_date=f'Дата оценки: {grade.grade_date.strftime("%d-%m-%Y")}',
                    name_of_task=grade.subject_task.task_name,
                    grades=tasks_grades
                )
        except DontHaveGrades as err:
            no_grades.value = 'У вас нет оценок'
            no_grades.visible = True
            page.update()

    def tabs_changed(e: ft.ControlEvent) -> None:
        """Function for filtering in filter tab"""
        no_grades.visible = False
        status = filter_tab.tabs[filter_tab.selected_index].text
        grades.controls.clear()
        if status == 'Все':
            add_tasks_grade()
        elif status == 'Итоговые оценки':
            tasks_grades.controls.clear()
            add_final_grades()
        else:
            tasks_grades.controls.clear()
            try:
                for _grade in sub_db.database.get_student_task_grades_with_subject_name(
                        USER_ID, status
                ):
                    create_task_grade_card(
                        subject_title=f'Предмет: {_grade.subject_task.subject.subject_name}',
                        grade_value=f"{_grade.grade_value}",
                        grade_date=f'Дата оценки: {_grade.grade_date.strftime("%d-%m-%Y")}',
                        name_of_task=_grade.subject_task.task_name,
                        grades=tasks_grades
                    )
            except UserDontHaveGrade:
                no_grades.value = 'Нет оценок по этому предмету'
                no_grades.visible = True
                e.page.update()
        e.page.update()

    # the row that contains all grade controls on this page
    grades = ft.ResponsiveRow()  # responsive row for final grades of subjects
    tasks_grades = ft.ResponsiveRow()  # responsive row for grades of tasks

    # hided text if you don't have grades
    no_grades = ft.Text('У вас нет оценок', size=25, color=ft.colors.GREY)
    no_grades.visible = False

    # list for tabs [default contains 'Все' 'Итоговые оценки']
    tabs = [ft.Tab('Все'), ft.Tab('Итоговые оценки')]
    # get all subjects and add to tabs
    try:
        subjects = sub_db.database.get_student_subjects(user_id=USER_ID)

        for subject in subjects:
            tabs.append(ft.Tab(str(subject.subject_name)))
    except DontHaveGrades as ex:
        no_grades.value = 'У вас нет оценок'
        no_grades.visible = True
        page.update()

    # tab for filtering grades
    filter_tab = ft.Tabs(
        scrollable=True,
        selected_index=0,
        on_change=tabs_changed,
        tabs=tabs
    )

    # adding user grades to the page
    add_tasks_grade()

    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        route=StudentRoutes.GRADES_URL,
        controls=[
            filter_tab,
            grades,
            tasks_grades,
            no_grades,
        ]
    )
