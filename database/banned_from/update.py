def add_to_banned_list(db, subreddit):
    insert_sql = f"""
        UPDATE banned_from
        SET usernames = array_append(subreddits, '{subreddit}')
        WHERE id=1
    """
    db.execute(insert_sql)