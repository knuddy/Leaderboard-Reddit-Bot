import praw
import prawcore.exceptions
import re
import sys
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
        self.time_between_posts = time_between_posts
        self.db = Database(db_url)

    def run(self, subreddit_name, search_term):
        subreddit = self.reddit_instance.subreddit(subreddit_name)

        for comment in subreddit.stream.comments(skip_existing=True):
            comment_text_lower = comment.body.lower()
            username = comment.author.name

            if username != self.username and re.search(search_term.lower(), comment_text_lower, re.IGNORECASE):
                character_index = username[:2]
                self.handle_user_comment(username, character_index)
                self.handle_user_post(comment, username, character_index, search_term)

    def handle_user_comment(self, username, character_index):
        if self.db.character_index_exists(character_index) is False:
            self.db.create_character_index(character_index)
            self.db.insert_new_user(character_index, username)
            print(f"new index {character_index} and new user {username}")
            sys.stdout.flush()
        else:
            user_data = self.db.get_user_data(character_index, username)
            if user_data is not None:
                user_index, user_score, _ = user_data
                self.db.update_user_score(character_index, user_index, user_score)
                print(f"updated {username} score")
                sys.stdout.flush()
            else:
                self.db.insert_new_user(character_index, username)
                print(f"new user {username}")
                sys.stdout.flush()

    def handle_user_post(self, comment, username, character_index, search_term):
        comment_comparisons = [comment.body.lower() == st for st in [search_term.lower(), search_term.lower() + "."]]

        can_post = (self.posting_enabled and
                    any(comment_comparisons) and
                    self.db.can_make_new_post(self.time_between_posts) and
                    self.db.is_banned_from_subreddit(comment.subreddit) is False)

        if can_post:
             self.make_new_post(character_index, username, comment)
             print(f"Made post to user {username}")
             sys.stdout.flush()

    def make_new_post(self, character_index, username, comment):
        user_score, user_index , user_timestamp = self.db.get_user_data(character_index, username)
        top_three, user_rank = self.db.top_three_and_user_rank(user_score, user_timestamp)

        post_reply = POST_TEMPLATE.format(
            top_three[0][1], top_three[0][0],
            top_three[1][1], top_three[1][0],
            top_three[2][1], top_three[2][0],
            user_rank, username, user_score
        )
        try:
            comment.reply(post_reply)
            self.db.update_time_since_last_post()
        except prawcore.exceptions.Forbidden:
            self.db.add_subreddit_to_ban_list(comment.subreddit)
            print(f"banned from commenting on r/{comment.subreddit}!")
            sys.stdout.flush()


        
        

