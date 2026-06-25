# Angel-in-Pocket Shopping Assistant (with GRA Nullification Engine)

## Описание
AI-ассистент для безопасного онлайн-шопинга с детектором враждебных продавцов и отзывов на основе игрового равновесия графа (GRA-Nullification-Equilibrium). Поддерживает три уровня подписок через Stripe.

## Установка и запуск
1. Клонируйте репозиторий.
2. Создайте файл `.env` по примеру `.env.example`.
3. Установите зависимости: `pip install -r requirements.txt`.
4. Запустите PostgreSQL и Redis.
5. Примените миграции (автоматически при старте).
6. Запустите сервер: `uvicorn app.main:app --reload`.

## API
- Документация доступна по `/docs` после запуска.
- Основные эндпоинты:
  - `/auth/register`, `/auth/login`
  - `/products/{id}/safety`
  - `/sellers/{id}/trust`
  - `/subscriptions/create-checkout-session`
  - `/subscriptions/webhook` (для Stripe)

## Лицензия
MIT
