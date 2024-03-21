-- Вставка тестовых данных в таблицу Users password default admin all users
INSERT INTO Users (last_name, first_name, middle_name, age, "group", course, email, username, password, is_staff)
VALUES
  ('Николаева', 'Анна', 'Владимеровна', 22, '', 0, 'john.doe@gmail.com', 'john123', '$2b$12$vPWDJZG7l2DgjBMn.NOjhuG9MPNtxZTTu/OT/6YgVSSu4nclJptjm', true),
  ('Алексеев', 'Денис', 'Вадимович', 23, 'Р12', 3, 'jane.smith@gmial.com', 'jane123', '$2b$12$vPWDJZG7l2DgjBMn.NOjhuG9MPNtxZTTu/OT/6YgVSSu4nclJptjm', true),
  ('Маркочев', 'Данила', 'Альбертович', 19, 'ИСП12', 1, 'markoch.johnson@gmail.com', 'mark123', '$2b$12$vPWDJZG7l2DgjBMn.NOjhuG9MPNtxZTTu/OT/6YgVSSu4nclJptjm', false),
  ('Альберт', 'Юрий', 'Максимович', 24, 'ИСП32', 1, 'bob.johnson@gmail.com', 'albert123', '$2b$12$vPWDJZG7l2DgjBMn.NOjhuG9MPNtxZTTu/OT/6YgVSSu4nclJptjm', false),
  ('Валериева', 'Аннита', 'Бековна', 24, 'МП12', 1, 'bob.johnson@gmail.com', 'anita123', '$2b$12$vPWDJZG7l2DgjBMn.NOjhuG9MPNtxZTTu/OT/6YgVSSu4nclJptjm', false);

-- Вставка тестовых данных в таблицу Courses (оставляем прежние данные)
INSERT INTO subjects (subject_name, short_description, description, user_id)
VALUES
('Математика', 'Изучение чисел и форм', 'Математика — это наука о числах, количестве и пространстве.', 1),
('Естествознание', 'Исследование природы', 'Естествознание — систематическое изучение природы и её законов.', 2),
('История', 'Изучение прошлых событий', 'История — наука о прошлом.', 1),
('Литература', 'Изучение письменных произведений', 'Литература — письменные произведения, особенно те, которые считаются выдающимися или имеющими долговечное художественное значение.', 2),
('Информатика', 'Изучение алгоритмов и вычислительных процессов', 'Информатика — наука о методах и процессах сбора, хранения, обработки, передачи информации.', 1);

-- Вставка тестовых данных в таблицу Enrollments
INSERT INTO Enrollments (user_id, subject_id)
VALUES
  (4, 1),
  (4, 4),
  (5, 2),
  (6, 5),
  (6, 2);

-- Вставка тестовых данных в таблицу Grades
INSERT INTO Grades (enrollment_id, grade_value)
VALUES
  (1, 90),
  (2, 85),
  (5, 69),
  (3, 95),
  (4, 88);

INSERT INTO subject_tasks (task_name, subject_id)
VALUES
('Решить уравнение', 1),
('Изучить законы Ньютона', 2),
('Написать эссе о Первой мировой войне', 3),
('Прочитать роман "Преступление и наказание"',  4),
('Написать программу для сортировки данных', 5);
