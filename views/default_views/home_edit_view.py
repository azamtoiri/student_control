import os
import shutil

import flet as ft
from flet_core.file_picker import FilePickerFile
from flet_route import Params, Basket

from database.database import UserDatabase
from user_controls.user_chang_field import UserChangField
from user_controls.user_image_picker import UserImage
from utils.banners import display_success_banner_async
from utils.create_container_home_view import create_container
from utils.exceptions import RequiredField
from utils.lazy_db import LazyDatabase
from utils.routes_url import StudentRoutes, TeacherRoutes, BaseRoutes

user_db = LazyDatabase(UserDatabase)


async def HomeEditView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    # constants
    USER_ID = page.session.get('user_id')
    USERNAME = page.session.get('username')

    teacher_experience = ''
    teacher_description = ''
    IS_DONE = False
    if page.session.get("is_staff") is not None:
        teacher = await user_db.database.get_teacher_info(USER_ID)
        teacher_experience = teacher.teacher_experience
        teacher_description = teacher.teacher_description
        IS_DONE = bool(teacher.is_done)

    # ref controls
    upload_button = ft.Ref[ft.ElevatedButton]()
    ft_image = ft.Ref[ft.Image]()

    # route
    main_page_url = TeacherRoutes.MAIN_URL if await user_db.database.is_staff(USER_ID) else StudentRoutes.MAIN_URL

    # region: Functions
    async def display_form_error(field: str, message: str) -> None:
        fields = {
            'Имя': first_name_field,
            'Фамилия': last_name_field,
            'Отчество': middle_name_field,
            'Опыт': teacher_experience_field,
            'Описание': teacher_description_field
        }
        if field in fields.keys():
            fields[field].set_error_text(message)
        page.update()

    async def save_changes(e: ft.ControlEvent) -> None:
        try:
            first_name = str(first_name_field.get_value).strip() if len(
                first_name_field.get_value) else None

            last_name = str(last_name_field.get_value).strip() if len(
                last_name_field.get_value) else None

            middle_name = str(middle_name_field.get_value).strip() if len(
                middle_name_field.get_value) else None

            group = str(group_field.get_value).strip() if len(
                group_field.get_value) else None

            course = str(course_field.get_value).strip() if len(
                course_field.get_value) else None

            age = str(age_field.get_value).strip() if len(
                age_field.get_value) else None

            email = str(email_field.get_value).strip() if len(
                email_field.get_value) else None

            await user_db.database.update_user(
                user_id=USER_ID,
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                group=group,
                course=course,
                age=age,
                email=email,
            )
            await display_success_banner_async(page, 'Изменения сохранены', ft.icons.SUNNY)
        except RequiredField as error:
            await display_form_error(error.field, str(error))
        except Exception as ex:
            print(ex)

        # page.go(main_page_url)

    async def save_changes_teacher(e: ft.ControlEvent) -> None:
        try:
            teacher_experience_ = str(teacher_experience_field.get_value).strip() if len(
                teacher_experience_field.get_value) else None

            teacher_description_ = str(teacher_description_field.get_value).strip() if len(
                teacher_description_field.get_value) else None
            is_done = True

            await user_db.database.update_teacher_information(USER_ID, teacher_experience_, teacher_description_,
                                                              is_done)

            await display_success_banner_async(page, 'Изменения сохранены', ft.icons.SUNNY)
        except RequiredField as error:
            await display_form_error(error.field, str(error))
        except Exception as ex:
            print(ex)

    async def on_dialog_result(e: ft.FilePickerResultEvent) -> None:
        if e.files is None: return
        await upload_files(e)
        page.update()

    async def upload_files(e: ft.FilePickerUploadFile):
        uf = []
        if page.web:
            f: FilePickerFile
            for f in pick_files.result.files:
                uf.append(ft.FilePickerUploadFile(f.name, upload_url=page.get_upload_url(f.name, 600)))
            pick_files.upload(uf)

            for f in pick_files.result.files:
                user_db.database.set_new_user_image(USER_ID, f.name)
                user_avatar.change_user_image(f'/uploads/{f.name}')
                user_avatar.update()
            page.update()
        else:
            for x in pick_files.result.files:
                if os.path.exists(x.name):
                    os.remove(x.name)
                dest = os.path.join(os.getcwd(), "assets/uploads")
                shutil.copy(x.path, f'{dest}')

                # here will be updating data in db
                _user_image_dir = f'{x.name}'
                await user_db.database.set_new_user_image(USER_ID, _user_image_dir)
                await user_avatar.change_user_image(f'/uploads/{x.name}')
                user_avatar.update()
                page.update()

    # endregion

    user = await user_db.database.get_user_by_id(USER_ID)

    # region: InputFields
    first_name_field = UserChangField(True, label="Фамилия *",
                                      value=user.last_name, save_changes=save_changes)  # Фамилия
    last_name_field = UserChangField(True, label="Имя *",
                                     value=user.first_name, save_changes=save_changes)  # Имя
    middle_name_field = UserChangField(True, label="Отчество *",
                                       value=user.middle_name, save_changes=save_changes)  # Отчество
    group_field = UserChangField(False, label="Группа",
                                 value=user.group, save_changes=save_changes)  # Группа
    course_field = UserChangField(False, label="Курс",
                                  value=user.course, save_changes=save_changes)  # Звание
    age_field = UserChangField(False, label="Возраст",
                               value=user.age, save_changes=save_changes)  # Возраст
    email_field = UserChangField(True, label="Email",
                                 value=user.email)  # Email
    username_field = UserChangField(disabled=True, value=f'{USERNAME}', label='Имя пользователя')

    teacher_experience_field = UserChangField(
        IS_DONE, teacher_experience, label='Ваш стаж', save_changes=save_changes_teacher
    )
    teacher_description_field = UserChangField(
        IS_DONE, teacher_description, label='Расскажите о себе', multiline=True, save_changes=save_changes_teacher
    )

    # filters
    age_field.edit_value.input_filter = ft.NumbersOnlyInputFilter()
    teacher_experience_field.edit_value.input_filter = ft.NumbersOnlyInputFilter()

    # endregion

    pick_files = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(pick_files)
    page.update()

    user_image_dir = await user_db.database.get_user_image_url(USER_ID)

    if (user_image_dir is None) or (os.path.exists(f'assets/uploads/{user_image_dir}') is False):
        user_avatar = UserImage(
            f'/default_user_image.png',
            on_click=lambda _: pick_files.pick_files(file_type=ft.FilePickerFileType.IMAGE), disabled=False
        )
    else:
        user_avatar = UserImage(
            f'/uploads/{user_image_dir}',
            on_click=lambda _: pick_files.pick_files(file_type=ft.FilePickerFileType.IMAGE), disabled=False
        )
    title = ft.Text('Изменить данные', size=40, color=ft.colors.BLACK, text_align=ft.TextAlign.CENTER)
    teacher_title = ft.Text('Изменить информацию о себе (преподаватель)', size=40, color=ft.colors.BLACK,
                            text_align=ft.TextAlign.CENTER)

    content = ft.ResponsiveRow(spacing=5, alignment=ft.MainAxisAlignment.CENTER, controls=[
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                title,
                ft.ElevatedButton('На главную страницу', on_click=lambda e: page.go(main_page_url))
            ]),
        ]),
        ft.Column(col={"sm": 6, "md": 4},
                  controls=[user_avatar], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Column(col={"sm": 12, "md": 4},
                  controls=[first_name_field, last_name_field, middle_name_field, course_field]),
        ft.Column(col={"sm": 12, "md": 4},
                  controls=[group_field, age_field, email_field, username_field]),
    ])

    teacher_warning_text = ft.Container(
        content=ft.Text(
            value=('Внимание!\nДанные можно редактировать только один раз, '
                   'пожалуйста убедитесь что все данные верны, перед тем как сохранить!'),
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.SURFACE_TINT,
            size=20,
        )
    )
    teacher_content = ft.ResponsiveRow(
        spacing=5, alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[teacher_title]),
            ft.Column(col={"sm": 6, "md": 4}, visible=not IS_DONE,
                      controls=[teacher_warning_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column(
                controls=[teacher_experience_field, teacher_description_field]
            )
        ]
    )
    # Background container for color and other
    user_data_container = create_container(content)
    teacher_container = create_container(teacher_content)
    teacher_container.visible = user.is_staff

    return ft.View(
        route=BaseRoutes.HOME_EDIT_URL,
        bgcolor=ft.colors.SURFACE_VARIANT,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(),
            user_data_container,
            teacher_container
        ]
    )
