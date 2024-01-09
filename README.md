# FOXFORD_API

> Библиотека для взаимодействия с Бекэндом платформы Foxford.

> Библиотека Поддерживает, как и Async, так и Sync.

> Используйте эту библиотеку только в учебных целях! Создатель FOXFORD_API не несёт ответственности за любые повреждения, нанесенные платформе во время использования.

> Эта библиотека не является официальной библиотекой FOXFORD.

## Установка:

Вы можете установить библиотеку при помощи `pip`:
```bash
pip install FOXFORD-API
```

Или Предварительную Версию при помощи `pip`:
```bash
pip install git+https://github.com/Vadim-Khristenko/foxford_api
```

## [Документация нажмите и вы перейдёте в Документацию.](https://volt-diamond.gitbook.io/foxford-api-docs/)
## Быстрый Старт:

### Синхронный код
```python
from fapi import Foxford_API_Sync as apis
# Вход по почте:
def email_main():
    email = input("Введите почту: ")
    password = input("Введите пароль: ")
    session = apis.login_by_email(email=email, password=password)
    me = session.get_me()
    print(f{me.full_name})
    session.close_session()

def phone_main():
    phone = input("Введите номер телефона в формате (79000000000): ")
    session = apis.login_by_phone(phone=phone)
    #Тут вас попросят в Терминал ввести код из SMS.
    me = session.get_me()
    print(f{me.full_name})
    session.close_session()

if __name__ == "__main__":
    email_main()
    phone_main()
    # После входа будет создан файл FOXSESSION.session и именно этот файл будет использоваться дальше. 
    # (Пока Сессия действительна Входить снова не придётся.)
    # Если Файл Сессии нужно будет обновить, то от вас потребуется снова ввести код из SMS.
    # Или указать Email и Пароль.
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
    print(f{me.full_name})
    await session.close_session()

async def phone_main():
    phone = input("Введите номер телефона в формате (79000000000): ")
    session = await apis.login_by_phone(phone=phone)
    #Тут вас попросят в Терминал ввести код из SMS.
    me = await session.get_me()
    print(f{me.full_name})
    await session.close_session()

if __name__ == "__main__":
    asyncio.run(email_main())
    asyncio.run(phone_main())
    # После входа будет создан файл FOXSESSION.session и именно этот файл будет использоваться дальше.
    # Если Файл Сессии нужно будет обновить, то от вас потребуется снова ввести код из SMS.
    # Или указать Email и Пароль.
```

Вы можете выбрать Один из способов выше чтобы войти и начать Использовать FOXFORD API!

> Примечание: То что мы выше использовали и Авторизацию по Почте и Авторизацию по Телефону это только пример вы можете выбрать, то что удобно именно вам. 🧡
