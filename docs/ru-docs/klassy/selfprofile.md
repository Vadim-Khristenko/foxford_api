---
description: Информация о Аккаунте пользователя под которым вы вошли в систему.
---

# SelfProfile

{% hint style="success" %}
Этот раздел успешно завершен.
{% endhint %}

{% code lineNumbers="true" fullWidth="true" %}
```python
### Весь список переменных, хранящихся в классе.
user_id: Идентификатор пользователя.
email: Электронная почта пользователя.
first_name: Имя пользователя.
last_name: Фамилия пользователя.
middle_name: Отчество пользователя.
full_name: Полное имя пользователя.
short_name: Краткое имя пользователя.
grade_checked: Флаг, указывающий, проверены ли оценки пользователя.
phone: Телефон пользователя.
timezone: Часовой пояс пользователя.
locale: Локальный язык пользователя в двух буквах. (ru, en, etc)
is_parent: Флаг, указывающий, является ли пользователь родителем.
fake_user: Флаг, указывающий, является ли пользователь поддельным.
is_customer: Флаг, указывающий, является ли пользователь покупателем.
email_confirmed: Флаг, указывающий, подтверждена ли электронная почта пользователя.
fake_email: Флаг, указывающий, является ли электронная почта пользователя поддельной.
phone_confirmed: Флаг, указывающий, подтвержден ли телефон пользователя.
created_at: Дата и время создания аккаунта пользователя.
recent_registration: Флаг, указывающий, был ли аккаунт пользователя недавно создан.
profile_enriched: Флаг, указывающий, заполнена ли профиль пользователя.
avatar_changes_gap_in_days: Количество дней, прошедших с последнего изменения аватара пользователя.
personal_data_changes_gap_in_days: Количество дней, прошедших с последнего изменения личных данных пользователя.
skype: Skype-имя пользователя.
school_entry_year: Год поступления в школу.
attestation_format_id: Идентификатор формата аттестатации.
education_form_id: Идентификатор формы обучения.
avatar_can_be_changed_at: Дата и время, когда можно изменить аватар пользователя.
personal_data_can_be_changed_at: Дата и время, когда можно изменить личные данные пользователя.
about: Описание пользователя.
can_change_school_info: Флаг, указывающий, может ли пользователь изменить информацию о школе.
privacy: Словарь с информацией о приватности профиля пользователя, включая публичный профиль.
parent_phone: Телефон родителя пользователя.
parent_phone_confirmed: Флаг, указывающий, подтвержден ли телефон родителя пользователя.
is_graduated: Флаг, указывающий, окончил ли пользователь обучение.
user_type: Тип пользователя.
avatar_url: URL аватара пользователя.
bonus_amount: Количество бонусов пользователя.
free_access_finishes_at: Дата окончания бесплатного доступа.
is_coach: Флаг, указывающий, является ли пользователь тренером.
is_mini_group_teacher: Флаг, указывающий, является ли пользователь учителем мини-группы.
methodist:  Флаг, указывающий, является ли пользователь методистом.
grade: Информация об уровне образования пользователя.
social_nets: Информация о социальных сетях пользователя.
tags: Теги, связанные с пользователем.
onboarding_finished: Указывает, завершил ли пользователь обучение.
onboarding_finished_at: Временная метка завершения обучения пользователя.
has_bookmarks: Указывает, есть ли у пользователя закладки.
externship_user: Указывает, является ли пользователь внештатным.
is_elementary_pupil: Указывает, является ли пользователь начальным школьником.
has_active_purchases: Указывает, есть ли у пользователя активные покупки.
discipline_ids: Идентификаторы дисциплин, связанных с пользователем.
has_access_to_multi_days_streaks: Указывает, есть ли у пользователя доступ к многодневным сериям.
cart_items_count: Количество товаров в корзине пользователя.
cart_template_id: Идентификатор шаблона корзины.
web_socket_notifications_jwt: JWT для уведомлений через веб-сокет.
has_children: Указывает, есть ли у пользователя дети.
address: Информация об адресе пользователя.
address_index: Индекс адреса пользователя.
address_country_id: Идентификатор страны в адресе пользователя.
address_country_name: Название страны в адресе пользователя.
address_region_id: Идентификатор региона в адресе пользователя.
address_region_name: Название региона в адресе пользователя.
address_city_name: Название города в адресе пользователя.
address_city_id: Идентификатор города в адресе пользователя.
address_street: Улица в адресе пользователя.
address_house: Дом в адресе пользователя.
address_building: Здание в адресе пользователя.
address_room: Комната в адресе пользователя.
externship_payment_required: Указывает, требуется ли оплата за внештатную работу.
externship_payment_required_contract_id: Идентификатор контракта для оплаты внештатной работы.
externship_payment_required_access_closing_date: Дата закрытия доступа к оплате внештатной работы.
is_base_product_activated: Указывает, активирован ли базовый продукт.
bonuses_page_visited: Указывает, посещена ли страница с бонусами.
about_city: Информация о городе в разделе "О себе" пользователя.
about_city_id: Идентификатор города в разделе "О себе" пользователя.
about_city_full_name: Полное название города в разделе "О себе" пользователя.
about_city_name: Название города в разделе "О себе" пользователя.
about_city_region_iso_code: ISO-код региона в разделе "О себе" пользователя.
about_city_region_name: Название региона в разделе "О себе" пользователя.
about_city_country_iso_code: ISO-код страны в разделе "О себе" пользователя.
about_hobby_ids: Идентификаторы хобби, связанные с разделом "О себе" пользователя.
social_links: Социальные ссылки, связанные с пользователем.
socialization_profile: Информация о профиле социализации пользователя.
socialization_profile_id: Идентификатор профиля социализации.
socialization_profile_state: Состояние профиля социализации.
```
{% endcode %}
