---
description: >-
  We tell you the basics of installation and show you the very beginning of
  programming.
---

# Start

### Library Installation

To begin, install the library using the following command:

```bash
pip install git+https://github.com/Vadim-Khristenko/foxford_api
```

{% hint style="warning" %}
**Note:** The library currently does not support Python 3.12. It is recommended to use Python version 3.11.
{% endhint %}

### Library Import

```python
from fapi import Foxford_API_Sync
# This allows you to import the Synchronous version of the library.

from fapi import Foxford_API_Async
# This allows you to import the Asynchronous version of the library.
```

{% hint style="info" %}
We recommend adding:

<pre class="language-python"><code class="lang-python"><strong>from fapi import Foxford_API_Sync / Foxford_API_Async as apis
</strong></code></pre>
{% endhint %}

### Synchronous Code

```python
from fapi import Foxford_API_Sync as apis

# Email login
def email_main():
    email = input("Enter email: ")
    password = input("Enter password: ")
    session = apis.login_by_email(email=email, password=password)
    me = session.get_me()
    print(f"{me.full_name}")
    session.close_session()

# Phone login
def phone_main():
    phone = input("Enter phone number (79000000000 format): ")
    session = apis.login_by_phone(phone=phone)
    # You will be prompted to enter the SMS code in the terminal.
    me = session.get_me()
    print(f"{me.full_name}")
    session.close_session()

if __name__ == "__main__":
    email_main()
    phone_main()
    # After logging in, the FOXSESSION.session file will be created, and this file will be used later.
    # As long as the session is valid, you won't have to log in again.
    # If you need to update the session file, you will need to enter the SMS code again
    # or provide an email and password.

```

### Asynchronous Code

```python
from fapi import Foxford_API_Async as apis
import asyncio

async def email_main():
    email = input("Enter email: ")
    password = input("Enter password: ")
    session = await apis.login_by_email(email=email, password=password, log=False)
    me = await session.get_me()
    print(f"{me.full_name}")
    await session.close_session()

async def phone_main():
    phone = input("Enter phone number (79000000000 format): ")
    session = await apis.login_by_phone(phone=phone, log=False)
    # You will be prompted to enter the SMS code in the terminal.
    me = await session.get_me()
    print(f"{me.full_name}")
    await session.close_session()

if __name__ == "__main__":
    asyncio.run(email_main())
    asyncio.run(phone_main())
    # After logging in, the FOXSESSION.session file will be created, and this file will be used later.
    # If you need to update the session file, you will need to enter the SMS code again
    # or provide an email and password.
```

{% hint style="info" %}
You can disable additional logging by adding log=False in login\_by\_email / login\_by\_phone.
{% endhint %}
