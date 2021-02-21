def make_timer(db):
    insert_sql = """
        INSERT INTO time_since_last_post(id,last_post_time) 
        VALUES(1, NOW() - INTERVAL '5 minutes')
    """
    db.execute(insert_sql)