import flet as ft


class GradeCard(ft.UserControl):
    def __init__(self, subject_name, grade_value, grade_date):
        super().__init__()
        self.subject_name = subject_name
        self.grade_value = grade_value
        self.grade_date = grade_date

    def build(self) -> ft.Card:
        card = ft.Card(col={'md': 12, 'lg': 4})
        card.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ListTile(leading=ft.Icon(ft.icons.GROUPS_OUTLINED),
                                title=ft.Text(self.grade_value),
                                subtitle=ft.Column([ft.Text(self.subject_name), ft.Text(self.grade_date)])),
                ]
            ), width=400, padding=10)
        return card
