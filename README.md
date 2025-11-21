# TickIt: продажа и бронирование билетов в кино

Финальное домашнее задание по курсу Python.

- **ФИО:** Загвоздин Денис Сергеевич
- **Группа:** РИМ-150950
- **Направление:** Прикладной анализ данных

## Требования

- В папке example/ находится проект-пример, никакой смысловой нагрузки он не несёт
- Создал командой `django-admin startproject tickit_site .` папку tickit_site/ с шаблонными файлами
- Создал командой `python manage.py startapp tickit` папку tickit/ с шаблонными файлами
- Сгенерируй для описания ниже модели, сущности и миграции
- Проект "Продажа и бронирование билетов в кино"

## Сущности

1. Залы `rooms`: 3 предопределённых зала (зал №1, зал №2 и зал №3)
2. 7 мест в каждом зале `places`: A1, A2, A3, B1, B2, B3, B4
3. Расписание сеансов `sessions`
4. Билеты `tickets`
5. При создании сессии `sessions` для всех мест `places` создаются билеты `tickets` изначально со статусом 'available'
6. В качестве БД пока что использовать sqlite

## Связи

1. `rooms`: id (int pk), name (varchar 100)
2. `places`: id (int pk), code (varchar 16, e.g. A1, A2, B1), room_id (int fk rooms); unique(code, room_id)
3. `movies`: id (int pk), title (varchar 256), description (varchar 512), duration (int)
4. `sessions`: id (int pk), movie_id (int fk movies), room_id (int fk rooms), start (timestamp with tz), end (timestamp with tz)
5. `tickets`: id (int pk), uuid (string unique), session_id (int fk sessions), place_id (int fk places), status (fk enum), price (decimal); unique(session_id, place_id)
6. `statuses` (enum): 'available', 'sold', 'reserved'
