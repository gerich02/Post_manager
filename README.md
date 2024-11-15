# Test task for Comsoftlab
#  Описание проекта "Comsoftlab_post_manager"

## Описание
Comsoftlab_post_manager является ресурсом, который посредством протокола IMAP загрузит в пользавательский интерфейс письма с почтового ящика
“yandex.ru”, “gmail.com” или “mail.ru”.


**Инструменты и стек:** #Python #Django #PostgreSQL #Channels #Channels-redis #Daphne #HTML #JavaScript #ImapLib #Docker #Python-dotenv #JSON #VsCode #GitHub

## Подготовка к запуску проекта
Перед тем как запускать данный проект Вам необходимо проделать определенную подготовительную работу, а именно:
- Дать разрешение в личном кабинете Вашего почтового клиента на использование протокола IMAP и сгенерировать пароль
- Установить и запустить Channels-redis. Рекомендую сделать это через Docker
Для этого установите Docker на свой ПК, запустите его и в терминале введите команду
```
docker run --name redis_container -p 6379:6379 -d redis:latest
```
- Настроить работу с PostgreSQL на вашем ПК, я использовал официальный дистрибутив по ссылке (https://www.postgresql.org/download/).
Через админ панель pgAdmin 4 Вам необходимо будет создать свою БД (https://info-comp.ru/how-to-create-database-in-postgresql)


## Установка проекта

1. Клонируйте репозиторий:

    ```
    git clone git@github.com:gerich02/Comsoftlab_post_manager.git
    ```
2. Создайте и запустите виртуальное окружение:
    ```
    python -m venv venv
    source venv/Scripts/activate
    ```
3. Перейдите в папку с проектом:
    ```
    cd Comsoftlab_post_manager
    ```
4. Создайте файл .env и заполните его своими данными:
    ```bash
    POSTGRES_USER=user                      #Имя пользователя для подключения к базе данных PostgreSQL.
    POSTGRES_PASSWORD=password              #Пароль пользователя для подключения к базе данных PostgreSQL.
    POSTGRES_DB=django                      #Название базы данных PostgreSQL.
    DB_HOST=db                              #Хост базы данных.
    DB_PORT=5432                            #Порт для подключения к базе данных.
    SECRET_KEY='secret_key'                 #Секретный ключ приложения Django, используемый для шифрования данных и безопасности. 
    ALLOWED_HOSTS='localhost,127.0.0.1'     #писок доменных имен или IP-адресов, которым разрешено подключаться к приложению.
    ```

5. Установите зависимости:
    ```
    cd backend/
    pip install -r requirements.txt
    ```
6. Выполните миграции:
    ```
    py manage.py migrate
    ```
7. Запустите сервер:
    ```
    py manage.py runserver
    ```

    В ответ Вы получите:
    ```
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    September 02, 2024 - 09:49:12
    Django version 4.2, using settings 'post_manager.settings'
    Starting ASGI/Daphne version 4.0.0 development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
    ```

Далее переходите на страницу http://127.0.0.1:8000/, введите логин  и сгенерированный пароль IMAP от почты.
Нажмите кнопку "Проверить почту", после чего Вас перенаправит на страницу, куда подгрузятся все Ваши письма из папки "Входящие".



## Об авторе
>[Gerich02](https://github.com/gerich02)
