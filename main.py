import os
import glob
import json
from pathlib import Path
from phe import paillier
from syftbox.lib import Client

def write_json(file_path: Path, result: dict) -> None:
    print(f"Writing to {file_path}.")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(result, f)

def write_syftperm(path, syftperm):
    syftperm["filepath"] = str(path)
    write_json(path, syftperm)

def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def L(u, n):
    return (u - 1) // n

def decrypt(c, n, lambda_param, mu):
    nsquare = n * n
    u = pow(c, lambda_param, nsquare)
    l_of_u = L(u, n)
    m = (l_of_u * mu) % n
    return m

def network_participants(datasite_path: Path):
    exclude_dir = ["apps", ".syft"]
    entries = os.listdir(datasite_path)
    users = []
    for entry in entries:
        if Path(datasite_path / entry).is_dir() and entry not in exclude_dir:
            users.append(entry)
    return users

def prepare_public_election_data(election, outcome=None):
    public_election = election.copy()
    public_election.pop('privateKey', None)
    public_election['outcome'] = outcome
    public_election['creator'] = election.get('creator')
    return public_election

def main():
    client = Client.load()
    datasite_path = client.datasite_path.parent

    # Our own directories
    api_dir = client.api_data("voting")
    public_dir = api_dir / "public"
    elections_dir = api_dir / "elections"
    ballots_dir = api_dir / "ballots"

    # Create directories if they don't exist
    public_dir.mkdir(parents=True, exist_ok=True)
    elections_dir.mkdir(parents=True, exist_ok=True)
    ballots_dir.mkdir(parents=True, exist_ok=True)

    # Set permissions
    syftperm = {
        "admin": [client.email],
        "read": [client.email],
        "write": [client.email],
        "filepath": None,
        "terminal": False
    }
    write_syftperm(public_dir / "_.syftperm", dict(syftperm, read=[client.email, "GLOBAL"]))
    write_syftperm(elections_dir / "_.syftperm", dict(syftperm))
    write_syftperm(ballots_dir / "_.syftperm", dict(syftperm, read=[client.email, "GLOBAL"]))


    # Get list of participants
    participants = network_participants(datasite_path)
    print(f"Participants: {participants}")

    # Load elections
    elections = {}
    expected_election_keys = {
        "question", "lowerValue", "upperValue", "publicKey",
        "privateKey", "publicKeyMetadata", "votesCounted",
        "creationDate", "lastUpdateTime", "outcome"
    }
    for election_file in elections_dir.glob('*.json'):
        try:
            election = load_json(election_file)
            if expected_election_keys.issubset(election.keys()):
                election_id = election['publicKeyMetadata']
                election['creator'] = client.email
                elections[election_id] = election
            else:
                print(f"Election file {election_file} missing expected keys, skipping.")
        except Exception as e:
            print(f"Error loading election file {election_file}: {e}")

    # Load ballots from all participants
    ballots = {}
    expected_ballot_keys = {"ciphertext", "publicKey", "publicKeyMetadata", "voteDate"}

    for participant in participants:
        participant_path = datasite_path / participant
        ballots_dir = participant_path / "api_data/voting/ballots"

        for ballot_file in ballots_dir.glob('*.json'):
            try:
                ballot = load_json(ballot_file)
                if expected_ballot_keys.issubset(ballot.keys()):
                    election_id = ballot['publicKeyMetadata']
                    participant_email = participant
                    ballots.setdefault(election_id, {})
                    # Only consider the most recent vote per participant per election
                    if participant_email not in ballots[election_id] or \
                       ballot['voteDate'] > ballots[election_id][participant_email]['voteDate']:
                        ballots[election_id][participant_email] = ballot
                else:
                    print(f"Ballot file {ballot_file} missing expected keys, skipping.")
            except Exception as e:
                print(f"Error loading ballot file {ballot_file}: {e}")

    # Aggregate election outcomes
    for election_id, election in elections.items():
        election_ballots = ballots.get(election_id, {})
        if not election_ballots:
            print(f"No ballots found for election {election_id}")
            outcome = None
        else:
            try:
                n = int(election['publicKey']['n'])
                lambda_param = int(election['privateKey']['lambda'])
                mu = int(election['privateKey']['mu'])
                nsquare = n * n

                # Aggregate encrypted votes
                sum_encrypted_votes = 1
                for ballot in election_ballots.values():
                    c = int(ballot['ciphertext'])
                    sum_encrypted_votes = (sum_encrypted_votes * c) % nsquare

                # Decrypt the sum
                total_score = decrypt(sum_encrypted_votes, n, lambda_param, mu)
                num_votes = len(election_ballots)
                average_score = total_score / num_votes

                print(f"Election {election_id}: total score {total_score}, average score {average_score}, voters: {num_votes}")

                # Store outcome
                outcome = {
                    'total_score': total_score,
                    'average_score': average_score,
                    'num_votes': num_votes
                }

            except Exception as e:
                print(f"Error processing election {election_id}: {e}")
                outcome = None
        

        # Write to our own public directory
        public_election = prepare_public_election_data(election, outcome)
        public_election_file = public_dir / f"election-{election_id}.json"
        write_json(public_election_file, public_election)

    return True

__name__ == '__main__' and main()