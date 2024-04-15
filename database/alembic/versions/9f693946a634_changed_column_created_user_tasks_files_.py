"""changed column: created user_tasks_files: add comments

Revision ID: 9f693946a634
Revises: 24b374495ce6
Create Date: 2024-03-25 22:23:51.153203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9f693946a634'
down_revision: Union[str, None] = '24b374495ce6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_task_files',
    sa.Column('subject_task_id', sa.Integer(), nullable=False, comment='Идентификатор задания'),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('enrollment_id', sa.Integer(), nullable=False),
    sa.Column('task_file', sa.String(), nullable=False),
    sa.Column('completed', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Отправил ли ученик задание'),
    sa.ForeignKeyConstraint(['enrollment_id'], ['enrollments.enrollment_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subject_task_id'], ['subject_tasks.subject_task_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('subject_task_id', 'user_id'),
    comment='Файлы для заданий пользователей. К каждому заданию может быть прикреплено несколько файлов'
    )
    op.drop_table('completed_task_status')
    op.alter_column('enrollments', 'enrollment_id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор записи о подписке',
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('enrollments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               comment='Пользователь, подписавшийся на предмет')
    op.alter_column('enrollments', 'subject_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               comment='Предмет, на который подписался пользователь. Сам предмет')
    op.alter_column('enrollments', 'enrollment_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='Дата подписки',
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('enrollments', 'completed',
               existing_type=sa.BOOLEAN(),
               comment='Статус завершения предмета',
               existing_nullable=True)
    op.create_table_comment(
        'enrollments',
        'Записи о подписках пользователей на предметы',
        existing_comment=None,
        schema=None
    )
    op.alter_column('grades', 'grade_id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор оценки',
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('grades', 'enrollment_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               comment='Идентификатор записи о подписке')
    op.alter_column('grades', 'grade_value',
               existing_type=sa.INTEGER(),
               nullable=False,
               comment='Сама оценка')
    op.alter_column('grades', 'grade_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='Дата выставления оценки',
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.create_table_comment(
        'grades',
        'Оценки студентов по предметам',
        existing_comment=None,
        schema=None
    )
    op.alter_column('subject_tasks', 'subject_task_id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор задания',
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('subject_tasks', 'task_name',
               existing_type=sa.VARCHAR(),
               comment='Название задания',
               existing_nullable=False)
    op.alter_column('subject_tasks', 'completed',
               existing_type=sa.BOOLEAN(),
               comment='Статус задания',
               existing_nullable=True)
    op.alter_column('subject_tasks', 'subject_id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор предмета',
               existing_nullable=True)
    op.create_table_comment(
        'subject_tasks',
        'Задания для предмета. У каждого предмета может быть несколько заданий',
        existing_comment=None,
        schema=None
    )
    op.alter_column('subject_theory', 'theory_id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор теории',
               existing_nullable=False)
    op.alter_column('subject_theory', 'theory_title',
               existing_type=sa.VARCHAR(),
               comment='Заголовок теории',
               existing_nullable=False)
    op.alter_column('subject_theory', 'theory_data',
               existing_type=sa.VARCHAR(),
               comment='Данные теории (файл, текст, ссылка)',
               existing_nullable=False)
    op.create_table_comment(
        'subject_theory',
        'Теория для предмета. У каждого предмета может быть только одна теория',
        existing_comment=None,
        schema=None
    )
    op.alter_column('subjects', 'subject_id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор предмета',
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('subjects', 'user_id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор пользователя',
               existing_nullable=False)
    op.alter_column('subjects', 'subject_name',
               existing_type=sa.VARCHAR(),
               nullable=False,
               comment='Название предмета')
    op.alter_column('subjects', 'short_description',
               existing_type=sa.VARCHAR(),
               comment='Краткое описание предмета',
               existing_nullable=False)
    op.alter_column('subjects', 'description',
               existing_type=sa.VARCHAR(),
               comment='Полное описание предмета',
               existing_nullable=False)
    op.create_table_comment(
        'subjects',
        'Предметы, на которые подписаны пользователи. У каждого пользователя может быть несколько предметов',
        existing_comment=None,
        schema=None
    )
    op.alter_column('task', 'task_id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор задания',
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('task', 'task_name',
               existing_type=sa.VARCHAR(),
               comment='Название задания',
               existing_nullable=False)
    op.alter_column('task', 'completed',
               existing_type=sa.BOOLEAN(),
               comment='Статус задания',
               existing_nullable=True)
    op.alter_column('task', 'user_id',
               existing_type=sa.INTEGER(),
               comment='Пользователь которому принадлежит задание',
               existing_nullable=False)
    op.create_table_comment(
        'task',
        'Todo list. Задания пользователей которые они должны выполнить (цели). ',
        existing_comment=None,
        schema=None
    )
    op.alter_column('user_theme', 'user_id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор пользователя',
               existing_nullable=False)
    op.alter_column('user_theme', 'theme',
               existing_type=sa.VARCHAR(),
               comment='Тема пользователя (светлая/темная)',
               existing_nullable=False,
               existing_server_default=sa.text("'light'::character varying"))
    op.alter_column('user_theme', 'seed_color',
               existing_type=sa.VARCHAR(),
               comment='Цвет цветовой схемы приложения',
               existing_nullable=False,
               existing_server_default=sa.text("'green'::character varying"))
    op.create_table_comment(
        'user_theme',
        'Цветовая схема пользователя (тема). Уникальная для каждого пользователя',
        existing_comment=None,
        schema=None
    )
    op.alter_column('users', 'user_id',
               existing_type=sa.INTEGER(),
               comment='User id column',
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('users_user_id_seq'::regclass)"))
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               comment='Фамилия',
               existing_nullable=True)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(),
               comment='Имя',
               existing_nullable=True)
    op.alter_column('users', 'middle_name',
               existing_type=sa.VARCHAR(),
               comment='Отчество',
               existing_nullable=True)
    op.alter_column('users', 'course',
               existing_type=sa.INTEGER(),
               comment='Курс обучения',
               existing_nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False,
               comment='уникальное Имя пользователя')
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'is_staff',
               existing_type=sa.BOOLEAN(),
               comment='является ли пользователь частью персонала (преподаватель)',
               existing_nullable=True)
    op.alter_column('users', 'is_superuser',
               existing_type=sa.BOOLEAN(),
               comment='является ли пользователь суперпользователем',
               existing_nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='Дата создания пользователя',
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('users', 'user_image',
               existing_type=sa.VARCHAR(),
               comment='Изображение пользователя',
               existing_nullable=True)
    op.create_table_comment(
        'users',
        'Таблица пользователей',
        existing_comment=None,
        schema=None
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table_comment(
        'users',
        existing_comment='Таблица пользователей',
        schema=None
    )
    op.alter_column('users', 'user_image',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Изображение пользователя',
               existing_nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='Дата создания пользователя',
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('users', 'is_superuser',
               existing_type=sa.BOOLEAN(),
               comment=None,
               existing_comment='является ли пользователь суперпользователем',
               existing_nullable=True)
    op.alter_column('users', 'is_staff',
               existing_type=sa.BOOLEAN(),
               comment=None,
               existing_comment='является ли пользователь частью персонала (преподаватель)',
               existing_nullable=True)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True,
               comment=None,
               existing_comment='уникальное Имя пользователя')
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'course',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Курс обучения',
               existing_nullable=True)
    op.alter_column('users', 'middle_name',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Отчество',
               existing_nullable=True)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Имя',
               existing_nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Фамилия',
               existing_nullable=True)
    op.alter_column('users', 'user_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='User id column',
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('users_user_id_seq'::regclass)"))
    op.drop_table_comment(
        'user_theme',
        existing_comment='Цветовая схема пользователя (тема). Уникальная для каждого пользователя',
        schema=None
    )
    op.alter_column('user_theme', 'seed_color',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Цвет цветовой схемы приложения',
               existing_nullable=False,
               existing_server_default=sa.text("'green'::character varying"))
    op.alter_column('user_theme', 'theme',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Тема пользователя (светлая/темная)',
               existing_nullable=False,
               existing_server_default=sa.text("'light'::character varying"))
    op.alter_column('user_theme', 'user_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Идентификатор пользователя',
               existing_nullable=False)
    op.drop_table_comment(
        'task',
        existing_comment='Todo list. Задания пользователей которые они должны выполнить (цели). ',
        schema=None
    )
    op.alter_column('task', 'user_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Пользователь которому принадлежит задание',
               existing_nullable=False)
    op.alter_column('task', 'completed',
               existing_type=sa.BOOLEAN(),
               comment=None,
               existing_comment='Статус задания',
               existing_nullable=True)
    op.alter_column('task', 'task_name',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Название задания',
               existing_nullable=False)
    op.alter_column('task', 'task_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Идентификатор задания',
               existing_nullable=False,
               autoincrement=True)
    op.drop_table_comment(
        'subjects',
        existing_comment='Предметы, на которые подписаны пользователи. У каждого пользователя может быть несколько предметов',
        schema=None
    )
    op.alter_column('subjects', 'description',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Полное описание предмета',
               existing_nullable=False)
    op.alter_column('subjects', 'short_description',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Краткое описание предмета',
               existing_nullable=False)
    op.alter_column('subjects', 'subject_name',
               existing_type=sa.VARCHAR(),
               nullable=True,
               comment=None,
               existing_comment='Название предмета')
    op.alter_column('subjects', 'user_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Идентификатор пользователя',
               existing_nullable=False)
    op.alter_column('subjects', 'subject_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Идентификатор предмета',
               existing_nullable=False,
               autoincrement=True)
    op.drop_table_comment(
        'subject_theory',
        existing_comment='Теория для предмета. У каждого предмета может быть только одна теория',
        schema=None
    )
    op.alter_column('subject_theory', 'theory_data',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Данные теории (файл, текст, ссылка)',
               existing_nullable=False)
    op.alter_column('subject_theory', 'theory_title',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Заголовок теории',
               existing_nullable=False)
    op.alter_column('subject_theory', 'theory_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Идентификатор теории',
               existing_nullable=False)
    op.drop_table_comment(
        'subject_tasks',
        existing_comment='Задания для предмета. У каждого предмета может быть несколько заданий',
        schema=None
    )
    op.alter_column('subject_tasks', 'subject_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Идентификатор предмета',
               existing_nullable=True)
    op.alter_column('subject_tasks', 'completed',
               existing_type=sa.BOOLEAN(),
               comment=None,
               existing_comment='Статус задания',
               existing_nullable=True)
    op.alter_column('subject_tasks', 'task_name',
               existing_type=sa.VARCHAR(),
               comment=None,
               existing_comment='Название задания',
               existing_nullable=False)
    op.alter_column('subject_tasks', 'subject_task_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Идентификатор задания',
               existing_nullable=False,
               autoincrement=True)
    op.drop_table_comment(
        'grades',
        existing_comment='Оценки студентов по предметам',
        schema=None
    )
    op.alter_column('grades', 'grade_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='Дата выставления оценки',
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('grades', 'grade_value',
               existing_type=sa.INTEGER(),
               nullable=True,
               comment=None,
               existing_comment='Сама оценка')
    op.alter_column('grades', 'enrollment_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               comment=None,
               existing_comment='Идентификатор записи о подписке')
    op.alter_column('grades', 'grade_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Идентификатор оценки',
               existing_nullable=False,
               autoincrement=True)
    op.drop_table_comment(
        'enrollments',
        existing_comment='Записи о подписках пользователей на предметы',
        schema=None
    )
    op.alter_column('enrollments', 'completed',
               existing_type=sa.BOOLEAN(),
               comment=None,
               existing_comment='Статус завершения предмета',
               existing_nullable=True)
    op.alter_column('enrollments', 'enrollment_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='Дата подписки',
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('enrollments', 'subject_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               comment=None,
               existing_comment='Предмет, на который подписался пользователь. Сам предмет')
    op.alter_column('enrollments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               comment=None,
               existing_comment='Пользователь, подписавшийся на предмет')
    op.alter_column('enrollments', 'enrollment_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Идентификатор записи о подписке',
               existing_nullable=False,
               autoincrement=True)
    op.create_table('completed_task_status',
    sa.Column('subject_task_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('completed', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['subject_task_id'], ['subject_tasks.subject_task_id'], name='completed_task_status_subject_task_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='completed_task_status_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('subject_task_id', 'user_id', name='completed_task_status_pkey')
    )
    op.drop_table('user_task_files')
    # ### end Alembic commands ###