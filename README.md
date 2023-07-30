# stepik_store

###### запуск Redis
`sudo systemctl status redis-server.service`

###### запуск Celery
из папки проекта, с включенным venv и переменными окружения
`. ./setenv.sh`
`celery -A store worker -l INFO`
