from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tweets.models import Favorite, Tweet

User = get_user_model()


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.signup_url = reverse("accounts:signup")
        self.create_url = reverse("tweets:create")
        self.home_url = reverse("welcome:home")
        self.user = User.objects.create_user(
            username="test", email="hoge@email.com", password="testpass0000"
        )
        self.client.force_login(self.user)

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
        response = self.client.post(self.create_url, data)
        form = response.context["form"]
        expected_errs = {"content": "このフィールドは必須です。"}
        for key, message in expected_errs.items():
            self.assertIn(message, form.errors[key])
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
        response = self.client.post(self.create_url, data)
        form = response.context["form"]
        expected_errs = {
            "content": "この値は 140 文字以下でなければなりません( 445 文字になっています)。",
        }
        for key, message in expected_errs.items():
            self.assertIn(message, form.errors[key])
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
        self.assertTemplateUsed(response, "tweets/tweets_detail.html")
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
        self.assertFalse(Tweet.objects.filter(pk=self.tweet_id).exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet_id + 1})
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn(
            b"The requested resource was not found on this server.", response.content
        )

    def test_failure_post_with_incorrect_user(self):
        incorrect_user = User.objects.create_user(
            username="incorrect_user", email="fuga@email.com", password="testpass0000"
        )
        self.client.force_login(user=incorrect_user)
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet_id})
        )
        self.assertEqual(response.status_code, 403)


class TestFavoriteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="hoge@email.com", password="testpass0000"
        )
        self.client.force_login(user=self.user)
        self.tweet = Tweet.objects.create(content="test_tweet", user=self.user)
        self.tweet_id = self.tweet.pk
        self.pre_favorite_count = Favorite.objects.count()

    def test_success_post(self):
        request = self.client.post(
            reverse("tweets:favorite", kwargs={"pk": self.tweet_id})
        )
        self.assertEqual(request.status_code, 200)
        post_favorite_count = Favorite.objects.count()
        self.assertEqual(post_favorite_count, self.pre_favorite_count + 1)

    def test_failure_post_with_not_exist_tweet(self):
        unexist_tweet_id = self.tweet_id + 1
        request = self.client.post(
            reverse("tweets:favorite", kwargs={"pk": unexist_tweet_id})
        )
        err_mes = b"The requested resource was not found on this server."
        self.assertIn(err_mes, request.content)
        self.assertEqual(request.status_code, 404)
        post_favorite_count = Favorite.objects.count()
        self.assertEqual(post_favorite_count, self.pre_favorite_count)

    def test_failure_post_with_favorited_tweet(self):
        self.tweet = Tweet.objects.create(content="favorited_tweet", user=self.user)
        self.favorited_tweet_id = self.tweet.pk
        Favorite.objects.create(user=self.user, tweet=self.tweet)
        pre_favorite_count = Favorite.objects.count()
        request = self.client.post(
            reverse("tweets:favorite", kwargs={"pk": self.favorited_tweet_id})
        )
        self.assertEqual(request.status_code, 200)
        post_favorite_count = Favorite.objects.count()
        self.assertEqual(post_favorite_count, pre_favorite_count)


class TestUnfavoriteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="hoge@email.com", password="testpass0000"
        )
        self.client.force_login(user=self.user)
        self.tweet = Tweet.objects.create(content="test_tweet", user=self.user)
        self.tweet_id = self.tweet.pk
        Favorite.objects.create(user=self.user, tweet=self.tweet)
        self.pre_favorite_count = Favorite.objects.count()

    def test_success_post(self):
        request = self.client.post(
            reverse("tweets:unfavorite", kwargs={"pk": self.tweet_id})
        )
        self.assertEqual(request.status_code, 200)
        post_favorite_count = Favorite.objects.count()
        self.assertEqual(post_favorite_count, self.pre_favorite_count - 1)

    def test_failure_post_with_not_exist_tweet(self):
        unexist_tweet_id = self.tweet_id + 1
        request = self.client.post(
            reverse("tweets:favorite", kwargs={"pk": unexist_tweet_id})
        )
        err_mes = b"The requested resource was not found on this server."
        self.assertIn(err_mes, request.content)
        self.assertEqual(request.status_code, 404)
        post_favorite_count = Favorite.objects.count()
        self.assertEqual(post_favorite_count, self.pre_favorite_count)

    def test_failure_post_with_unfavorited_tweet(self):
        tweet = Tweet.objects.create(content="unfavorited_tweet", user=self.user)
        self.unfavorited_tweet_id = tweet.pk
        request = self.client.post(
            reverse("tweets:favorite", kwargs={"pk": self.unfavorited_tweet_id})
        )
        self.assertEqual(request.status_code, 200)
