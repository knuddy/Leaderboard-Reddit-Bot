def make_ban_list(db, subreddit):
    insert_sql = f"""
        INSERT INTO banned_from (id, subreddits)
        VALUES (1, ARRAY[]::text[])
    """
    db.execute(insert_sql)