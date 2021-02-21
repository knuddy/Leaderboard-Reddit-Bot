import sys
from datetime import datetime
from sqlalchemy import create_engine
from . import user_scores, time_since_last_post, banned_from, corrupt_users, time_since_last_fix


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
                try:
                    if score > user_score or (score == user_score and user_added_timestamp > added_timestamp): user_rank += 1

                    if score > top_three[0][0] or (score == top_three[0][0] and added_timestamp < top_three[0][2]):
                        top_three = [(score, username, added_timestamp)] + top_three[:2]

                    elif score > top_three[1][0] or (score == top_three[1][0] and added_timestamp < top_three[1][2]):
                        top_three =  top_three[:1] + [(score, username, added_timestamp)] + top_three[1:2]

                    elif score > top_three[2][0] or (score == top_three[2][0] and added_timestamp < top_three[2][2]):
                        top_three = top_three[:2] + [(score, username, added_timestamp)]
                except TypeError:
                    if self._has_user_been_added_to_corrupt_list(username) is False:
                        self._add_user_to_corrupt_list(username)

                    print(f"user {username} score is corrupt.")
                    sys.stdout.flush()

        return top_three, user_rank

    def create_tables(self):
        user_scores.create.table_user_scores(self.db)

        time_since_last_post.create.table_time_since_last_post(self.db)
        if time_since_last_post.select_.no_entries(self.db):
            time_since_last_post.insert.make_timer(self.db)

        banned_from.create.table_banned_from(self.db)
        if banned_from.select_.no_entries(self.db):
            banned_from.insert.make_ban_list(self.db)

        corrupt_users.create.table_corrupt_users(self.db)
        if corrupt_users.select_.no_entries(self.db):
            corrupt_users.insert.make_corrupt_list(self.db)

        time_since_last_fix.create.table_time_since_last_fix(self.db)
        if time_since_last_fix.select_.no_entries(self.db):
            time_since_last_fix.insert.make_timer(self.db)


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

    def add_subreddit_to_ban_list(self, subreddit):
        banned_from.update.add_to_banned_list(self.db, subreddit)

    def is_banned_from_subreddit(self, subreddit):
        return banned_from.select_.is_banned_from_subreddit(self.db, subreddit)

    def can_fix_corrupt_users(self, time_between_fixes):
        return time_since_last_fix.select_.can_fix(self.db, time_between_fixes)

    def _update_time_since_last_fix(self):
        time_since_last_fix.update.time_since_last_fix(self.db)

    def _add_user_to_corrupt_list(self, username):
        corrupt_users.update.add_to_corrupt_list(self.db, username)

    def _has_user_been_added_to_corrupt_list(self, username):
        return corrupt_users.select_.has_already_been_added(self.db, username)

    def fix_corrupt_users(self):
        _, list_corrupt_users = corrupt_users.select_.get_corrupt_users(self.db)

        for username in list_corrupt_users:
            character_index = username[:2]
            user_index, _, __ = self.db.get_user_data(character_index, username)
            self.update_user_score(character_index, user_index, 0)

        corrupt_users.update.clear_corrupt_users(self.db)
        self._update_time_since_last_fix()



    
