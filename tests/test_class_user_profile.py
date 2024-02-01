import unittest
from fapi import UserProfile
import json

class TestUserProfile(unittest.TestCase):

    def test_user_profile_creation_from_json_string(self):
        json_data = '{"id": 1, "name": "John Doe", "avatar_url": "https://example.com/avatar", "caption": "Hello World", "is_agent": false, "default_achievement_image_url": "https://example.com/achievement", "school": {"city": "City", "name": "School Name"}, "grade": 10, "level_data": {"level": 5, "gained_xp": 100, "available_xp": 200, "progress": 50}}'
        profile = UserProfile(json_data)
        
        self.assertEqual(profile.user_id, 1)
        self.assertEqual(profile.name, "John Doe")
        self.assertEqual(profile.avatar_url, "https://example.com/avatar")
        self.assertEqual(profile.caption, "Hello World")
        self.assertFalse(profile.is_agent)
        self.assertEqual(profile.default_achievement_image_url, "https://example.com/achievement")
        self.assertEqual(profile.school_city, "City")
        self.assertEqual(profile.school_name, "School Name")
        self.assertEqual(profile.grade, 10)
        self.assertEqual(profile.level, 5)
        self.assertEqual(profile.gained_xp, 100)
        self.assertEqual(profile.available_xp, 200)
        self.assertEqual(profile.progress, 50)

    def test_user_profile_creation_from_dict(self):
        json_data = {"id": 2, "name": "Jane Doe", "avatar_url": "https://example.com/avatar2", "caption": "Hi There", "is_agent": True, "default_achievement_image_url": "https://example.com/achievement2", "school": {"city": "City2", "name": "School Name2"}, "grade": 12, "level_data": {"level": 3, "gained_xp": 50, "available_xp": 150, "progress": 30}}
        profile = UserProfile(json_data)
        
        self.assertEqual(profile.user_id, 2)
        self.assertEqual(profile.name, "Jane Doe")
        self.assertEqual(profile.avatar_url, "https://example.com/avatar2")
        self.assertEqual(profile.caption, "Hi There")
        self.assertTrue(profile.is_agent)
        self.assertEqual(profile.default_achievement_image_url, "https://example.com/achievement2")
        self.assertEqual(profile.school_city, "City2")
        self.assertEqual(profile.school_name, "School Name2")
        self.assertEqual(profile.grade, 12)
        self.assertEqual(profile.level, 3)
        self.assertEqual(profile.gained_xp, 50)
        self.assertEqual(profile.available_xp, 150)
        self.assertEqual(profile.progress, 30)

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
