---
description: Описание метода get_me
---

# get\_me()

Метод get\_me():

Данный метод не требует ввода значений.

#### Получает информацию о профиле пользователя под которым вы вошли.

Возвращает: - `SelfProfile`: Экземпляр класса [SelfProfile](klassy/selfprofile.md), представляющий профиль пользователя.

Вызывает исключения: - `UnknwonError`: Если произошла непредвиденная ошибка при получении профиля пользователя. - `NotLoggedIn`: Если пользователь не авторизован.

#### Синхронный Вызов:

```python
from fapi import Foxford_API_Sync

try:
    me = session.get_me()
    print(f"Данные пользователя {me.full_name} успешно получены!")
except UnknwonError as e:
    print(f"Произошла ошибка: {e}")
except NotLoggedIn:
    print("Пользователь не авторизован")

```

#### Асинхронный вызов

```python
from fapi import Foxford_API_Async

try:
    me = await session.get_me()
    print(f"Данные пользователя {me.full_name} успешно получены!")
except UnknwonError as e:
    print(f"Произошла ошибка: {e}")
except NotLoggedIn:
    print("Пользователь не авторизован")
```
