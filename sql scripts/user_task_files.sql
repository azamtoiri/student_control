create table user_task_files
(
    subject_task_id uuid                 not null
        references subject_tasks
            on delete cascade,
    user_id         uuid                 not null
        references users
            on delete cascade,
    enrollment_id   uuid                 not null
        references enrollments
            on delete cascade,
    task_file       varchar              not null,
    completed       boolean default true not null,
    primary key (subject_task_id, user_id)
);

comment on table user_task_files is 'Файлы для заданий пользователей. К каждому заданию может быть прикреплено несколько файлов';

comment on column user_task_files.subject_task_id is 'Идентификатор задания';

comment on column user_task_files.user_id is 'пользователь';

comment on column user_task_files.enrollment_id is 'предмет на который записан пользователй';

comment on column user_task_files.task_file is 'файл прикрепленный к заданию';

comment on column user_task_files.completed is 'Отправил ли ученик задание';

