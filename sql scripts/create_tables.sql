-- Таблица курсов
CREATE TABLE Subjects
(
    subject_id   SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    description  TEXT,
    short_description VARCHAR(250) NOT NULL
);

CREATE TABLE SubjectTasks
(
    subject_task_id SERIAL PRIMARY KEY NOT NULL UNIQUE,
    task_name VARCHAR(250) NOT NULL UNIQUE,
    completed BOOLEAN default false,
    subject_id INTEGER,

    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);

-- Таблица пользователей
CREATE TABLE Users
(
    user_id      SERIAL PRIMARY KEY,
    last_name    VARCHAR(250),
    first_name   VARCHAR(250),
    middle_name  VARCHAR(250),
    age          INT,
    "group"      VARCHAR(250),
    course       INT,
    email        VARCHAR(250),
    username     VARCHAR(250) NOT NULL UNIQUE,
    password     VARCHAR(250) NOT NULL,
    is_staff     BOOLEAN   DEFAULT false,
    is_superuser BOOLEAN   DEFAULT false,
    created_at   TIMESTAMP DEFAULT now(),
    user_image   VARCHAR(250) NOT NULL
);

-- Таблица записей на курсы (связывает студентов и курсы)
CREATE TABLE Enrollments
(
    enrollment_id   SERIAL PRIMARY KEY,
    user_id         INT,
    subject_id      INT,
    enrollment_date TIMESTAMP DEFAULT now(),
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (subject_id) REFERENCES Subjects (subject_id)
);

-- Таблица оценок
CREATE TABLE Grades
(
    grade_id      SERIAL PRIMARY KEY,
    enrollment_id INT,
    grade_value   FLOAT,
    grade_date    TIMESTAMP DEFAULT now(),
    FOREIGN KEY (enrollment_id) REFERENCES Enrollments (enrollment_id)
);