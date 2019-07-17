## Для запуска проекта необходимо:

* Установить Django Widget Tweaks
```bash
pip install django-widget-tweaks
```

* Созданть миграции приложения для базы данных
```bash
python manage.py migrate
```

* Добавить данные из базы данных
```bash
python manage.py loaddata db.json
```

* При добавлении раздела/товара необходимо добавить slug, сначала можно добавить что-то временное, а потом
   воспользоваться командой slugify и поле slug заполнится автоматически исходя из названия
```bash
python manage.py slugify
```
