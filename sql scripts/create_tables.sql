CREATE TABLE IF NOT EXISTS ALEMBIC_VERSION
(
    VERSION_NUM VARCHAR(32) NOT NULL
        CONSTRAINT ALEMBIC_VERSION_PKC
            PRIMARY KEY
);

ALTER TABLE ALEMBIC_VERSION
    OWNER TO POSTGRES;

CREATE TABLE IF NOT EXISTS users
(
    user_id      UUID    NOT NULL
        PRIMARY KEY,
    last_name    VARCHAR,
    first_name   VARCHAR,
    middle_name  VARCHAR,
    age          INTEGER,
    "group"      VARCHAR,
    course       INTEGER,
    email        VARCHAR NOT NULL,
    username     VARCHAR NOT NULL
        UNIQUE,
    password     VARCHAR NOT NULL,
    is_staff     BOOLEAN                  DEFAULT FALSE,
    is_superuser BOOLEAN                  DEFAULT FALSE,
    created_at   TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_image   VARCHAR                  DEFAULT 'default_user_image.PNG'::CHARACTER VARYING
);

COMMENT ON TABLE users IS 'таблица пользователей';

COMMENT ON COLUMN users.user_id IS 'USER ID COLUMN';

COMMENT ON COLUMN users.last_name IS 'ФАМИЛИЯ';

COMMENT ON COLUMN users.first_name IS 'ИМЯ';

COMMENT ON COLUMN users.middle_name IS 'ОТЧЕСТВО';

COMMENT ON COLUMN users.course IS 'КУРС ОБУЧЕНИЯ';

COMMENT ON COLUMN users.username IS 'УНИКАЛЬНОЕ ИМЯ ПОЛЬЗОВАТЕЛЯ';

COMMENT ON COLUMN users.is_staff IS 'ЯВЛЯЕТСЯ ЛИ ПОЛЬЗОВАТЕЛЬ ЧАСТЬЮ ПЕРСОНАЛА (ПРЕПОДАВАТЕЛЬ)';

COMMENT ON COLUMN users.IS_SUPERUSER IS 'ЯВЛЯЕТСЯ ЛИ ПОЛЬЗОВАТЕЛЬ СУПЕРПОЛЬЗОВАТЕЛЕМ';

COMMENT ON COLUMN users.created_at IS 'ДАТА СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ';

COMMENT ON COLUMN users.user_image IS 'ИЗОБРАЖЕНИЕ ПОЛЬЗОВАТЕЛЯ';

ALTER TABLE users
    OWNER TO postgres;

CREATE TABLE IF NOT EXISTS subjects
(
    subject_id        UUID                                                   NOT NULL
        PRIMARY KEY,
    user_id           UUID                                                   NOT NULL
        REFERENCES USERS
            ON DELETE CASCADE,
    subject_name      VARCHAR                                                NOT NULL,
    short_description VARCHAR                                                NOT NULL,
    description       VARCHAR                                                NOT NULL,
    subject_image     VARCHAR DEFAULT 'subject_image.png'::CHARACTER VARYING NOT NULL
);

COMMENT ON TABLE SUBJECTS IS 'ПРЕДМЕТЫ, НА КОТОРЫЕ ПОДПИСАНЫ ПОЛЬЗОВАТЕЛИ. У КАЖДОГО ПОЛЬЗОВАТЕЛЯ МОЖЕТ БЫТЬ НЕСКОЛЬКО ПРЕДМЕТОВ';

COMMENT ON COLUMN SUBJECTS.SUBJECT_ID IS 'ИДЕНТИФИКАТОР ПРЕДМЕТА';

COMMENT ON COLUMN SUBJECTS.USER_ID IS 'ИДЕНТИФИКАТОР ПОЛЬЗОВАТЕЛЯ';

COMMENT ON COLUMN SUBJECTS.SUBJECT_NAME IS 'НАЗВАНИЕ ПРЕДМЕТА';

COMMENT ON COLUMN SUBJECTS.SHORT_DESCRIPTION IS 'КРАТКОЕ ОПИСАНИЕ ПРЕДМЕТА';

COMMENT ON COLUMN SUBJECTS.DESCRIPTION IS 'ПОЛНОЕ ОПИСАНИЕ ПРЕДМЕТА';

