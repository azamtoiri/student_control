create table grades
(
    grade_id      uuid    not null
        primary key,
    enrollment_id uuid    not null
        references enrollments
            on delete cascade,
    grade_value   integer not null,
    grade_date    timestamp with time zone default now()
);

comment on table grades is 'Итоговая оценка студентов по предметам';

comment on column grades.grade_id is 'Идентификатор оценки';

comment on column grades.enrollment_id is 'Идентификатор записи о подписке';

comment on column grades.grade_value is 'Сама оценка';

comment on column grades.grade_date is 'Дата выставления оценки';

