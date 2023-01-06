function set_favorite_tweet(tweet_url) {
    // Fetch APIの実行
    fetch('api.json', {
        headers: {
            'Content-Type': `${tweet_url}; charset=utf-8`
        },
        body: JSON.stringify()
    })
        // 通信が成功したとき
        .then(function (response) {
            return response.json();
        })
        .then(function (json) {
            console.log(json);
        })
        // 通信が失敗したとき
        .catch(function (error) {
            console.error('Error:', error);
        });
}

function unset_favorite_tweet(tweet_url) {
    // Fetch APIの実行
    fetch('api.json', {
        headers: {
            'Content-Type': `${tweet_url}; charset=utf-8`
        },
        body: JSON.stringify()
    })
        // 通信が成功したとき
        .then(function (response) {
            return response.json();
        })
        .then(function (json) {
            console.log(json);
        })
        // 通信が失敗したとき
        .catch(function (error) {
            console.error('Error:', error);
        });
}
