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

function set_favorite_button_space_inner_html(tweet_id,is_favorite) {
    alert("Hello World");
    let favorite_button = document.getElementById("favorite_button" + tweet_id);
    let unfavorite_button = document.getElementById("unfavorite_button" + tweet_id);
    let url = is_favorite ? `{% url 'tweets:unfavorite' ${tweet_id} %}')` : `{% url 'tweets:unfavorite' ${tweet_id} %}')`;
    favorite_button.style.visibility = is_favorite ? "hidden" : "visible";
    unfavorite_button.style.visibility = is_favorite ? "visible" : "hidden";
}

function set_or_unset_favorite_tweet(tweet_url,tweet_id,is_favorite) {
	const csrftoken = getCookie("csrftoken");
	const request_options = {
		method: "POST",
		headers: {
			"X-CSRFToken": csrftoken,
		},
	};
	// Fetch APIの実行
	fetch(tweet_url, {
		method: "POST",
		headers: {
			"X-CSRFToken": csrftoken,
		},
	})
		// 通信が成功したとき
		.then((response) => {
			console.log(response);
		})
		.then((json) => {
			console.log(`done successfully! at url: ${tweet_url}`);
			set_favorite_button_space_inner_html(tweet_id,is_favorite);
			console.log(json);
		})
		// 通信が失敗したとき
		.catch(function (error) {
			console.error(`error occured!: ${error} at url: ${tweet_url} `);
		});
}
