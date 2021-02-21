def time_since_last_fix(db):
    update_sql = """
        UPDATE time_since_last_fix
        SET last_post_time=NOW()
        WHERE id=1
    """
    db.execute(update_sql)