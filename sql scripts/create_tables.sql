CREATE TABLE users
(
    user_id      UUID    NOT NULL PRIMARY KEY,
    last_name    varchar,
    first_name   varchar,
    middle_name  varchar,
    age          integer,
    "group"      varchar,
    course       integer,
    email        varchar NOT NULL,
    username     varchar NOT NULL UNIQUE,
    password     varchar NOT NULL,
    is_staff     boolean                  DEFAULT FALSE,
    is_superuser boolean                  DEFAULT FALSE,
    created_at   timestamp WITH TIME ZONE DEFAULT now(),
    user_image   varchar                  DEFAULT 'default_user_image.png'::CHARACTER varying
);

COMMENT ON TABLE users IS 'Таблица пользователей';

COMMENT ON COLUMN users.user_id IS 'User id column';

COMMENT ON COLUMN users.last_name IS 'Фамилия';

COMMENT ON COLUMN users.first_name IS 'Имя';

COMMENT ON COLUMN users.middle_name IS 'Отчество';

COMMENT ON COLUMN users.course IS 'Курс обучения';

COMMENT ON COLUMN users.username IS 'уникальное Имя пользователя';

COMMENT ON COLUMN users.is_staff IS 'является ли пользователь частью персонала (преподаватель)';

COMMENT ON COLUMN users.is_superuser IS 'является ли пользователь суперпользователем';

COMMENT ON COLUMN users.created_at IS 'Дата создания пользователя';

COMMENT ON COLUMN users.user_image IS 'Изображение пользователя';


CREATE TABLE subjects
(
    subject_id        UUID                                                   NOT NULL PRIMARY KEY,
    user_id           UUID                                                   NOT NULL REFERENCES users ON DELETE CASCADE,
    subject_name      varchar                                                NOT NULL,
    short_description varchar                                                NOT NULL,
    description       varchar                                                NOT NULL,
    subject_image     varchar DEFAULT 'subject_image.png'::CHARACTER varying NOT NULL
);

COMMENT ON TABLE subjects IS 'Предметы, на которые подписаны пользователи. У каждого пользователя может быть несколько предметов';

COMMENT ON COLUMN subjects.subject_id IS 'Идентификатор предмета';

COMMENT ON COLUMN subjects.user_id IS 'Идентификатор пользователя';

COMMENT ON COLUMN subjects.subject_name IS 'Название предмета';

COMMENT ON COLUMN subjects.short_description IS 'Краткое описание предмета';

COMMENT ON COLUMN subjects.description IS 'Полное описание предмета';

COMMENT ON COLUMN subjects.subject_image IS 'Изображения для предмета';


CREATE TABLE task
(
    task_id   UUID    NOT NULL PRIMARY KEY,
    task_name varchar NOT NULL,
    completed boolean DEFAULT FALSE,
    user_id   UUID    NOT NULL REFERENCES users
);

COMMENT ON TABLE task IS 'Todo list. Задания пользователей которые они должны выполнить (цели). ';

COMMENT ON COLUMN task.task_id IS 'Идентификатор задания';

COMMENT ON COLUMN task.task_name IS 'Название задания';

COMMENT ON COLUMN task.completed IS 'Статус задания';

COMMENT ON COLUMN task.user_id IS 'Пользователь которому принадлежит задание';


CREATE TABLE teacher_information
(
    teacher_information_id UUID                  NOT NULL PRIMARY KEY,
    user_id                UUID                  NOT NULL REFERENCES users ON DELETE CASCADE,
    teacher_experience     integer,
    teacher_description    varchar,
    is_done                boolean DEFAULT FALSE NOT NULL
);

COMMENT ON TABLE teacher_information IS 'Дополнительная информация о преподавателе';

COMMENT ON COLUMN teacher_information.teacher_information_id IS 'идентификатор информации';

COMMENT ON COLUMN teacher_information.user_id IS 'id пользователя';

COMMENT ON COLUMN teacher_information.teacher_experience IS 'опыт преподавателя';

COMMENT ON COLUMN teacher_information.teacher_description IS 'Информация о преподавателе';


CREATE TABLE user_theme
(
    user_id    UUID                                       NOT NULL PRIMARY KEY REFERENCES users ON DELETE CASCADE,
    theme      varchar DEFAULT 'light'::CHARACTER varying NOT NULL,
    seed_color varchar DEFAULT 'green'::CHARACTER varying NOT NULL
);

COMMENT ON TABLE user_theme IS 'Цветовая схема пользователя (тема). Уникальная для каждого пользователя';

COMMENT ON COLUMN user_theme.user_id IS 'Идентификатор пользователя';

COMMENT ON COLUMN user_theme.theme IS 'Тема пользователя (светлая/темная)';

COMMENT ON COLUMN user_theme.seed_color IS 'Цвет цветовой схемы приложения';


CREATE TABLE enrollments
(
    enrollment_id   UUID NOT NULL PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES users ON DELETE CASCADE,
    subject_id      UUID NOT NULL REFERENCES subjects ON DELETE CASCADE,
    enrollment_date timestamp WITH TIME ZONE DEFAULT now(),
    completed       boolean                  DEFAULT FALSE
);

