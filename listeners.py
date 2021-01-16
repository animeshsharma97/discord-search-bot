from discord.ext import commands

from config import db, discord_token

from exceptions import EmptyQueryException

from helpers.db_helpers import get_search_response, get_user_latest_searches, insert_user_query_in_mongo

from server import keep_alive

from utils.search_utils import get_search_term 


bot = commands.Bot(command_prefix="!")

# listener which listens to the !google command
@bot.command(name="google", help="Responds with google search results based on your query")
async def google_search(ctx):

    user_id = str(ctx.message.author.id)
    msg_content = ctx.message.content
    search_term = get_search_term("!google ", msg_content)

    response = get_search_response(db, search_term)
    
    await ctx.send(response)
    insert_user_query_in_mongo(db, user_id, search_term)


# listener which listens to the !recent command
@bot.command(name="recent", help="Responds with your recent google search query.")
async def recent_searches(ctx):

    user_id = str(ctx.message.author.id)
    msg_content = ctx.message.content
    search_term = get_search_term("!recent ", msg_content)

    response = get_user_latest_searches(db, user_id, search_term)
    await ctx.send(response)

# listener which responds to any error events
@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.errors.CommandNotFound):
        response = "Oh No! We don't do that here. Please type !google or !recent, and your search query to proceed.\nE.g. !google discord"

    elif isinstance(error, EmptyQueryException):
        response = "Search term cannot be empty."

    elif isinstance(error, commands.errors.CommandInvokeError):
        response = "The request can't be processed. Please try again!"

    else:
        response = "Something went wrong. Please wait while we work our magic."
    await ctx.send(response)

"""
This is done to keep the flask server running indefinitely through HTTP calls from an external service
to keep the heroku deployment from going into sleep mode so that it can listen to discord requests indefinitely.
"""
keep_alive()

# Start the listener
bot.run(discord_token)
