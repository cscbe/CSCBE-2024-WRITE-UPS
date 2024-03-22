from flask import Blueprint, render_template
from auth import token_required
from db import Repository, User
import yaml

repository_blueprint = Blueprint("repository", __name__)

@repository_blueprint.route("/repository/<repo_id>")
@token_required
def view_repository(repo_id: str, current_user: User):
    repository = Repository.from_id(repo_id)

    if not repository:
        return "Repository does not exist", 400

    if not repository.folder.exists():
        return "Invalid repository configuration, contact admin!", 500

    if repository.is_at_least_guest(current_user):
        return "Unauthorized", 401

    try:
        packages = []

        for file in repository.folder.iterdir():
            if file.suffix == ".yaml":
                # HA, NO YAML INJECTION FOR YOU
                packagedef = yaml.safe_load(open(file))
                packages.append(
                    {
                        "name": packagedef["name"],
                        "author": packagedef["author"],
                        "version": packagedef["version"],
                        "publisher": packagedef["publisher"],
                        "size": file.with_suffix(".zip").stat().st_size,
                    }
                )
        return render_template("repository.html", packages=packages, repo=repository, current_user=current_user)
    except Exception as e:
        return "Failed to get packages, contact admin!", 500