import datetime
import json
import logging
from fapi.foxford_api_datatypes import *
from fapi.foxford_api_errors import *

"""


$$$$$$$$\  $$$$$$\  $$$$$$$\  $$$$$$\        $$$$$$\  $$\                                                   
$$  _____|$$  __$$\ $$  __$$\ \_$$  _|      $$  __$$\ $$ |                                                  
$$ |      $$ /  $$ |$$ |  $$ |  $$ |        $$ /  \__|$$ | $$$$$$\   $$$$$$$\  $$$$$$$\  $$$$$$\   $$$$$$$\ 
$$$$$\    $$$$$$$$ |$$$$$$$  |  $$ |        $$ |      $$ | \____$$\ $$  _____|$$  _____|$$  __$$\ $$  _____|
$$  __|   $$  __$$ |$$  ____/   $$ |        $$ |      $$ | $$$$$$$ |\$$$$$$\  \$$$$$$\  $$$$$$$$ |\$$$$$$\  
$$ |      $$ |  $$ |$$ |        $$ |        $$ |  $$\ $$ |$$  __$$ | \____$$\  \____$$\ $$   ____| \____$$\ 
$$ |      $$ |  $$ |$$ |      $$$$$$\       \$$$$$$  |$$ |\$$$$$$$ |$$$$$$$  |$$$$$$$  |\$$$$$$$\ $$$$$$$  |
\__|      \__|  \__|\__|      \______|       \______/ \__| \_______|\_______/ \_______/  \_______|\_______/ 
                                                                                                            
                                                                                                            
                                                                                                        

"""

class UserProfile:
    def __init__(self, json_data):
        """Информация о Профиле Пользователя"""
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        else:
            raise ValueError("Неверный формат данных. Ожидается JSON-строка или словарь.")

        self.user_id =                       data.get("id")
        self.name =                          data.get("name")
        self.avatar_url =                    data.get("avatar_url")
        self.caption =                       data.get("caption")
        self.is_agent =                      data.get("is_agent")
        self.default_achievement_image_url = data.get("default_achievement_image_url")
        self.school =                        data.get("school")

        if self.school:
            self.school_city = self.school.get("city")
            self.school_name = self.school.get("name")

        self.grade =      data.get("grade")
        self.level_data = data.get("level_data")

        if self.level_data:
            self.level =        self.level_data.get("level")
            self.gained_xp =    self.level_data.get("gained_xp")
            self.available_xp = self.level_data.get("available_xp")
            self.progress =     self.level_data.get("progress")

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.user_id

