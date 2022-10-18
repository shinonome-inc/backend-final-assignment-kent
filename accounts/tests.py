from django.test import Client, TestCase
from django.urls import reverse


def print_red(code):
    print("\033[31m" + f"status_code:{code}" + "\033[0m")


class TestSignUpView(TestCase):
    """def __init__(self, *args, **kwargs):
    super().__init__()
    self.setUp()"""

    def setUp(self):
        self.client = Client()
        self.url = reverse("accounts:signup")

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
            "password1": "passcode0000",
            "password2": "passcode0000",
        }
        response = self.client.post(reverse("accounts:signup"), data)
        # リダイレクトされるため200は返ってこないが、302が返ってくる
        self.assertEqual(response.status_code, 302)

    def test_failure_post_with_empty_form(self):
        data_empty_form = {
            "username": "hello_world",
            "password1": "aaaaaaff123",
            "password2": "aaaaaaff123",
        }
        response_empty_form = self.client.post(
            reverse("accounts:signup"), data_empty_form
        )
        self.assertFormError(response_empty_form, "form", "username", "このフィールドは必須です。")
        self.assertFormError(response_empty_form, "form", "password1", "このフィールドは必須です。")
        self.assertFormError(response_empty_form, "form", "password2", "このフィールドは必須です。")
        self.assertFormError(response_empty_form, "form", None, "このフィールドは必須です。")

    def test_failure_post_with_empty_username(self):
        data_empty_name = {
            "username": "",
            "password1": "pass0000",
            "password2": "pass0000",
        }
        response_empty_username = self.client.post(
            reverse("accounts:signup"), data_empty_name
        )
        self.assertFormError(
            response_empty_username, "form", "username", "このフィールドは必須です。"
        )
        self.assertFormError(
            response_empty_username,
            "form",
            "username",
            "Response did not use any contexts to render the response.",
        )

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
