# 🎉 VK Draw Bot — автоматизация розыгрышей ВКонтакте

Простой Django-проект с Celery-задачей, которая:

- парсит комментарии к посту ВКонтакте
- проверяет подписку на указанные паблики
- выдает участникам номера для розыгрыша
- сохраняет всех участников и билеты в базу данных

---

## 🚀 Возможности

- Поддержка нескольких групп/пабликов
- Проверка, был ли выдан номер ранее
- Ответы на комментарии ВКонтакте: авто-выдача номера или напоминание о подписке
- Админка
- Интерфейс розыгрыша с выбором победителей

---

## 📦 Стек технологий

- Python 3.11+
- Django 4.x
- Django REST Framework
- Celery + Redis
- VK API
- SQLite / PostgreSQL

---

## ⚙️ Установка

1. Клонируй репозиторий:

```bash
git clone https://github.com/yourname/vk-draw-bot.git
cd vk-draw-bot
```
