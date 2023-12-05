import secrets
import string


def generate_random_token(length: int = 16):
    """
    Generates a random token of specified length.

    Args:
        length (int): Length of the token to be generated. Default is 16.

    Returns:
        str: A random token string.
    """
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


def resolve_abs_local_file_path_from(filename: str):
    return f"shared_data/{filename}"
