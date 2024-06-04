create table subject_tasks
(
    subject_task_id uuid    not null
        primary key,
    task_name       varchar not null,
    completed       boolean default false,
    subject_id      uuid
        references subjects
            on delete cascade
);

comment on table subject_tasks is 'Задания для предмета. У каждого предмета может быть несколько заданий';

comment on column subject_tasks.subject_task_id is 'Идентификатор задания';

comment on column subject_tasks.task_name is 'Название задания';

comment on column subject_tasks.completed is 'Статус задания';

comment on column subject_tasks.subject_id is 'Идентификатор предмета';

null, 2);