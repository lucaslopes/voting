# e-Voting

## Overview

This Voting App is a decentralized voting system that allows participants to create and participate in elections securely and privately in [SyftBox](https://syftbox-documentation.openmined.org/). The app aggregates votes while maintaining individual vote privacy. It supports both global elections (open to all SyftBox Datasites) and restricted elections (limited to specific participants).

### Features

- **Decentralized Voting**: No central authority; participants submit votes independently.
- **Privacy**: Individual votes are kept private and are not exposed publicly.
- **Flexible Elections**: Supports binary and scaled elections with customizable vote ranges.
- **Automatic Aggregation**: Aggregates votes and computes results automatically.
- **Participant Management**: Allows specifying eligible participants for each election.
- **Result Distribution**: Election results are distributed to all participants.

### Folder Structure

- `main.py`: The main script that runs the voting aggregation.
- `election_sample.json`: A sample election file to help participants get started.

### Installation and Usage

1. Make sure you have [SyftBox](https://syftbox-documentation.openmined.org/#install-syftbox) installed.
2. Clone or Download this Repository and copy it into your `apis/` directory in SyftBox folder.
3. Cast your first vote by editing the `"ballot"` value in the `elections/election_template.json` file that was created in your Datasite.

## Creating or Participanting of an Election

To create a new election:

1. Create a JSON file for your election in your `/elections` folder `(client.datasite_path / "elections")` (e.g., my_election.json), using the following structure:
```
{
  "election": "unique_election_id",
  "ballot": your_vote_value,
  "description": "Description of the election.",
  "participants": ["a@openmined.org", "b@openmined.org", "c@openmined.org"],
  "min_value": minimum_vote_value,
  "max_value": maximum_vote_value,
  "allow_intermediary": true_or_false
}
```

### Election Fields Explanation:

- **election**: A unique identifier for the election.
- **ballot**: Your vote. Can be a number within the specified range.
- **description**: (Optional) Description of the election.
- **participants**: (Optional) List of participants eligible to vote. Use "GLOBAL" to allow all participants.
- **min_value**: (Optional) Minimum allowable vote value. Default is 0.
- **max_value**: (Optional) Maximum allowable vote value. Default is 1.
- **allow_intermediary**: (Optional) true to allow decimal values between min_value and max_value; false to restrict votes to integers. Default is false.


### Share the Election Details:

Notify the eligible participants about the election and its `election_id` so they can cast their votes.

### Casting a Vote

To cast a vote in an existing election:

1.	Obtain the Election Details: Get the `election_id` and any specific details (e.g., vote range, description) from the election creator.

2.	Create Your Vote File: In your `/elections` folder, create a JSON file with the election details and your vote. Example:
```
{
  "election": "unique_election_id",
  "ballot": your_vote_value
}
```
> Note: You can include optional fields like description, min_value, max_value, and allow_intermediary if they differ from defaults.

3.	Save the File: Name the file appropriately (e.g., unique_election_id.json) and save it in your `/elections` folder.

Aggregating Votes

When the API is run, it will:

- Collect all votes from participants’ `/elections` folders.
- Aggregate the votes for each election.
- Compute the results based on the specified parameters.
- Write the results to the api data path `(client.api_data("voting"))`, accessible to all participants.
- Print a summary of the election results to the console.

Viewing Election Results

- Election results are stored in the api data results directory `(client.api_data("voting"))`.
- Results are saved as JSON files named after the election_id (e.g., unique_election_id.json).
- Participants can access this directory to view the results.

## Examples

### Sample Election Creation

Suppose Alice wants to create a new **binary** election where participants vote 0 or 1.

1.	Alice’s Vote File (elections/my_binary_election.json):
```
{
  "election": "my_binary_election",
  "ballot": 1,
  "description": "Vote on adopting the new policy.",
  "participants": ["alice", "bob", "carol"],
  "min_value": 0,
  "max_value": 1,
  "allow_intermediary": false
}
```

2.	Bob and Carol’s Vote Files:

Bob votes 0:
```
{
  "election": "my_binary_election",
  "ballot": 0
}
```

Carol votes 1:
```
{
  "election": "my_binary_election",
  "ballot": 1
}
```

#### Running the Aggregation

- The app automatically aggregates the votes and computes the result.
- The result is saved in the results directory as `my_binary_election.json`.
- One can always change their vote by editing the ballot value in the json file (soon we will add valid period date for elections)

Result File (results/my_binary_election.json):
```
{
  "election": "my_binary_election",
  "description": "Vote on adopting the new policy.",
  "result": 1,
  "participants": ["alice", "bob", "carol"],
  "voters": ["alice", "bob", "carol"],
  "invalid_votes": [],
  "missing_votes": [],
  "min_value": 0,
  "max_value": 1,
  "allow_intermediary": false
}
```

Console Output:
```
Election ID: my_binary_election
Description: Vote on adopting the new policy.
Result: 1
Valid votes from 3 participants.
```

## Advanced Features

### Global Elections

To create an election open to all participants in SyftBox network, set participants to "GLOBAL" or omit the participants field.
```
{
  "election": "company_wide_vote",
  "ballot": 1,
  "description": "Company-wide vote on new benefits.",
  "participants": "GLOBAL",
  "min_value": 0,
  "max_value": 1,
  "allow_intermediary": false
}
```

### Scaled Elections

For elections requiring a range of values (e.g., -10 to 10), set min_value, max_value, and allow_intermediary accordingly.
```
{
  "election": "satisfaction_survey",
  "ballot": 7.5,
  "description": "Rate your satisfaction from -10 to 10.",
  "min_value": -10,
  "max_value": 10,
  "allow_intermediary": true
}
```

### Handling Invalid or Missing Votes

- The app automatically detects invalid or missing votes.
- Invalid votes are recorded if the vote value is not a number or outside the specified range.
- Missing votes are recorded for eligible participants who have not submitted a vote.
- This information is included in the result JSON file under invalid_votes and missing_votes.

## Contributing

Contributions are welcome! Please submit issues or pull requests for enhancements, bug fixes, or new features.

### Security Considerations

- **Vote Privacy**: Individual votes are stored in participants’ private `/elections` folders and are not exposed publicly.
- **Result Access**: Results are stored a copy in each client's api data location accessible to all participants.
- **Participant Verification**: Currently, there’s a known issue where unauthorized participants could attempt to vote in restricted elections. This will be addressed in future updates.

### Known Issues and TODOs

- Unauthorized Voting: Participants could potentially submit votes for elections they are not invited to. A mechanism to verify participant eligibility is needed.
- Vote Tampering: Since votes are stored as JSON files, there is potential for tampering. Implementing digital signatures or encryption is recommended.
- Late Votes: Votes submitted after the aggregation may not be counted. Consider implementing a cutoff time or re-running aggregation periodically.