COMMENT ON COLUMN SUBJECTS.SUBJECT_IMAGE IS 'ИЗОБРАЖЕНИЯ ДЛЯ ПРЕДМЕТА';

ALTER TABLE SUBJECTS
    OWNER TO POSTGRES;

CREATE TABLE IF NOT EXISTS task
(
    task_id   UUID    NOT NULL
        PRIMARY KEY,
    task_name VARCHAR NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    user_id   UUID    NOT NULL
        REFERENCES users
);

COMMENT ON TABLE TASK IS 'TODO LIST. ЗАДАНИЯ ПОЛЬЗОВАТЕЛЕЙ КОТОРЫЕ ОНИ ДОЛЖНЫ ВЫПОЛНИТЬ (ЦЕЛИ). ';

COMMENT ON COLUMN TASK.TASK_ID IS 'ИДЕНТИФИКАТОР ЗАДАНИЯ';

COMMENT ON COLUMN TASK.TASK_NAME IS 'НАЗВАНИЕ ЗАДАНИЯ';

COMMENT ON COLUMN TASK.COMPLETED IS 'СТАТУС ЗАДАНИЯ';

COMMENT ON COLUMN TASK.USER_ID IS 'ПОЛЬЗОВАТЕЛЬ КОТОРОМУ ПРИНАДЛЕЖИТ ЗАДАНИЕ';

ALTER TABLE TASK
    OWNER TO POSTGRES;

CREATE TABLE IF NOT EXISTS TEACHER_INFORMATION
(
    teacher_information_id UUID                  NOT NULL
        PRIMARY KEY,
    user_id                UUID                  NOT NULL
        REFERENCES USERS
            ON DELETE CASCADE,
    teacher_experience     INTEGER,
    teacher_description    VARCHAR,
    is_done                BOOLEAN DEFAULT FALSE NOT NULL
);

COMMENT ON TABLE TEACHER_INFORMATION IS 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ О ПРЕПОДАВАТЕЛЕ';

COMMENT ON COLUMN TEACHER_INFORMATION.TEACHER_INFORMATION_ID IS 'ИДЕНТИФИКАТОР ИНФОРМАЦИИ';

COMMENT ON COLUMN TEACHER_INFORMATION.USER_ID IS 'ID ПОЛЬЗОВАТЕЛЯ';

COMMENT ON COLUMN TEACHER_INFORMATION.TEACHER_EXPERIENCE IS 'ОПЫТ ПРЕПОДАВАТЕЛЯ';

COMMENT ON COLUMN TEACHER_INFORMATION.TEACHER_DESCRIPTION IS 'ИНФОРМАЦИЯ О ПРЕПОДАВАТЕЛЕ';

ALTER TABLE TEACHER_INFORMATION
    OWNER TO POSTGRES;

CREATE TABLE IF NOT EXISTS USER_THEME
(
    user_id    UUID                                       NOT NULL
        PRIMARY KEY
        REFERENCES USERS
            ON DELETE CASCADE,
    theme      VARCHAR DEFAULT 'LIGHT'::CHARACTER VARYING NOT NULL,
    seed_color VARCHAR DEFAULT 'GREEN'::CHARACTER VARYING NOT NULL
);

COMMENT ON TABLE USER_THEME IS 'ЦВЕТОВАЯ СХЕМА ПОЛЬЗОВАТЕЛЯ (ТЕМА). УНИКАЛЬНАЯ ДЛЯ КАЖДОГО ПОЛЬЗОВАТЕЛЯ';

COMMENT ON COLUMN USER_THEME.USER_ID IS 'ИДЕНТИФИКАТОР ПОЛЬЗОВАТЕЛЯ';

COMMENT ON COLUMN USER_THEME.THEME IS 'ТЕМА ПОЛЬЗОВАТЕЛЯ (СВЕТЛАЯ/ТЕМНАЯ)';

COMMENT ON COLUMN USER_THEME.SEED_COLOR IS 'ЦВЕТ ЦВЕТОВОЙ СХЕМЫ ПРИЛОЖЕНИЯ';

ALTER TABLE USER_THEME
    OWNER TO POSTGRES;

CREATE TABLE IF NOT EXISTS ENROLLMENTS
(
    enrollment_id   UUID NOT NULL
        PRIMARY KEY,
    user_id         UUID NOT NULL
        REFERENCES users
            ON DELETE CASCADE,
    subject_id      UUID NOT NULL
        REFERENCES subjects
            ON DELETE CASCADE,
    enrollment_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed       BOOLEAN                  DEFAULT FALSE
);

