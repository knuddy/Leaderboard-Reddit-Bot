from datetime import datetime
from sqlalchemy import create_engine
from . import user_scores
from . import time_since_last_post


class Database:
    def __init__(self, db_string):
        self.db = create_engine(db_string)
        self.create_tables()

    def top_three_and_user_rank(self, user_score, user_added_timestamp):
        top_three = [
            (0, "placeholder", datetime.now()),
            (0, "placeholder", datetime.now()),
            (0, "placeholder", datetime.now())
        ]
        user_rank = 1

        all_rows = user_scores.select_.all_user_scores(self.db)

        for row in all_rows:
            for username, score, added_timestamp in zip(row[1], row[2], row[3]):
                if score > user_score or (score == user_score and user_added_timestamp > added_timestamp): user_rank += 1

                if score > top_three[0][0] or (score == top_three[0][0] and added_timestamp < top_three[0][2]):
                    top_three = [(score, username, added_timestamp)] + top_three[:2]
                    
                elif score > top_three[1][0] or (score == top_three[1][0] and added_timestamp < top_three[1][2]):
                    top_three =  top_three[:1] + [(score, username, added_timestamp)] + top_three[1:2]
                    
                elif score > top_three[2][0] or (score == top_three[2][0] and added_timestamp < top_three[2][2]):
                    top_three = top_three[:2] + [(score, username, added_timestamp)]

        return top_three, user_rank

    def create_tables(self):
        user_scores.create.table_user_scores(self.db)
        time_since_last_post.create.table_time_since_last_post(self.db)

        if time_since_last_post.select_.time_since_last_post(self.db) is None:
            time_since_last_post.insert.time_since_last_post(self.db)

    def can_make_new_post(self, time_between_posts):
        return time_since_last_post.select_.can_make_new_post(self.db, time_between_posts)

    def update_time_since_last_post(self):
        time_since_last_post.update.time_since_last_post(self.db)

    def character_index_exists(self, character_index):
        return user_scores.select_.character_index_exists(self.db, character_index)

    def create_character_index(self, character_index):
        user_scores.insert.character_index(self.db, character_index)

    def insert_new_user(self, character_index, username):
        user_scores.insert.user_score(self.db, character_index, username)

    def get_user_data(self, character_index, username):
        return user_scores.select_.user_data(self.db, character_index, username)

    def update_user_score(self, character_index, user_index, user_score):
        user_scores.update.user_score(self.db, character_index, user_index, user_score)


    
