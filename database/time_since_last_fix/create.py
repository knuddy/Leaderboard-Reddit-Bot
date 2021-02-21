def table_time_since_last_fix(db):
    create_sql = """
        CREATE TABLE IF NOT EXISTS time_since_last_fix(
            id integer,
            last_post_time timestamp
        )
    """
    db.execute(create_sql)