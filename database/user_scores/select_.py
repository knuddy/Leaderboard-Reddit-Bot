def all_user_scores(db):
    select_sql = "SELECT * FROM user_scores"
    return db.execute(select_sql)


def user_data(db, character_index, username):
    select_sql = f"""
        SELECT * from user_scores
        WHERE character_index='{character_index}'
        AND EXISTS (
            SELECT
            FROM unnest(usernames) elem
            WHERE elem LIKE '%%{username}%%'
        )
    """
    character_index_row = db.execute(select_sql).first()

    if character_index_row is None:
        return None
    else:
        _, usernames, scores, timestamps = character_index_row

        for i, (potential_username, score, timestamp) in enumerate(zip(usernames, scores, timestamps)):
            if potential_username == username:
                return score, i + 1, timestamp

def character_index_exists(db, character_index):
    select_sql = f"""
        SELECT * from user_scores
        WHERE character_index='{character_index}'
    """
    return db.execute(select_sql).first() is not None
