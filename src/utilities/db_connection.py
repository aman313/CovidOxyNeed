import mongoengine
from src.constants import CommonConstants

db_connection = mongoengine.connect(CommonConstants.DB_NAME)