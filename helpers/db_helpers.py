import bson
import re

from datetime import datetime

from helpers.api_helpers import get_google_search_response

def get_search_response(db, search_term):
    """Method to get search result from db or google api.

    Args:
        db: The database object.
        search_term: The search term.

    Returns:
        String: List of relevant links separated by line break.
    """

    # Find if the search results for the term is stored in mongo.
    response = (
        db["SearchResults"].find_one(
            {
                "searchTerm": search_term
            }
        ) or {}
    ).get("result")

    if not response:

        # Fetch search results from Google API if not found in mongo.
        response = get_google_search_response(search_term)

        # Cache the results in mongo where lastSearchedOn is a TTL index with timeout of 3600 seconds.
        db["SearchResults"].insert_one(
            {
                "searchTerm": search_term,
                "lastSearchedOn": datetime.now(),
                "result": response
            }
        )
    return response

def insert_user_query_in_mongo(db, user_id, search_term):
    """Method to insert or update user query in mongo.
    
    Args:
        db: The database object.
        user_id: Id of the user.
        search_term: The search term.
    """

    db["UserQueries"].update_one(
        {
            "userId": user_id,
            "searchTerm": search_term,
        },
        {
            "$set": {"lastSearchedOn": datetime.now()}
        },
        upsert=True
    )


def get_user_latest_searches(db, user_id, search_term):
    """Method to get latest user searches from mongo.

    Args:
        db: The database object.
        user_id: Id of the user.
        search_term: The search term.

    Returns:
        String: Search history of user separated by line break.
    """

    regx = bson.regex.Regex(".*{search_term}.*".format(search_term=search_term), re.IGNORECASE)
    result = db["UserQueries"].find(
        {
            "userId": user_id,
            "searchTerm": {"$regex": regx},
        }
    ).sort("lastSearchedOn", -1).limit(5)
    
    response = "\n".join([item["searchTerm"] for item in result]) or "Sorry!! We couldn't find anything for this. Please try again!"
    return response
