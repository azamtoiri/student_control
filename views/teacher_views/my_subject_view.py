import os
from datetime import datetime
from typing import Type

import flet as ft
from flet_core.file_picker import FilePickerFile
from flet_route import Basket, Params

from database.database import StudentDatabase
from database.models import Subjects
from user_controls.modal_alert_dialog import ModalAlertDialog
from user_controls.user_image_picker import UserImage as SubjectImage
from utils.banners import display_success_banner
from utils.create_container_home_view import create_container
from utils.display_error import display_form_error
from utils.exceptions import RequiredField
from utils.routes_url import TeacherRoutes
from utils.zip_file import compress_file_to_zip

db = StudentDatabase()


def MySubjectView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # constants
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')
    DEFAULT_SUBJECT_IMAGE = '/subject_image.png'
    SUBJECT_ID = params.get('id')

    # alert dialog
    dlg = ModalAlertDialog(
        title=ft.Text('Внимание'),
        content=ft.Text('Вы точно хотите сохранить изменения?',
                        text_align=ft.TextAlign.CENTER) if SUBJECT_ID is not None else ft.Text(
            'Добавить новый курс?', text_align=ft.TextAlign.CENTER),
        yes_click=lambda e: yes_click(e)
    )

    delete_dlg = ModalAlertDialog(
        title=ft.Text('Внимание'),
        content=ft.Text('Вы точно хотите удалить курс?',
                        text_align=ft.TextAlign.CENTER) if SUBJECT_ID is not None else ft.Text(
            'Добавить новый курс?', text_align=ft.TextAlign.CENTER),
        yes_click=lambda e: yes_delete_click(e)
    )

    # if page have subject id we will show like updating
    subject: Type[Subjects]
    subject_image_url = ''
    subject_name = ''
    subject_description = ''
    subject_short_description = ''
    file_name = ft.Text(value='Прикрепить файл')
    if SUBJECT_ID is not None:
        subject = db.get_subject(SUBJECT_ID)

        subject_image_url = subject.subject_image
        subject_name = subject.subject_name
        subject_description = subject.description
        subject_short_description = subject.short_description
        # file_name = subject.subject_theory.task_file if subject.subject_theory.task_file is not None else 'Нет файла'

    my_picker = ft.FilePicker(on_result=lambda e: on_dialog_result(e))
    page.overlay.append(my_picker)
    page.update()

    # region: Functions
    def delete_subject(e: ft.ControlEvent) -> None:
        db.delete_subject(SUBJECT_ID)
        e.page.route = e.page.views[-2].route
        e.page.update()

    def show_dlg(e: ft.ControlEvent) -> None:
        e.page.dialog = dlg
        dlg.dlg.open = True
        e.page.update()
        dlg.update()

    def show_delete_dlg(e: ft.ControlEvent) -> None:
        e.page.dialog = delete_dlg
        delete_dlg.dlg.open = True
        e.page.update()
        delete_dlg.update()

    def yes_click(e: ft.ControlEvent) -> None:
        dlg.dlg.open = False
        dlg.update()
        save_changes(e)
        e.page.update()

    def yes_delete_click(e: ft.ControlEvent) -> None:
        dlg.dlg.open = False
        delete_subject(e)
        e.page.update()

    def upload_files(e: ft.FilePickerUploadEvent) -> None:
        uf = []

        if page.web:
            f: FilePickerFile
            if my_picker.result.files is not None:
                uf.append(ft.FilePickerUploadFile(f.name, upload_url=page.get_upload_url(f.name, 600)))
                print(uf)
            my_picker.upload(uf)

            page.update()
        else:
            for f in my_picker.result.files:
                dest = os.path.join(os.getcwd(), "assets/uploads")
                new_filename = f"file_{page.session.get('username')}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{f.name}.zip"
                new_filepath = os.path.join(dest, new_filename)
                compress_file_to_zip(f.path, new_filepath)

    def on_dialog_result(e: ft.FilePickerResultEvent) -> None:
        if e.files is None: return
        # нужно изменить file_name на файл который выбирается
        try:
            display_success_banner(page, 'Успешно загружено', ft.icons.SUNNY, duration=500)
            file_name.value = e.files[0].name
            e.page.update()
        except Exception as ex:
            print(ex)
        e.page.update()

    def on_focus(e: ft.ControlEvent) -> None:
        subject_name_field.error_text = None
        short_description_field.error_text = None
        description_field.error_text = None
        e.page.update()

    def save_changes(e: ft.ControlEvent) -> None:
        e.page.update()
        fields = {
            "Имя предмета": subject_name_field,
            "Краткое описание предмета": short_description_field,
            "Описание предмета": description_field,
        }
        subject_name_ = str(subject_name_field.value).strip() if len(subject_name_field.value) else None
        subject_short_description_ = str(short_description_field.value).strip() if len(
            short_description_field.value) else None
        subject_description_ = str(description_field.value).strip() if len(description_field.value) else None

        try:
            if SUBJECT_ID:
                db.update_subject(
                    subject_id=SUBJECT_ID, subject_name=subject_name_,
                    subject_short_description=subject_short_description_,
                    subject_description=subject_description_,
                )
                if file_name.value != 'Прикрепить файл':
                    upload_files(e)
            else:
                db.create_subject(
                    user_id=USER_ID, subject_name=subject_name_,
                    subject_short_description=subject_short_description_,
                    subject_description=subject_description_
                )
                if file_name.value != 'Прикрепить файл':
                    upload_files(e)
            display_success_banner(
                page=page,
                message='Успешно обновлено' if SUBJECT_ID is not None else 'Успешно добавлено', icons=ft.icons.SUNNY
            )
            e.page.update()
        except RequiredField as err:
            display_form_error(err.field, str(err), fields)
            e.page.update()
        except Exception as err:
            print(err)

    # endregion

    # region: Fields
    subject_name_field = ft.TextField(
        label='Имя предмета *', value=subject_name if subject_name != '' else None, on_focus=lambda e: on_focus(e)
    )
    short_description_field = ft.TextField(
        label='Краткое описание *', hint_text='Краткое описание вашего курса',
        value=subject_short_description if subject_short_description != '' else None, on_focus=lambda e: on_focus(e)
    )
    description_field = ft.TextField(
        label='Описание *', hint_text='Полное описание вашего курса', multiline=True, min_lines=1, max_lines=5,
        value=subject_description if subject_description != '' else None, on_focus=lambda e: on_focus(e)
    )
    # endregion

    # title of the page
    if SUBJECT_ID is not None:
        title = ft.Text(
            'Редактирование курса', size=40, color=ft.colors.BLACK,
            text_align=ft.TextAlign.CENTER
        )
    else:
        title = ft.Text(
            'Добавление курса', size=40, color=ft.colors.BLACK,
            text_align=ft.TextAlign.CENTER
        )

    # subject_image
    if subject_image_url != '':
        subject_image = SubjectImage(
            subject_image_url, disabled=False,
            on_click=lambda _: my_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE)
        )
    else:
        subject_image = SubjectImage(
            DEFAULT_SUBJECT_IMAGE, disabled=False,
            on_click=lambda _: my_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE)
        )

    delete_button = ft.ElevatedButton(
        text='Удалить курс',
        on_click=lambda e: show_delete_dlg(e),
        visible=False if SUBJECT_ID is None else True,
        bgcolor=ft.colors.INVERSE_SURFACE
    )
    save_button = ft.ElevatedButton(
        text='Сохранить изменения' if SUBJECT_ID is not None else 'Добавить курс',
        on_click=lambda e: show_dlg(e)
    )
    task_file_add_button = ft.IconButton(
        ft.icons.ADD,
        bgcolor=ft.colors.ON_INVERSE_SURFACE,
        icon_color=ft.colors.SURFACE_TINT,
        on_click=lambda _: my_picker.pick_files()
    )

    user_info_content = ft.ResponsiveRow(spacing=5, alignment=ft.MainAxisAlignment.CENTER, controls=[
        title,
        # ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[title]),
        ft.Column(col={"sm": 8, "md": 4},
                  controls=[subject_image], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Column(col={"sm": 12, "md": 8},
                  controls=[subject_name_field, short_description_field, description_field]),
        ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[file_name, task_file_add_button]
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[delete_button]
        ),
        ft.Column(col={"sm": 12, "md": 4},
                  controls=[
                      ft.Row(
                          alignment=ft.MainAxisAlignment.CENTER,
                          controls=[save_button]
                      )
                  ]
                  ),
    ])
    container = create_container(user_info_content)

    return ft.View(
        bgcolor=ft.colors.SURFACE_VARIANT,
        route=TeacherRoutes.SUBJECT_URL if SUBJECT_ID is not None else TeacherRoutes.SUBJECT_ADD_URL,
        controls=[
            container
        ]
    )
