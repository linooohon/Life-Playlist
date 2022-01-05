import unittest
from flask import url_for
from app import create_app, mail
from app.views import auth
from app.settings import TEST_EMAIL_TARGET


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


# check sign up
class CheckSignUpAndLogin(SettingBase):
    def test_sign_up_user_exist(self):
        self.email = "linooohon@gmail.com"
        print(self.email)
        # print(auth.sign_up_user_exist(self.email))
        self.assertEqual(auth.sign_up_user_exist(
            self.email), "User is already exist")
        # self.assertRaises(ValueError, auth.sign_up_user_exist, self.email)


# check soulmate email sending function is okay
class CheckSoulmateEmailSending(SettingBase):
    def test_soulmate_email_send_success(self):
        email = [TEST_EMAIL_TARGET]
        with mail.record_messages() as outbox:
            # already setting default sender in .env so here don't need to set sender
            mail.send_message(subject='testing', body='test', recipients=email)
            assert len(outbox) == 1
            assert outbox[0].subject == 'testing'

if __name__ == '__main__':
    unittest.main()
