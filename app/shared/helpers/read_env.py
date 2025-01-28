"""
This file implements the logics to get the environment variables.
"""
from os import (
    environ,
    getcwd,
    path,
)

from dotenv import load_dotenv


# load the environment variables
env_path = path.join(getcwd(), r"app/.env")
load_dotenv(dotenv_path=env_path)


def get_db_creds() -> dict[str, str]:
    """
    This function will read the environment variables
    and return the database credentials.
    input: None
    return: dict contains the database credentials as follows:
    {
        'host': str,
        'user': str,
        'password': str,
        'database': str
    }
    """
    db_creds: dict = {
        'host': environ.get('DB_HOST'),
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASSWORD'),
        'database': environ.get('DB')
    }
    return db_creds
