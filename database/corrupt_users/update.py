def add_to_corrupt_list(db, username):
    update_sql = f"""
        UPDATE corrupt_users
        SET users = array_append(users, '{username}')
        WHERE id=1
    """
    db.execute(update_sql)

def clear_corrupt_users(db):
    update_sql = f"""
        UPDATE corrupt_users
        SET users = ARRAY[]::text[]
        WHERE id=1
    """
    db.execute(update_sql)