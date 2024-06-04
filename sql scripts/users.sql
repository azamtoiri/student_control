create table users
(
    user_id      uuid    not null
        primary key,
    last_name    varchar,
    first_name   varchar,
    middle_name  varchar,
    age          integer,
    "group"      varchar,
    course       integer,
    email        varchar not null,
    username     varchar not null
        unique,
    password     varchar not null,
    is_staff     boolean                  default false,
    is_superuser boolean                  default false,
    created_at   timestamp with time zone default now(),
    user_image   varchar                  default 'default_user_image.png'::character varying
);

comment on table users is 'Таблица пользователей';

comment on column users.user_id is 'User id column';

comment on column users.last_name is 'Фамилия';

comment on column users.first_name is 'Имя';

comment on column users.middle_name is 'Отчество';

comment on column users.course is 'Курс обучения';

comment on column users.username is 'уникальное Имя пользователя';

comment on column users.is_staff is 'является ли пользователь частью персонала (преподаватель)';

comment on column users.is_superuser is 'является ли пользователь суперпользователем';

comment on column users.created_at is 'Дата создания пользователя';

comment on column users.user_image is 'Изображение пользователя';

IBgcoEFo14y3JIhUXu', false, false, '2024-03-21 22:21:01.053280 +00:00', '99px_ru_wallpaper_283670_devushka_s_sirenevimi_volosami_i_dredami_v_profil.jpg');