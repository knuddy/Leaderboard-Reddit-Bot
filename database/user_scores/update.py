def user_score(db, character_index, user_index, user_score):
    update_sql =f"""
        UPDATE user_scores
        SET scores[{user_index}] = {user_score + 1},
            users_added[{user_index}] = NOW()
        WHERE character_index='{character_index}'
    """ 
    db.execute(update_sql)