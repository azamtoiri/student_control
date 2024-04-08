import flet as ft


def create_subject_grade_card(
        subject_title: str, grade_value: str, grade_date: str,
        grades: ft.ResponsiveRow, final_grade_text: str = 'Итоговая оценка'
) -> ft.ResponsiveRow:
    """Карточка итоговой оценки по предмету"""
    _grade_value = ft.Text(f'Оценка {grade_value}')

    _subject_title = ft.Text(subject_title)

    _grade_date = ft.Text(grade_date)
    grade_icon = ft.Icon(name=ft.icons.GRADE_OUTLINED)

    _final_grade_text = ft.Text(final_grade_text, weight=ft.FontWeight.BOLD, color=ft.colors.SURFACE_TINT)

    _card = ft.Card(col={"md": 12, "lg": 4}, color=ft.colors.SURFACE_VARIANT)

    if int(grade_value) == 100:
        grade_icon.name = ft.icons.GRADE
        grade_icon.color = ft.colors.SURFACE_TINT

    _card.content = ft.Container(
        content=ft.Column(
            [
                ft.Stack(
                    controls=[
                        ft.Row(alignment=ft.MainAxisAlignment.END, controls=[_final_grade_text]),
                        ft.ListTile(
                            leading=grade_icon, title=_grade_value,
                            subtitle=ft.Column([
                                _subject_title,
                                ft.Row([_grade_date], alignment=ft.MainAxisAlignment.END),
                            ], adaptive=True)
                        ),
                    ]
                ),
            ]
        ), width=400, padding=10
    )
    return grades.controls.append(_card)


def create_task_grade_card(
        subject_title: str, grade_value: str, grade_date: str, name_of_task,
        grades: ft.ResponsiveRow
) -> ft.ResponsiveRow:
    """Карточка оценки по заданию предмета"""
    _grade_value = ft.Text(f'Оценка {grade_value}')

    _subject_title = ft.Text(subject_title)

    _grade_date = ft.Text(grade_date)
    grade_icon = ft.Icon(name=ft.icons.GRADE_OUTLINED)

    _name_of_task = ft.Text(name_of_task)

    _card = ft.Card(
        col={"md": 12, "lg": 4},
        color=ft.colors.SURFACE_VARIANT
    )

    # if grade is 100 whe are show the filed icon
    if int(grade_value) == 100:
        grade_icon.name = ft.icons.GRADE
        grade_icon.color = ft.colors.SURFACE_TINT

    _card.content = ft.Container(
        content=ft.Column(
            [
                ft.ListTile(
                    leading=grade_icon,
                    title=_grade_value,
                    subtitle=ft.Column(
                        [
                            _subject_title, _name_of_task,
                            ft.Row(alignment=ft.MainAxisAlignment.END, controls=[
                                _grade_date
                            ], spacing=0)
                        ],
                        adaptive=True
                    )
                ),
                ft.Row(alignment=ft.MainAxisAlignment.END)
            ]
        ), width=400, padding=10
    )
    return grades.controls.append(_card)
