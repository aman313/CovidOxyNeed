from mongoengine import Document, StringField, URLField, DateField


class Tweet(Document):
    tweet_data = StringField(required=True)
    tweet_url = URLField(required=True)
    tweet_time = DateField(required=True)
