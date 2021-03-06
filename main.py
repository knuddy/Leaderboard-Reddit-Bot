#!/usr/bin/python
from bot import StarWarsBot
import config

if __name__ == "__main__":
    bot = StarWarsBot(
        config.CLIENT_ID, 
        config.CLIENT_SECRET,
        config.PASSWORD,
        config.USER_AGENT,
        config.USERNAME, 
        config.DATABASE_URL,
        config.POSTING_ENABLED,
        config.TIME_BETWEEN_POSTS,
        config.TIME_BETWEEN_FIXES
    )
    
    bot.run(config.SUBREDDIT_NAME, config.SEARCH_TERM)