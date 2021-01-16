# discord-search-bot
Source code of a discord bot with google search capabilities

## Technologies used

1. Python
2. Flask
3. Heroku
4. MongoDB Atlas
5. Google Custom Search API
6. Discord python library

In this implementation, Python async IO is used to listen to the bot commands issued on the discord server.
The permissible commands for the bot are: **!google** and **!recent**

A user can write **!google python**, and they will get atmost 5 links related to Python. The queries made by a user are persisted on MongoDB as their search history. Also, the search results are stored in a different collection for an hour. This is done to cache the response from Google Search API and serve response from MongoDB itself for further requests of the same search term.

A user can look at their search history by issuing the command **!recent py** which will do a regex search on the user's past searches and return atmost 5 related search terms.

Steps to run the application:

1. Clone the git repo.
```
git clone https://github.com/animeshsharma97/discord-search-bot && cd discord-search-bot
```

2. Create a virtual environment and activate it.
```
virtualenv -p python3 venv && source venv/bin/activate
```

3. Install all dependencies.
```
pip install -r requirements.txt
```

4. Create a .env file with the follwoing values:
```
DISCORD_TOKEN=
GOOGLE_SEARCH_API_KEY=
SEARCH_ENGINE_ID=
MONGO_URI=
```

For local deployment, run the command:
```
python listeners.py
```

For deploying on heroku, you need to have an account on heroku and Heroku CLI installed on your device. You can follow the steps provided [here](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true "Heroku Python setup"). The following steps will then get you started on Heroku.

1. Login on Heroku.
```
heroku login
```

2. Create an app on heroku.
```
heroku create
```

3. Deploy your code on heroku.
```
git push heroku main
```

4. Set all env variables on your Heroku app which are stored in .env.
```
heroku config:set $(cat .env | sed '/^$/d; /#[[:print:]]*$/d')
```

5. To start an instance of the deloyed app:
```
heroku ps:scale web=1
```

Heroku reads the content of the Procfile and issues commands mentioned there on startup. This will start our listeners which can then listen to discord requests.
