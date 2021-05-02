def insert_tweet(tweets, connection):
    cur = connection.cursor()
    for tweet in tweets:
        cur.execute(
            "INSERT INTO tweets (tweet_data, tweet_url)"
            " VALUES(?, ?)",
            (
                tweet.get_tweet_data(),
                tweet.get_tweet_url()
            )
        )
    connection.commit()