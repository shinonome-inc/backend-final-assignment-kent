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

function set_or_unset_favorite_tweet(tweet_url) {
    const csrftoken = getCookie('csrftoken');
    const request_options = {
        'method': 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    };
    const request = new Request(tweet_url, request_options);
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
            window.location.reload();
            console.log(`done successfully! at url: ${tweet_url}`);
            console.log(json);
        })
        // 通信が失敗したとき
        .catch(function (error) {
            console.error(`error occured!: ${error} at url: ${tweet_url} `);
        });
}
