import flet as ft
from flet_route import Params, Basket

from database.database import AsyncBaseDatabase
from database.database import StudentDatabase
from user_controls.grades_card import create_subject_grade_card, create_task_grade_card
from utils.exceptions import DontHaveGrades
from utils.lazy_db import LazyDatabase
from utils.routes_url import StudentRoutes

sub_db = LazyDatabase(StudentDatabase)


async def GradesView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # constants
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')
    async_db = AsyncBaseDatabase()

    # Глобальные переменные для хранения данных
    student_final_grades = []
    student_grades = []

    try:
        student_final_grades = list(sub_db.database.get_student_grades(user_id=USER_ID))
    except DontHaveGrades:
        pass

    try:
        student_grades = sub_db.database.get_student_tasks_grades_v2(user_id=USER_ID)
    except DontHaveGrades:
        pass

    def add_final_grades():
        """Добавления итоговых оценок на страницу"""
        if not student_final_grades:
            no_grades.value = 'У вас нет итоговых оценок'
            no_grades.visible = True
            page.update()
            return

        for grade in student_final_grades:
            create_subject_grade_card(
                f'Предмет: {grade[1]}', f"{grade[2]}",
                f"Дата оценки: {grade[3].strftime('%d-%m-%Y')}",
                grades
            )

    def add_tasks_grades():
        """Добавления оценок по заданиям на страницу"""
        if not student_grades:
            no_grades.value = 'У вас нет оценок по заданиям'
            no_grades.visible = True
            page.update()
            return

        for grade in student_grades:
            create_task_grade_card(
                subject_title=f'Предмет: {grade.subject_task.subject.subject_name}',
                grade_value=f"{grade.grade_value}",
                grade_date=f'Дата оценки: {grade.grade_date.strftime("%d-%m-%Y")}',
                name_of_task=grade.subject_task.task_name,
                grades=tasks_grades
            )

    def add_filtered_grades(subject_name: str) -> None:
        filtered_grades = [
            grade for grade in student_grades if grade.subject_task.subject.subject_name == subject_name
        ]
        if not filtered_grades:
            no_grades.value = f'Нет оценок по предмету: {subject_name}'
            no_grades.visible = True
            page.update()
            return

        for _grade in filtered_grades:
            create_task_grade_card(
                subject_title=f'Предмет: {_grade.subject_task.subject.subject_name}',
                grade_value=f"{_grade.grade_value}",
                grade_date=f'Дата оценки: {_grade.grade_date.strftime("%d-%m-%Y")}',
                name_of_task=_grade.subject_task.task_name,
                grades=tasks_grades
            )

    def tabs_changed(e: ft.ControlEvent) -> None:
        """Function for filtering in filter tab"""
        no_grades.visible = False
        status = filter_tab.tabs[filter_tab.selected_index].text
        grades.controls.clear()
        tasks_grades.controls.clear()
        tasks_filtered.controls.clear()

        if status == 'Все':
            add_tasks_grades()
            add_final_grades()
        elif status == 'Итоговые оценки':
            add_final_grades()
        else:
            add_filtered_grades(subject_name=status)
        e.page.update()

    # the row that contains all grade controls on this page
    grades = ft.ResponsiveRow()  # responsive row for final grades of subjects
    tasks_grades = ft.ResponsiveRow()  # responsive row for grades of tasks
    tasks_filtered = ft.ResponsiveRow()  # responsive row for grades of tasks

    # hidden text if you don't have grades
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
    add_tasks_grades()
    add_final_grades()

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
            tasks_filtered,
            no_grades,
        ]
    )
