create table task_grades
(
    task_grade_id   uuid                                   not null
        primary key,
    enrollment_id   uuid
        references enrollments
            on delete cascade,
    subject_task_id uuid                                   not null
        references subject_tasks
            on delete cascade,
    user_id         uuid                                   not null
        references users
            on delete cascade,
    grade_value     integer                                not null,
    grade_date      timestamp with time zone default now() not null
);

comment on table task_grades is 'Оценки за задания по предметам';

comment on column task_grades.task_grade_id is 'Идентификатор оценки за задание';

comment on column task_grades.enrollment_id is 'Идентификатор записи о подписке';

comment on column task_grades.subject_task_id is 'Идентификатор задания';

comment on column task_grades.user_id is 'Идентификатор пользователя, который выполнил задание';

comment on column task_grades.grade_value is 'Оценка за задание';

comment on column task_grades.grade_date is 'Дата постановки оценки';

