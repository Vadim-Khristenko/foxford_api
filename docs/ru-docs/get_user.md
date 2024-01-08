---
description: Описание метода get_user()
---

# get\_user()

Метод get\_user(user\_id)

Данный метод требует ввода значения user\_id

#### Возвращает информацию о пользователе в виде класса UserProfile



#### Синхронный Вызов:

```python
from fapi import Foxford_API_Sync

user_id = 1
me = session.get_user(user_id)
```

#### Асинхронный вызов

```python
from fapi import Foxford_API_Async

user_id = 1
me = await session.get_me()
```
