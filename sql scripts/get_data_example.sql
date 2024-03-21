SELECT DISTINCT
    Users.user_id,
  Subjects.subject_name AS subject_name,
  Grades.grade_value AS grade_value,
  subject_tasks.task_name
FROM
    Users
JOIN
  Enrollments ON Users.user_id = Enrollments.user_id
JOIN
  Subjects ON Enrollments.subject_id = Subjects.subject_id
JOIN
  Grades ON Enrollments.enrollment_id = Grades.enrollment_id
JOIN
    subject_tasks ON Subjects.subject_id = subject_tasks.subject_id
WHERE
    users.user_id = 4
