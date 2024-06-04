create table enrollments
(
    enrollment_id   uuid not null
        primary key,
    user_id         uuid not null
        references users
            on delete cascade,
    subject_id      uuid not null
        references subjects
            on delete cascade,
    enrollment_date timestamp with time zone default now(),
    completed       boolean                  default false
);

comment on table enrollments is 'Записи о подписках пользователей на предметы';

comment on column enrollments.enrollment_id is 'Идентификатор записи о подписке';

comment on column enrollments.user_id is 'Пользователь, подписавшийся на предмет';

comment on column enrollments.subject_id is 'Предмет, на который подписался пользователь. Сам предмет';

comment on column enrollments.enrollment_date is 'Дата подписки';

comment on column enrollments.completed is 'Статус завершения предмета';

