class Tweet(object):
    tweet_data = ''
    tweet_url = ''

    def __init__(self, tweet_data, tweet_url):
        self.tweet_data = tweet_data
        self.tweet_url = tweet_url

    def get_tweet_data(self):
        return self.tweet_data

    def get_tweet_url(self):
        return self.tweet_url

    def __str__(self):
        return self.tweet_data + ' | ' \
                + self.tweet_url
