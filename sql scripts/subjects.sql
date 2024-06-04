create table subjects
(
    subject_id        uuid                                                   not null
        primary key,
    user_id           uuid                                                   not null
        references users
            on delete cascade,
    subject_name      varchar                                                not null,
    short_description varchar                                                not null,
    description       varchar                                                not null,
    subject_image     varchar default 'subject_image.png'::character varying not null
);

comment on table subjects is 'Предметы, на которые подписаны пользователи. У каждого пользователя может быть несколько предметов';

comment on column subjects.subject_id is 'Идентификатор предмета';

comment on column subjects.user_id is 'Идентификатор пользователя';

comment on column subjects.subject_name is 'Название предмета';

comment on column subjects.short_description is 'Краткое описание предмета';

comment on column subjects.description is 'Полное описание предмета';

comment on column subjects.subject_image is 'Изображения для предмета';

