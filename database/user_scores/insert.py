def character_index(db, character_index):
    insert_sql = f"""
        INSERT INTO user_scores (character_index, usernames, scores, users_added)
        VALUES ('{character_index}', ARRAY[]::text[], ARRAY[]::integer[], ARRAY[]::timestamp[])
    """
    db.execute(insert_sql)


def user_score(db, character_index, username):
    update_sql = f"""
        UPDATE user_scores
        SET usernames = array_append(usernames, '{username}'),
            scores = array_append(scores, 1),
            users_added = array_append(users_added, NOW()::timestamp)
        WHERE character_index='{character_index}'
    """
    db.execute(update_sql)
