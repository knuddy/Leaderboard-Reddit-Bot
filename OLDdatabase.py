from datetime import datetime
from sqlalchemy import create_engine

class Database:
    def __init__(self, db_string, time_between_posts=15):
        self.db = create_engine(db_string)
        self.create_table_user_scores()
        self.create_table_time_since_last_post()
        self.time_between_posts = time_between_posts

    def top_three_and_user_rank(self, user_score, user_added_timestamp):
        top_three = [
            (0, "placeholder", datetime.now()),
            (0, "placeholder", datetime.now()),
            (0, "placeholder", datetime.now())
        ]
        user_rank = 1

        select_sql = "SELECT * FROM user_scores"
        for row in self.db.execute(select_sql):
            for username, score, added_timestamp in zip(row[1], row[2], row[3]):
                if score > user_score or (score == user_score and user_added_timestamp > added_timestamp): user_rank += 1

                if score > top_three[0][0] or (score == top_three[0][0] and added_timestamp < top_three[0][2]):
                    top_three = [(score, username, added_timestamp)] + top_three[:2]
                    
                elif score > top_three[1][0] or (score == top_three[1][0] and added_timestamp < top_three[1][2]):
                    top_three =  top_three[:1] + [(score, username, added_timestamp)] + top_three[1:2]
                    
                elif score > top_three[2][0] or (score == top_three[2][0] and added_timestamp < top_three[2][2]):
                    top_three = top_three[:2] + [(score, username, added_timestamp)]

        return (top_three, user_rank)


    def create_table_user_scores(self):
        self.db.execute("CREATE TABLE IF NOT EXISTS user_scores (character_index text, usernames text[], scores integer[], users_added timestamp[])")


    def create_table_time_since_last_post(self):
        self.db.execute("CREATE TABLE IF NOT EXISTS time_since_last_post (id integer, last_post_time timestamp)")
        if self.db.execute("SELECT * FROM time_since_last_post").first() is None:
            self.db.execute("INSERT INTO time_since_last_post (id, last_post_time) VALUES(1, NOW() - INTERVAL '15 minutes')")


    def can_make_new_post(self):
        select_sql = f"""
            SELECT * FROM time_since_last_post
            WHERE last_post_time > NOW() - INTERVAL '{self.time_between_posts} minutes'
        """
        return self.db.execute(select_sql).first() is None


    def update_time_since_last_post(self):
        self.db.execute("UPDATE time_since_last_post SET last_post_time=NOW() WHERE id=1")


    def character_indexs(self):
        select_sql = "SELECT * FROM user_scores"
        return [row[0] for row in self.db.execute(select_sql)]


    def create_character_index_and_insert_new_user_score(self, character_index, username):
        insert_sql = f"""
            INSERT INTO user_scores (character_index, usernames, scores, users_added)
            VALUES ('{character_index}', ARRAY['{username}'], ARRAY[1], ARRAY[NOW()])
        """
        self.db.execute(insert_sql)


    def user_data(self, character_index, username):
        select_sql =  f"""
            select * from user_scores
            WHERE character_index='{character_index}'
            AND EXISTS (
                SELECT
                FROM unnest(usernames) elem
                WHERE elem LIKE '%%{username}%%'
            )
        """
        return self.db.execute(select_sql).first()


    def user_score_and_index(self, username, usernames, scores):
        for i, (potential_username, score) in enumerate(zip(usernames, scores)):
            if potential_username == username:
                return (score, i + 1)


    def update_user_score(self, character_index, username, usernames, scores):
        score, score_index = self.user_score_and_index(username, usernames, scores)
        update_sql =f"""
            UPDATE user_scores
            SET scores[{score_index}] = {score + 1},
                users_added[{score_index}] = NOW()
            WHERE character_index='{character_index}'
        """ 
        self.db.execute(update_sql)


    def add_new_user_to_character_index(self, character_index, username):
        update_sql = f"""
            UPDATE user_scores
            SET usernames = array_append(usernames, '{username}'),
                scores = array_append(scores, 1),
                users_added = array_append(users_added, NOW()::timestamp)
            WHERE character_index='{character_index}'
        """
        self.db.execute(update_sql)

    
