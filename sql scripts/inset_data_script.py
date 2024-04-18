import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import Connection
from database.models import Users, Subjects, Enrollments, Grades, SubjectTasks, SubjectTheory, TeacherInformation, \
    UserTasksFiles

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
     'description': 'Математика - это широкая и глубокая наука, занимающаяся изучением чисел, форм, структур и отношений. Она пронизывает практически все области науки, техники и повседневной жизни, предоставляя инструменты для анализа и решения различных задач. Одной из основных областей математики является арифметика, которая изучает основные арифметические операции - сложение, вычитание, умножение и деление, а также их свойства и законы. Геометрия занимается изучением фигур, их свойств и взаимных отношений в пространстве. Алгебра и анализ рассматривают структуры и операции над ними, такие как алгебраические уравнения, функции и производные. Математика также играет важную роль в научных исследованиях, физике, экономике, информатике, инженерии и многих других областях. Она предоставляет инструменты для моделирования и анализа сложных систем, а также разработки алгоритмов и методов решения задач. Более того, математика является искусством само по себе, вдохновляя ученых и математиков на создание новых теорий и методов, а также на поиск красоты и гармонии в мире чисел и форм.',
     "user_id": users_data[0]['user_id']},
    {'subject_name': 'Естествознание', 'short_description': 'Исследование природы',
     'description': 'Естествознание - это научная дисциплина, изучающая природу и ее законы. В ее основе лежит стремление к пониманию мира через наблюдение, эксперимент и анализ. Естественные науки включают в себя такие области как физика, химия, биология, астрономия и геология. Физика изучает основные законы природы, такие как законы движения, электромагнетизм и термодинамика. Химия занимается строением вещества и химическими реакциями. Биология изучает живые организмы и их взаимодействие с окружающей средой. Астрономия исследует космос, звезды, планеты и галактики. Геология изучает структуру Земли, ее геологическую историю и процессы, происходящие на ее поверхности. Естествознание играет важную роль в понимании мира и в развитии технологий. Оно помогает нам понять природные явления, предсказывать их развитие и использовать их в нашу пользу. Кроме того, естествознание способствует развитию критического мышления и научного метода, что является основой современной научной деятельности.',
     "user_id": users_data[0]['user_id']},
    {'subject_name': 'История', 'short_description': 'Изучение прошлых событий',
     'description': 'История - это наука о прошлом человечества, изучающая события, процессы, личности и культуру различных эпох и цивилизаций. Она помогает нам понять, как формировался и развивался мир, какие силы и события влияли на ход истории, и какие уроки можно извлечь из прошлого. История включает в себя изучение политических, социальных, экономических, культурных и религиозных аспектов жизни обществ и народов. Она позволяет нам понять, какие ошибки были допущены в прошлом и как избежать их в будущем, а также какие достижения и прогресс были достигнуты благодаря усилиям предыдущих поколений. История также помогает нам сформировать нашу идентичность, понять наше место в мире и принять наше прошлое, как часть нашего настоящего и будущего.',
     "user_id": users_data[1]['user_id']},
    {'subject_name': 'Литература', 'short_description': 'Изучение письменных произведений',
     'description': 'Литература - это искусство слова, выраженное в письменной форме. Она включает в себя различные литературные жанры, такие как проза, поэзия, драма, эссе, роман и т. д. Литература является не только средством развлечения, но и способом передачи идей, чувств, мыслей и опыта автора. Она отражает культурные, социальные и исторические аспекты общества, а также помогает нам понять человеческую природу и человеческие отношения. Через литературу мы можем погрузиться в разные эпохи и культуры, испытать разнообразные эмоции и пережить приключения воображаемых персонажей. Литература также способствует развитию языковых навыков, эмоционального интеллекта и критического мышления.',
     "user_id": users_data[0]['user_id']},
    {'subject_name': 'Информатика', 'short_description': 'Изучение алгоритмов и вычислительных процессов',
     'description': 'Информатика - это увлекательная наука о информации, ее обработке, передаче и хранении. В мире, где технологии играют все более важную роль, знание информатики становится ключом к успешной карьере и самореализации. На курсе по информатике вы познакомитесь с основами программирования, изучите алгоритмы и структуры данных, научитесь создавать веб-сайты и приложения, освоите навыки анализа данных и машинного обучения. Наша программа обучения разработана с учетом современных технологий и требований рынка труда, что позволит вам получить актуальные знания и навыки, необходимые для успешной карьеры в сфере информационных технологий. Присоединяйтесь к нам и откройте для себя мир возможностей, который открывает перед вами информатика!',
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

# Добавление данных в таблицу SubjectTheory
subject_theory_data = [
    {'theory_data': 'test_theory.pdf', 'subject_id': subjects_data[0]['subject_id']},
    {'theory_data': 'test_theory.pdf', 'subject_id': subjects_data[1]['subject_id']}
]

for theory_data in subject_theory_data:
    theory_data['theory_id'] = uuid.uuid4()
    subject_theory = SubjectTheory(**theory_data)
    session.add(subject_theory)
session.commit()

teacher_info_data = [
    {'teacher_experience': 5, 'teacher_description': 'Опытный преподаватель', 'user_id': users_data[2]['user_id']}
]

for info_data in teacher_info_data:
    teacher_info = TeacherInformation(**info_data)
    session.add(teacher_info)
session.commit()

# Добавление данных в таблицу UserTasksFiles
user_tasks_files_data = [
    {
        'task_file': 'file1.pdf',
        'user_id': users_data[0]['user_id'],
        'enrollment_id': enrollments_data[0]['enrollment_id'],
        'subject_task_id': subject_tasks_data[0]['subject_task_id']
    },
    {
        'task_file': 'file2.pdf', 'user_id': users_data[1]['user_id'],
        'enrollment_id': enrollments_data[1]['enrollment_id'],
        'subject_task_id': subject_tasks_data[1]['subject_task_id']
    }
]

for file_data in user_tasks_files_data:
    user_tasks_file = UserTasksFiles(**file_data)
    session.add(user_tasks_file)
session.commit()

print("Данные успешно добавлены во все таблицы.")
