# Função para atualizar para a tag da nova release
import os
import git
from app import app
from .path import format_path
from github import Github
from dotenv import dotenv_values

config_vals = dotenv_values()

GITHUB_API_TOKEN = config_vals.get("GITHUB_API_TOKEN", "")
REPO_NAME = config_vals.get("REPO_NAME", "")
LOCAL_REPO_PATH = config_vals.get("LOCAL_REPO_PATH", "")
USER_GITHUB = config_vals.get("USER_GITHUB", "")

if LOCAL_REPO_PATH == "":
    LOCAL_REPO_PATH = format_path(REPO_NAME)

repo_url = f"https://{USER_GITHUB}:{GITHUB_API_TOKEN}@github.com/{REPO_NAME}.git"
g = Github(GITHUB_API_TOKEN)


def checkout_release_tag(tag_: str):
    try:
        # Abre o repositório local
        if not os.path.exists(LOCAL_REPO_PATH):
            git.Repo.clone_from(repo_url, LOCAL_REPO_PATH)

        repo = git.Repo(LOCAL_REPO_PATH)

        # Busca e alterna para a tag da nova release
        repo.git.fetch("--all", "--tags")
        repo.git.checkout(f"{tag_}")

        app.logger.info(f"Atualizado para a tag: {tag_}")
        version_file = os.path.join(LOCAL_REPO_PATH, ".version")
        with open(version_file, "w") as f:
            f.write(tag_)

    except Exception as e:
        app.logger.info(f"Erro ao atualizar para a tag {tag_}: {e}")
        raise e
