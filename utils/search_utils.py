from exceptions import EmptyQueryException


def get_search_term(command, msg_content):
    """Method to get search term from message content.
    
    Args:
        command: The name of command.
        msg_content: Message content. ("!<command> <search_term>")

    Returns:
        String: The search term.
    """

    try:
        _, search_term = msg_content.split(command)

    except Exception:
        raise EmptyQueryException

    return search_term
