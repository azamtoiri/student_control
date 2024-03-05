-- Вставка тестовых данных в таблицу Users
INSERT INTO Users (last_name, first_name, middle_name, age, "group", course, email, username, password )
VALUES
  ('Doe', 'John', 'Middle', 22, 'GroupA', 2, 'john.doe@example.com', 'john123', 'password123'),
  ('Smith', 'Jane', 'Anne', 23, 'GroupB', 3, 'jane.smith@example.com', 'jane123', 'password456' ),
  ('Johnson', 'Bob', 'Robert', 24, 'GroupC', 1, 'bob.johnson@example.com', 'bob123', 'password789' );

-- Вставка тестовых данных в таблицу Courses (оставляем прежние данные)
INSERT INTO Subjects (subject_name, description)
VALUES
  ('Introduction to Programming', 'Learn the basics of programming'),
  ('Database Management', 'Explore the world of database systems'),
  ('Web Development', 'Build dynamic and interactive websites');

-- Вставка тестовых данных в таблицу Enrollments
INSERT INTO Enrollments (user_id, subject_id)
VALUES
  (1, 1),
  (1, 2),
  (2, 3),
  (3, 1);

-- Вставка тестовых данных в таблицу Grades
INSERT INTO Grades (enrollment_id, grade_value)
VALUES
  (1, 90),
  (2, 85),
  (3, 95),
  (4, 88);
