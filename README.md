# Тестовое задание FUNBOX

### Задание:
> Реализуйте web-приложение для простого учета посещенных (неважно, как, кем и когда) ссылок
### Копирование репозитория и установка зависимостей
```bash
git clone https://github.com/p2cbbb/visits_fastapi
cd visits_fastapi
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Запуск тестов
 
```bash
cd app
python -m pytest test_main.py
```

### Запуск redis-сервера
```bash
sudo service redis-server start
```

### Запуск проекта
```bash
cd app
uvicorn main:app --reload
```

### Эндпоинты
- Ресурс загрузки посещений. POST /visited_links    
##### Запрос:
```json
{
    "links": [
        "https://ya.ru",
        "https://ya.ru?q=123",
        "funbox.ru",
        "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
    ]
}
```
##### Ответ:
```json
{
    "status": "ok"
}
```
- Ресурс получения статистики. GET /visited_domains?from=1545221231&to=1545217638
##### Ответ:
```json
{
    "domains": [
        "ya.ru",
        "funbox.ru",
        "stackoverflow.com"
    ],
    "status": "ok"
}
```
