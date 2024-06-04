create table subject_theory
(
    theory_id   uuid not null
        primary key
        references subjects
            on delete cascade,
    theory_data varchar
);

comment on table subject_theory is 'Теория для предмета. У каждого предмета может быть только одна теория в виде файла';

comment on column subject_theory.theory_id is 'Идентификатор теории';

comment on column subject_theory.theory_data is 'Данные теории (файл, текст, ссылка)';

