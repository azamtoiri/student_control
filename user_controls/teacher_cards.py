import shutil
from datetime import datetime

import flet as ft

from database.database import StudentDatabase
from user_controls.modal_alert_dialog import ModalAlertDialog


def create_student_subject_card(
        subject_name, student_fio: str
):
    raise NotImplemented


def create_students_subject_card(
        subject_title: str,
        student_fio: str,
        student_row: ft.ResponsiveRow,
        subject_url: str,
) -> ft.ResponsiveRow:
    """Create students subject cards"""
    tile_icon = ft.Icon(ft.icons.PERSON)

    _card = ft.Card(col={"md": 12, "lg": 4}, color=ft.colors.SURFACE_VARIANT)

    _card.content = ft.Container(
        content=ft.Column(
            [
                ft.ListTile(
                    leading=tile_icon, title=ft.Text(subject_title),
                    subtitle=ft.Column([
                        ft.Text(student_fio),
                        ft.Row(
                            [
                                ft.ElevatedButton("Поставить оценку", on_click=lambda e: e.page.go(subject_url)),
                                # _task_upload_date,
                                # ft.IconButton(ft.icons.DOWNLOAD, on_click=lambda e: save_file_dialog.save_file(e))
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    ], adaptive=True)
                ),
            ]
        ), width=400, padding=10
    )

    return student_row.controls.append(_card)


def create_student_task_card(
        task_title: str,
        task_upload_date: str,
        student_fio: str,
        grades: ft.ResponsiveRow,
        save_file_dialog: ft.FilePicker,
        grade_value: str = None,
        enrollment_id: int = None,
        subject_task_id: int = None,
        user_id: int = None,
        db: StudentDatabase = None,
        task_file_url: str = None
) -> ft.ResponsiveRow:
    """Карточка итоговой оценки по предмету"""

    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            # Копирование файла
            shutil.copy2(f'assets/uploads/{task_file_url}', e.path)

    save_file_dialog.on_result = save_file_result

    set_grade_dlg = ModalAlertDialog(
        title=ft.Text('Поставить оценку'),
        content=ft.Column(
            controls=[
                ft.TextField(
                    hint_text='Оценка', input_filter=ft.NumbersOnlyInputFilter(),
                    on_submit=lambda e: yes_click(e), expand=True, height=100
                ),
            ], height=80, scroll=ft.ScrollMode.AUTO, adaptive=True
        ),
        yes_click=lambda e: yes_click(e)
    )

    def show_dlg(e: ft.ControlEvent) -> None:
        e.page.dialog = set_grade_dlg
        set_grade_dlg.dlg.open = True
        e.page.update()
        set_grade_dlg.update()

    def yes_click(e: ft.ControlEvent) -> None:
        set_grade_vale = int(set_grade_dlg.dlg.content.controls[0].value)
        try:
            if set_grade_vale > 100 or set_grade_vale < 0:
                raise ValueError('Оценка должна быть не больше 100 и больше 0')
        except ValueError as err:
            set_grade_dlg.dlg.content.controls[0].error_text = str(err)
            set_grade_dlg.update()
            return

        if grade_value == "Нет оценки":
            # Если оценка различается от предыдущей, то обновляем ее
            if grade_value != set_grade_vale:
                db_req: bool = db.set_grade_for_task(
                    enrollment_id=enrollment_id,
                    subject_task_id=subject_task_id,
                    user_id=user_id,
                    grade_value=set_grade_vale
                )
                _task_upload_date.value = datetime.now().strftime('%d.%m.%Y')
                status.visible = True
                set_grade_button.text = 'Изменить оценку'
            else:
                e.page.update()
        else:
            db_req: bool = db.update_grade_for_task(
                enrollment_id=enrollment_id,
                subject_task_id=subject_task_id,
                user_id=user_id,
                grade_value=set_grade_vale
            )
            _task_upload_date.value = datetime.now().strftime('%d.%m.%Y')
            status.visible = True
            set_grade_button.text = 'Изменить оценку'

        set_grade_dlg.dlg.open = False
        set_grade_dlg.update()
        e.page.update()

    _grade_value = ft.Text(f'Оценка {grade_value}')

    _task_title = ft.Text(task_title)

    _task_upload_date = ft.Text(task_upload_date, tooltip='Дата выполнения задания')

    _student_fio = ft.Text(student_fio, tooltip='Студент')

    tile_icon = ft.Icon(name=ft.icons.PERSON)

    _card = ft.Card(col={"md": 12, "lg": 4}, color=ft.colors.SURFACE_VARIANT)

    status = ft.Text(
        value='Оценено',
        visible=False if grade_value == 'Нет оценки' else True,
        color=ft.colors.SURFACE_TINT,
        weight=ft.FontWeight.BOLD, size=15
    )
    status2 = ft.Text(
        value='Не выполнено',
        visible=False if task_file_url else True,
        color=ft.colors.SURFACE_TINT,
        weight=ft.FontWeight.BOLD, size=15
    )
    set_grade_button = ft.ElevatedButton(
        text="Поставить оценку" if grade_value == "Нет оценки" else "Изменить оценку",
        on_click=lambda e: show_dlg(e), tooltip='Поставить оценку',
        disabled=True if task_file_url is None else False
    )

    download_button = ft.IconButton(
        ft.icons.DOWNLOAD,
    )
    _card.content = ft.Container(
        content=ft.Column(
            [
                ft.Stack(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END, controls=[status, status2],
                        ),
                        ft.Container(height=20),
                        ft.ListTile(
                            leading=tile_icon, title=_task_title,
                            subtitle=ft.Column([
                                _grade_value,
                                _student_fio,
                                ft.Row(
                                    [
                                        set_grade_button,
                                        _task_upload_date,
                                        ft.IconButton(
                                            ft.icons.DOWNLOAD,
                                            on_click=lambda e: save_file_dialog.save_file(
                                                e, file_name=f'{task_file_url}'
                                            ),
                                            tooltip='Скачать файл',
                                            visible=False if task_file_url is None else True
                                        )
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                            ], adaptive=True)
                        ),
                    ]
                ),
            ]
        ), width=400, padding=10
    )
    return grades.controls.append(_card)
