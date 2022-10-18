from django.test import Client, TestCase
from django.urls import reverse


def print_red(code):
    print("\033[31m" + f"status_code:{code}" + "\033[0m")


class TestSignUpView(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setUp()

    def setUp(self):
        self.url = reverse("accounts:signup")
        self.client = Client()

    def test_success_get(self):
        response = self.client.get(reverse("accounts:home"))
        print(
            "\033[31m"
            + f"status_code:{str(response.status_code)} type:{type(response.status_code)}"
            + "\033[0m"
        )
        # self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "username": "test",
            "password1": "passcode0000",
            "password2": "passcode0000",
        }
        response = self.client.post(reverse("accounts:signup"), data)
        print_red(response)
        # self.assertEqual(response.status_code, 200)

    def test_failure_post_with_empty_form(self):
        data = {
            "username": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password1", "This field is required.")
        self.assertFormError(response, "form", "password2", "This field is required.")

    def test_failure_post_with_empty_username(self):
        pass

    def test_failure_post_with_empty_email(self):
        pass

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
