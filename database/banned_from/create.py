def table_banned_from(db):
    create_sql = """
        CREATE TABLE IF NOT EXISTS banned_from(
            id integer,
            subreddits text[]
        )
    """
    db.execute(create_sql)