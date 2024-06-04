create table teacher_information
(
    teacher_information_id uuid                  not null
        primary key,
    user_id                uuid                  not null
        references users
            on delete cascade,
    teacher_experience     integer,
    teacher_description    varchar,
    is_done                boolean default false not null
);

comment on table teacher_information is 'Дополнительная информация о преподавателе';

comment on column teacher_information.teacher_information_id is 'идентификатор информации';

comment on column teacher_information.user_id is 'id пользователя';

comment on column teacher_information.teacher_experience is 'опыт преподавателя';

comment on column teacher_information.teacher_description is 'Информация о преподавателе';

