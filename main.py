import json
from pathlib import Path
from syftbox.lib import Client


def write_json(file_path: Path, result: dict) -> None:
    print(f"Writing to {file_path}.")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(result, f)


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def main():

    client = Client.load()
    datasite_path = client.datasite_path.parent
    api_dir = client.api_data("voting")
    public_dir = api_dir / "public"
    elections_dir = api_dir / "elections"
    ballots_dir = api_dir / "ballots"
    
    datasite_path.mkdir(parents=True, exist_ok=True)
    api_dir.mkdir(parents=True, exist_ok=True)
    public_dir.mkdir(parents=True, exist_ok=True)
    elections_dir.mkdir(parents=True, exist_ok=True)
    ballots_dir.mkdir(parents=True, exist_ok=True)

    syftperm = {"admin": [client.email], "read": [client.email], "write": [client.email], "filepath": None, "terminal": False}

    public_syftperm = dict(syftperm)
    public_syftperm_filepath = public_dir / "_.syftperm"
    public_syftperm["filepath"] = str(public_syftperm_filepath)
    public_syftperm["read"] = [client.email, "GLOBAL"]
    write_json(public_syftperm_filepath, public_syftperm)
    
    elections_syftperm = dict(syftperm)
    elections_syftperm_filepath = elections_dir / "_.syftperm"
    elections_syftperm["filepath"] = str(elections_syftperm_filepath)
    write_json(elections_syftperm_filepath, elections_syftperm)

    ballots_syftperm = dict(syftperm)
    ballots_syftperm_filepath = ballots_dir / "_.syftperm"
    ballots_syftperm["filepath"] = str(ballots_syftperm_filepath)
    ballots_syftperm["read"] = [client.email, "GLOBAL"]
    write_json(ballots_syftperm_filepath, ballots_syftperm)

    return True


__name__ == '__main__' and main()

