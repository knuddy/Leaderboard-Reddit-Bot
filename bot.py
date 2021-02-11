import praw
import re
import sys
from datetime import datetime, timedelta
from post_template import POST_TEMPLATE
from database import Database


class StarWarsBot:
    def __init__(self, client_id, client_secret, password, user_agent, username, db_url, posting_enabled, time_between_posts):
        self.reddit_instance = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            password=password,
            user_agent=user_agent,
            username=username,
        )
        
        self.username = username
        self.posting_enabled = posting_enabled

        self.db = Database(db_url, time_between_posts)
        self.cached_character_indexs = self.db.character_indexs()

    def run(self, subreddit_name, search_term):
        subreddit = self.reddit_instance.subreddit(subreddit_name)

        for comment in subreddit.stream.comments(skip_existing=True):
            comment_text_lower = comment.body.lower()
            username = comment.author.name

            if username != self.username and re.search(search_term.lower(), comment_text_lower, re.IGNORECASE):
                self.handle_user_comment(comment, username)



    def handle_user_comment(self, comment, username):
        character_index = username[:2]

        if character_index not in self.cached_character_indexs:
            self.db.create_character_index_and_insert_new_user_score(character_index, username)
            self.cached_character_indexs.append(character_index)
            print(f"new index {character_index} and new user {username}")
            sys.stdout.flush()
        else:
            row = self.db.user_data(character_index, username)
            
            if row is not None:
                self.db.update_user_score(character_index, username, row[1], row[2])
                print(f"updated {username} score")
                sys.stdout.flush()
            else:
                self.db.add_new_user_to_character_index(character_index, username)
                print(f"new user {username}")
                sys.stdout.flush()

        if self.posting_enabled and self.db.can_make_new_post():
             self.make_new_post(character_index, username, comment)
             self.db.update_time_since_last_post()
             print(f"Made post to user {username}")
             sys.stdout.flush()

    def make_new_post(self, character_index, username, comment):
        _, usernames, scores, user_timestamps = self.db.user_data(character_index, username)
        user_score, user_index = self.db.user_score_and_index(username, usernames, scores)

        top_three, user_rank = self.db.top_three_and_user_rank(user_score, user_timestamps[user_index - 1])

        post_reply = POST_TEMPLATE.format(
            top_three[0][1], top_three[0][0],
            top_three[1][1], top_three[1][0],
            top_three[2][1], top_three[2][0],
            user_rank, username, user_score
        )

        comment.reply(post_reply)

        
        