COMMENT ON TABLE ENROLLMENTS IS 'ЗАПИСИ О ПОДПИСКАХ ПОЛЬЗОВАТЕЛЕЙ НА ПРЕДМЕТЫ';

COMMENT ON COLUMN ENROLLMENTS.ENROLLMENT_ID IS 'ИДЕНТИФИКАТОР ЗАПИСИ О ПОДПИСКЕ';

COMMENT ON COLUMN ENROLLMENTS.USER_ID IS 'ПОЛЬЗОВАТЕЛЬ, ПОДПИСАВШИЙСЯ НА ПРЕДМЕТ';

COMMENT ON COLUMN ENROLLMENTS.SUBJECT_ID IS 'ПРЕДМЕТ, НА КОТОРЫЙ ПОДПИСАЛСЯ ПОЛЬЗОВАТЕЛЬ. САМ ПРЕДМЕТ';

COMMENT ON COLUMN ENROLLMENTS.ENROLLMENT_DATE IS 'ДАТА ПОДПИСКИ';

COMMENT ON COLUMN ENROLLMENTS.COMPLETED IS 'СТАТУС ЗАВЕРШЕНИЯ ПРЕДМЕТА';

ALTER TABLE ENROLLMENTS
    OWNER TO POSTGRES;

CREATE TABLE IF NOT EXISTS subject_tasks
(
    subject_task_id UUID    NOT NULL
        PRIMARY KEY,
    task_name       VARCHAR NOT NULL,
    completed       BOOLEAN DEFAULT FALSE,
    subject_id      UUID
        REFERENCES subjects
            ON DELETE CASCADE
);

COMMENT ON TABLE SUBJECT_TASKS IS 'ЗАДАНИЯ ДЛЯ ПРЕДМЕТА. У КАЖДОГО ПРЕДМЕТА МОЖЕТ БЫТЬ НЕСКОЛЬКО ЗАДАНИЙ';

COMMENT ON COLUMN SUBJECT_TASKS.SUBJECT_TASK_ID IS 'ИДЕНТИФИКАТОР ЗАДАНИЯ';

COMMENT ON COLUMN SUBJECT_TASKS.TASK_NAME IS 'НАЗВАНИЕ ЗАДАНИЯ';

COMMENT ON COLUMN SUBJECT_TASKS.COMPLETED IS 'СТАТУС ЗАДАНИЯ';

COMMENT ON COLUMN SUBJECT_TASKS.SUBJECT_ID IS 'ИДЕНТИФИКАТОР ПРЕДМЕТА';

ALTER TABLE SUBJECT_TASKS
    OWNER TO POSTGRES;

CREATE TABLE IF NOT EXISTS subject_theory
(
    theory_id   UUID NOT NULL
        PRIMARY KEY
        REFERENCES subjects
            ON DELETE CASCADE,
    theory_data VARCHAR
);

COMMENT ON TABLE SUBJECT_THEORY IS 'ТЕОРИЯ ДЛЯ ПРЕДМЕТА. У КАЖДОГО ПРЕДМЕТА МОЖЕТ БЫТЬ ТОЛЬКО ОДНА ТЕОРИЯ В ВИДЕ ФАЙЛА';

COMMENT ON COLUMN SUBJECT_THEORY.THEORY_ID IS 'ИДЕНТИФИКАТОР ТЕОРИИ';

COMMENT ON COLUMN SUBJECT_THEORY.THEORY_DATA IS 'ДАННЫЕ ТЕОРИИ (ФАЙЛ, ТЕКСТ, ССЫЛКА)';

ALTER TABLE SUBJECT_THEORY
    OWNER TO POSTGRES;

