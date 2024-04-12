import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import Connection
from database.models import Users, Subjects, Enrollments, Grades, SubjectTasks

# Подключение к базе данных
engine = create_engine(Connection.DATABASE_URL)  # Подставьте свою строку подключения
Session = sessionmaker(bind=engine)
session = Session()

# Создание записей в таблице Users
users_data = [
    {'last_name': 'Николаева', 'first_name': 'Анна', 'middle_name': 'Владимеровна', 'age': 22, 'group': '',
     'course': 0, 'email': 'john.doe@gmail.com', 'username': 'john123',
     'password': '$2b$12$vPWDJZG7l2DgjBMn.NOjhuG9MPNtxZTTu/OT/6YgVSSu4nclJptjm',
     'is_staff': True},
    {'last_name': 'Алексеев', 'first_name': 'Денис', 'middle_name': 'Вадимович', 'age': 23, 'group': 'Р12',
     'course': 3, 'email': 'jane.smith@gmial.com', 'username': 'jane123',
     'password': '$2b$12$vPWDJZG7l2DgjBMn.NOjhuG9MPNtxZTTu/OT/6YgVSSu4nclJptjm',
     'is_staff': True},
    {'last_name': 'Маркочев', 'first_name': 'Данила', 'middle_name': 'Альбертович', 'age': 19, 'group': 'ИСП12',
     'course': 1, 'email': 'markoch.johnson@gmail.com', 'username': 'mark123',
     'password': '$2b$12$vPWDJZG7l2DgjBMn.NOjhuG9MPNtxZTTu/OT/6YgVSSu4nclJptjm',
     'is_staff': False},
    {'last_name': 'Альберт', 'first_name': 'Юрий', 'middle_name': 'Максимович', 'age': 24, 'group': 'ИСП32',
     'course': 1, 'email': 'bob.johnson@gmail.com', 'username': 'albert123',
     'password': '$2b$12$vPWDJZG7l2DgjBMn.NOjhuG9MPNtxZTTu/OT/6YgVSSu4nclJptjm',
     'is_staff': False},
    {'last_name': 'Валериева', 'first_name': 'Аннита', 'middle_name': 'Бековна', 'age': 24, 'group': 'МП12',
     'course': 1, 'email': 'bob.johnson@gmail.com', 'username': 'anita123',
     'password': '$2b$12$vPWDJZG7l2DgjBMn.NOjhuG9MPNtxZTTu/OT/6YgVSSu4nclJptjm',
     'is_staff': False}
]

for user_data in users_data:
    user_data['user_id'] = uuid.uuid4()  # Генерация UUID для идентификатора пользователя
    user = Users(**user_data)
    session.add(user)
session.commit()

# Создание записей в таблице Subjects
subjects_data = [
    {'subject_name': 'Математика', 'short_description': 'Изучение чисел и форм',
     'description': 'Математика — это наука о числах, количестве и пространстве.', "user_id": users_data[0]['user_id']},
    {'subject_name': 'Естествознание', 'short_description': 'Исследование природы',
     'description': 'Естествознание — систематическое изучение природы и её законов.',
     "user_id": users_data[0]['user_id']},
    {'subject_name': 'История', 'short_description': 'Изучение прошлых событий',
     'description': 'История — наука о прошлом.', "user_id": users_data[1]['user_id']},
    {'subject_name': 'Литература', 'short_description': 'Изучение письменных произведений',
     'description': 'Литература — письменные произведения, особенно те, которые считаются выдающимися или имеющими долговечное художественное значение.',
     "user_id": users_data[0]['user_id']},
    {'subject_name': 'Информатика', 'short_description': 'Изучение алгоритмов и вычислительных процессов',
     'description': 'Информатика — наука о методах и процессах сбора, хранения, обработки, передачи информации.',
     "user_id": users_data[1]['user_id']}
]

for subject_data in subjects_data:
    subject_data['subject_id'] = uuid.uuid4()  # Генерация UUID для идентификатора предмета
    subject = Subjects(**subject_data)
    session.add(subject)
session.commit()

# Вставка тестовых данных в таблицу Enrollments
enrollments_data = [
    {'user_id': users_data[2]['user_id'], 'subject_id': subjects_data[0]['subject_id']},
    {'user_id': users_data[3]['user_id'], 'subject_id': subjects_data[3]['subject_id']},
    {'user_id': users_data[2]['user_id'], 'subject_id': subjects_data[1]['subject_id']},
    {'user_id': users_data[3]['user_id'], 'subject_id': subjects_data[4]['subject_id']},
    {'user_id': users_data[4]['user_id'], 'subject_id': subjects_data[1]['subject_id']}
]

for enrollment_data in enrollments_data:
    enrollment_data['enrollment_id'] = uuid.uuid4()  # Генерация UUID для идентификатора записи о подписке
    enrollment = Enrollments(**enrollment_data)
    session.add(enrollment)
session.commit()

# Вставка тестовых данных в таблицу Grades
grades_data = [
    {'enrollment_id': enrollments_data[0]['enrollment_id'], 'grade_value': 90},
    {'enrollment_id': enrollments_data[1]['enrollment_id'], 'grade_value': 85},
    {'enrollment_id': enrollments_data[2]['enrollment_id'], 'grade_value': 69},
    {'enrollment_id': enrollments_data[3]['enrollment_id'], 'grade_value': 95},
    {'enrollment_id': enrollments_data[4]['enrollment_id'], 'grade_value': 88}
]

for grade_data in grades_data:
    grade_data['grade_id'] = uuid.uuid4()  # Генерация UUID для идентификатора оценки
    grade = Grades(**grade_data)
    session.add(grade)

# Сохранение изменений в таблице Grades
session.commit()

# Вставка тестовых данных в таблицу SubjectTasks
subject_tasks_data = [
    {'task_name': 'Решить уравнение', 'subject_id': subjects_data[0]['subject_id']},
    {'task_name': 'Изучить законы Ньютона', 'subject_id': subjects_data[1]['subject_id']},
    {'task_name': 'Написать эссе о Первой мировой войне', 'subject_id': subjects_data[2]['subject_id']},
    {'task_name': 'Прочитать роман "Преступление и наказание"', 'subject_id': subjects_data[3]['subject_id']},
    {'task_name': 'Написать программу для сортировки данных', 'subject_id': subjects_data[4]['subject_id']},
    {'task_name': 'Решить дискриминантное уравнение', 'subject_id': subjects_data[0]['subject_id']},
    {'task_name': 'Изучить экватор, что это такое', 'subject_id': subjects_data[1]['subject_id']},
    {'task_name': 'Узнать сколько звезд есть в галактике', 'subject_id': subjects_data[1]['subject_id']}
]

for task_data in subject_tasks_data:
    task_data['subject_task_id'] = uuid.uuid4()  # Генерация UUID для идентификатора задания
    task = SubjectTasks(**task_data)
    session.add(task)

# Сохранение изменений в таблице SubjectTasks
session.commit()
