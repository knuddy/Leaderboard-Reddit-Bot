def make_corrupt_list(db):
    insert_sql = f"""
        INSERT INTO corrupt_users (id, users)
        VALUES (1, ARRAY[]::text[])
    """
    db.execute(insert_sql)