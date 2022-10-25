from django.test import TestCase
from django.urls import reverse

from accounts.forms import UserCreateForm


def print_red(code):
    print("\033[31m" + f"status_code:{code}" + "\033[0m")


class TestSignUpView(TestCase):
    """def __init__(self, *args, **kwargs):
    super().__init__()
    self.setUp()

    def setUp(self):
        self.client = Client()
        self.url = reverse("accounts:signup")"""

    def runTest():
        test = TestSignUpView()
        # test.test_success_get()
        test.test_success_post()
        # test.test_failure_post_with_empty_form()
        # test.test_failure_post_with_empty_username()

    def test_success_get(self):
        response = self.client.get(reverse("accounts:home"))
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "username": "test",
            "email": "hoge@email.com",
            "password1": "passcode0000",
            "password2": "passcode0000",
        }
        response = self.client.post(reverse("accounts:signup"), data)
        # リダイレクトされるため200は返ってこないが、302が返ってくる
        self.assertEqual(response.status_code, 302)

    def test_failure_post_with_empty_form(self):
        data_empty_form = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        form = UserCreateForm(data_empty_form)
        form.is_valid()
        print_red(f"{form.errors.as_json}\n")

    def test_failure_post_with_empty_username(self):
        data_empty_name = {
            "username": "",
            "email": "hoge@email.com",
            "password1": "pass0000",
            "password2": "pass0000",
        }
        form = UserCreateForm(data_empty_name)
        form.is_valid()
        print_red(f"{form.errors.as_json}\n")

    def test_failure_post_with_empty_email(self):
        data_empty_name = {
            "username": "test",
            "email": "",
            "password1": "pass0000",
            "password2": "pass0000",
        }
        form = UserCreateForm(data_empty_name)
        form.is_valid()
        print_red(f"{form.errors.as_json}\n")

    def test_failure_post_with_empty_password(self):
        pass

    def test_failure_post_with_duplicated_user(self):
        pass

    def test_failure_post_with_invalid_email(self):
        pass

    def test_failure_post_with_too_short_password(self):
        pass

    def test_failure_post_with_password_similar_to_username(self):
        pass

    def test_failure_post_with_only_numbers_password(self):
        pass

    def test_failure_post_with_mismatch_password(self):
        pass


class TestHomeView(TestCase):
    def test_success_get(self):
        pass


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
