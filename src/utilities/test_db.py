import src.utilities.db_connection as db
from src.models.tweet import Tweet

connection = db.db_connection
Tweet(tweet_data='test_data',tweet_url='http://test.com').save()