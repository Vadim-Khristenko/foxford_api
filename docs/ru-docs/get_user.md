---
description: Описание метода get_user()
---

# get\_user()

Метод get\_user(user\_id)

Данный метод требует ввода значения user\_id

#### Получает Профиль пользователя из API на основе предоставленного идентификатора пользователя.

Параметры: - `user_id (int)`: Идентификатор пользователя для получения Профиля пользователя.

Возвращает: - `UserProfile`: Экземпляр класса [UserProfile](klassy/userprofile.md), представляющий Профиль полученного пользователя.

Исключения: - `UserNotFound`: Если профиль пользователь с предоставленным идентификатором не найден. - `UnknwonError`: Если произошла непредвиденная ошибка при получении профиля пользователя. - `NotLoggedIn`: Если пользователь не авторизован.



#### Синхронный Вызов:

```python
from fapi import Foxford_API_Sync

try:
    user_id = 1
    user = session.get_user(user_id)
    print(f"Данные пользователя {user.name} успешно получены!")
except UnknwonError as e:
    print(f"Произошла ошибка: {e}")
except NotLoggedIn:
    print("Пользователь не авторизован")
```

#### Асинхронный вызов

```python
from fapi import Foxford_API_Async

try:
    user_id = 1
    user = await session.get_me()
    print(f"Данные пользователя {user.name} успешно получены!")
except UnknwonError as e:
    print(f"Произошла ошибка: {e}")
except NotLoggedIn:
    print("Пользователь не авторизован")
```
