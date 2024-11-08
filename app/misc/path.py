import os


def format_path(REPO_NAME: str):

    if REPO_NAME is None:
        raise Exception("REPO_NAME IS NONE!!!!!")

    if "/" in REPO_NAME:
        file_p = REPO_NAME.split("/")[1]

    return os.path.join(os.path.abspath(os.sep), file_p)
