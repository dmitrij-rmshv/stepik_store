# stepik_store

##### зависимости
    pip3 install requirements.txt

###### активация виртуального окружения
из папки проекта

    source ../venv/bin/activate

###### импорт секретных ключей
из папки проекта

    . ./setenv.sh

###### запуск Redis

    sudo systemctl status redis-server.service

###### запуск Celery
из папки проекта, с включенным venv и переменными окружения

    celery -A store worker -l INFO

###### запуск прослушки webhook для взаимодействия со stripe

    stripe listen --forward-to 127.0.0.1:8000/webhook/stripe/