COMMENT ON TABLE enrollments IS 'Записи о подписках пользователей на предметы';

COMMENT ON COLUMN enrollments.enrollment_id IS 'Идентификатор записи о подписке';

COMMENT ON COLUMN enrollments.user_id IS 'Пользователь, подписавшийся на предмет';

COMMENT ON COLUMN enrollments.subject_id IS 'Предмет, на который подписался пользователь. Сам предмет';

COMMENT ON COLUMN enrollments.enrollment_date IS 'Дата подписки';

COMMENT ON COLUMN enrollments.completed IS 'Статус завершения предмета';


CREATE TABLE subject_tasks
(
    subject_task_id UUID    NOT NULL PRIMARY KEY,
    task_name       varchar NOT NULL,
    completed       boolean DEFAULT FALSE,
    subject_id      UUID REFERENCES subjects ON DELETE CASCADE
);

COMMENT ON TABLE subject_tasks IS 'Задания для предмета. У каждого предмета может быть несколько заданий';

COMMENT ON COLUMN subject_tasks.subject_task_id IS 'Идентификатор задания';

COMMENT ON COLUMN subject_tasks.task_name IS 'Название задания';

COMMENT ON COLUMN subject_tasks.completed IS 'Статус задания';

COMMENT ON COLUMN subject_tasks.subject_id IS 'Идентификатор предмета';


CREATE TABLE subject_theory
(
    theory_id   UUID NOT NULL PRIMARY KEY REFERENCES subjects ON DELETE CASCADE,
    theory_data varchar
);

COMMENT ON TABLE subject_theory IS 'Теория для предмета. У каждого предмета может быть только одна теория в виде файла';

COMMENT ON COLUMN subject_theory.theory_id IS 'Идентификатор теории';

COMMENT ON COLUMN subject_theory.theory_data IS 'Данные теории (файл, текст, ссылка)';


CREATE TABLE grades
(
    grade_id      UUID    NOT NULL PRIMARY KEY,
    enrollment_id UUID    NOT NULL REFERENCES enrollments ON DELETE CASCADE,
    grade_value   integer NOT NULL,
    grade_date    timestamp WITH TIME ZONE DEFAULT now()
);

COMMENT ON TABLE grades IS 'Итоговая оценка студентов по предметам';

COMMENT ON COLUMN grades.grade_id IS 'Идентификатор оценки';

COMMENT ON COLUMN grades.enrollment_id IS 'Идентификатор записи о подписке';

COMMENT ON COLUMN grades.grade_value IS 'Сама оценка';

COMMENT ON COLUMN grades.grade_date IS 'Дата выставления оценки';


CREATE TABLE task_grades
(
    task_grade_id   UUID                                   NOT NULL PRIMARY KEY,
    enrollment_id   UUID REFERENCES enrollments ON DELETE CASCADE,
    subject_task_id UUID                                   NOT NULL REFERENCES subject_tasks ON DELETE CASCADE,
    user_id         UUID                                   NOT NULL REFERENCES users ON DELETE CASCADE,
    grade_value     integer                                NOT NULL,
    grade_date      timestamp WITH TIME ZONE DEFAULT now() NOT NULL
);

COMMENT ON TABLE task_grades IS 'Оценки за задания по предметам';

COMMENT ON COLUMN task_grades.task_grade_id IS 'Идентификатор оценки за задание';

COMMENT ON COLUMN task_grades.enrollment_id IS 'Идентификатор записи о подписке';

COMMENT ON COLUMN task_grades.subject_task_id IS 'Идентификатор задания';

COMMENT ON COLUMN task_grades.user_id IS 'Идентификатор пользователя, который выполнил задание';

COMMENT ON COLUMN task_grades.grade_value IS 'Оценка за задание';

COMMENT ON COLUMN task_grades.grade_date IS 'Дата постановки оценки';


CREATE TABLE user_task_files
(
    subject_task_id UUID                 NOT NULL REFERENCES subject_tasks ON DELETE CASCADE,
    user_id         UUID                 NOT NULL REFERENCES users ON DELETE CASCADE,
    enrollment_id   UUID                 NOT NULL REFERENCES enrollments ON DELETE CASCADE,
    task_file       varchar              NOT NULL,
    completed       boolean DEFAULT TRUE NOT NULL,
    PRIMARY KEY (subject_task_id,
                 user_id)
);

COMMENT ON TABLE user_task_files IS 'Файлы для заданий пользователей. К каждому заданию может быть прикреплено несколько файлов';

COMMENT ON COLUMN user_task_files.subject_task_id IS 'Идентификатор задания';

COMMENT ON COLUMN user_task_files.user_id IS 'пользователь';

COMMENT ON COLUMN user_task_files.enrollment_id IS 'предмет на который записан пользователй';

COMMENT ON COLUMN user_task_files.task_file IS 'файл прикрепленный к заданию';

COMMENT ON COLUMN user_task_files.completed IS 'Отправил ли ученик задание';