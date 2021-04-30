import db_connection as db

connection = db.DbConnection().get_connection()

cur = connection.cursor()

cur.execute("INSERT INTO tweets (tweet_data, tweet_url)"
            " VALUES(?, ?)",
            (
                "test test",
                "test.test"
            ))

connection.commit()
connection.close()
