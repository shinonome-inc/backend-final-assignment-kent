function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(
					cookie.substring(name.length + 1)
				);
				break;
			}
		}
	}
	return cookieValue;
}

function set_or_unset_favorite_tweet(event) {
	set_or_unset_favorite_tweet_backend_process(event)
}

function set_or_unset_favorite_tweet_backend_process(click_event) {
	const tweet_url = click_event.target.dataset.tweetUrl;
	const csrftoken = getCookie("csrftoken");
	const request_options = {
		method: "POST",
		headers: {
			"X-CSRFToken": csrftoken,
		},
	};
	// Fetch APIの実行
	fetch(tweet_url, request_options)
		// 通信が成功したとき
		.then((response) => {
			console.log(response);
		})
		.then((json) => {
			console.log(`done successfully! @ url: ${tweet_url}`);
			set_or_unset_favorite_tweet_frontend_process(click_event);
			console.log(json);
		})
		// 通信が失敗したとき
		.catch(function (error) {
			console.error(`error occured!: ${error} @ url: ${tweet_url} `);
		});
}
function set_or_unset_favorite_tweet_frontend_process(event) {
	const tweet_id = event.target.dataset.tweetId;
	const favorite_button = document.getElementById("favorite_button" + tweet_id);
	const unfavorite_button = document.getElementById("unfavorite_button" + tweet_id);
	favorite_button.style.visibility = favorite_button.style.visibility == "hidden" ? "visible" : "hidden";
	unfavorite_button.style.visibility = favorite_button.style.visibility == "hidden" ? "visible" : "hidden";
}
