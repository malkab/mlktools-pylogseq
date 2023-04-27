import os

# ----------------------------------
#
# A bunch of common functions.
#
# ----------------------------------

# ----------------------------------
#
# Sanitizes a path.
#
# ----------------------------------
def sanitize_path(path: str) -> str:
    """Sanitizes a path.

    Parameters
    ----------
    path : str
        The path to sanitize.

    Returns
    -------
    str
        The sanitized path.
    """
    return os.path.abspath(os.path.normpath(path)) if path else None


# --------------------------------------
#
# Sanitize content.
#
# ----------------------------------
def sanitize_content(content: str) -> str:
    """Sanitizes the content of the page.

    Args:
        content (str): The content to sanitize.

    Returns:
        str: The sanitized content.
    """
    return content.strip("\n").strip()
