# Voting API

Empower your community with a secure, decentralized, and private voting system.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [How It Works](#how-it-works)
  - [Data Flow](#data-flow)
  - [API Operation Cycle](#api-operation-cycle)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Accessing the Web Interface](#accessing-the-web-interface)
  - [Creating an Election](#creating-an-election)
  - [Casting a Vote](#casting-a-vote)
  - [Viewing Election Results](#viewing-election-results)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

Welcome to the Voting API! This project revolutionizes the way we conduct elections by leveraging decentralized technology and homomorphic encryption. Say goodbye to centralized servers and hello to a transparent, secure, and participant-driven voting experience.

Whether you're organizing a community poll, a student council election, or gathering decentralized feedback, the Voting API provides a platform that's easy to set up and enjoyable to use.

## Features

- **Decentralized Architecture**: Eliminates dependency on a central server; every participant runs the API locally.
- **Privacy-Preserving Voting**: Individual votes remain confidential through homomorphic encryption.
- **Participant Empowerment**: Users can create new elections and participate in existing ones.
- **Automated Processing**: The API automatically aggregates votes and updates results.
- **SyftBox Integration**: Leverages SyftBox's privacy controls and synchronization capabilities.

## How It Works

In traditional web applications, the availability of a central server is critical. If the server is down, users cannot submit votes or access crucial features, which undermines the independence and resilience a voting application should provide.

Our Voting API addresses this challenge by adopting a synchronous model between client and server, made possible through [SyftBox](https://syftbox-documentation.openmined.org/). SyftBox not only functions like cloud storage solutions but also allows code execution on the client side, running installed APIs every 10 seconds.

### Data Flow

Each participant's SyftBox directory structure includes:

`SyftBox/Datasites/<your_email>/api__data/voting/`

- _**`ballots/`**_: Public folder where users submit their encrypted votes by placing JSON files.
- _**`elections/`**_: Private folder where users can create new elections. Contains sensitive data like the private key used for decrypting election results.
- _**`public/`**_: Public folder where the API writes sanitized election data and results without exposing private keys.

### API Operation Cycle

Every 10 seconds, the Voting API performs the following tasks:

1. _**Election Loading**_: Reads election JSON files from the `elections/` folder and stores them in memory.
2. _**Ballot Collection**_: Gathers votes from the `ballots/` folders of all network participants for the elections in memory.
3. _**Vote Aggregation**_: Aggregates encrypted votes using homomorphic properties and decrypts the aggregate result using the private key.
4. _**Result Publishing**_: Writes sanitized election data and results to the `public/` folder, excluding any private keys.
5. _**Outcome Compilation**_: Reads public election results from all participants and compiles them into a single `election_outcomes.json` file in `SyftBox/Datasites/<your_email>/public/`.

**This decentralized operation ensures that all participants have access to the latest election results without relying on a central server.**

## Getting Started

### Prerequisites

- _**Operating System**_: MacOS or Linux.
- _**SyftBox**_: Installed and set up on your machine.

### Installation

#### 1. Install SyftBox

SyftBox is required to run the Voting API. Install it by running the following command in your terminal:

```bash
curl -LsSf https://syftbox.openmined.org/install.sh | sh
```

For more information, refer to the [SyftBox Documentation](https://syftbox-documentation.openmined.org/).

#### 2. Set Up the Voting API

After installing SyftBox:

• **Option A: Using Git**

Navigate to your `SyftBox/apis/` directory and clone the Voting API repository:

```bash
cd ~/Desktop/SyftBox/apis

git clone https://github.com/lucaslopes/voting.git
```

• **Option B: Download ZIP**

1. Click below to download the ZIP file of the repository: [Download Repository](https://github.com/lucaslopes/voting/archive/refs/heads/main.zip)
2. Extract the ZIP file.
3. Move the extracted voting folder into the `SyftBox/apis/` directory.

SyftBox will automatically detect and install the new API during its execution cycle.

## Usage

### Accessing the Web Interface

1. **Locate the Interface**: After the Voting API syncs with SyftBox, the web interface will be accessible via the URL:

```url
https://syftbox.openmined.org/datasites/<your_email>/voting.html
```

2. **Open in Browser**: Paste the above URL into your browser’s address bar to access the voting interface.

### Creating an Election

1. **Open the Interface**: Ensure you’re viewing `voting.html` in your browser.
2. **Click "Create Election"**: This opens a modal window for creating a new election.
3. **Fill in Election Details**:
   - **Election Question**: The question or statement to be voted on.
   - **Lower Value Description**: Describes the lowest rating (e.g., "Strongly Disagree").
   - **Upper Value Description**: Describes the highest rating (e.g., "Strongly Agree").
4. **Create the Election**: Click the "Create Election" button.
5. **Download the Election File**:
   - A JSON file (`election-<metadata>.json`) containing the election data and private key will be downloaded.
   - **Important**: Keep this file secure; it contains the private key needed to decrypt results.
6. **Submit the Election**: Move the downloaded JSON file to `SyftBox/Datasites/<your_email>/api_data/voting/elections/`.

### Casting a Vote

1. **Open the Interface**: Ensure you’re on `voting.html`.
2. **Select an Election**: Browse and choose an election to participate in.
3. **Set Your Vote**: Adjust the slider to reflect your vote.
4. **Vote**: Click the "Vote" button.
5. **Download the Ballot File**: A JSON file (`ballot-<metadata>.json`) containing your encrypted vote will be downloaded.
6. **Submit Your Vote**: Move the ballot file to `SyftBox/Datasites/<your_email>/api_data/voting/ballots/`.

### Viewing Election Results

1. **Wait for Processing**: The API processes data every 10 seconds.
2. **Refresh the Interface**: Reload `voting.html` via the URL.
3. **View Results**: Results, including total and average scores, are displayed for each election.

## Contributing

We welcome contributions to enhance the Voting API:

1. **Fork the Repository**: Click "Fork" on GitHub to create your copy.
2. **Create a Branch**: Develop your feature or fix in a new branch.
3. **Submit a Pull Request**: Provide a detailed description for review.

## License

This project is licensed under the GNU General Public License (Version 3, 29 June 2007). See the [LICENSE](LICENSE) file for details.

## Acknowledgments

• **SyftBox**: For providing the platform enabling decentralized applications.
• **Paillier Cryptosystem**: For the homomorphic encryption methods utilized.
• **OpenMined Community**: Thank you to everyone who has contributed to this project during the [30DaysOfFLCode](https://30daysofflcode.com/) challenge! - [my daily updates](https://syftbox.openmined.org/datasites/lucaslopesf2@gmail.com/30DaysOfFLCode.html)

Enjoy secure and independent voting with the Voting API!

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Run End-to-End Tests with [Playwright](https://playwright.dev)

```sh
# Install browsers for the first run
npx playwright install

# When testing on CI, must build the project first
npm run build

# Runs the end-to-end tests
npm run test:e2e
# Runs the tests only on Chromium
npm run test:e2e -- --project=chromium
# Runs the tests of a specific file
npm run test:e2e -- tests/example.spec.ts
# Runs the tests in debug mode
npm run test:e2e -- --debug
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
