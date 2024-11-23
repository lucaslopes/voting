'''
Code example from the tutorial:
https://syftbox.openmined.org/datasites/ionesio@openmined.org/tutorial01.html
Adapted for election use case
'''

from pathlib import Path
from syftbox.lib import Client
import os

# Iterate over a list of participants, looking for their /public/value.txt
# If they have the file and the value is 0 or 1, add it to the list of valid values,
# otherwise, add the username to the missing list.
# Return both the list of valid values and the missing list.
def aggregate(participants: list[str], datasite_path: Path):
    values = []  # Store valid values (0 or 1)
    missing = []  # Participants with missing or invalid value

    for user_folder in participants:
        value_file: Path = Path(datasite_path) / user_folder / "public" / "value.txt"

        if value_file.exists():
            with value_file.open("r") as file:
                value_str = file.read().strip()
                try:
                    value = int(value_str)
                    if value in [0, 1]:
                        values.append(value)
                    else:
                        missing.append(user_folder)
                except ValueError:
                    # Not an integer
                    missing.append(user_folder)
        else:
            missing.append(user_folder)

    return values, missing

# Return a list of all network peers
def network_participants(datasite_path: Path):
    exclude_dir = ["apps", ".syft"]

    entries = os.listdir(datasite_path)

    users = []
    for entry in entries:
        if Path(datasite_path / entry).is_dir() and entry not in exclude_dir:
            users.append(entry)

    return users


if __name__ == "__main__":
    client = Client.load()

    participants = network_participants(client.datasite_path.parent)

    values, missing = aggregate(participants, client.datasite_path.parent)
    
    if values:
        mean_value = sum(values) / len(values)
    else:
        mean_value = None

    print("\n====================\n")
    if mean_value is not None:
        print("Mean aggregation value: ", mean_value)
        if mean_value < 0.5:
            print("Result is closer to 0 (No)")
        else:
            print("Result is closer to 1 (Yes)")
    else:
        print("No valid votes were counted.")
    print("Missing or invalid value.txt peers: ", missing)
    print("\n====================\n")