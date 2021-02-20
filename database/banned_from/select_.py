def no_entries(db):
    select_sql = "SELECT * FROM time_since_last_post"
    return db.execute(select_sql).first() is None

def is_banned_from_subreddit(db, subreddit):
    select_sql = f"""
        SELECT * FROM time_since_last_post
        WHERE '{subreddit}' = ANY(subreddits)
    """
    return db.execute(select_sql).first() is not None