def no_entries(db):
    select_sql = "SELECT * FROM time_since_last_fix"
    return db.execute(select_sql).first() is None


def can_fix(db, time_between_fixes):
    select_sql = f"""
        SELECT * FROM time_since_last_fix
        WHERE last_post_time > NOW() - INTERVAL '{time_between_fixes} minutes'
    """
    return db.execute(select_sql).first() is None
