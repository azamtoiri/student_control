from .student_repository import StudentRepository
from .task_repository import TaskRepository
from .teacher_repository import TeacherRepository
from .user_repository import UserRepository
from .user_theme_repository import UserThemeRepository

student_repository = StudentRepository()
task_repository = TaskRepository()
teacher_repository = TeacherRepository()
user_theme_repository = UserThemeRepository()
user_repository = UserRepository()
