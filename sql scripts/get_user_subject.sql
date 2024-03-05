SELECT
    users.first_name,
    users.last_name,
    Subjects.subject_name
FROM users
INNER JOIN
  Enrollments ON Users.user_id = Enrollments.user_id
INNER JOIN
  Subjects ON Enrollments.subject_id = Subjects.subject_id
WHERE
    users.user_id = 2