CREATE TABLE IF NOT EXISTS grades
(
    grade_id      UUID    NOT NULL
        PRIMARY KEY,
    enrollment_id UUID    NOT NULL
        REFERENCES enrollments
            ON DELETE CASCADE,
    grade_value   INTEGER NOT NULL,
    grade_date    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE GRADES IS 'ИТОГОВАЯ ОЦЕНКА СТУДЕНТОВ ПО ПРЕДМЕТАМ';

COMMENT ON COLUMN GRADES.GRADE_ID IS 'ИДЕНТИФИКАТОР ОЦЕНКИ';

COMMENT ON COLUMN GRADES.ENROLLMENT_ID IS 'ИДЕНТИФИКАТОР ЗАПИСИ О ПОДПИСКЕ';

COMMENT ON COLUMN GRADES.GRADE_VALUE IS 'САМА ОЦЕНКА';

COMMENT ON COLUMN GRADES.GRADE_DATE IS 'ДАТА ВЫСТАВЛЕНИЯ ОЦЕНКИ';

ALTER TABLE GRADES
    OWNER TO POSTGRES;

CREATE TABLE IF NOT EXISTS task_grades
(
    task_grade_id   UUID                                   NOT NULL
        PRIMARY KEY,
    enrollment_id   UUID
        REFERENCES enrollments
            ON DELETE CASCADE,
    subject_task_id UUID                                   NOT NULL
        REFERENCES subject_tasks
            ON DELETE CASCADE,
    user_id         UUID                                   NOT NULL
        REFERENCES users
            ON DELETE CASCADE,
    grade_value     INTEGER                                NOT NULL,
    grade_date      TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

COMMENT ON TABLE TASK_GRADES IS 'ОЦЕНКИ ЗА ЗАДАНИЯ ПО ПРЕДМЕТАМ';

COMMENT ON COLUMN TASK_GRADES.TASK_GRADE_ID IS 'ИДЕНТИФИКАТОР ОЦЕНКИ ЗА ЗАДАНИЕ';

COMMENT ON COLUMN TASK_GRADES.ENROLLMENT_ID IS 'ИДЕНТИФИКАТОР ЗАПИСИ О ПОДПИСКЕ';

COMMENT ON COLUMN TASK_GRADES.SUBJECT_TASK_ID IS 'ИДЕНТИФИКАТОР ЗАДАНИЯ';

COMMENT ON COLUMN TASK_GRADES.USER_ID IS 'ИДЕНТИФИКАТОР ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ ВЫПОЛНИЛ ЗАДАНИЕ';

COMMENT ON COLUMN TASK_GRADES.GRADE_VALUE IS 'ОЦЕНКА ЗА ЗАДАНИЕ';

COMMENT ON COLUMN TASK_GRADES.GRADE_DATE IS 'ДАТА ПОСТАНОВКИ ОЦЕНКИ';

ALTER TABLE TASK_GRADES
    OWNER TO POSTGRES;

CREATE TABLE IF NOT EXISTS USER_TASK_FILES
(
    subject_task_id UUID                 NOT NULL
        REFERENCES subject_tasks
            ON DELETE CASCADE,
    user_id         UUID                 NOT NULL
        REFERENCES users
            ON DELETE CASCADE,
    enrollment_id   UUID                 NOT NULL
        REFERENCES enrollments
            ON DELETE CASCADE,
    task_file       VARCHAR              NOT NULL,
    completed       BOOLEAN DEFAULT TRUE NOT NULL,
    PRIMARY KEY (subject_task_id, user_id)
);

COMMENT ON TABLE USER_TASK_FILES IS 'ФАЙЛЫ ДЛЯ ЗАДАНИЙ ПОЛЬЗОВАТЕЛЕЙ. К КАЖДОМУ ЗАДАНИЮ МОЖЕТ БЫТЬ ПРИКРЕПЛЕНО НЕСКОЛЬКО ФАЙЛОВ';

COMMENT ON COLUMN USER_TASK_FILES.SUBJECT_TASK_ID IS 'ИДЕНТИФИКАТОР ЗАДАНИЯ';

COMMENT ON COLUMN USER_TASK_FILES.USER_ID IS 'ПОЛЬЗОВАТЕЛЬ';

COMMENT ON COLUMN USER_TASK_FILES.ENROLLMENT_ID IS 'ПРЕДМЕТ НА КОТОРЫЙ ЗАПИСАН ПОЛЬЗОВАТЕЛЙ';

COMMENT ON COLUMN USER_TASK_FILES.TASK_FILE IS 'ФАЙЛ ПРИКРЕПЛЕННЫЙ К ЗАДАНИЮ';

COMMENT ON COLUMN USER_TASK_FILES.COMPLETED IS 'ОТПРАВИЛ ЛИ УЧЕНИК ЗАДАНИЕ';

ALTER TABLE USER_TASK_FILES
    OWNER TO POSTGRES;