class SelfProfile:
    """Информация о Себе или же о Аккаунте под которым вы вошли."""
    def __init__(self, json_data):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        else:
            raise ValueError("Неверный формат данных. Ожидается JSON-строка или словарь.")
        
        self.user_id =                    data.get("id")
        self.email =                      data.get("email")
        self.first_name =                 data.get("first_name")
        self.last_name =                  data.get("last_name")
        self.middle_name =                data.get("middle_name")
        self.full_name =                  data.get("full_name")
        self.short_name =                 data.get("short_name")
        self.grade_checked =              data.get("grade_checked")
        self.phone =                      data.get("phone")
        self.timezone =                   data.get("timezone")
        self.locale =                     data.get("locale")
        self.is_parent =                  data.get("is_parent")
        self.fake_user =                  data.get("fake_user")
        self.is_customer =                data.get("is_customer")
        self.email_confirmed =            data.get("email_confirmed")
        self.fake_email =                 data.get("fake_email")
        self.phone_confirmed =            data.get("phone_confirmed")
        self.created_at =                 data.get("created_at")
        self.recent_registration =        data.get("recent_registration")
        self.profile_enriched =           data.get("profile_enriched")
        self.avatar_changes_gap_in_days =        data.get("avatar_changes_gap_in_days")
        self.personal_data_changes_gap_in_days = data.get("personal_data_changes_gap_in_days")
        self.skype =                      data.get("skype")
        self.school_entry_year =          data.get("school_entry_year") 
        self.attestation_format_id =      data.get("attestation_format_id")
        self.education_form_id =          data.get("education_form_id")
        self.avatar_can_be_changed_at =        data.get("avatar_can_be_changed_at")
        self.personal_data_can_be_changed_at = data.get("personal_data_can_be_changed_at")
        self.about =                      data.get("about")
        self.can_change_school_info =     data.get("can_change_school_info")

        self.privacy =                    data.get("privacy")
        if self.privacy:
            self.public_profile =         self.privacy.get("public_profile")

        self.parent_phone =               data.get("parent_phone")
        self.parent_phone_confirmed =     data.get("parent_phone_confirmed")
        self.is_graduated =               data.get("is_graduated")
        self.user_type =                  data.get("type")
        self.avatar_url =                 data.get("avatar_url")
        self.bonus_amount =               data.get("bonus_amount")
        self.free_access_finishes_at =    data.get("free_access_finishes_at")
        self.is_coach =                   data.get("is_coach")
        self.is_mini_group_teacher =      data.get("is_mini_group_teacher")
        self.methodist =                  data.get("methodist")

        self.grade =                      data.get("grade")
        if self.grade:
            self.grade_id =               self.grade.get("id")
            self.grade_index =            self.grade.get("index")

        self.social_nets =                data.get("social_nets")
        if self.social_nets:
            for social_net in self.social_nets:
                provider = social_net.get("provider")
                uid =      social_net.get("uid")
                setattr(self, f"social_net_{provider}", [provider, uid])
                setattr(self, f"social_net_{provider}_uid", uid)

        self.tags =                       data.get("tags")
        self.onboarding_finished =        data.get("onboarding_finished")
        self.onboarding_finished_at =     data.get("onboarding_finished_at")
        self.has_bookmarks =              data.get("has_bookmarks")
        self.externship_user =            data.get("externship_user")
        self.is_elementary_pupil =        data.get("is_elementary_pupil")
        self.has_active_purchases =       data.get("has_active_purchases")
        self.discipline_ids =             data.get("discipline_ids")
        self.has_access_to_multi_days_streaks = data.get("has_access_to_multi_days_streaks")
        self.cart_items_count =           data.get("cart_items_count")
        self.cart_template_id =           data.get("cart_template_id")
        self.web_socket_notifications_jwt=data.get("web_socket_notifications_jwt")
        self.has_children =               data.get("has_children")

        self.address =                    data.get("address")
        if self.address:
            self.address_index =          self.address.get("index")
            self.address_country_id =     self.address.get("country_id")
            self.address_country_name =   self.address.get("country_name")
            self.address_region_id =      self.address.get("region_id")
            self.address_region_name =    self.address.get("region_name")
            self.address_city_name =      self.address.get("city_name")
            self.address_city_id =        self.address.get("city_id")
            self.address_street =         self.address.get("street")
            self.address_house =          self.address.get("house")
            self.address_building =       self.address.get("building")
            self.address_room =           self.address.get("room")

        self.purchase_any_externship_contracts =  data.get("purchase_any_externship_contracts")
        self.has_purchased_externship_contracts = data.get("has_purchased_externship_contracts")
        self.has_externship_attestation_access =  data.get("has_externship_attestation_access")
        self.can_prolongate_contract =            data.get("can_prolongate_contract")

        self.externship_payment_required =        data.get("externship_payment_required")
        if self.externship_payment_required:
            self.externship_payment_required_contract_id =         self.externship_payment_required.get("contract_id")
            self.externship_payment_required_access_closing_date = self.externship_payment_required.get("access_closing_date")
        
        self.is_base_product_activated =          data.get("is_base_product_activated")
        self.bonuses_page_visited =               data.get("bonuses_page_visited")

        self.about_city =                         data.get("city")
        if self.about_city:
            self.about_city_id =                  self.about_city.get("id")
            self.about_city_full_name =           self.about_city.get("full_name")
            self.about_city_name =                self.about_city.get("city_name")
            self.about_city_region_iso_code =     self.about_city.get("region_iso_code")
            self.about_city_region_name =         self.about_city.get("region_name")
            self.about_city_country_iso_code =    self.about_city.get("country_iso_code")

        self.about_hobby_ids =                    data.get("hobby_ids")
        if self.about_hobby_ids:
            for hobby_id in self.about_hobby_ids:
                Hobby_Name =     HOBBY_NAMES.get(hobby_id)
                Hobby_API_Name = HOBBY_TRANSLATIONS.get(hobby_id)
                setattr(self, Hobby_API_Name, [Hobby_Name, hobby_id])

        self.social_links =                       data.get("social_links")
        if self.social_links:
            for social_link in self.social_links:
                id =       social_link.get("id")
                provider = social_link.get("provider")
                login =    social_link.get("login")
                setattr(self, f"social_link_{provider}", [id, provider, login])
                setattr(self, f"social_link_{provider}_id", id)
                setattr(self, f"social_link_{provider}_login", login)
        
        self.socialization_profile =              data.get("socialization_profile")
        if self.socialization_profile:
            self.socialization_profile_id =    self.socialization_profile.get("id")
            self.socialization_profile_state = self.socialization_profile.get("state")
        
        self.referer =                            data.get("referer")
        if self.referer:
            self.refer_user_id =                  self.referer.get("user_id")
            self.refer_name =                self.referer.get("name")
            self.refer_avatar_url =          self.referer.get("avatar_url")

