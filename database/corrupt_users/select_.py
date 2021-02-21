def no_entries(db):
    select_sql = "SELECT * FROM corrupt_users"
    return db.execute(select_sql).first() is None


def has_already_been_added(db, username):
    select_sql = f"""
        SELECT * FROM corrupt_users
        WHERE '{username}' = ANY(users)
    """
    return db.execute(select_sql).first() is not None

def get_corrupt_users(db):
    select_sql = "SELECT * FROM corrupt_users"
    return db.execute(select_sql).first()

