from googleapiclient.discovery import build

from config import google_search_api_key, search_engine_id


def get_google_search_response(search_term):
    """Method to get response form google custom search API.

    Args:
       search_term: The query passed to the google custom search API.

    Returns:
        String: List of relevant links separated by line break.
    """

    service = build("customsearch", "v1", developerKey=google_search_api_key)
    google_response = service.cse().list(
        q=search_term,
        cx=search_engine_id,
        num=5,
    ).execute()

    response = [
        "{title}: {url}".format(title=item.get("title", ""), url=item["link"])
        for item in google_response.get("items", [])
    ]

    response = "\n".join(response) or "Sorry!! We couldn't find anything for this. Please try again!"
    return response