class FoxBonus:
    def __init__(self, json_data):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        else:
            raise ValueError("Неверный формат данных. Ожидается JSON-строка или словарь.")
        
        self.bonus_amount =                  data.get("amount")
        self.bonus_nearest_expired_amount =  data.get("nearest_expired_amount")
        self.bonus_nearest_expiration_date = data.get("nearest_expiration_date")

        self.bonus_all_transactions =        data.get("bonus_transactions")
        if self.bonus_all_transactions:
            i = 0
            for transaction in self.bonus_all_transactions:
                i = i+1
                amount =      transaction.get("amount")
                date =        transaction.get("date")
                description = transaction.get("description")
                setattr(self, f"transaction_{i}", [amount, date, description])

class Unseen_Webinars:
    """
    Параметры:
        - `json_data (str или dict)`: JSON-данные для обработки. Может быть как строкой JSON, так и словарем.
            
    Исключения:
        - `DataNotFound`: Если JSON-данные являются пустым списком.
        - `ValueError`: Если JSON-данные не являются правильным форматом (строка JSON или словарь).
    """
    def __init__(self, json_data):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        elif json_data == []:
            logging.warning("Данных не обнаружено. | Unseen_Webinars")
            raise DataNotFound
        else:
            raise ValueError("Неверный формат данных. Ожидается JSON-строка или словарь.")
        
        self.unseen_webinars = data
        if self.unseen_webinars:
            i = 0
            for webinar in self.unseen_webinars:
                i += 1
                setattr(self, f'unseen_webinar_id_{i}', webinar.get("id"))
                setattr(self, f'unseen_webinar_title_{i}', webinar.get("title"))
                setattr(self, f'unseen_webinar_subtitle_{i}', webinar.get("subtitle"))
                metadata = webinar.get("meta_data")
                if metadata:
                    setattr(self, f'unseen_webinar_metadata_{i}', metadata)
                    setattr(self, f'unseen_webinar_metadata_gained_xp_{i}', metadata.get("gained_xp"))
                    setattr(self, f'unseen_webinar_metadata_available_xp_{i}', metadata.get("available_xp"))
                    setattr(self, f'unseen_webinar_metadata_double_xp_deadline_{i}', metadata.get("double_xp_deadline"))
                    setattr(self, f'unseen_webinar_metadata_discipline_{i}', metadata.get("discipline"))

                    discipline_data = metadata.get("discipline_data")
                    if discipline_data:
                        setattr(self, f"unseen_webinar_metadata_discipline_data_{i}", discipline_data)
                        setattr(self, f'unseen_webinar_metadata_discipline_data_name_{i}', discipline_data.get("name"))
                        setattr(self, f'unseen_webinar_metadata_discipline_data_color_{i}', discipline_data.get("color"))

                    setattr(self, f'unseen_webinar_metadata_duration_{i}', metadata.get("duration"))
                    setattr(self, f'unseen_webinar_metadata_lesson_number_{i}', metadata.get("lesson_number"))
                    setattr(self, f'unseen_webinar_metadata_short_subtitle_{i}', metadata.get("short_subtitle"))

                    teacher = metadata.get("teacher")
                    if teacher:
                        setattr(self, f'unseen_webinar_metadata_teacher_{i}', teacher)
                        setattr(self, f'unseen_webinar_metadata_teacher_full_name_{i}', teacher.get("full_name"))
                        setattr(self, f'unseen_webinar_metadata_teacher_transparent_photo_url_{i}', teacher.get("transparent_photo_url"))
                        setattr(self, f'unseen_webinar_metadata_teacher_medium_photo_url_{i}', teacher.get("medium_photo_url"))
                    
                    setattr(self, f'unseen_webinar_metadata_tasks_count_{i}', metadata.get("tasks_count"))
                    setattr(self, f'unseen_webinar_metadata_completed_tasks_count_{i}', metadata.get("completed_tasks_count"))
                
                setattr(self, f'unseen_webinar_deadline_{i}', webinar.get("deadline"))
                setattr(self, f'unseen_webinar_type_{i}', webinar.get("type"))
                setattr(self, f'unseen_webinar_path_{i}', webinar.get("path"))
                setattr(self, f'unseen_webinar_completed_{i}', webinar.get("completed"))
                setattr(self, f'unseen_webinar_dismissed_{i}', webinar.get("dismissed"))
                setattr(self, f'unseen_webinar_visited_{i}', webinar.get("visited"))
                setattr(self, f'unseen_webinar_double_xp_deadline_{i}', webinar.get("double_xp_deadline"))
            setattr(self, f'total_unseen_webinars', i)

