def table_user_scores(db):
    create_sql = """
        CREATE TABLE IF NOT EXISTS user_scores(
            character_index text,
            usernames text[],
            scores integer[],
            users_added timestamp[]
        )
    """
    db.execute(create_sql)