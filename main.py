# main.py

from pathlib import Path
from syftbox.lib import Client
import json
import os
import shutil

def load_json(file_path: Path):
    with open(file_path, "r") as f:
        return json.load(f)

def write_json(file_path: Path, data: dict):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def get_all_participants(datasite_path: Path):
    exclude_dirs = ["apps", ".syft"]
    return [
        entry for entry in os.listdir(datasite_path)
        if (datasite_path / entry).is_dir() and entry not in exclude_dirs
    ]

def collect_votes(participants: list[str], datasite_path: Path, results_path: Path):
    # Map of election_id to votes and election details
    elections = {}
    for participant in participants:
        ballot_folder = datasite_path / participant / "elections"  # Changed from "ballot" to "elections"
        if not ballot_folder.exists():
            continue  # Participant hasn't submitted any votes
        for ballot_file in ballot_folder.glob("*.json"):
            try:
                ballot_data = load_json(ballot_file)
                election_id = ballot_data["election"]
                vote = ballot_data["ballot"]
                # Optional fields
                description = ballot_data.get("description", "")
                election_participants = ballot_data.get("participants", None)
                min_value = ballot_data.get("min_value", 0)
                max_value = ballot_data.get("max_value", 1)
                allow_intermediary = ballot_data.get("allow_intermediary", False)

                # Handle "GLOBAL" participants
                if election_participants == "GLOBAL" or election_participants == ["GLOBAL"]:
                    election_participants = None  # Treat as no participants key (all participants)

                # Initialize election entry if not exists
                if election_id not in elections:
                    elections[election_id] = {
                        "votes": {},
                        "description": description,
                        "participants": election_participants,
                        "min_value": min_value,
                        "max_value": max_value,
                        "allow_intermediary": allow_intermediary,
                        "invalid_votes": [],
                        "missing_votes": []
                    }

                # Check if participant is eligible
                if elections[election_id]["participants"] is None or participant in elections[election_id]["participants"]:
                    # Validate and adjust vote
                    try:
                        vote = float(vote)
                        if vote < min_value:
                            vote = min_value
                        elif vote > max_value:
                            vote = max_value
                        else:
                            if not allow_intermediary:
                                # Round to nearest integer within min and max
                                vote = round(vote)
                    except ValueError:
                        # Invalid vote format
                        elections[election_id]["invalid_votes"].append(participant)
                        continue

                    # Save the valid vote
                    elections[election_id]["votes"][participant] = vote
                else:
                    # Participant not eligible
                    continue

            except Exception as e:
                # Error in processing ballot file
                elections.setdefault(election_id, {
                    "votes": {},
                    "description": "",
                    "participants": None,
                    "min_value": 0,
                    "max_value": 1,
                    "allow_intermediary": False,
                    "invalid_votes": [],
                    "missing_votes": []
                })
                elections[election_id]["invalid_votes"].append(participant)
                continue

    # Identify participants who haven't voted
    for election_id, data in elections.items():
        eligible_participants = data["participants"] or participants
        for participant in eligible_participants:
            if participant not in data["votes"] and participant not in data["invalid_votes"]:
                data["missing_votes"].append(participant)

    return elections

def aggregate_elections(elections: dict, results_path: Path):
    for election_id, data in elections.items():
        votes = list(data["votes"].values())
        if votes:
            mean_result = sum(votes) / len(votes)
            # Round result if intermediary values are not allowed
            if not data["allow_intermediary"]:
                mean_result = round(mean_result)
        else:
            mean_result = None

        result_data = {
            "election": election_id,
            "description": data["description"],
            "result": mean_result,
            "participants": data["participants"] or "All participants",
            "voters": list(data["votes"].keys()),
            "invalid_votes": data["invalid_votes"],
            "missing_votes": data["missing_votes"],
            "min_value": data["min_value"],
            "max_value": data["max_value"],
            "allow_intermediary": data["allow_intermediary"]
        }

        # Write the result to /elections/{ELECTION_ID}.json in the results path
        result_file = results_path / f"{election_id}.json"
        write_json(result_file, result_data)

        # Print summary
        print(f"\nElection ID: {election_id}")
        print(f"Description: {data['description']}")
        print(f"Result: {mean_result}")
        print(f"Valid votes from {len(data['votes'])} participants.")
        if data["invalid_votes"]:
            print(f"Invalid votes from: {data['invalid_votes']}")
        if data["missing_votes"]:
            print(f"Missing votes from: {data['missing_votes']}")

if __name__ == "__main__":
    client = Client.load()
    datasite_path = client.datasite_path.parent
    results_path = client.api_data("voting")  # This is where the results will be stored

    # Copy the election_template.json if it doesn't exist
    sample_election_src = Path(os.path.abspath(__file__)).parent / "election_template.json"
    sample_election_dst = client.datasite_path / "elections" / "election_template.json"
    if not sample_election_dst.exists():
        sample_election_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(sample_election_src, sample_election_dst)
        print(f"Copied sample election to {sample_election_dst}")

    participants = get_all_participants(datasite_path)

    elections = collect_votes(participants, datasite_path, results_path)

    aggregate_elections(elections, results_path)