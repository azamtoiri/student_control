create table task
(
    task_id   uuid    not null
        primary key,
    task_name varchar not null,
    completed boolean default false,
    user_id   uuid    not null
        references users
);

comment on table task is 'Todo list. Задания пользователей которые они должны выполнить (цели). ';

comment on column task.task_id is 'Идентификатор задания';

comment on column task.task_name is 'Название задания';

comment on column task.completed is 'Статус задания';

comment on column task.user_id is 'Пользователь которому принадлежит задание';

