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
        err_mes = "{'content': [ValidationError(['このフィールドは必須です。'])]}"
        self.assertEqual(err_mes, str(form.errors.as_data()))
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
        err_mes = "{'content': [ValidationError(['この値は 140 文字以下でなければなりません( 445 文字になっています)。'])]}"
        self.assertEqual(err_mes, str(form.errors.as_data()))
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="hoge@email.com", password="testpass0000"
        )
        self.client.force_login(user=self.user)
        self.tweet = Tweet.objects.create(content="test_tweet", user=self.user)

    def test_success_get(self):
        tweet_pk = self.tweet.pk
        response = self.client.get(reverse("tweets:detail", kwargs={"pk": tweet_pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets_detail.html")
        self.assertEqual(response.context["tweet"], self.tweet)


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="hoge@email.com", password="testpass0000"
        )
        self.client.force_login(user=self.user)
        self.tweet = Tweet.objects.create(content="test_tweet", user=self.user)
        self.tweet_id = self.tweet.pk

    def test_success_post(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet_id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("welcome:home"), 302, 200)
        self.assertIsNone(Tweet.objects.filter(pk=self.tweet_id).first())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet_id + 1})
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn(
            b"The requested resource was not found on this server.", response.content
        )

    def test_failure_post_with_incorrect_user(self):
        incorrect_user = self.user = User.objects.create_user(
            username="incorrect_user", email="fuga@email.com", password="testpass0000"
        )
        self.client.force_login(user=incorrect_user)
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet_id})
        )
        self.assertEqual(response.status_code, 403)


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
