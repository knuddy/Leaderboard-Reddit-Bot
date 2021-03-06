def no_entries(db):
    select_sql = "SELECT * FROM banned_from"
    return db.execute(select_sql).first() is None

def is_banned_from_subreddit(db, subreddit):
    select_sql = f"""
        SELECT * FROM banned_from
        WHERE '{subreddit}' = ANY(subreddits)
    """
    return db.execute(select_sql).first() is not None