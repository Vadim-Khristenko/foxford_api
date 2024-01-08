---
description: Рассказываем азы установки и показываем самое начало программирования.
---

# Начало

Конечно, добавим комментарии и опцию отключения дополнительного логгирования. Вот обновленный код:

***

### Установка библиотеки

Для начала, установите библиотеку, используя следующую команду:

```bash
pip install git+https://github.com/Vadim-Khristenko/foxford_api
```

{% hint style="warning" %}
**Примечание:** Библиотека в настоящее время не поддерживает Python 3.12. Рекомендуется использовать Python версии 3.11.
{% endhint %}

## Импорт Библиотеки:

```python
from fapi import Foxford_API_Sync
# Это позволит вам импортировать Синхронную версию Библиотеки.

from fapi import Foxford_API_Async
# Это позволит вам импортировать Асинхронную версию Библиотеки.
```

{% hint style="info" %}
Мы рекомендуем добавлять:&#x20;

```python
from fapi import Foxford_API_Sync / Foxford_API_Async as apis
```
{% endhint %}

### Синхронный код

```python
from fapi import Foxford_API_Sync as apis

# Вход по почте
def email_main():
    email = input("Введите почту: ")
    password = input("Введите пароль: ")
    session = apis.login_by_email(email=email, password=password)
    me = session.get_me()
    print(f"{me.full_name}")
    session.close_session()

# Вход по номеру телефона
def phone_main():
    phone = input("Введите номер телефона в формате (79000000000): ")
    session = apis.login_by_phone(phone=phone)
    # Тут вас попросят в терминал ввести код из SMS.
    me = session.get_me()
    print(f"{me.full_name}")
    session.close_session()

if __name__ == "__main__":
    email_main()
    phone_main()
    # После входа будет создан файл FOXSESSION.session, и именно этот файл будет использоваться дальше. 
    # Пока сессия действительна, входить снова не придется.
    # Если файл сессии нужно будет обновить, от вас потребуется снова ввести код из SMS
    # или указать email и пароль.
```

### Асинхронный код

```python
from fapi import Foxford_API_Async as apis
import asyncio

async def email_main():
    email = input("Введите почту: ")
    password = input("Введите пароль: ")
    session = await apis.login_by_email(email=email, password=password)
    me = await session.get_me()
    print(f"{me.full_name}")
    await session.close_session()

async def phone_main():
    phone = input("Введите номер телефона в формате (79000000000): ")
    session = await apis.login_by_phone(phone=phone)
    # Тут вас попросят в терминал ввести код из SMS.
    me = await session.get_me()
    print(f"{me.full_name}")
    await session.close_session()

if __name__ == "__main__":
    asyncio.run(email_main())
    asyncio.run(phone_main())
    # После входа будет создан файл FOXSESSION.session, и именно этот файл будет использоваться дальше.
    # Если файл сессии нужно будет обновить, от вас потребуется снова ввести код из SMS
    # или указать email и пароль.
```

{% hint style="info" %}
Вы можете отключить Дополнительный Логи добавив log = False в login\_by\_email / login\_by\_phone
{% endhint %}
