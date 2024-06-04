create table user_theme
(
    user_id    uuid                                       not null
        primary key
        references users
            on delete cascade,
    theme      varchar default 'light'::character varying not null,
    seed_color varchar default 'green'::character varying not null
);

comment on table user_theme is 'Цветовая схема пользователя (тема). Уникальная для каждого пользователя';

comment on column user_theme.user_id is 'Идентификатор пользователя';

comment on column user_theme.theme is 'Тема пользователя (светлая/темная)';

comment on column user_theme.seed_color is 'Цвет цветовой схемы приложения';

