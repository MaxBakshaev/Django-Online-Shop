
Образец сайта: <https://shop.risen2ie.beget.tech/>

# Интернет-магазин с товарами на все случаи жизни

### Установка и запуск:

1. Клонируйте репозиторий и перейдите в рабочую директорию проекта:
```
git clone https://github.com/MaxBakshaev/Django-Online-Shop.git
```
```
cd Django-Online-Shop
```

2. Создайте виртуальную среду:
```
python -m venv venv
```

3. Активируйте виртуальную среду:

Для Linux или macOS:
```
source venv/bin/activate
```
Для Windows:
```
venv\Scripts\activate
```

4. Установите зависимости:
```
pip install -r requirements.txt
```

5. Создайте базу данных в PostgreSQL и пользователя для нее;

6. Создайте файл в корне проекта .env и добавьте в него переменные окружения:<br/>
SECRET_KEY='Ваш_секретный_ключ'<br/>
NAME='Имя_БД'<br/>
USER='Имя_пользователя_в_БД'<br/>
PASSWORD='Пароль_пользователя_в_БД'<br/><br/>
Необязательно, можно оставить пустым (для отправки сообщения о проблеме):<br/>
EMAIL_HOST='Имя_хоста_SMTP-сервера'<br/>
EMAIL_HOST_USER='Имя_пользователя_SMTP-сервера'<br/>
EMAIL_HOST_PASSWORD='Пароль_SMTP-сервера.' <br/>

7. Примените миграции:
```
python manage.py migrate
```

8. Создайте суперпользователя:
```
python manage.py createsuperuser
```

9. Запустите сервер:
```
python manage.py runserver
```
Для отключения сервера используйте команду:
```
Ctrl + C
```

10. Перейдите по адресу http://127.0.0.1:8000/ для доступа к сайту:
```
python manage.py runserver
```