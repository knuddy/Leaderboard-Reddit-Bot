def table_corrupt_users(db):
    create_sql = """
        CREATE TABLE IF NOT EXISTS corrupt_users(
            id integer,
            users text[]
        )
    """
    db.execute(create_sql)