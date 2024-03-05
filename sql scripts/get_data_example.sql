SELECT
  Users.first_name AS student_first_name,
  Users.last_name AS student_last_name,
  Subjects.subject_name AS subject_name,
  Grades.grade_value AS grade_value,
  Grades.grade_date AS grade_date
FROM
    Users
JOIN
  Enrollments ON Users.user_id = Enrollments.user_id
JOIN
  Subjects ON Enrollments.subject_id = Subjects.subject_id
JOIN
  Grades ON Enrollments.enrollment_id = Grades.enrollment_id
WHERE
  Users.user_id = 1