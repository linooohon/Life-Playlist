import unittest
from flask import url_for
from app import create_app
from app.views import auth


class SettingBase(unittest.TestCase):
    def create_app(self):
        return create_app("testing")

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUpStart')
        self.email = "default@gmail.com"
        print('setUpEnd')

    def tearDown(self):
        print('tearDownStart')
        print('tearDownEnd')


class CheckSignUpAndLogin(SettingBase):
    def test_sign_up_user_exist(self):
        self.email = "linooohon@gmail.com"
        print(self.email)
        # print(auth.sign_up_user_exist(self.email))
        self.assertEqual(auth.sign_up_user_exist(
            self.email), "User is already exist")
        # self.assertRaises(ValueError, auth.sign_up_user_exist, self.email)


if __name__ == '__main__':
    unittest.main()
