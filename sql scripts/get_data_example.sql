SELECT
    Users.user_id,
  Subjects.subject_name AS subject_name,
  Grades.grade_value AS grade_value
FROM
    Users
JOIN
  Enrollments ON Users.user_id = Enrollments.user_id
JOIN
  Subjects ON Enrollments.subject_id = Subjects.subject_id
JOIN
  Grades ON Enrollments.enrollment_id = Grades.enrollment_id
WHERE
    Subjects.subject_name = 'Database Management'
AND
    Users.user_id = 1