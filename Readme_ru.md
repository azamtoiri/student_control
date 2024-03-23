# версия студенческого контроля 2.0 с flet_route

Использование библиотеки `flet_route` для маршрутизации между страницами и получения ресурсов и элементов управления из
первой версии [Student Control](https://github.com/azamtoiri/Flet_student_control)

# Пример файла `.env`

```dotenv
# ДАННЫЕ для версии для разработчиков
DATABASE_URL=postgresql+psycopg2://{пользователь}:{пароль}@{хост}:{порт}/{имя_базы_данных}
# БАЗА ДАННЫХ для локального тестирования и прочего
LOCAL_DB_URL=postgresql+psycopg2://{пользователь}:{пароль}@{хост}:{порт}/{имя_базы_данных}
# Настройки разработчика с использованием удаленной БД
DEV=False
# Отладка
DEBUG=False
# СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ ПО УМОЛЧАНИЮ
DEFAULT_USERNAME=админ
DEFAULT_PASSWORD=администратор
# СЕКРЕТНЫЙ КЛЮЧ для флет-приложения
FLET_SECRET_KEY='a;lskdfj;lasdkjf;lsdajfw-oeirj089j02=3984jh320iji'
```

# Последняя стабильная версия

[Стабильная версия](https://github.com/azamtoiri/student_control/releases)