class SocialProfile:
    def __init__(self, json_data):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        elif json_data == []:
            logging.warning("Данных не обнаружено. | SocialProfile")
            raise DataNotFound
        else:
            raise ValueError("Неверный формат данных. Ожидается JSON-строка или словарь.")
        
        self.social_profiles = data
        if self.social_profiles:
            i = 0
            for social_profile in self.social_profiles:
                i += 1
                setattr(self, f'social_profile_id_{i}', social_profile.get("id"))
                setattr(self, f'social_profile_user_id_{i}', social_profile.get("user_id"))
                setattr(self, f'social_profile_first_name_{i}', social_profile.get("first_name"))
                setattr(self, f'social_profile_last_name_{i}', social_profile.get("last_name"))
                setattr(self, f'social_profile_birthday_{i}', social_profile.get("birthday"))
                setattr(self, f'social_profile_age_{i}', social_profile.get("age"))
                setattr(self, f'social_profile_state_{i}', social_profile.get("state"))
                setattr(self, f'social_profile_is_filled_{i}', social_profile.get("is_filled"))
                setattr(self, f'social_profile_avatar_url_{i}', social_profile.get("avatar_url"))
                
                grade = social_profile.get("grade")
                if grade:
                    setattr(self, f'social_profile_grade_{i}', grade)
                    setattr(self, f'social_profile_grade_id_{i}', grade.get("id"))
                    setattr(self, f'social_profile_grade_index_{i}', grade.get("index"))
                    setattr(self, f'social_profile_grade_name_{i}', grade.get("name"))
                    
                city = social_profile.get("city")
                if city:
                    setattr(self, f'social_profile_city_{i}', city)
                    setattr(self, f'social_profile_city_id_{i}', city.get("id"))
                    setattr(self, f'social_profile_city_name_{i}', city.get("city_name"))
                    setattr(self, f'social_profile_city_region_iso_code_{i}', city.get("region_iso_code"))
                    setattr(self, f"social_profile_city_region_name_{i}", city.get("region_name"))
                    setattr(self, f"social_profile_city_country_iso_code_{i}", city.get("country_iso_code"))
                    setattr(self, f"social_profile_city_country_name_{i}", city.get("country_name"))
                
                about_hobby_ids = social_profile.get("hobby_ids")
                if about_hobby_ids:
                    setattr(self, f'social_profile_hobby_{i}', about_hobby_ids)
                    hobby_total = 0
                    for hobby_id in about_hobby_ids:
                        hobby_total += 1
                        Hobby_Name =     HOBBY_NAMES.get(hobby_id)
                        Hobby_API_Name = HOBBY_TRANSLATIONS.get(hobby_id)
                        setattr(self, f"social_profile_hobby_{Hobby_API_Name}_{i}", [Hobby_Name, hobby_id])
                    setattr(self, f"social_profile_hobby_total_{i}", hobby_total)
                
                social_links = social_profile.get("social_links")
                if social_links:
                    setattr(self, f'social_profile_links_{i}', social_links)
                    links_total = 0
                    for social_link in social_links:
                        links_total += 1
                        id =       social_link.get("id")
                        provider = social_link.get("provider")
                        login =    social_link.get("login")
                        setattr(self, f"social_profile_link_{provider}_{i}", [id, provider, login])
                        setattr(self, f"social_profile_link_{provider}_id_{i}", id)
                        setattr(self, f"social_profile_link_{provider}_login_{i}", login)
                    setattr(self, f"social_profile_links_total_{i}", links_total)
                
                setattr(self, f'social_profile_about_{i}', social_profile.get("about"))
                
                matches = social_profile.get("matches")
                if matches:
                    setattr(self, f"social_profile_matches_{i}", matches)
                    setattr(self, f"social_profile_matches_same_country_{i}", matches.get("same_country"))
                    setattr(self, f"social_profile_matches_same_grade_{i}", matches.get("same_grade"))
                    same_hobbies_about_hobby_ids = matches.get("same_hobbies")
                    if same_hobbies_about_hobby_ids:
                        setattr(self, f'social_profile_matches_same_hobbies_{i}', same_hobbies_about_hobby_ids)
                        same_hobby_total = 0
                        for same_hobby_id in same_hobbies_about_hobby_ids:
                            same_hobby_total += 1
                            Same_Hobby_Name =     HOBBY_NAMES.get(same_hobby_id)
                            Same_Hobby_API_Name = HOBBY_TRANSLATIONS.get(same_hobby_id)
                            setattr(self, f"social_profile_matches_same_hobby_{Same_Hobby_API_Name}_{i}", [Same_Hobby_Name, same_hobby_id])
                        setattr(self, f"social_profile_matches_same_hobby_total_{i}", same_hobby_total)
                    setattr(self, f"social_profile_matches_score_{i}", matches.get("score"))
                
                setattr(self, f"social_profile_search_score_{i}", social_profile.get("search_score"))
                setattr(self, f"social_profile_favorite_{i}", social_profile.get("favorite"))
                    
            setattr(self, f'total_social_profiles', i)
            
