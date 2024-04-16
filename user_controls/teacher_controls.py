import flet as ft

from database.database import TeacherDatabase
from utils.exceptions import DontHaveGrades


class TeacherStudentsCard(ft.UserControl):

    def __init__(self, user_id, button_click):
        super().__init__()
        self.user_id = user_id
        self.button_click = button_click
        self.db = TeacherDatabase()
        self.count_of_grades_text = ft.Ref[ft.Text]()

        try:
            self.all_grades_count = len(self.db.get_teacher_students_no_async(self.user_id))
        except DontHaveGrades as err:
            self.all_grades_count = 0

    def build(self):
        teachers_students = self.create_student_controls()

        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.GOLF_COURSE),
                            title=ft.Text(f'Кол-во студентов: {self.all_grades_count}',
                                          ref=self.count_of_grades_text)
                        ),
                        ft.ExpansionTile(
                            title=ft.Text('Студенты'),
                            controls=teachers_students
                        ),
                        ft.ListTile(
                            title=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text('Посмотреть всех студентов', text_align=ft.TextAlign.START),
                                    ft.IconButton(
                                        icon=ft.icons.NAVIGATE_NEXT, on_click=self.button_click,
                                        icon_color=ft.colors.SURFACE_TINT, bgcolor=ft.colors.SURFACE_VARIANT
                                    )
                                ]
                            ),
                        )
                    ]
                )
            )
        )

    def create_student_controls(self) -> list[ft.Control]:
        all_subjects = []
        count = 1
        try:
            for i in self.db.get_teacher_students_no_async(user_id=self.user_id):
                all_subjects.append(
                    ft.ListTile(
                        title=ft.Text(f'{count}. {i[1]} {i[2]}'),
                    )
                )
                count += 1
            # return first 5 students
            return all_subjects[:5]
        except DontHaveGrades as ex:
            return []


class TeacherSubjectsCard(ft.UserControl):
    def __init__(self, user_id, button_click):
        super().__init__()
        self.user_id = user_id
        self.button_click = button_click
        self.db = TeacherDatabase()
        self.count_of_subjects = ft.Ref[ft.Text]()

        try:
            self.all_subjects_count = len(self.db.get_teacher_students_no_async(self.user_id))
        except DontHaveGrades as err:
            self.all_subjects_count = 0

    def build(self):
        teachers_students = self.create_subjects_controls()

        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.SUBJECT),
                            title=ft.Text(f'Мои курсы: {self.all_subjects_count}',
                                          ref=self.count_of_subjects)
                        ),
                        ft.ExpansionTile(
                            title=ft.Text('Курсы'),
                            controls=teachers_students
                        ),
                        ft.ListTile(
                            title=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text('Посмотреть все курсы', text_align=ft.TextAlign.START),
                                    ft.IconButton(
                                        icon=ft.icons.NAVIGATE_NEXT, on_click=self.button_click,
                                        icon_color=ft.colors.SURFACE_TINT, bgcolor=ft.colors.SURFACE_VARIANT
                                    )
                                ]
                            ),
                        )
                    ]
                )
            )
        )

    def create_subjects_controls(self) -> list[ft.Control]:
        all_subjects = []
        count = 1
        try:
            for i in self.db.get_teacher_students_no_async(user_id=self.user_id):
                all_subjects.append(
                    ft.ListTile(
                        title=ft.Text(f'{count}. {i.subject_name}'),
                    )
                )
                count += 1
            # return first 5 students
            return all_subjects[:5]
        except DontHaveGrades as ex:
            return []


class TeacherExperience(ft.UserControl):
    def __init__(self, user_id, button_click):
        super().__init__()
        self.user_id = user_id
        self.button_click = button_click
        self.have_information = False

    def build(self):
        self.db = TeacherDatabase()
        try:
            information = self.db.get_teacher_information(self.user_id)
            if information.teacher_description or information.teacher_experience is not None:
                self.have_information = True
            self.count_of_experience = information.teacher_experience
            teacher_description = information.teacher_description
        except Exception as ex:
            self.count_of_experience = 0
            teacher_description = ''
            self.have_information = True

        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.GOLF_COURSE),
                            title=ft.Text(f'Стаж: {self.count_of_experience}'),
                            subtitle=ft.Text(
                                f'{teacher_description[:20] if teacher_description is not None else teacher_description}...'),
                            visible=self.have_information
                        ),
                        ft.ElevatedButton(
                            'Заполнить информацию о себе',
                            on_click=self.button_click,
                            visible=not self.have_information
                        )
                    ]
                )
            )
        )
