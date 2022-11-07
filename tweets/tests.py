from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from tweets.forms import TweetCreateForm
from tweets.models import Tweet


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.signup_url = reverse("accounts:signup")
        self.create_url = reverse("tweets:create")
        self.home_url = reverse("welcome:home")
        self.user = User.objects.create_user(
            username="test", email="hoge@email.com", password="testpass0000"
        )

    def test_success_get(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        self.client.force_login(user=self.user)
        data = {"content": "Hello, world!"}
        response = self.client.post(self.create_url, data)
        self.assertRedirects(response, self.home_url, 302, 200)

    def test_failure_post_with_empty_content(self):
        self.client.force_login(user=self.user)
        data = {"content": ""}
        form = TweetCreateForm(data)
        form.is_valid()
        e_mes = "{'content': [ValidationError(['このフィールドは必須です。'])]}"
        self.assertEqual(e_mes, str(form.errors.as_data()))
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)

    def test_failure_post_with_too_long_content(self):
        self.client.force_login(user=self.user)
        data = {
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
            + " sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,"
            + " quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
            + " Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
            + " Excepteur sint occaecat cupidatat non proident,"
            + " sunt in culpa qui officia deserunt mollit anim id est laborum."
        }
        form = TweetCreateForm(data)
        form.is_valid()
        e_mes = "{'content': [ValidationError(['この値は 140 文字以下でなければなりません( 445 文字になっています)。'])]}"
        self.assertEqual(e_mes, str(form.errors.as_data()))
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)


class TestTweetDetailView(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="test_user", email="hoge@email.com", password="testpass0000"
        )
        self.client.force_login(user=user)
        Tweet.objects.create(content="test_tweet", user=user)

    def test_success_get(self):
        response = self.client.get(reverse("tweets:detail"), data={"pk": 1})
        print(response)
        self.assertInHTML("{{ tweet.content }}")


class TestTweetDeleteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
