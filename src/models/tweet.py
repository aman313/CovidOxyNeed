from mongoengine import Document, StringField, URLField


class Tweet(Document):
    tweet_data = StringField(required=True)
    tweet_url = URLField(required=True)