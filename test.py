import shutil

import flet as ft

from user_controls.modal_alert_dialog import ModalAlertDialog


def main(page: ft.Page):
    page.title = "AlertDialog examples"

    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            shutil.copy2('assets/default_user_image.png', e.path)

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(save_file_dialog)

    def create_subject_grade_card(
            task_title: str, grade_value: str, task_upload_date: str,
            student_fio: str,
            grades: ft.ResponsiveRow,
    ) -> ft.ResponsiveRow:
        """Карточка итоговой оценки по предмету"""

        set_grade_dlg = ModalAlertDialog(
            title=ft.Text('Поставить оценку'),
            content=ft.Column(
                controls=[
                    ft.TextField(hint_text='Оценка'),
                ], height=80, scroll="auto", adaptive=True
            ),
            yes_click=lambda _: print("Yes")
        )

        def show_dlg(e: ft.ControlEvent) -> None:
            e.page.dialog = set_grade_dlg
            set_grade_dlg.dlg.open = True
            e.page.update()
            set_grade_dlg.update()

        _grade_value = ft.Text(f'Оценка {grade_value}')

        _task_title = ft.Text(task_title)

        _task_upload_date = ft.Text(task_upload_date, tooltip='Дата выполнения задания')

        _student_fio = ft.Text(student_fio, tooltip='Студент')

        tile_icon = ft.Icon(name=ft.icons.PERSON)

        _card = ft.Card(col={"md": 12, "lg": 4}, color=ft.colors.SURFACE_VARIANT)

        download_button = ft.IconButton(
            ft.icons.DOWNLOAD,
        )

        _card.content = ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=tile_icon, title=_grade_value,
                        subtitle=ft.Column([
                            _task_title,
                            _student_fio,
                            ft.Row(
                                [
                                    ft.ElevatedButton("Поставить оценку", on_click=lambda e: show_dlg(e)),
                                    _task_upload_date,
                                    ft.IconButton(ft.icons.DOWNLOAD, on_click=lambda e: save_file_dialog.save_file(e))
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                        ], adaptive=True)
                    ),
                ]
            ), width=400, padding=10
        )
        return grades.controls.append(_card)

    grades = ft.ResponsiveRow()

    for i in range(5):
        create_subject_grade_card(
            f'Test {i}', str(i),
            f'date: {i + 1}.{i + 2}', f'Stud {i} fio {i}',
            grades
        )

    page.add(
        grades
    )
    page.update()


ft.app(target=main)
