function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function set_favorite_button_space_inner_html(tweet_url) {
    let button_elem = document.getElementById("favorite_unfavorite_button");
    button_elem.innerHTML = get_favorite_button_space_html(tweet_url);
}

function get_favorite_button_space_html(tweet_url) {
    const button_msg = tweet_url.includes("unfavorite") ? "いいね" : "いいね取消";
    const html = `<input type=\"button\" value=\"${button_msg}\" onclick=\"set_or_unset_favorite_tweet('{% url 'tweets: favorite' tweet.id %}')\">`;
    return html;
}

function set_or_unset_favorite_tweet(tweet_url) {
    const csrftoken = getCookie('csrftoken');
    const request_options = {
        'method': 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    };
    // Fetch APIの実行
    fetch(tweet_url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
        // 通信が成功したとき
        .then((response) => {
            console.log(response);
        })
        .then((json) => {
            console.log(`done successfully! at url: ${tweet_url}`);
            set_favorite_button_space_inner_html(tweet_url);
            console.log(json);
        })
        // 通信が失敗したとき
        .catch(function (error) {
            console.error(`error occured!: ${error} at url: ${tweet_url} `);
        });
}
