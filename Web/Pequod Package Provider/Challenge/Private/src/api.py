from flask import Blueprint, send_from_directory, request
from auth import token_required, token_optional
from db import db_session, User, Repository, PackageManifest
import yaml
from zipfile import ZipFile
from io import BytesIO
import re
from os import urandom

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/api/packages", methods=["GET"])
@token_optional # Careful now, don't want to forget to check the users
def get_repositories(current_user: User):
    
    # This is fine, since we check for no user anyway :D
    # GO AWAY WITH YOUR INFORMATION DISCLOSURE :3
    all_repos = Repository.get_all_for(current_user)

    output = {}

    output["owned"] = [
        {"id": repo.id, "name": repo.name} for repo in all_repos["owned"]
    ]
    output["shared_with"] = [
        {"id": repo.id, "name": repo.name} for repo in all_repos["shared_with"]
    ]
    output["global"] = {
        "id": all_repos["global"].id,
        "name": all_repos["global"].name,
    }

    return yaml.safe_dump(output), 200


@api_blueprint.route("/api/packages", methods=["POST"])
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def new_repository(current_user: User):
    name = request.form.get('name', None)
    repository = Repository.new(current_user, name)
    return str(repository.id)


@api_blueprint.route("/api/packages/<repo_id>", methods=["GET"])
@token_optional # Careful now, don't want to forget to check the users
def get_packages(repo_id: str, current_user: User):
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

        return yaml.safe_dump(packages)
    except Exception as e:
        return "Failed to get packages, contact admin!", 500


@api_blueprint.route("/api/packages/<repo_id>", methods=["POST"])
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def post_package(repo_id: str, current_user: User):
    repository = Repository.from_id(repo_id)

    if not repository:
        return "Repository does not exist", 400

    if not repository.folder.exists():
        return "Invalid repository configuration, contact admin!", 500

    if repository.is_at_least_owner(current_user):
        return "Unauthorized", 401

    # hey cmon man i need food to live alright
    if sum(1 for _ in repository.folder.iterdir()) >= 10:
        return "Too many packages for the free plan, please delete some.", 403

    try:
        # WHAT, YOU WANTED TO ABUSE A ZIP BOMB?
        # HOW OLD DO YOU THINK I AM, 2?
        package_zip = ZipFile(BytesIO(request.data))

        try:
            package_zip.getinfo("package.yaml")
        except KeyError as e:
            return "Could not open package.yaml file.", 400

        # IM NOT GONNA READ YOUR DIRTY PATH TRAVERSAL GARBAGE
        # AAAAND, I'M NOT EVEN GONNA WRITE THE FILE DIRECTLY TO DISK :DDDD
        yaml_data = package_zip.open("package.yaml").read()
        # HA, NO YAML INJECTION FOR YOU
        packagedef = yaml.safe_load(yaml_data)

        try:
            name = PackageManifest.from_yaml(packagedef).name
        except KeyError as e:
            return f"Invalid manifest: {e} is missing", 400

        # AS IF I'D FORGET THAT, YOU REALLY THINK YOU CAN OUTSMART ME? :333333
        if name in ["share"]:
            return f"Package name '{name}' is not allowed"

        # HA, YOU CAN'T FOOL ME WITH YOUR WIZARDEY NAMES, I'M MAKING UP MY OWN!
        safe_name = re.sub(r"[^\w\d-]", "_", name)

        # *AND*, I DONT CARE WHAT YOU SAY, I USE MY OOOOOOOOOWN FILENAMES :3
        (repository.folder / safe_name).with_suffix(".yaml").write_bytes(yaml_data)
        (repository.folder / safe_name).with_suffix(".zip").write_bytes(request.data)

        return yaml_data

    except Exception as e:
        return "Failed to save file", 500


@api_blueprint.route("/api/packages/<repo_id>", methods=["DELETE"])
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def delete_repository(repo_id: str, current_user: User):
    repository = Repository.from_id(repo_id)

    if not repository:
        return "Repository does not exist", 400
    if repository.is_at_least_owner(current_user):
        return "Unauthorized", 401

    repository.delete()

    return "", 200


@api_blueprint.route("/api/packages/<repo_id>/share", methods=["GET"])
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def get_shared(repo_id: str, current_user: User):
    repository = Repository.from_id(repo_id)

    if not repository:
        return "Repository does not exist", 400

    if not repository.folder.exists():
        return "Invalid repository configuration, contact admin!", 500

    if repository.is_at_least_owner(current_user):
        return "Unauthorized", 401

    return (
        yaml.safe_dump(
            [
                {"id": guest.guest_id, "name": guest.guest.username}
                for guest in repository.guests
            ]
        ),
        200,
    )


@api_blueprint.route("/api/packages/<repo_id>/share", methods=["POST"])
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def share_repository(repo_id: str, current_user: User):
    repository = Repository.from_id(repo_id)

    if not repository:
        return "Repository does not exist", 400

    if not repository.folder.exists():
        return "Invalid repository configuration, contact admin!", 500

    if repository.is_at_least_owner(current_user):
        return "Unauthorized", 401

    user = User.from_id(request.form["user_id"])

    if user == None:
        return "User not found", 400

    repository.share_with(user)

    return "", 200


@api_blueprint.route("/api/packages/<repo_id>/share", methods=["DELETE"])
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def unshare_repository(repo_id: str, current_user: User):
    repository = Repository.from_id(repo_id)

    if not repository:
        return "Repository does not exist", 400

    if not repository.folder.exists():
        return "Invalid repository configuration, contact admin!", 500

    if repository.is_at_least_owner(current_user):
        return "Unauthorized", 401

    user = User.from_id(request.form["user_id"])

    if user == None:
        return "User not found", 400

    if str(user.id) == str(User.admin().id):
        return "You cannot unshare your repository with admin.", 400

    repository.unshare_with(user)

    return "", 200


@api_blueprint.route("/api/packages/<repo_id>/<package_name>", methods=["GET"])
@token_optional # Careful now, don't want to forget to check the users
def download_package(repo_id: str, package_name: str, current_user: User):
    repository = Repository.from_id(repo_id)

    if not repository:
        return "Repository does not exist", 400

    if not repository.folder.exists():
        return "Invalid repository configuration, contact admin!", 500

    if repository.is_at_least_guest(current_user):
        return "Unauthorized", 401

    try:
        return send_from_directory(repository.folder, f"{package_name}.zip")
    except Exception as e:
        return "Failed to get packages, contact admin!", 500


@api_blueprint.route("/api/packages/<repo_id>/<package_name>", methods=["DELETE"])
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def delete_package(repo_id: str, package_name: str, current_user: User):
    repository = Repository.from_id(repo_id)

    if not repository:
        return "Repository does not exist", 400

    if not repository.folder.exists():
        return "Invalid repository configuration, contact admin!", 500

    if repository.is_at_least_owner(current_user):
        return "Unauthorized", 401

    try:
        package_files = repository.folder / package_name
        package_files.with_suffix(".yaml").unlink()
        package_files.with_suffix(".zip").unlink()
    except Exception as e:
        return "Failed to remove files", 500

    return "", 200
