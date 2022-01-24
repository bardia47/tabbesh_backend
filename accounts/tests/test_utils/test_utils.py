from accounts.tests.test_utils.test_utils_base import TestBaseUtils
from accounts.utils.temp_utils import SerializerUtils, ViewUtils


class TestSerializerUtils(TestBaseUtils):

    def test_check_expire(self):
        self.assertIsNotNone(SerializerUtils.check_expire(self.code))
        try:
            self.assertIsNotNone(SerializerUtils.check_expire(self.wrong_code))
            self.fail()
        except:
            pass


class TestViewUtils(TestBaseUtils):

    def test_get_phone_number_from_temp_code(self):
        self.assertEqual(ViewUtils.get_phone_number_from_temp_code(self.key), self.phone_number)

    def test_get_phone_number_from_temp_code(self):
        try:
            key = ViewUtils.create_new_temp_code()
            self.assertIsNotNone(key)
        except:
            self.fail()
        self.assertNotEqual(key,self.key)
