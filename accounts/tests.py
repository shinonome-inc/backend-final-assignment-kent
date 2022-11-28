from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse

from accounts.forms import UserCreateForm, UserSignInForm
from accounts.models import User


class TestSignUpView(TestCase):
    def setUp(self):
        self.signup_url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "username": "test",
            "email": "hoge@email.com",
            "password1": "passcode0000",
            "password2": "passcode0000",
        }
        response = self.client.post(self.signup_url, data)
        self.assertRedirects(response, reverse("welcome:home"), 302, 200)
        added_user = User.objects.filter(username="test")
        self.assertTrue(added_user.exists())
        self.assertEquals(added_user[0].username, "test")
        self.assertEquals(added_user[0].email, "hoge@email.com")

    def test_failure_post_with_empty_form(self):
        data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.signup_url, data)
        form = response.context["form"]
        form.is_valid()
        err_mes = "このフィールドは必須です。"
        for key in form.errors.as_data().keys():
            self.assertIn(err_mes, form.errors[key])
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_empty_username(self):
        data = {
            "username": "",
            "email": "hoge@email.com",
            "password1": "pass0000",
            "password2": "pass0000",
        }
        response = self.client.post(self.signup_url, data)
        form = response.context["form"]
        form.is_valid()
        err_mes = "このフィールドは必須です。"
        for key in form.errors.as_data().keys():
            self.assertIn(err_mes, form.errors[key])
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_empty_email(self):
        data = {
            "username": "test",
            "email": "",
            "password1": "pass0000",
            "password2": "pass0000",
        }
        response = self.client.post(self.signup_url, data)
        form = response.context["form"]
        form.is_valid()
        err_mes = "このフィールドは必須です。"
        for key in form.errors.as_data().keys():
            self.assertIn(err_mes, form.errors[key])
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_empty_password(self):
        data = {
            "username": "test",
            "email": "hoge@email.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.signup_url, data)
        form = response.context["form"]
        form.is_valid()
        err_mes = "このフィールドは必須です。"
        for key in form.errors.as_data().keys():
            self.assertIn(err_mes, form.errors[key])
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_duplicated_user(self):
        User.objects.create_user(
            username="test", email="fuga@email.com", password="passcode0000"
        )
        data2 = {
            "username": "test",
            "email": "fuga@email.com",
            "password1": "passcode0000",
            "password2": "passcode0000",
        }
        response = self.client.post(self.signup_url, data2)
        form = response.context["form"]
        form.is_valid()
        err_mes = "同じユーザー名が既に登録済みです。"
        for key in form.errors.as_data().keys():
            self.assertIn(err_mes, form.errors[key])
        response = self.client.post(self.signup_url, data2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    def test_failure_post_with_invalid_email(self):
        data = {
            "username": "testpscd",
            "email": "fuga.email.com",
            "password1": "test0000",
            "password2": "test0000",
        }
        form = UserCreateForm(data)
        form.is_valid()
        err_mes = "有効なメールアドレスを入力してください。"
        for key in form.errors.as_data().keys():
            self.assertIn(err_mes, form.errors[key])
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_too_short_password(self):
        data = {
            "username": "test",
            "email": "fuga@email.com",
            "password1": "passcd",
            "password2": "passcd",
        }
        response = self.client.post(self.signup_url, data)
        form = response.context["form"]
        form.is_valid()
        err_mes = "このパスワードは短すぎます。最低 8 文字以上必要です。"
        for key in form.errors.as_data().keys():
            self.assertIn(err_mes, form.errors[key])
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_password_similar_to_username(self):
        data = {
            "username": "testpscd",
            "email": "fuga@email.com",
            "password1": "testpscd",
            "password2": "testpscd",
        }
        response = self.client.post(self.signup_url, data)
        form = response.context["form"]
        form.is_valid()
        err_mes = "このパスワードは ユーザー名 と似すぎています。"
        for key in form.errors.as_data().keys():
            self.assertIn(err_mes, form.errors[key])
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_only_numbers_password(self):
        data = {
            "username": "testpscd",
            "email": "fuga@email.com",
            "password1": "20040326",
            "password2": "20040326",
        }
        response = self.client.post(self.signup_url, data)
        form = response.context["form"]
        form.is_valid()
        err_mes = "このパスワードは数字しか使われていません。"
        for key in form.errors.as_data().keys():
            self.assertIn(err_mes, form.errors[key])
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_mismatch_password(self):
        data = {
            "username": "testpscd",
            "email": "fuga@email.com",
            "password1": "testpasscd",
            "password2": "testpassdc",
        }
        response = self.client.post(self.signup_url, data)
        form = response.context["form"]
        form.is_valid()
        err_mes = "確認用パスワードが一致しません。"
        for key in form.errors.as_data().keys():
            self.assertIn(err_mes, form.errors[key])
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)


class TestHomeView(TestCase):
    def test_success_get(self):
        response = self.client.get(reverse("welcome:home"))
        self.assertEqual(response.status_code, 200)


class TestLoginView(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="successtest", email="test@email.com", password="testpasscd"
        )
        self.signin_url = reverse("accounts:signin")

    def test_success_get(self):
        response = self.client.get(self.signin_url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        userdata = {
            "username": "successtest",
            "password": "testpasscd",
        }
        response = self.client.post(self.signin_url, userdata)
        form = UserSignInForm(data=userdata)
        self.assertTrue(form.is_valid())
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL), 302, 200)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        userdata = {
            "username": "testuser",
            "password": "testpasscd",
        }
        response = self.client.post(self.signin_url, userdata)
        form = UserSignInForm(data=userdata)
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        userdata = {
            "username": "testuser",
            "password": "",
        }
        response = self.client.post(self.signin_url, userdata)
        form = UserSignInForm(data=userdata)
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="test", password="testpasscd", email="hoge@email.com"
        )
        self.client.force_login(user)

    def test_success_post(self):
        response = self.client.post(reverse("accounts:signout"))
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL), 302, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