class UnreadNotification:
    def __init__(self, json_data):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        elif json_data == []:
            logging.warning("Данных не обнаружено. | UnreadNotification")
            raise DataNotFound
        else:
            raise ValueError("Неверный формат данных. Ожидается JSON-строка или словарь.")
    
        self.unread_notifications = data
        if self.unread_notifications:
            i = 0
            for notifiaction in self.unread_notifications:
                i += 1
                pre_data_class = notifiaction.get("title")
                type_class = next((translation for ru_code, translation in NOTIFICATION_TRANSLATIONS.items() if ru_code in pre_data_class.lower()), "unknown")
                setattr(self, f'unread_notification_id_{i}', notifiaction.get("id"))
                setattr(self, f'unread_notification_type_{i}', type_class)
                setattr(self, f'unread_notification_created_at_{i}', notifiaction.get("created_at"))
                setattr(self, f'unread_notification_read_at_{i}', notifiaction.get("read_at"))
                setattr(self, f'unread_notification_title_{i}', notifiaction.get("title"))
                setattr(self, f'unread_notification_text_{i}', notifiaction.get("text"))
                setattr(self, f'unread_notification_action_url_{i}', notifiaction.get("action_url"))
                setattr(self, f'unread_notification_icon_url_{i}', notifiaction.get("icon_url"))
                
            setattr(self, f'total_unread_notifications', i)
            
class FoxCalendar:
    def __init__(self, json_data):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        elif json_data == []:
            logging.warning("Данных не обнаружено. | FoxCalendar")
            raise DataNotFound
        else:
            raise ValueError("Неверный формат данных. Ожидается JSON-строка или словарь.")
    
        self.fox_calendar = data
        if self.fox_calendar:
            course = 0
            coach = 0
            event = 0
            attestation = 0
            payment = 0
            prolongation = 0
            self.course_lessons = self.fox_calendar.get("course_lessons")
            for course_lesson in self.course_lessons:
                course += 1
                setattr(self, f"course_lesson_starts_at_{course}", course_lesson.get("starts_at"))
                setattr(self, f"course_lesson_duration_{course}", course_lesson.get("duration"))
                setattr(self, f"course_lesson_short_url_{course}", course_lesson.get("url"))
                setattr(self, f"course_lesson_full_url_{course}", f"https://foxford.ru{course_lesson.get('url')}")
                setattr(self, f"course_lesson_title_{course}", course_lesson.get("title"))
                setattr(self, f"discipline_name_{course}", course_lesson.get("discipline_name"))