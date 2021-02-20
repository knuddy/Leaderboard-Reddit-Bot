def time_since_last_post(db):
    select_sql = "SELECT * FROM time_since_last_post"
    return db.execute(select_sql).first()


def can_make_new_post(db, time_between_posts):
    select_sql = f"""
        SELECT * FROM time_since_last_post
        WHERE last_post_time > NOW() - INTERVAL '{time_between_posts} minutes'
    """
    return db.execute(select_sql).first() is None
