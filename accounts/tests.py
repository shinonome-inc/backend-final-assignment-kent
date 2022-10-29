import json

import colorama
from colorama import Fore
from django.core import serializers
from django.test import TestCase
from django.urls import reverse

from accounts.forms import UserCreateForm

from .models import User


def print_colored_text(code, *styles):
    colorama.init()
    text_to_print = ""
    for style in styles:
        text_to_print += style
    text_to_print += str(code)
    print(f"{text_to_print}" + Fore.RESET)


class TestSignUpView(TestCase):
    def test_success_get(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "username": "test",
            "email": "hoge@email.com",
            "password1": "passcode0000",
            "password2": "passcode0000",
        }
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertRedirects(response, reverse("accounts:home"), 302, 200)
        added_record = User.objects.filter(username="test")
        self.assertTrue(added_record.exists())
        self.assertEquals(added_record[0].username, "test")
        self.assertEquals(added_record[0].email, "hoge@email.com")

    def test_failure_post_with_empty_form(self):
        data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        form = UserCreateForm(data)
        form.is_valid()
        expected_error_mes = "{'username': [ValidationError(['このフィールドは必須です。'])], 'email': [ValidationError(['このフィールドは必須です。'])], 'password1': [ValidationError(['このフィールドは必須です。'])], 'password2': [ValidationError(['このフィールドは必須です。'])]}"
        self.assertEqual(expected_error_mes, str(form.errors.as_data()))
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_empty_username(self):
        data = {
            "username": "",
            "email": "hoge@email.com",
            "password1": "pass0000",
            "password2": "pass0000",
        }
        form = UserCreateForm(data)
        form.is_valid()
        expected_error_mes = "{'username': [ValidationError(['このフィールドは必須です。'])]}"
        self.assertEqual(expected_error_mes, str(form.errors.as_data()))
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_empty_email(self):
        data = {
            "username": "test",
            "email": "",
            "password1": "pass0000",
            "password2": "pass0000",
        }
        form = UserCreateForm(data)
        form.is_valid()
        expected_error_mes = "{'email': [ValidationError(['このフィールドは必須です。'])]}"
        self.assertEqual(expected_error_mes, str(form.errors.as_data()))
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_empty_password(self):
        data = {
            "username": "test",
            "email": "hoge@email.com",
            "password1": "",
            "password2": "",
        }
        form = UserCreateForm(data)
        form.is_valid()
        expected_error_mes = "{'password1': [ValidationError(['このフィールドは必須です。'])], 'password2': [ValidationError(['このフィールドは必須です。'])]}"
        self.assertEqual(expected_error_mes, str(form.errors.as_data()))
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_duplicated_user(self):
        data1 = {
            "username": "test",
            "email": "fuga@email.com",
            "password1": "passcode0000",
            "password2": "passcode0000",
        }
        self.client.post(reverse("accounts:signup"), data1)
        data2 = {
            "username": "test",
            "email": "fuga@email.com",
            "password1": "passcode0000",
            "password2": "passcode0000",
        }
        form = UserCreateForm(data2)
        form.is_valid()
        expected_error_mes = "{'username': [ValidationError(['同じユーザー名が既に登録済みです。'])]}"
        self.assertEqual(expected_error_mes, str(form.errors.as_data()))
        response = self.client.post(reverse("accounts:signup"), data2)
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
        expected_error_mes = "{'email': [ValidationError(['有効なメールアドレスを入力してください。'])]}"
        self.assertEqual(expected_error_mes, str(form.errors.as_data()))
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_too_short_password(self):
        data = {
            "username": "test",
            "email": "fuga@email.com",
            "password1": "passcd",
            "password2": "passcd",
        }
        form = UserCreateForm(data)
        form.is_valid()
        expected_error_mes = (
            "{'password2': [ValidationError(['このパスワードは短すぎます。最低 8 文字以上必要です。'])]}"
        )
        self.assertEqual(expected_error_mes, str(form.errors.as_data()))
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_password_similar_to_username(self):
        data = {
            "username": "testpscd",
            "email": "fuga@email.com",
            "password1": "testpscd",
            "password2": "testpscd",
        }
        form = UserCreateForm(data)
        form.is_valid()
        expected_error_mes = (
            "{'password2': [ValidationError(['このパスワードは ユーザー名 と似すぎています。'])]}"
        )
        self.assertEqual(expected_error_mes, str(form.errors.as_data()))
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_only_numbers_password(self):
        data = {
            "username": "testpscd",
            "email": "fuga@email.com",
            "password1": "20040326",
            "password2": "20040326",
        }
        form = UserCreateForm(data)
        form.is_valid()
        expected_error_mes = (
            "{'password2': [ValidationError(['このパスワードは数字しか使われていません。'])]}"
        )
        self.assertEqual(expected_error_mes, str(form.errors.as_data()))
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_mismatch_password(self):
        data = {
            "username": "testpscd",
            "email": "fuga@email.com",
            "password1": "testpasscd",
            "password2": "testpassdc",
        }
        form = UserCreateForm(data)
        form.is_valid()
        expected_error_mes = "{'password2': [ValidationError(['確認用パスワードが一致しません。'])]}"
        self.assertEqual(expected_error_mes, str(form.errors.as_data()))
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)


class TestHomeView(TestCase):
    def test_success_get(self):
        response = self.client.get(reverse("accounts:home"))
        self.assertEqual(response.status_code, 200)


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


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
