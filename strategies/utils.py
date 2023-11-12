
def quote_name(name):
    """
    Ensure the SQL name is properly quoted to handle reserved keywords.

    Args:
        name (str): The name to be quoted.

    Returns:
        str: The quoted name.
    """
    return f'"{name}"'

def sanitize_name(name):
    """
    Sanitize a name to handle reserved SQL keywords.

    Args:
        name (str): The name to be sanitized.

    Returns:
        str: The sanitized name.
    """
    name = name.strip("[]")
    reserved_words = {"table", "select", "insert", "update", "delete", "where"}
    return f'_{name}_' if name.lower() in reserved_words else name