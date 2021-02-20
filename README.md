# Leaderboard Reddit Bot

A simple reddit bot, created in python, to count the number of times users comment the phrase "This is the way". Certain comments using the aforementioned phrase will be replied to with the current top 3 users on the leaderboard, as well as their rank overall. 

Technologies Used:
- The [PRAW](https://praw.readthedocs.io/en/latest/) library was used to interact with Reddit's API 
- I used [Heroku](https://www.heroku.com) to host the bot, specifically their free tier.
- The [Heroku Postgres](https://www.heroku.com/postgres) add-on to hold the leaderboard data. 10k rows are available for free.
